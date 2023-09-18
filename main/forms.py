from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import User
from main.models import (JobCategory, Job, Rating,
                         SkillaProfile, Skill, ClientProfile
                         )


class RegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username","first_name", "last_name", "email", "phone_no", "role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["phone_no"].required = True
        
        

class JobCategoryForm(forms.ModelForm):
    class Meta:
        model = JobCategory
        fields = ["title", "creator"]
        
        
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields ="__all__"
        
        
class SkillaProfileForm(forms.ModelForm):
    model = SkillaProfile
    fields = [
          "user",
          "country",
          "state",
          "current_location",
          "experience",
          "certifications",
          "portfolio",
          "professional_profiles_links",
          "hourly_rate"
    ]
    
    
    
class ClientProfileForm(forms.ModelForm):
    model = ClientProfile
    fields = [
          "user",
          "country",
          "state",
          "current_location",
          "home_address",
          "occupation",
          "id_card",
          "services_needed",
          "terms_and_conditions"
    ]
    
    
    
class RatingForm(forms.ModelForm):
    model = Rating
    fields = [
        "rating",
        "skilla",
        "client"
    ]
    
    
class SkillForm(forms.ModelForm):
    model = Skill
    fields = [
        "skilla",
        "skill_category",
        "skill",
        "skill_level",
        "base_price"
    ]
    
    
