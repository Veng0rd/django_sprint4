from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'comment_count', 'is_published')

        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'datetime-local'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username', 'first_name', 'last_name',
            'email', "password1", "password2",
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username', 'first_name',
            'last_name', 'email',
        )
