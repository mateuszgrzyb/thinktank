from django import forms
from django.core.exceptions import ValidationError

from user.models import User
from user.models import users


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        data = super().clean()

        user_exist = users().filter(username=data.get('username')).exists()
        equal_pass = data.get('password') == data.get('password2')
        if not equal_pass:
            raise ValidationError("Passwords differ.")
        elif user_exist:
            raise ValidationError("The username is taken.")

    def save(self):
        return users().create_user(**{
            k: self.cleaned_data[k] for k in [
                'username',
                'email',
                'password',
            ]
        })


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'bio',
        ]

