from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import (Payment, User, UserReview, JobCategory, Job,
                         SkillaProfile, Skill, ClientProfile,
                         CompanyProfile, AboutSkilla, TrainingAndCertification,
                         ProfilePicture, Brief, Order, Compliance
                         )
from django.core.exceptions import ValidationError



class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email")

class SetPasswordForm(forms.Form):
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm new password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

class RegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username","first_name", "last_name", "email", "phone_no", "role")


        widgets = {
            "username": forms.Select(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),
            "first_name": forms.TextInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),
            "last_name": forms.TextInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),
            "email": forms.EmailInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),
            "phone_no": forms.TextInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),
            "role": forms.Select(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),
            "password1": forms.PasswordInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),
            "password2": forms.PasswordInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["phone_no"].required = True

    # def clean_email(self):
    #     email_input = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email_input).exists():
    #         raise forms.ValidationError("email already exists!")

    #     return email_input
        
        

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
            "portfolio",
            "passport_photo",
            "professional_profiles_links",
            # new fields
            "house_address",
            "street_name",
            "region",
            "city",
            "Postal_code",

        )

        widgets = {
            "country": forms.Select(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),
            "state": forms.TextInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md', "placeholder": "State"}),
            "current_location": forms.TextInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md', "placeholder": "Current location"}),
            "experience": forms.NumberInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md', "placeholder": "Years of experience"}),
            "portfolio": forms.TextInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md', "placeholder": "Link to your works"}),
            "identification": forms.ClearableFileInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md bg-veryDarkGreen text-white'}),
            "professional_profiles_links": forms.TextInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md', "placeholder": "Professional Profile links"}),
            "terms_and_conditions": forms.CheckboxInput(attrs={'class': 'border border-gray-700 p-2 mb-4 mr-2 rounded-md',}),
            "hourly_rate": forms.NumberInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),

            "house_address": forms.TextInput(attrs={'class': 'mt-3 shadow appearance-none border border-shadeAsh_6 hover:border-veryDarkGreen rounded-md w-5/6  py-3 lg:px-3 text-darkBlue_2 leading-tight focus:outline-none focus:shadow-outline', "placeholder": "House no"}),
            "street_name": forms.TextInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md', "placeholder": "Current location"}),
            "region": forms.TextInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md', "placeholder": "Current location"}),
            "city": forms.TextInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md', "placeholder": "Current location"}),
            "Postal_code": forms.TextInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md', "placeholder": "Current location"}),

        }
    
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


        widgets = {
            "country": forms.Select(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md text-light_ash text-xl'}),
            "current_location": forms.TextInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),
            "home_address": forms.TextInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),
            "occupation": forms.TextInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),
            "id_card": forms.ClearableFileInput(attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}),
            "terms_and_conditions": forms.CheckboxInput(attrs={'class': 'border border-gray-700 mr-2 rounded-md'}),
        }

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
    
    
class UserReviewForm(forms.ModelForm):
    class Meta:
        model = UserReview
        fields = [
            "rating",
            "comment"
        ]

        widgets = {
                "rating": forms.Select(attrs={'class': 'rounded-md bg-gray-300 w-40'}),
                "comment": forms.TextInput(attrs={'class': 'rounded-md bg-gray-300 w-40'}),
                
            }
    
    
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = [
            # "skilla",
            "title",
            "description",
            "category",
            "skill",
            "image",
            "level",
            "base_price"
        ]
        
        widgets = {
            "title": forms.TextInput(attrs={'class': 'border border-veryDarkGreen my-2 mx-5 rounded-md w-3/4', "placeholder": "Title of your service"}),
            "description": forms.Textarea(attrs={'class': 'border border-veryDarkGreen my-2 mx-5 rounded-md resize-none w-3/4', "placeholder": "Describe what you are offering"}),
            "category": forms.Select(attrs={'class': 'border border-gray-700 my-5 mx-5 rounded-md text-2xl w-3/4'}),
            "skill": forms.Select(attrs={'class': 'border border-gray-700 my-5 mx-5 rounded-md text-2xl'}),
            "image": forms.ClearableFileInput(attrs={'class': 'border border-gray-700 my-2 mx-5 rounded-md w-1/2', "required": "required"}),
            "level": forms.Select(attrs={'class': 'border border-gray-700 my-5 mx-5 rounded-md text-2xl'}),
            "base_price": forms.NumberInput(attrs={'class': 'border border-gray-700 my-2 mx-5  rounded-md'}),
        }
    
    

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
            "title": forms.TextInput(attrs={'class': 'border border-gray-700 p-2 mb-4 xl:w-full w-3/4 mt-10 rounded-md'}),
            "description": forms.Textarea(attrs={'class': 'border border-gray-700 p-2 mb-4 xl:w-full w-3/4 rounded-md'}),
            "attach_files": forms.ClearableFileInput(attrs={'class': 'text-veryDarkGreen font-bold text-base bg-veryLightGreen rounded-md w-3/4'}),
            "categories": forms.Select(attrs={'class': 'border border-gray-700 p-2 mb-4 xl:w-full w-3/4 rounded-md'}),
            "budget": forms.NumberInput(attrs={'class': 'border border-gray-700 p-2 mb-4 xl:w-full w-3/4 rounded-md'}),
            "budget_flexible": forms.CheckboxInput(attrs={'class': 'border border-gray-700 mr-2 rounded-md'}),
            "date": forms.SelectDateWidget(attrs={'class': 'border border-gray-700 p-2 mb-4 xl:w-full w-3/4 rounded-md'})
        }


