from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.query import QuerySet

# Create your models here.


# def percentage_return(self, *args, **kwargs):
#         self.mul = self.investment_fund * ((self.percent)/100)
#         super(Investors, self).save(*args, **kwargs)
#         return self.mul


# def snip(self):
#         return self.building_description[:20] + "..."   




class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CLIENT = "CLIENT", "Client"
        SKILLAS = "SKILLAS", "Skillas"

    # base_role = Role.ADMINa
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

    def __str__(self):
        return self.title
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_id = models.IntegerField(null=True, blank=True)
    country = models.CharField(null=True, blank=True, max_length=20)
    city = models.CharField(null=True, blank=True, max_length=20)
    reason = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    
    

class Material(models.Model):
    name = models.CharField(max_length=20, null=True, blank=False)
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        self.name




class Skill(models.Model):
    
    SkillLevel = models.TextChoices("SkillLevel", "BEGINNER INTERMEDIATE EXPERT")
    skilla = models.ForeignKey(Skillas, on_delete=models.CASCADE)
    skill_level = models.CharField(max_length=15, blank=True, null=True, choices=SkillLevel.choices)
    base_price = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.skilla.username




class Rating(models.Model):
    
    class Rate(models.IntegerChoices):
        STAR_1 = 1, "*"
        STAR_2 = 2, "**"
        STAR_3 = 3, "***"
        STAR_4 = 4, "****"
        STAR_5 = 5, "*****"
        
    rating = models.IntegerField(blank=True, null=True, choices=Rate.choices)
    ratee = models.ForeignKey(Skillas, on_delete=models.CASCADE, related_name="Ratings_reciever")
    rater = models.ForeignKey(Clients, on_delete=models.PROTECT, related_name="ratings_giver")
    
    def __str__(self):
        return f'{self.rater} rated {self.ratee}'
    
    
    
    