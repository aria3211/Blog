from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .forms import UserRegistrationForm,UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Relation




class SigninView(View):
    form_class = UserRegistrationForm
    template_name = "Register/Signin.html"


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)
    def get(self,request):
        '''
        از متد dispatch استفاده می کنیم تا کاربر به هر url که نوشته ایم دسترسی نداشته باشد
        شکل یک واسط بین درخواست و پاسخ کاربر فکر کنید
        '''
        form = self.form_class
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'],cd['email'],cd['password'])
            messages.success(request,"Your Sigin was successfully",extra_tags="success")
            return redirect('home:home')
        else:
            return render(request,self.template_name,{'form':form})

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "Register/Login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request,*args,**kwargs)
    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,{"form":form})
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,"Your log was successfully",extra_tags="success")
                return redirect("home:home")
            messages.error(request,"Username or password is wrong",extra_tags="warning")
        return render(request,self.template_name,{"form":form})

class UserLogOutView(LoginRequiredMixin,View):
    # add register/logout
    # دسترسی به log out را محدود میکنیم
    def get(self,request):
        logout(request)
        messages.success(request,"Your loged out was succefully",extra_tags="success")
        return redirect("home:home")

class UserProfileView(View):
    def get(self,request,user_id):
         is_following = False
         user = get_object_or_404(User,pk=user_id)
         posts = Post.objects.filter(user=user)
         username = get_object_or_404(User,username=user)
         relation = Relation.objects.filter(from_user=request.user,to_user=user.id).exists()
         if relation:
             is_following=True

         return render(request,"Register/profile.html",{'user':user,'username':username,'posts':posts,'is_following':is_following})

class UserPassResetView(auth_views.PasswordResetView):
    template_name = "Register/password_reset_form.html"
    success_url = reverse_lazy('Register:password_reset_done')
    email_template_name = 'Register/password_reset_email.html'

class UserPassRestDoneView(auth_views.PasswordResetDoneView):
    template_name = "Register/password_reset_done.html"

class UserPassResetConfrim(auth_views.PasswordResetConfirmView):
    template_name = "Register/password_reset_confrim.html"
    success_url = reverse_lazy('Register:password_reset_complete')
class UserPasswordRestCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "Register/password_reset_complete.html"

class UserFollowView(LoginRequiredMixin,View):
    def setup(self, request, *args, **kwargs):
        self.user_instance = User.objects.get(id=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        user = self.user_instance
        if request.user.id == user.id:
            messages.error(request,"You can not follow yourself",extra_tags='dangers')
            return redirect('Register:profile',user.id)
        return super().dispatch(request,*args,**kwargs)

    def get(self,request,user_id):
        user = self.user_instance
        relation = Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            messages.error(request,'You are already follow this user','danger')
        else:
            relation.create(from_user=request.user,to_user=user)
            messages.success(request,'You followed this user','success')
        return redirect('Register:profile',user.id)

class UserUnFollowView(LoginRequiredMixin,View):
    def setup(self, request, *args, **kwargs):
        self.user_instance = User.objects.get(id=kwargs['user_id'])
        return super().setup(request,*args,**kwargs)

    def dispatch(self, request, *args, **kwargs):
        user = self.user_instance
        if request.user.id == user.id:
            messages.error(request,"You can not follow yourself",extra_tags='danger')
            return redirect('Register:profile',user.id)
        return super().dispatch(request,*args,**kwargs)

    def get(self,request,user_id):
        user = self.user_instance
        relation = Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request,'You Unfollowed this user','success')

        else:
            messages.error(request,'You don''t follow this user yet !!!!','danger')
        return redirect('Register:profile',user.id)

