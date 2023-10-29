from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

from .models import (
    User, Clients, Skillas, SkillaProfile, Skill, Rating, ClientRequest, Order,
    ClientProfile, CompanyProfile, JobCategory, Job, AboutSkilla, TrainingAndCertification,
    ProfilePicture, Brief
)

# Register your models here.


admin.site.site_header = "Yolad Global Admin"
admin.site.site_title = "Welcome to Yolad Global"
admin.site.index_title = "Yolad Global"


class UsersAdmin(admin.ModelAdmin):
     list_display = ["username", "role", "email", "phone_no", "first_name"]
     


class JobsCategoryAdmin(admin.ModelAdmin):
     list_display = ["title"]



class JobsAdmin(admin.ModelAdmin):
     list_display = ["title", "price", "category", "desc"]



class SkillaProfileAdmin(admin.ModelAdmin):
     list_display = [
          "user",
          "country",
          "state",
          "current_location",
          "experience",
          "certifications",
          "portfolio",
          "professional_profiles_links",
          "hourly_rate",
          "activated"
     ]
     
     
class ClientProfileAdmin(admin.ModelAdmin):
     list_display = [
          "user",
          "country",
          "current_location",
          "home_address",
          "occupation",
          "id_card",
          "terms_and_conditions",
          "activated"
     ]



class CompanyProfileAdmin(admin.ModelAdmin):
     list_display = [
          "user",
          "company_name",
          "location",
          "state",
          "industry",
          "company_size",
          "services",
          "work_history_with_freelancer",
          "terms_and_conditions",
          "activated"
     ]
     
     
    
    
    
class SkillAdmin(admin.ModelAdmin):
     list_display = ["skilla", "skill", "skill_level", "base_price"]
     


class RatingAdmin(admin.ModelAdmin):
     list_display = ["skilla", "rating", "client"]
     

class ClientRequestAdmin(admin.ModelAdmin):
     list_display = ["title", "price", "desc", "created"]


class OrderAdmin(admin.ModelAdmin):
     list_display = ["skilla", "client", "paid", "order_no", "order_status", "order_created"]


class AboutSkillaAdmin(admin.ModelAdmin):
     list_display = [
          "user", "about", "work_experience"
     ]


class TrainingAndCertificationForm(admin.ModelAdmin):
     list_display = [
          "user", "cert_earned", "skill_learned", "grade", "assessed"
     ]


class BriefAdmin(admin.ModelAdmin):
     list_display = [
          "user", "title", "description", "attach_files", "categories", "budget", "budget_flexible", "date"
     ]



admin.site.register(Rating, RatingAdmin)
admin.site.register(SkillaProfile, SkillaProfileAdmin)
admin.site.register(User, UsersAdmin)
admin.site.register(Clients)
admin.site.register(Skillas)
admin.site.register(JobCategory, JobsCategoryAdmin)
admin.site.register(Job, JobsAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(ClientRequest, ClientRequestAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ClientProfile, ClientProfileAdmin)
admin.site.register(CompanyProfile, CompanyProfileAdmin)
admin.site.register(AboutSkilla, AboutSkillaAdmin)
admin.site.register(TrainingAndCertification, TrainingAndCertificationForm)
admin.site.register(ProfilePicture)
admin.site.register(Brief, BriefAdmin)



