from django import forms
from blog.models import Post,Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'title', 'text')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'email','website', 'text')

        # widgets = {
        #     'author': forms.TextInput(attrs={'class':'col-sm-4 blank-arrow'}),
        #     'email': forms.TextInput(attrs={'class':'col-sm-4 blank-arrow'}),
        #     'website': forms.TextInput(attrs={'class':'col-sm-4 blank-arrow'}),
        # }
