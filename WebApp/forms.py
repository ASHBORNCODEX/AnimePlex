from django import forms
from AdminApp.models import CommentDB , RatingDB

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentDB
        fields = ['content']
        labels = {
            'content': ''  # no label
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'})
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = RatingDB
        fields = ['value']
