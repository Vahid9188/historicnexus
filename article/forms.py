from django import forms
from article.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content','image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter article title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter article content'}),
        }
        labels = {
            'title': 'Article Title',
            'content': 'Article Content',
        }