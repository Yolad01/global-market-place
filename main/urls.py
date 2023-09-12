
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings






app_name = "main"


urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    
    path("register_skilla/", views.register_skilla, name="register_skill"),
    path("welcome_skillas/", views.welcome_skillas, name="welcome_skillas"),
    path("skilla_qualification/", views.skilla_qualification, name="skilla_qualification"),
    path("skill_rate/", views.skill_rate, name="skill_rate"),
    
    path("sign_in/", views.sign_in, name="sign_in"),
    path("client_dashboard/", views.client, name="client"),
    path("skillas_dashboard/", views.Skillas, name="skillas"),
]
