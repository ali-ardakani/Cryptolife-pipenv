from django import forms
from django.forms import fields, widgets
from .models import News, Comment


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'header_image', 'body', 'category')

        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'body' : forms.Textarea(attrs={'class':'form-control'}),
            'category' : forms.SelectMultiple(attrs={'class':'form-control'}),

        }

    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

        widgets = {
            'comment' : forms.Textarea(attrs={'class':'form-control'})
        }