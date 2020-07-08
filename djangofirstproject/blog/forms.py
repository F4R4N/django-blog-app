from django import forms
from .models import Comment, NewsLetter


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'id': 'comment-name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'id': 'comment-email'}),
            'body': forms.Textarea(attrs={'placeholder': 'comment body . . . ', 'id': 'comment-body'})
        }


class SearchForm(forms.Form):
    query = forms.CharField()

class News(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = ('name', 'last_name', 'email')