class BriefAppForm(forms.Form):
    client = forms.CharField(max_length=100)
    title = forms.CharField(max_length=100)
    # description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 20}))
    categories = forms.CharField(max_length=100)
    budget = forms.IntegerField()
    # skilla = forms.CharField(max_length=100)


class ChatMessageForm(forms.Form):
    msg_body = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4, 'cols': 80, "class": "border border-veryDarkGreen p-2 mx-3 w-3/4 xl:w-full rounded-md resize-none",
        "placeholder": "Enter your messsage here"
    }))


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "gig_desc",
            "delivery",
            "price"
        ]
        widgets = {
            "gig_desc": forms.Textarea(attrs={
                "class": 'border border-green-700 p-2 mb-4 w-full rounded-md',
                "rows":4,
                "cols":10,
                "placeholder": "Describe the service you need."
            }),
            "delivery": forms.NumberInput(attrs={
                'class': 'border border-green-700 p-2 mb-4 rounded-md',
                "placeholder": "Days till delivery"
            }),
            "price": forms.NumberInput(attrs={
                'class': 'border border-green-700 p-2 mb-4 rounded-md',
                "placeholder": "Price"
            }),

        }



class AcceptQuoteForm(forms.Form):
    accept = forms.BooleanField(initial=True)
    form_id = forms.IntegerField()


class DeclineQuoteForm(forms.Form):
    decline = forms.BooleanField(initial=True)
    form_id = forms.IntegerField()



class DeleteBriefForm(forms.Form):
    delete_brief = forms.IntegerField()



class EditBriefForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'border border-gray-700 p-2 mb-4 w-full mt-10 rounded-md'}
        )
    )
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 20, 'class': 'border border-gray-700 p-2 mb-4 w-full mt-10 rounded-md'}))
    attach_files = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'class': 'text-veryDarkGreen font-bold text-base bg-veryLightGreen rounded-md'}
        )
    )
    categories = forms.ModelChoiceField(
        queryset=JobCategory.objects.all(),
        widget=forms.Select(
            attrs={'class': 'border border-gray-700 p-2 mb-4 xl:w-full w-3/4 rounded-md'}
        )
    )
    budget = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'border border-gray-700 p-2 mb-4 w-full rounded-md'}
        )
    )
    budget_flexible = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'border border-gray-700 mr-2 rounded-md'}
        )
    )
    date = forms.DateTimeField(
        widget=forms.SelectDateWidget(
            attrs={'class': 'border border-gray-700 p-2 mb-4 xl:w-full w-3/4 rounded-md'}
        )
    )
    

class SearchForm(forms.Form):
    search_input = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'border border-gray-700 w-full ml-20 pr-5 rounded-md',
                   "placeholder": "Search"
            }
        )
    )


class PaymentForm(forms.Form):
    
    amount = forms.IntegerField(
        min_value=2,
        max_value=100000,
        widget=forms.NumberInput(
             attrs={
                 "class": "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-veryLightGreen sm:text-sm sm:leading-6",
                 "placeholder": "Amount"
             }
        )
       
    )


class ComplianceForm(forms.ModelForm):
    class Meta:
        model = Compliance
        fields = ["complied"]
