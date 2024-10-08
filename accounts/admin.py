from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_admin')
    search_fields = ('email',)

admin.site.register(User, UserAdmin)

