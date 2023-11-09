from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from main.forms import (RegistrationForm, JobForm, SkillaProfileForm,
                        ClientProfileForm, CompanyProfileForm, AboutSkillaForm,
                        TrainingAndCertificationForm, ProfilePictureForm, BriefForm,
                        BriefAppForm
                        )
from main.models import ( AboutSkilla, Skillas, TrainingAndCertification, JobCategory, Job, SkillaProfile,
                         ClientProfile, CompanyProfile, ProfilePicture, Brief,
                         SkillaReachoutToClient, Clients
                        )
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
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
                messages.success(request, f"Logged in as {username}")
                return redirect("main:client_profile")
            elif user.role == "SKILLAS":
                SkillaProfile.objects.create(user_id=request.user.id)
                messages.success(request, f"Logged in as {username}")
                return redirect("main:skilla_profile")
            elif user.role == "COMPANY":
                messages.success(request, f"Logged in as {username}")
                return redirect("main:company_profile")
        else:
            messages.error(request, "Passwords isn't complex enough.")
            return redirect("main:register")
            
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
        context={
            "form": form,
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user)
        }
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
        context={
            "form": form,
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
        }
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
            "form": form,
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user)
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
                    messages.success(request, f"Logged in as {username}") 
                    return redirect("main:client_dashboard")
                elif user.role == "SKILLAS":
                    messages.success(request, f"Logged in as {username}")
                    return redirect("main:skillas_dashboard")
        else:
            messages.error(request, "Wrong login credentials. Please enter a correct credential to access your dashboard")
            return redirect("main:sign_in")

            
    return render(request=request, template_name="main/sign_in.html",
                    context={"form": form})


@login_required
def client_dashboard(request):
    job_categories = JobCategory.objects.all()
    jobs = Job.objects.all()
    profile = ClientProfile.objects.all().filter(user=request.user)

    try:
        client_pp = ProfilePicture.objects.get(user=request.user)
    except ProfilePicture.DoesNotExist:
        client_pp = ProfilePicture(user=request.user)

    if request.method == "POST":
        client_pp_form = ProfilePictureForm(request.POST, request.FILES, instance=client_pp)

        if client_pp_form.is_valid():
            client_pp_form.save()
            return redirect("main:client_dashboard")
        
    client_pp_form = ProfilePictureForm()
    
    return render(
            request=request, template_name="main/client/client_dashboard.html",
            context={
                "job_categories": job_categories,
                "jobs": jobs,
                "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
                "profile": profile,
                "profile_pic_form": client_pp_form,
                "client_profile_info": ClientProfile.objects.all().filter(user=request.user)
            }
        )



def applications(request):
    skilla_client = SkillaReachoutToClient.objects.all().filter(client=request.user)
    return render(
        request=request,
        template_name="main/client/application.html",
        context={
            "skilla_client": skilla_client
        }
    )
    

#### add @login_required decorator
def skilla(request):
    brief = Brief.objects.all().order_by("-title")
    if request.method == "POST":
        form = BriefAppForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data["client"]
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            categories = form.cleaned_data["categories"]
            budget = form.cleaned_data["budget"]
            client = form.cleaned_data["client"]

            get_categories = JobCategory.objects.get(title=categories)
            get_client = Clients.objects.get(username=client)

            print(client)

            user = request.user

            reachout = SkillaReachoutToClient(
                user=user,
                title=title,
                description=description,
                categories=get_categories,
                budget=budget,
                client=get_client
            )
            reachout.save()
        return redirect("main:skillas_dashboard")

    form = BriefAppForm()
    return render(
        request=request, template_name="main/skilla/skillas_dashboard.html",
        context={
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user),
            "brief": brief,
            "form": form
        }
    )


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
        skilla_pp_form = ProfilePictureForm(request.POST, request.FILES, instance=skilla_pp)
        
        if about_form.is_valid():
            about_form.save()
            messages.success(request, "Updated successfully")
            return redirect("main:s_profile")

        if skilla_pp_form.is_valid():
            skilla_pp_form.save() ## skilla__pp == skilla profile picture
            messages.success(request, "Profile Picture updated successfully")
            return redirect("main:s_profile")

        if cert_form.is_valid():
            cert_instance = cert_form.save(commit=False)
            cert_instance.user = request.user
            cert_instance.save()
            messages.success(request, "Info saved successfully")
            return redirect("main:s_profile")
    

    about_form = AboutSkillaForm()
    cert_form = TrainingAndCertificationForm()
    skilla_pp_form = ProfilePictureForm()

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
            "profile_pic_form": skilla_pp_form
        }
    )



def wallet(request):
    return render(
        request=request,
        template_name="main/skilla/wallet/wallet.html",
        context={
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user)
        }
    )



def fund_withdrawal(request):
    return render(
        request=request,
        template_name="main/skilla/wallet/fund_withdrawal.html",
        context={
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user)
        }
    )



def continue_to_withdrawal(request):
    return render(
        request=request,
        template_name="main/skilla/wallet/continue_to_withdrawal.html",
        context={
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user)
        }
    )


def withdraw_success(request):
    return render(
        request=request,
        template_name="main/skilla/wallet/success_page.html",
        context={
            "profile_pic": ProfilePicture.objects.all().filter(user=request.user)
        }
    )
    
    
def client_brief(request):
    if request.method =="POST":
        form = BriefForm(request.POST, request.FILES)
        if form.is_valid():
            brief_form = form.save(commit=False)
            brief_form.user = request.user
            brief_form.save()
            ##### messages
            return redirect("main:client_dashboard")
            
    form = BriefForm()
    return render(
        request=request,
        template_name="main/client/brief/create_brief.html",
        context={
            "form": form
            
        }
    )
    