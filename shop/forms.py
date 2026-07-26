from django import forms

from shop.models import Comments


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('name', 'title', 'content')

