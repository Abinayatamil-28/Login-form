from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one number")
        if not any(char.isalpha() for char in password):
            raise ValidationError("Password must contain at least one letter")
        if not any(char in '!@#$%^&*()_+-=[]{};:,.<>?/' for char in password):
            raise ValidationError("Password must contain at least one special character")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password!= confirm_password:
            raise ValidationError("Passwords do not match")

class PasswordResetForm(forms.Form):
    username = forms.CharField()
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if len(new_password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in new_password):
            raise ValidationError("Password must contain at least one number")
        if not any(char.isalpha() for char in new_password):
            raise ValidationError("Password must contain at least one letter")
        if not any(char in '!@#$%^&*()_+-=[]{};:,.<>?/' for char in new_password):
            raise ValidationError("Password must contain at least one special character")
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise ValidationError("Passwords do not match")
