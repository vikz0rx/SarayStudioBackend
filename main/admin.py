from PIL import Image
from django.contrib import admin
from .models import *

class MultipleImagePhotographsInline(admin.TabularInline):
    model = MultipleImagePhotographs
    extra = 4

    def save_model(self, *args, **kwargs):
       instance = super(MultipleImagePhotographs, self).save(*args, **kwargs)
       image = Image.open(instance.image.path)
       image.save(instance.image.path, quality=20, optimize=True)
       return instance

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstname', 'lastname', )

    def get_queryset(self, request):
        return Profile.objects.filter(user__is_staff=False)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ()

        if obj:
            if request.user != obj.user:
                readonly_fields += ('user', 'firstname', 'lastname', 'middlename', 'birthdate', 'p_series', 'p_number', 'insurance', 'sms_notification', 'email_notification', )

        return readonly_fields

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', )

    def get_queryset(self, request):
        return User.objects.filter(is_staff=True)

    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)
        obj.save()

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

@admin.register(Photographs)
class PhotographsAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'instagram', 'is_staff')
    inlines = (MultipleImagePhotographsInline, )