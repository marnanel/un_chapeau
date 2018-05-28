from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
import trilby_api.models as models

class TrilbyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = models.User

class TrilbyUserAdmin(UserAdmin):

    form = TrilbyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {
                'fields': (
                    'avatar',
                    'header',
                    'locked',
                    'note',
                    'url',
                    'moved_to',
                    )}),
            )

admin.site.register(models.User, TrilbyUserAdmin)
admin.site.register(models.Status)

