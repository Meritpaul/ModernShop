from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model  = Review
        fields = ('rating', 'title', 'body')
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Review title (optional)'}),
            'body':  forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your experience...'}),
        }
