from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'salt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter salt'}),
            'grade_level': forms.Select(attrs={'class': 'form-select'}),
            'schedules': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter schedules'}),
            'course_catalog': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'high_school_gpa_w': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'high_school_gpa_uw': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sat_reading': forms.NumberInput(attrs={'class': 'form-control'}),
            'sat_math': forms.NumberInput(attrs={'class': 'form-control'}),
            'act': forms.NumberInput(attrs={'class': 'form-control'}),
            'chosen_major': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter chosen major'}),
            'college_level': forms.Select(attrs={'class': 'form-select'}),
            'extracurr_awards': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter extracurricular awards'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter notes'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
