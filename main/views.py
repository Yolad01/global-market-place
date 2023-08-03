from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from main.forms import RegistrationForm
from main.models import ( User, Skillas, Clients, JobCategory, Job, Material
)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


# Create your views here.



def home(request):
    return render(request=request, template_name="main/home.html")



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
                return redirect("main:client")
            elif user.role == "Skillas":
                return redirect("main:skillas")
    else:
        registration_form = RegistrationForm()
    return render(request=request, template_name="main/register.html",context={"form": registration_form})



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



