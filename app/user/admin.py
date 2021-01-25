from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, Contact
from django.contrib import admin


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'staff', 'superuser', 'active')
    list_filter = ('superuser',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('active', 'staff', 'superuser')}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
         ),
    )

    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


class ContactAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'call_iso_code',
        'call_dial_code',
        'call',
        'whatsapp_iso_code',
        'whatsapp_dial_code',
        'whatsapp',
        'date_added',
        'date_modified',
    ]

    search_fields = [
        'user__username',
        'call',
        'whatsapp',
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Contact, ContactAdmin)
