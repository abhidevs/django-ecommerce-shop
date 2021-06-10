from django.forms import ModelForm, TextInput, Textarea, FileInput
from .models import Post

class AddPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'author', 'image']
        widgets = {
            'title' : TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'category' : TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'author' : TextInput(attrs={'class': 'form-control', 'placeholder': 'Author'}),
            'content': Textarea(attrs={'cols': 80, 'rows': 20, 'class' : 'form-control', 'id': 'content'}),
            'image': FileInput(attrs={'class': 'form-control', 'id': 'imageInput'})
        }