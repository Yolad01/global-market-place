
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
    
    path("skilla_profile", views.skilla_profile, name="skilla_profile"),
    
    path("client_dashboard/", views.client, name="client"),
    path("skillas_dashboard/", views.Skillas, name="skillas"),
]
