from django.forms import ModelForm

from user.models import User


class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'bio',
        ]
