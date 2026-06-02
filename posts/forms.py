from django import forms
from .models import Post, Comment, Profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'github_url', 'website_url']