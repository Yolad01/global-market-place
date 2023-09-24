
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings






app_name = "main"


urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),    
    path("sign_in/", views.sign_in, name="sign_in"),
    
    path("skilla_profile/", views.skilla_profile, name="skilla_profile"),
    path("client_profile/", views.client_profile, name="client_profile"),
    path("company_profile/", views.company_profile, name="company_profile"),
    
    path("client_dashboard/", views.client, name="client_dashboard"),
    path("skillas_dashboard/", views.skilla, name="skillas_dashboard"),
    path("company_dashboard/", views.company, name="company_dashboard")
]
