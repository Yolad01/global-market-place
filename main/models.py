from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.query import QuerySet

from .options import Country, Role, SkillLevel, Rate, OrderStatus
import random
from django.utils import timezone
from datetime import datetime
from django.conf import settings

from main.managers import ThreadManager
from django.db import models






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
    title = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Job Categories"
        

    def __str__(self):
        return self.title


class Job(models.Model):
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=15, null=True, blank=True)
    price  = models.PositiveIntegerField()
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    
    
class ClientRequest(models.Model):
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=15, null=True, blank=True)
    price  = models.PositiveIntegerField()
    desc = models.TextField(null=True, blank=True)
    user = models.ForeignKey(Clients, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name="Request Created on", default=timezone.now)

    def __str__(self):
        return self.title
    



class Skill(models.Model):      
    skilla = models.ForeignKey(Skillas, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(JobCategory, blank=True, null=True, on_delete=models.CASCADE)
    skill = models.ForeignKey(Job, null=True, blank=True, on_delete=models.CASCADE)
    level = models.CharField(max_length=15, blank=True, null=True, choices=SkillLevel.choices)
    image = models.ImageField(upload_to="skill_images", blank=True)
    base_price = models.PositiveIntegerField(blank=True, null=True)
    activate = models.BooleanField(default=True, blank=True, null=True)
    
    def __str__(self):
        return f'{self.skilla.username} ==> {self.skill.title}'
    


class SkillaProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=20, blank=True, null=True, choices=Country.choices)# change blank to false later
    state = models.CharField(max_length=20, null=True, blank=True) # change blank to false 
    current_location = models.CharField(max_length=20, null=True, blank=True)
    experience = models.PositiveSmallIntegerField(verbose_name="Years of Experience", blank=True, null=True)
    portfolio = models.URLField(verbose_name="links to your works", blank=True, null=True)
    professional_profiles_links = models.CharField(max_length=256, null=True, blank=True)
    identification = models.ImageField(upload_to="skillas_id_cards_for_kyc", null=True, blank=True)
    hourly_rate = models.PositiveIntegerField(verbose_name="Hourly_rate or salary", blank=True, null=True)
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
    terms_and_conditions = models.BooleanField(default=False, blank=True, null=False)
    
    activated = models.BooleanField(default=False)
    
    def activate_user(self, *args, **kwargs):
        if self.country is not None and self.home_address is not None and self.current_location is not None:
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
    company_size = models.PositiveSmallIntegerField(verbose_name="company size (Number of Employees)", blank=True, null=True)
    services = models.CharField(verbose_name="Describe the services or skills needed (Optional)", max_length=200, blank=True, null=True)
    work_history_with_freelancer = models.BooleanField(verbose_name="Have you worked with a freelancer or skilled workers Before", null=True, blank=True)
    terms_and_conditions = models.BooleanField(default=False, blank=True, null=False)
    
    activated = models.BooleanField(default=False)
    
    def activate_user(self, *args, **kwargs):
        if self.company_name is not None and self.state is not None and self.location is not None:
            self.activated = True
        
        super(ClientProfile, self).save(*args, **kwargs)
        if self.activated:
            return self.activated
    
    def __str__(self):
        return self.company_name
    
    

class Rating(models.Model):
        
    Rate = Rate
    
    rating = models.PositiveSmallIntegerField(blank=True, null=True, choices=Rate.choices)
    skilla = models.ForeignKey(Skillas, on_delete=models.CASCADE, related_name="Ratings_reciever")
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name="ratings_giver")
    
    def __str__(self):
        return f'{self.client} rated {self.skilla}'
    

def order_number() -> int:
    num = random.randint(100000, 999999)
    return num
    
