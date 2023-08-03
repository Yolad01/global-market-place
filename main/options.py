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
	
        
        
class Rate(models.IntegerChoices):
	STAR_1 = 1, "1"
	STAR_2 = 2, "2"
	STAR_3 = 3, "3"
	STAR_4 = 4, "4"
	STAR_5 = 5, "5"


 
class OrderStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    IN_PROGRESS = "IN_PROGRESS", "In progress"
    COMPLETED = "COMPLETED", "Completed"
    
    