from django.contrib import admin
from .models import Record, User
from django.contrib.auth.admin import UserAdmin

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class MyUserAdmin(UserAdmin):
    pass

