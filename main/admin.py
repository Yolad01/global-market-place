from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

from .models import (
    BlogCategory, BlogPost, User, Clients, Skillas, SkillaProfile, Skill, ClientRequest, Order,
    ClientProfile, CompanyProfile, JobCategory, Job, AboutSkilla, TrainingAndCertification,
    ProfilePicture, Brief, SkillaReachoutToClient, ConnectRequest,
    Message, Thread, ContactList, Payment, MessageReadStatus, UserReview, Wallet

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
          "country",
          "state",
          "current_location",
          "experience",
          "portfolio",
          "passport_photo",
          "professional_profiles_links",
          # new fields
          "house_address",
          "street_name",
          "region",
          "city",
          "Postal_code",
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
     list_display = ["title", "skill", "category", "image", "level", "base_price"]
     
     

class ClientRequestAdmin(admin.ModelAdmin):
     list_display = ["title", "price", "desc", "created"]


class OrderAdmin(admin.ModelAdmin):
     list_display = [
          "skilla", "client", "paid", "order_no",
          "delivery", "price", "accepted", "decline", "created_at"
     ]


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


class SkillaReachoutToClientAdmin(admin.ModelAdmin):
     list_display = [
           "user",
           "client",
           "title",
           "description",
           "categories",
           "budget"
     ]


class ContactListAdmin(admin.ModelAdmin):
     list_filter = ['user']
     list_display = ['user']
     search_fields = ['user']
     readonly_fields = ['user']

     class Meta:
          model = ContactList



class ConnectRequestAdmin(admin.ModelAdmin):
     list_filter = ["sender", "receiver"]
     list_display = ["sender", "receiver"]
     search_fields = ["sender__username", "receiver__username","sender__email", "receiver__email"]

     class Meta:
          model = ConnectRequest



class MessageInline(admin.StackedInline):
    model = Message
    fields = ('sender', 'text')
    readonly_fields = ('sender', 'text')


class ThreadAdmin(admin.ModelAdmin):
    model = Thread
    inlines = (MessageInline,)



class PaymentAdmin(admin.ModelAdmin):
     list_display = [
          "user",
          "skilla",
          "amount",
          "reference",
          "status",
          "completed"
     ]

admin.site.register(Payment, PaymentAdmin)


class WalletAdmin(admin.ModelAdmin):
     list_display = [
          "user",
          "main",
          "pending",
          "withdrawn"
     ]

admin.site.register(Wallet, WalletAdmin)


class UserReviewAdmin(admin.ModelAdmin):
     list_display = [
          "user",
          "rater",
          "rating",
          "comment"
     ]
admin.site.register(UserReview, UserReviewAdmin)




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
admin.site.register(SkillaReachoutToClient, SkillaReachoutToClientAdmin)

admin.site.register(ContactList, ContactListAdmin)
admin.site.register(ConnectRequest, ConnectRequestAdmin)

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message)
admin.site.register(MessageReadStatus)

admin.site.register(BlogCategory)
admin.site.register(BlogPost)


