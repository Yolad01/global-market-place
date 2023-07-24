from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import User



class RegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username","first_name", "last_name", "email", "phone_no", "role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["phone_no"].required = True