from django import forms
from .models import Article
from mdeditor.fields import MDTextField

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model=Article
        fields=('title','category','body','tags')
