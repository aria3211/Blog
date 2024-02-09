from django import forms
from .models import Post,Comment



class PostUpdateCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body':forms.Textarea(attrs={'class':'col-sm-12 col-md-6 col-lg-6 col-xl-6 mt-3'})
        }

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body':forms.Textarea(attrs={'class':'col-sm-12 col-md-6 col-lg-6 col-xl-6 mt-3'})
        }

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mr-sm-2'}))