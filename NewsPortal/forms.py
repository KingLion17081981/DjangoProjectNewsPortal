from django import forms
from .models import Post, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'content']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

        labels = {
            'name': 'Имя'
        }

