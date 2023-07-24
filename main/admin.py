from django.contrib import admin
from main.models import JobCategory, Job
# from django.contrib.auth.admin import UserAdmin

from .models import (
    User, Clients, Skillas, Profile, Material
)

# Register your models here.


admin.site.site_header = "Yolad Global Admin"
admin.site.site_title = "Welcome to Yolad Global"
admin.site.index_title = "Yolad Global"


class UsersAdmin(admin.ModelAdmin):
     list_display = ["username", "role", "email", "phone_no", "first_name"]
     


class JobsCategoryAdmin(admin.ModelAdmin):
     list_display = ["creator", "title"]



# class JobsAdmin(admin.ModelAdmin):
#      list_display = ["jobs", "price", "description"]



class JobsAdmin(admin.ModelAdmin):
     list_display = ["title", "price", "category", "desc"]



class ProfileAdmin(admin.ModelAdmin):
     list_display = ["user", "profile_id", "country", "city", "reason"]



class MaterialAdmin(admin.ModelAdmin):
    list_display = ["name", "desc"]





admin.site.register(Material, MaterialAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(User, UsersAdmin)
admin.site.register(Clients)
admin.site.register(Skillas)
admin.site.register(JobCategory, JobsCategoryAdmin)
admin.site.register(Job, JobsAdmin)



