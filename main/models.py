from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.query import QuerySet

from .utils.options import Country, Role, SkillLevel, Rate
import random
from django.utils import timezone
from datetime import datetime
from django.conf import settings

from main.managers import ThreadManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg



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
    is_certified = models.BooleanField(default=False)
    

    REQUIRED_FIELDS = ["first_name", "last_name", "email", "phone_no"]


    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.role = self.role
    #         return super().save(*args, **kwargs)
        


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
    
    
    
# class CompanyManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs) -> QuerySet:
#         results =  super().get_queryset(*args, **kwargs)
#         return results.filter(role=User.Role.COMPANY)


# class Company(User):
#     base_role = User.Role.COMPANY

#     class Meta:
#         proxy = True # links to the original model table. this means that all the user types will be in the same table
#     company = CompanyManager()



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
    skilla = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(JobCategory, blank=True, null=True, on_delete=models.CASCADE)
    skill = models.ForeignKey(Job, null=True, blank=True, on_delete=models.CASCADE)
    level = models.CharField(max_length=15, blank=True, null=True, choices=SkillLevel.choices)
    image = models.ImageField(upload_to="skill_images", blank=True, null=False, default=None)
    base_price = models.PositiveIntegerField(blank=True, null=True)
    activate = models.BooleanField(default=True, blank=True, null=True)

    def view_gigs(self, user_id, *args, **kwargs):
        ...
    
    def __str__(self):
        return f'{self.skilla.username} ==> {self.skill.title}'
    


class SkillaProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="skillas_profile")
    country = models.CharField(max_length=20, blank=True, null=True, choices=Country.choices)# change blank to false later
    state = models.CharField(max_length=20, null=True, blank=True) # change blank to false 
    house_address = models.CharField(max_length=100, default=None, null=True, blank=True)
    street_name = models.CharField(max_length=100, default=None, null=True, blank=True)
    region = models.CharField(max_length=100, default=None, null=True, blank=True)
    city = models.CharField(max_length=100, default=None, null=True, blank=True)
    Postal_code = models.CharField(max_length=10, default=None, null=True, blank=True)
    current_location = models.CharField(max_length=20, null=True, blank=True)
    experience = models.PositiveSmallIntegerField(verbose_name="Years of Experience", blank=True, null=True)
    portfolio = models.URLField(verbose_name="links to your works", blank=True, null=True)
    professional_profiles_links = models.CharField(max_length=256, null=True, blank=True)
    nin = models.CharField(max_length=11, null=True, blank=True)
    id_card = models.ImageField(upload_to="skillas_id_cards_for_kyc", null=True, blank=True)
    passport_photo = models.ImageField(upload_to="passport_photo", null=True, blank=True)
    # hourly_rate = models.PositiveIntegerField(verbose_name="Hourly_rate or salary", blank=True, null=True)
    # terms_and_conditions = models.BooleanField(default=False, blank=True, null=False)
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
    
    

def order_number() -> int:
    num = random.randint(100000, 999999)
    return num
    
class Order(models.Model):
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
    completed = models.BooleanField(default=False)

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
        null=False,
        default=None
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
    



class MessageReadStatus(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('message', 'user')

    def __str__(self) -> str:
        return self.user.username


@receiver(post_save, sender=Message)
def create_message_read_status(sender, instance, created, **kwargs):
    if created:
        for user in instance.thread.users.all():
            if user != instance.sender:
                MessageReadStatus.objects.create(message=instance, user=user, is_read=False)

def get_unread_messages_count(user):
    return MessageReadStatus.objects.filter(user=user, is_read=False).count()



class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_wallet")
    main = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    pending = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    withdrawn = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self) -> str:
        return self.user.username
    


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_payer")
    email = models.EmailField(blank=True, null=True)
    skilla = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="skilla_paid", blank=True, null=True)
    skilla_image = models.ImageField(default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reference = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=12, blank=True, null=True)
    channel = models.CharField(max_length=10, blank=True, null=True)
    card_type = models.CharField(max_length=10, blank=True, null=True)
    time_of_payment = models.CharField(max_length=20, blank=True, null=True)
    order_no = models.PositiveSmallIntegerField(default=0)
    completed = models.BooleanField(default=False)


    def get_skilla_order_count(self, user):
        self.count = Payment.objects.filter(skilla=user).count()
        return self.count
    

    def __str__(self) -> str:
        return self.user.username
    


class UserReview(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rated_user")
    rater = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="rater")
    rating = models.IntegerField(choices=Rate.choices, default=None)
    comment = models.CharField(max_length=100, null=True, blank=True)

    def get_rating(self, user_id) -> list:
        """
            returns the average rating, and 
            a queryset of all the ratings
        """
        self.ratings = UserReview.objects.filter(user=user_id)
        self.average_rating = UserReview.objects.aggregate(average_rating=Avg("rating"))
        return [self.average_rating, self.ratings]

    def __str__(self) -> str:
        return f'{self.rater.username} rated {self.user.username} {self.rating} star(s)'
    



class Compliance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complied = models.BooleanField(default=False)

    def __str__(self) -> str:
        if self.complied == True:
            return f'{self.user} has complied'
        else:
            return f'{self.user} has not complied'


# class Identity(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     house_address = models.CharField(max_length=100)
#     street_name = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     region = models.CharField(max_length=100)
#     country = models.CharField(max_length=50)
#     Postal_code = models.CharField(max_length=10)
#     passport_photo = models.ImageField(upload_to="compliance", height_field=None, width_field=None)
#     ...

