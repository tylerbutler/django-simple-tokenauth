from django.contrib import admin
from tokenauth.models import AccessToken

class AccessTokenAdmin(admin.ModelAdmin):
    ordering = ['_time_issued']
    list_display = ('token', 'expiry_time', '_content_type', 'resource')

admin.site.register(AccessToken, AccessTokenAdmin)
