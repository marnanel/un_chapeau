from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
import trilby_api.models as models

class TrilbyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = models.User

class TrilbyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = UserCreationForm.Meta.fields + (
                'email',
                )

class TrilbyUserAdmin(UserAdmin):

    form = TrilbyUserChangeForm
    add_form = TrilbyUserCreationForm

    add_fieldsets = UserAdmin.add_fieldsets + (
            (None, {
                'classes': 'wide',
                'fields': (
                    'email',
                    ),
                }),
            )

    fieldsets = UserAdmin.fieldsets + (
            (None, {
                'fields': (
                    '_avatar',
                    '_header',
                    'locked',
                    'note',
                    'linked_url',
                    'moved_to',
                    ),
                }),
            ('Relationships', {
                'fields': (
                    ('following', 'blocking',), 
                    ),
                }),
             )

admin.site.register(models.User)
admin.site.register(models.Status)

