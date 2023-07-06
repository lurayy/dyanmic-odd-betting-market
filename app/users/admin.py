from django.contrib import admin
from .models import UserProfile, UserBase

admin.site.register(UserBase)
admin.site.register(UserProfile)
