from django.contrib import admin

# Register your models here.
from .models import User
# admin.py
from django.contrib import admin


class UserModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(UserModelAdmin, self).get_queryset(request)
        if not request.user.is_tl:
            return qs
        return qs.filter(team_name=request.user.team_name, is_superuser=False)


admin.site.register(User,UserModelAdmin)