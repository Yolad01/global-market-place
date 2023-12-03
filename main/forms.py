from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import User
from main.models import (JobCategory, Job, Rating,
                         SkillaProfile, Skill, ClientProfile,
                         CompanyProfile, AboutSkilla, TrainingAndCertification,
                         ProfilePicture, Brief, ChatMessage
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
        fields = ["title"]
        
        
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields ="__all__"
        
        
class SkillaProfileForm(forms.ModelForm):
    class Meta:
        model = SkillaProfile
        fields = (
            "country",
            "state",
            "current_location",
            "experience",
            "certifications",
            "portfolio",
            "professional_profiles_links",
            "hourly_rate",
        )
    
      ##### Validation checks
    def clean_experience(self):
        experience = self.cleaned_data.get("experience")
        if experience < 0:
            raise forms.ValidationError("Experience shall not be negative")
        return experience

    
    
    
class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = [
            "country",
            "current_location",
            "home_address",
            "occupation",
            "id_card",
            "terms_and_conditions"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['terms_and_conditions'].required = True


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
          "company_name",
          "location",
          "state",
          "industry",
          "company_size",
          "services",
          "work_history_with_freelancer",
          "terms_and_conditions",
     ]
    
    
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = [
            "rating",
            "skilla",
            "client"
        ]
    
    
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = [
            "skilla",
            "skill_category",
            "skill",
            "skill_level",
            "base_price"
        ]
    
    

class AboutSkillaForm(forms.ModelForm):
    class Meta:
        model = AboutSkilla
        fields = ["about", "work_experience"]



class TrainingAndCertificationForm(forms.ModelForm):
    class Meta:
        model = TrainingAndCertification
        fields = [
            "cert_earned",
            "skill_learned",
            "grade",
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cert_earned'].required = True
        self.fields['skill_learned'].required = True
        self.fields['grade'].required = True
        
        

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = ProfilePicture
        fields = [
            "image"
        ]



class BriefForm(forms.ModelForm):
    class Meta:
        model = Brief
        fields = [
            "title",
            "description",
            "attach_files",
            "categories",
            "budget",
            "budget_flexible",
            "date"
        ]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full mt-10 rounded-md'}),
            "description": forms.Textarea(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),
            "attach_files": forms.ClearableFileInput(attrs={'class': 'text-veryDarkGreen font-bold text-base bg-veryLightGreen rounded-md'}),
            "categories": forms.Select(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),
            "budget": forms.NumberInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),
            "budget_flexible": forms.CheckboxInput(attrs={'class': 'border border-gray-700 mr-2 rounded-md'}),
            "date": forms.SelectDateWidget(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'})
        }


class BriefAppForm(forms.Form):
    client = forms.CharField(max_length=100)
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 20}))
    categories = forms.CharField(max_length=100)
    budget = forms.IntegerField()
    # skilla = forms.CharField(max_length=100)


class ChatMessageForm(forms.Form):
    msg_body = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 2, 'cols': 80, "class": "border border-gray-400 p-2 mx-3 rounded-md",
        "placeholder": "Enter your messsage here"
    }))