class Order(models.Model):
    status = OrderStatus
    
    skilla = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobber")
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payer")
    notification  = models.PositiveIntegerField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    order_no = models.PositiveSmallIntegerField(default=order_number)
    gig_desc = models.TextField(verbose_name="Gig description", max_length=200, null=True, blank=False)
    delivery = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    accepted = models.BooleanField(default=False)
    decline = models.BooleanField(default=False)
    order_status = models.CharField(
        max_length=15,
        null=False,
        choices=status.choices,
        default=status.PENDING
    )

    order_created = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return f"Order between {self.skilla} and {self.client}"
    
    
class AboutSkilla(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=150)
    work_experience = models.CharField(max_length=128, null=True, blank=True)

    def snip(self):
        return self.about[:20] + "..."

    def __str__(self):
        return self.user.username

class TrainingAndCertification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cert_earned = models.CharField(max_length=100, null=True, blank=True)
    skill_learned = models.CharField(max_length=100, null=True, blank=True)
    grade = models.CharField(max_length=128, null=True, blank=True)
    assessed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    

class ProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        verbose_name="Profile Picture",
        upload_to="profile_pictures",
    )

    def __str__(self):
        return self.user.username
    


class Brief(models.Model):
    user = models.ForeignKey(
        Clients,
        on_delete=models.CASCADE,
        related_name="client"
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    attach_files = models.FileField(
        upload_to="project_description_files",
        blank=True,
        null=True
    )
    categories = models.ForeignKey(
        JobCategory,
        models.CASCADE
    )
    budget = models.IntegerField(
        blank=True,
        null=False
    )
    budget_flexible =  models.BooleanField(
        default=False
    )
    date = models.DateTimeField(default=datetime.now)
    skilla = models.ForeignKey(
        Skillas,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="skilla"
    )

    def __str__(self):
        return self.user.username
    


class SkillaReachoutToClient(models.Model):
    user = models.ForeignKey(
        Skillas,
        on_delete=models.CASCADE,
        related_name="client_skilla_reachout_to_client"
    )
    client = models.ForeignKey(
        Clients,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="skilla_skilla_reachout_to_client"
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    categories = models.ForeignKey(
        JobCategory,
        models.CASCADE
    )
    budget = models.IntegerField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.user.username} and {self.client.username}'
    



class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True




class Thread(TrackingModel):
    THREAD_TYPE = (
        ('personal', 'Personal'),
        ('group', 'Group')
    )

    name = models.CharField(max_length=50, null=True, blank=True)
    thread_type = models.CharField(max_length=15, choices=THREAD_TYPE, default='group')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    objects = ThreadManager()

    def __str__(self) -> str:
        if self.thread_type == 'personal' and self.users.count() == 2:
            return f'{self.users.first()} and {self.users.last()}'
        return f'{self.name}'


class Message(TrackingModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)

    def __str__(self) -> str:
        return f'From <Thread - {self.thread}>'



class ContactList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="owner")
    contacts = models.ManyToManyField(User, blank=True, related_name="contacts")

    def __str__(self):
        return self.user.username
    
    def add_contact(self, account):
        # if not account in self.contacts.all():
        if not self.contacts.filter(id=account.id).exists():
            self.contacts.add(account)
            self.save()

    # def remove_contact(self, account):
    #     if account in self.contacts.all():
    #         self.contacts.remove(account)

    # def uncontact(self, removee):
    #     remover = self
    #     remover.remove_contact(removee)
    #     contact_list = ContactList.objects.get(user=removee)
    #     contact_list.remove_contact(self.owner)

    # def is_contact(self, contact):
    #     if contact in self.contacts.all():
    #         return True
    #     return False
    


class ConnectRequest(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sender"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="receiver"
    )
    is_active = models.BooleanField(
        blank=True,
        null=False,
        default=True
    )

    def __str__(self):
        self.sender.username

    def connect_with_contact(self):
        receiver_contact_list = ContactList.objects.get(user=self.receiver)
        if receiver_contact_list:
            receiver_contact_list.add_contact(self.sender)
            sender_contact_list = ContactList.objects.get(user=self.sender)
            if sender_contact_list:
                sender_contact_list.add_contact(self.receiver)
                self.is_active: bool = False
                self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()
    


