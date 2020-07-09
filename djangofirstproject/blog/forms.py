from django import forms
from .models import Comment, NewsLetterSubscriber


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label='', widget=forms.TextInput(attrs={'placeholder': "name"}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': "email"}))
    to = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': "email"}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'your comment body (optional)', 'class': 'comment-body'}), label='')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'id': 'comment-name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'id': 'comment-email'}),
            'body': forms.Textarea(attrs={'placeholder': 'comment body . . . ', 'class': 'comment-body'})
        }


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search . . .'}))

class News(forms.ModelForm):
    class Meta:
        model = NewsLetterSubscriber
        fields = ('name', 'last_name', 'email')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'LastName'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'})
        }