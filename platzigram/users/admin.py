from django.contrib.auth.models import User
from users.models import Profile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'phone_number', 'website', 'picture')
    list_display_links = ('user', 'id', 'website')

    list_editable = ('phone_number', 'picture')

    search_fields = ('user__email', 'user__first_name',
                     'user__last_name', 'user__username')

    list_filter = ('created_at', 'updated_at', 'user__is_active')

    fieldsets = (
        ('Profile', {
            'fields': (
                ('user', 'picture'),
            )
        }),
        ('Extra Info', {
            'fields': (
                ('website', 'phone_number'),
                ('biography')
            ),
        }),
        ('Metadata', {
            'fields': (('created_at', 'updated_at'))
        })
    )

    readonly_fields = ('created_at', 'updated_at', 'user')


class ProfileInline(admin.StackedInline):

    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):

    inlines = (ProfileInline,)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff'
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
