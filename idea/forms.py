from django import forms
from django.forms import fields, widgets
from .models import Idea, CommentIdea


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('title', 'header_image', 'body', 'category')

        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'body' : forms.Textarea(attrs={'class':'form-control'}),
            'category' : forms.SelectMultiple(attrs={'class':'form-control'}),

        }

    
class CommentIdeaForm(forms.ModelForm):
    class Meta:
        model = CommentIdea
        fields = ('comment_idea',)

        widgets = {
            'comment_idea' : forms.Textarea(attrs={'class':'form-control'})
        }