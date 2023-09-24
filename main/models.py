from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.query import QuerySet

from .options import Country, Role, SkillLevel, Rate, OrderStatus
import random
from django.utils import timezone





# def percentage_return(self, *args, **kwargs):
#         self.mul = self.investment_fund * ((self.percent)/100)
#         super(Investors, self).save(*args, **kwargs)
#         return self.mul


# def snip(self):
#         return self.building_description[:20] + "..."   




class User(AbstractUser):
    
    Role = Role
    # base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(verbose_name="Phone Number", unique=True, max_length=15)
    

    REQUIRED_FIELDS = ["first_name", "last_name", "email", "phone_no"]


    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.role
            return super().save(*args, **kwargs)
        


class SkillasManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        results =  super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.SKILLAS)


class Skillas(User):
    base_role = User.Role.SKILLAS

    class Meta:
        proxy = True # links to the original model table. this means that all the user types will be in the same table
    skillas = SkillasManager()
    



class ClientManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        results =  super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CLIENT)


class Clients(User):
    base_role = User.Role.CLIENT

    class Meta:
        proxy=True
    clients = ClientManager()
    
    
    
class CompanyManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        results =  super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.COMPANY)


class Company(User):
    base_role = User.Role.COMPANY

    class Meta:
        proxy = True # links to the original model table. this means that all the user types will be in the same table
    company = CompanyManager()



class JobCategory(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Job Categories"
        

    def __str__(self):
        return self.title


class Job(models.Model):
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=15, null=True, blank=True)
    price  = models.IntegerField()
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    
    
class ClientRequest(models.Model):
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=15, null=True, blank=True)
    price  = models.IntegerField()
    desc = models.TextField(null=True, blank=True)
    user = models.ForeignKey(Clients, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name="Request Created on", default=timezone.now)

    def __str__(self):
        return self.title
    



class Skill(models.Model):      
    skilla = models.ForeignKey(Skillas, on_delete=models.CASCADE)
    # skill_category = models.ForeignKey(JobCategory, blank=True, null=False, on_delete=models.CASCADE)
    skill = models.ForeignKey(Job, null=True, blank=True, on_delete=models.CASCADE)
    skill_level = models.CharField(max_length=15, blank=True, null=True, choices=SkillLevel.choices)
    base_price = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.skilla.username} ::: {self.skill.title}'
    


class SkillaProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=20, blank=True, null=True, choices=Country.choices)# change blank to false later
    state = models.CharField(max_length=20, null=True, blank=True) # change blank to false 
    current_location = models.CharField(max_length=20, null=True, blank=True)
    experience = models.IntegerField(verbose_name="Years of Experience", blank=True, null=True)
    certifications = models.CharField(verbose_name="Education and Certification (Optional)", blank=True, null=True, max_length=256)# may need to be chaged to false depending
    portfolio = models.URLField(verbose_name="Provide url/link or file upload", blank=True, null=True)
    professional_profiles_links = models.CharField(max_length=256, null=True, blank=True)
    hourly_rate = models.IntegerField(verbose_name="Hourly_rate or salary", blank=True, null=True)
    terms_and_conditions = models.BooleanField(default=False, blank=True, null=False)
    # Add BVN column
    
    activated = models.BooleanField(default=False)
    
    def activate_user(self, *args, **kwargs):
        if self.country is not None and self.state is not None and self.current_location is not None:
            self.activated = True
        
        super(SkillaProfile, self).save(*args, **kwargs)
        if self.activated:
            return self.activated
        else:
            self.activated = False
            return self.activated
    

    def __str__(self):
        return self.user.username
    

    

    
    
    
######### Client profile goes here
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=20, blank=True, null=True, choices=Country.choices)
    current_location = models.CharField(max_length=20, null=True, blank=True)
    home_address = models.CharField(max_length=256, null=True, blank=True)
    occupation = models.CharField(max_length=50, null=True, blank=True)
    id_card = models.ImageField(upload_to="id_cards_for_kyc")
    services_needed = models.CharField(max_length=256, null=True, blank=True)
    terms_and_conditions = models.BooleanField(default=False, blank=True, null=False)
    
    activated = models.BooleanField(default=False)
    
    def activate_user(self, *args, **kwargs):
        if self.country is not None and self.state is not None and self.current_location is not None:
            self.activated = True
        
        super(ClientProfile, self).save(*args, **kwargs)
        if self.activated:
            return self.activated
    
    def __str__(self):
        return self.user.username

######### Company Profile Goes here

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200, blank=True, null=False)
    location = models.CharField(verbose_name="Location (City/Country)", max_length=100, blank=True, null=False, choices=Country.choices)
    state = models.CharField(max_length=50, blank=True, null=False)
    industry = models.CharField(verbose_name="Industry or Business Type", max_length=100, blank=True, null=False)
    company_size = models.IntegerField(verbose_name="company size (Number of Employees)", blank=True, null=True)
    services = models.CharField(verbose_name="Describe the services or skills needed (Optional)", max_length=200, blank=True, null=True)
    work_history_with_freelancer = models.BooleanField(verbose_name="Have you worked with a freelancer or skilled workers Before", null=True, blank=True)
    terms_and_conditions = models.BooleanField(default=False, blank=True, null=False)
    
    activated = models.BooleanField(default=False)
    
    def activate_user(self, *args, **kwargs):
        if self.country is not None and self.state is not None and self.location is not None:
            self.activated = True
        
        super(ClientProfile, self).save(*args, **kwargs)
        if self.activated:
            return self.activated
    
    def __str__(self):
        return self.company_name
    
    


class Rating(models.Model):
        
    Rate = Rate
    
    rating = models.IntegerField(blank=True, null=True, choices=Rate.choices)
    skilla = models.ForeignKey(Skillas, on_delete=models.CASCADE, related_name="Ratings_reciever")
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name="ratings_giver")
    
    def __str__(self):
        return f'{self.client} rated {self.skilla}'
    

def order_number() -> int:
    num = random.randint(100000, 999999)
    return num
    
class Order(models.Model):
    status = OrderStatus
    
    skilla = models.ForeignKey(Skillas, on_delete=models.CASCADE, related_name="jobber")
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name="payer")
    notification  = models.CharField(max_length=256, null=True, blank=True)
    paid = models.BooleanField(default=False)
    order_no = models.IntegerField(default=order_number)
    gig_desc = models.TextField(verbose_name="Gig description", max_length=200, null=True, blank=False)
    order_status = models.CharField(
        max_length=15,
        null=False,
        choices=status.choices,
        default=status.PENDING
    )
    order_created = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return f"Order between {self.skilla} and {self.client}"
    
    
