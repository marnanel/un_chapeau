from django import forms
from django.contrib import admin
import buckethat_salmon.models

class MessageAdmin(admin.ModelAdmin):

    # idea found at
    # https://stackoverflow.com/questions/430592/django-admin-charfield-as-textarea#431412

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)

        if db_field.name == 'data':

            attrs = formfield.widget.attrs

            formfield.widget = forms.Textarea(
                    attrs=attrs,
                    )

        return formfield

admin.site.register(buckethat_salmon.models.Message,
        MessageAdmin)
