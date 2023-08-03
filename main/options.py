from django.db import models


class Country(models.TextChoices):
    
    NIGERIA = "NIGERIA", "Nigeria"
    UK = "UK", "United Kingdom"
    USA = "USA", "United States of America"
    GHANA = "GHANA", "Ghana"
    
    
    
class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CLIENT = "CLIENT", "Client"
        SKILLAS = "SKILLAS", "Skillas"
        
        
        
class SkillLevel(models.TextChoices):
        LEVEL_1 = "BEGINNER", "Beginner"
        LEVEL_2= "INTERMEDIATE", "Intermediate"
        LEVEL_3 = "EXPERT", "Expert"