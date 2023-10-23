from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from main.forms import (RegistrationForm, JobForm, SkillaProfileForm,
                        ClientProfileForm, CompanyProfileForm, AboutSkillaForm,
                        TrainingAndCertificationForm, ProfilePictureForm
                        )
from main.models import ( AboutSkilla, TrainingAndCertification, User, Skillas, Clients, JobCategory, Job, SkillaProfile,
                         ClientProfile, CompanyProfile, ProfilePicture
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
                return redirect("main:client_profile")
            elif user.role == "SKILLAS":
                SkillaProfile.objects.create(user_id=request.user.id)
                return redirect("main:skilla_profile")
            elif user.role == "COMPANY":
                return redirect("main:company_profile")
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
    if request.method == "POST":
        form = SkillaProfileForm(request.POST, instance=skilla_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "profile updated successfully")
            profile = SkillaProfile.objects.get(user=request.user)
            profile.activate_user()
            profile.save()
            return redirect("main:skillas_dashboard")
    
    form = SkillaProfileForm()
    
    return render(
        request=request,
        template_name="main/skilla/skilla_profile.html",
        context={"form": form}
    )
        
        
    
def client_profile(request):
    try:
        client_profile = request.user.clientprofile
    except ClientProfile.DoesNotExist:
        client_profile = ClientProfile(user=request.user)
    if request.method == "POST":
        form = ClientProfileForm(request.POST, instance=client_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated Successfully")
            profile = SkillaProfile.objects.get(user=request.user)
            profile.activate_user()
            profile.save()
            return redirect("main:profile_dashboard")
        
    form = ClientProfileForm()
    
    return render(
        request=request,
        template_name="main/client/client_profile.html",
        context={"form": form}
    )
    
    
def company_profile(request):
    try:
        company_profile = request.user.companyprofile
    except CompanyProfile.DoesNotExist:
        company_profile = CompanyProfile(user=request.user)
    
    if request.method == "POST":
        form = CompanyProfileForm(request.POST, instance=company_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "profile saved successfully")
            profile = CompanyProfile.objects.get(user=request.user)
            profile.activate_user()
            profile.save()
            return redirect("main:company_dashboard")
    form = CompanyProfileForm()
    
    return render(
        request=request,
        template_name="main/company/company_profile.html",
        context={
            "form": form
        }
    )
    
    

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
                    return redirect("main:client_dashboard")
                elif user.role == "SKILLAS":
                    return redirect("main:skillas_dashboard")
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
    return render(request=request, template_name="main/skilla/skillas_dashboard.html")


#### add @login_required decorator
def company(request):
    return render(
        request=request,
        template_name="main/company/company_dashboard.html"
    )
    



def log_out(request):
    logout(request)
    return redirect("main:home")



def s_profile(request):
    try:
        about_skilla = AboutSkilla.objects.get(user=request.user)
        skilla_pp = ProfilePicture.objects.get(user=request.user)
    except (AboutSkilla.DoesNotExist, ProfilePicture.DoesNotExist):
        about_skilla = AboutSkilla(user=request.user)
        skilla_pp = ProfilePicture(user=request.user)

    if request.method == "POST":
        about_form = AboutSkillaForm(request.POST, instance=about_skilla)
        cert_form =TrainingAndCertificationForm(request.POST)
        skilla_pp_form = ProfilePictureForm(request.POST, request.FILES,  instance=skilla_pp)
        
        if about_form.is_valid():
            about_form.save()

        if skilla_pp_form.is_valid():
            skilla_pp_form.save()

        
        if cert_form.is_valid():
            cert_instance = cert_form.save(commit=False)
            cert_instance.user = request.user
            cert_instance.save()

            return redirect("main:s_profile")
    

    about_form = AboutSkillaForm()
    cert_form = TrainingAndCertificationForm()
    skilla_pp = ProfilePictureForm()

    return render(
        request=request,
        template_name="main/skilla/s_profile.html",
        context={
            "profile": SkillaProfile.objects.all().filter(user=request.user),
            "about_skilla": AboutSkilla.objects.all().filter(user=request.user),
            "train_and_cert": TrainingAndCertification.objects.all().filter(user=request.user),
            "about_form": about_form,
            "cert_form": cert_form,
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
            "profile_pic_form": skilla_pp
        }
    )



def wallet(request):
    return render(
        request=request,
        template_name="main/skilla/wallet/wallet.html",
    )



def fund_withdrawal(request):
    return render(
        request=request,
        template_name="main/skilla/wallet/fund_withdrawal.html"
    )



def continue_to_withdrawal(request):
    return render(
        request=request,
        template_name="main/skilla/wallet/continue_to_withdrawal.html"
    )


def withdraw_success(request):
    return render(
        request=request,
        template_name="main/skilla/wallet/success_page.html"
    )