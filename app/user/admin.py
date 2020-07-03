from django.contrib import admin
from .models import User, Contact
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'group', 'country',
                    'staff', 'superuser', 'active')
    list_filter = ('superuser',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Group & Country', {'fields': ('group', 'country',)}),
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

admin.site.register (User, UserAdmin)
admin.site.register (Contact)