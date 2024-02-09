from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import Post,Comment,Like
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateCreateForm,CommentForm,CommentReplyForm,SearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class HomeView(View):
    template_name = "home/home.html"
    def get(self,request):
        form_search = SearchForm
        details = Post.objects.all()
        if request.GET.get('search'):
            details = details.filter(body__contains=request.GET['search'])
        return render(request,self.template_name,{'details':details,'form':form_search})

class listmembers(View):
    template_name= 'home/about.html'
    def get(self,request):
        listmember = User.objects.all()
        return render(request,self.template_name,{'listmembers':listmember})
class PostView(View):
    template_name = 'home/detail.html'
    form_class = CommentForm
    form_reply_class = CommentReplyForm
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'],slug=kwargs['post_slug'])
        return super().setup(request,*args,**kwargs)
    def get(self,request,post_id,post_slug):
        comments = self.post_instance.pcomment.filter(is_reply=False)
        unlike = 'light'
        if self.post_instance.unlike(request.user):
            unlike = 'primary'
        return render(request,self.template_name,{'post':self.post_instance,'comments':comments,'form':self.form_class,
                                                  'form_relpy':self.form_reply_class,'unlike':unlike})
    def post(self,request,*args,**kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.post = self.post_instance
            new_form.save()
            messages.success(request,'You comment sent it to admin',extra_tags='success')
        return redirect('home:detail',self.post_instance.id,self.post_instance.slug)

class PostDelete(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        post = get_object_or_404(Post,pk=kwargs['post_id'])
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request,"delete was successfully",extra_tags='success')
        else:
            messages.error(request,"you can't delete this post",extra_tags='danger')
        return redirect("home:home")

class PostUpdateView(LoginRequiredMixin,View):
    form_class = PostUpdateCreateForm
    # متد setup اطلاعاتی که قرار است در تمامی متد ها مورد استفاده قرار گیرد را درون خود ذخیره می کند
    def setup(self, request, *args, **kwargs):
        self.post_instanse = get_object_or_404(Post,pk=kwargs['post_id'])
        return super().setup(request,*args,**kwargs)


    # قبل از هر متدی اجرا بشه اول این متد ااجرا میشه
    def dispatch(self, request, *args, **kwargs):
        post = self.post_instanse
        # اگه ای دی کاربری که پست را ایجاد کرده با ای دی کاربری که میخواد آپدیت کنه یکی نبود اررو نشون بده (باید برای هردو متد این شرط را قرار داد)
        if not post.user.id == request.user.id:
            messages.error(request, "You can not update this post first Login/singn", 'danger')
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):
        post = self.post_instanse
        form = self.form_class(instance=post)
        return render(request,'home/update.html',{'form':form})
    def post(self,request,*args,**kwargs):
        post = self.post_instanse
        form = self.form_class(request.POST,instance=post)
        if form.is_valid():
            new_post = form.save(commit=False) # یعنی به دیتابیس وصل نشو تا یه سری کار انجام بده
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request,"you updated your post",'success')
            return redirect("home:detail",post.id,post.slug)


class PostCrateView(LoginRequiredMixin,View):
    form_class = PostUpdateCreateForm
    def get(self,request,*args,**kwargs):
        form = self.form_class
        return render(request,'home/create.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            print(request.user)
            new_post.user = request.user
            new_post.save()
            messages.success(request,"You create new post",'success')
            return redirect("home:detail",new_post.id,new_post.slug)

class PostReplyView(View):
    form_relpy = CommentReplyForm
    def post(self,request,*args,**kwargs):
        post = get_object_or_404(Post,id=kwargs['post_id'])
        comment = get_object_or_404(Comment,id=kwargs['comment_id'])
        form = self.form_relpy(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.post = post
            new_reply.reply = comment
            new_reply.user = request.user
            new_reply.is_reply = True
            new_reply.save()
        return redirect("home:detail",post.id,post.slug)
class LikePostView(View):
    def get(self,request,*args,**kwargs):
        post = get_object_or_404(Post,id=kwargs['post_id'])
        like = Like.objects.filter(post=post,user= request.user)
        if like.exists():
            like.delete()
            # messages.error(request,"You already liked this post",'danger')
        else:
            Like.objects.create(post=post,user=request.user)
        return redirect('home:detail',post.id,post.slug)