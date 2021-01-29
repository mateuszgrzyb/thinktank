from django.contrib import admin

from user.models import PrivRoom
from user.models import User

admin.site.register(User)
admin.site.register(PrivRoom)
