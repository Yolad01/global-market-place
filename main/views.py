from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from main.forms import (RegistrationForm, JobForm, SkillaProfileForm,
                        ClientProfileForm
                        )
from main.models import ( User, Skillas, Clients, JobCategory, Job, Material, SkillaProfile,
                         ClientProfile
)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


# Create your views here.



def home(request):
    job_form = JobForm(request.POST)
    return render(request=request, template_name="main/home.html",
                  context={"form": job_form}
                  )


def register(request):
    if request.method == "POST":
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            username = registration_form.cleaned_data["username"]
            password = registration_form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            if user.role == "CLIENT":
                ClientProfile.objects.create(user_id=request.user.id)
                return redirect("main:client")
            elif user.role == "SKILLAS":
                SkillaProfile.objects.create(user_id=request.user.id)
                return redirect("main:skilla_profile")
            # elif user.role == "COMPANY":
            #     return redirect("main:company")
    else:
        registration_form = RegistrationForm()
    return render(request=request, template_name="main/register.html",
                  context={
                        "reg_form": registration_form,
                      })
    


def skilla_profile(request):
    try:
        skilla_profile = request.user.skillaprofile
    except SkillaProfile.DoesNotExist:
        skilla_profile = SkillaProfile(user=request.user)
    form = SkillaProfileForm(request.POST, instance=skilla_profile)
    if form.is_valid():
        form.save()
        messages.success(request, "profile updated successfully")
    form = SkillaProfileForm()
    
    return render(
        request=request,
        template_name="main/skilla/skilla_profile.html",
        context={"form": form}
    )
        
        
    
    
    
def client_profile(request):
    ...
    
    
def company_profile(request):
    ...
    
    


def sign_in(request):
    user = request.user
    if user.is_authenticated:
        return redirect("main:home")
    form = AuthenticationForm(request, data=request.POST)
    if request.method =="POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user != None:
                login(request, user)
                if user.role == "CLIENT":  
                    return redirect("main:client")
                elif user.role == "SKILLAS":
                    return redirect("main:skillas")
            else:
                messages.error(request, "Wrong login credentials. Please enter a correct credential to access your dashboard")
            
    return render(request=request, template_name="main/sign_in.html",
                    context={"form": form})


#### add @login_required decorator
def client(request):
    job_categories = JobCategory.objects.all()
    jobs = Job.objects.all()
    
    return render(
            request=request, template_name="main/client_dashboard.html",
            context={
                "job_categories": job_categories,
                "jobs": jobs
            }
        )


#### add @login_required decorator
def skilla(request):
    return render(request=request, template_name="main/skillas_dashboard.html")




def log_out(request):
    logout(request)
    return redirect("user:home")



