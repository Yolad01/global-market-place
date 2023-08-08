from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.query import QuerySet

from .options import Country, Role, SkillLevel, Rate, OrderStatus
import random





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




class JobCategory(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Job Categories"

    def __str__(self):
        return self.title


class Job(models.Model):
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=15, null=True, blank=True)
    price  = models.IntegerField()
    desc = models.TextField(null=True, blank=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    
    
class ClientRequest(models.Model):
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=15, null=True, blank=True)
    price  = models.IntegerField()
    desc = models.TextField(null=True, blank=True)
    user = models.ForeignKey(Clients, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    



class Skill(models.Model):      
    skilla = models.ForeignKey(Skillas, on_delete=models.CASCADE)
    skill = models.ForeignKey(Job, null=True, blank=True, on_delete=models.CASCADE)
    skill_level = models.CharField(max_length=15, blank=True, null=True, choices=SkillLevel.choices)
    base_price = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.skilla.username} ::: {self.skill.title}'
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=20, blank=True, null=True, choices=Country.choices)# change blank to false later
    state = models.CharField(max_length=20, null=True, blank=True) # change blank to false 
    current_location = models.CharField(max_length=20, null=True, blank=True) # may need to be chaged to false depending
    reason = models.TextField(max_length=150, null=True, blank=True)
    activated = models.BooleanField(default=False)
    
    def activate_user(self, *args, **kwargs):
        if self.country is not None and self.state is not None and self.current_location is not None:
            self.activated == True
        
        super(Profile, self).save(*args, **kwargs)
        if self.activated == True:
            return "Account has been activated"
        return "User has not provided location details"

    def __str__(self):
        return self.user.username
    
    

class Material(models.Model):
    name = models.CharField(max_length=20, null=True, blank=False)
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        self.name



class Rating(models.Model):
        
    Rate = Rate
    
    rating = models.IntegerField(blank=True, null=True, choices=Rate.choices)
    skilla = models.ForeignKey(Skillas, on_delete=models.CASCADE, related_name="Ratings_reciever")
    client = models.ForeignKey(Clients, on_delete=models.PROTECT, related_name="ratings_giver")
    
    def __str__(self):
        return f'{self.rater} rated {self.ratee}'
    

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
    
 