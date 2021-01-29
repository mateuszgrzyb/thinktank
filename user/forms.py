from django import forms

from user.models import users


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def is_valid(self):
        user_exist = users().filter(username=self.data['username']).exists()
        equal_pass = self.data['password'] == self.data['password2']
        return super().is_valid() and user_exist and equal_pass

