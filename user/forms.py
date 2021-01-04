from django import forms

from user.models import users


class PasswordField(forms.CharField):
    widget = forms.PasswordInput


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = PasswordField()
    password2 = PasswordField()

    def is_valid(self):
        return super().is_valid() and \
            not users() \
            .filter(username=self.data['username']) \
            .exists() and \
            self.data['password1'] == self.data['password2']
