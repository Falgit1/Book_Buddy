from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    phone_number = forms.CharField(max_length=15, required=True)

