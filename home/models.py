from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    slug = models.SlugField()
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created']
    def __str__(self):
        return f'{self.slug}-{self.user}-{self.updated}'
    def get_absolute_url(self):
        return reverse('home:detail',args=(self.id,self.slug,))
    def like_count(self):
        return self.plike.count()

    def unlike(self,user):
        unlike = False
        if self.user.ulike:
            unlike = True
        return unlike


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ucomment')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='pcomment')
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name='rcomment',blank=True,null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user} Comment on {self.post}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ulike')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='plike')
    def __str__(self):
        return f'{self.user} Liekd {self.post}'
