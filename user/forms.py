from django import forms

from user.models import users


class PasswordField(forms.CharField):
    widget = forms.PasswordInput


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = PasswordField()
    password_again = PasswordField()

    def is_valid(self):
        return super().is_valid() and \
            not users() \
            .filter(username=self.data['username']) \
            .exists() and \
            self.data['password'] == self.data['password_again']
