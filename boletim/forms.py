from django import forms
from .models import Issue

class IssueUploadForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'week_number', 'start_date', 'end_date', 'pdf']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }