from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from djangoapp.models import Comment, Post, UserExtended


class UserExtendedInline(admin.StackedInline):
    model = UserExtended
    can_delete = False
    verbose_name = 'user'
    verbose_name_plural = 'users'


class UserAdmin(BaseUserAdmin):
    inlines = (UserExtendedInline, )


class CommentAdmin(admin.ModelAdmin):
    pass


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
