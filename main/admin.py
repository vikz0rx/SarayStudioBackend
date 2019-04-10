from django.contrib import admin
from .models import *

admin.site.register(Profile)

@admin.register(User)
class SarayUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', )

    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)

    def get_exclude(self, request, obj=None):
        exclude = ('last_login', 'groups', 'user_permissions', )

        if obj:
            if request.user == obj:
                exclude += ('is_staff', )
            else:
                exclude += ('password', )

        return exclude

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ()

        if obj:
            if request.user == obj:
                readonly_fields += ('is_active', 'is_superuser', )
            else:
                readonly_fields += ('username', 'email', 'is_superuser', 'is_staff', )

        return readonly_fields