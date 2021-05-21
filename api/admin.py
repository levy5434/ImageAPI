from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AccountTier, ExpiringLink, Image, Thumbnail, User

fields = list(UserAdmin.fieldsets)
fields[0] = (None, {"fields": ("username", "password", "accountTier")})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(Thumbnail)
admin.site.register(AccountTier)
admin.site.register(ExpiringLink)
admin.site.register(Image)
admin.site.register(User, UserAdmin)
