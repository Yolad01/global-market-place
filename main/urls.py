
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
    
    path("client_dashboard/", views.client_dashboard, name="client_dashboard"),
    path("client_brief/", views.client_brief, name="client_brief"),
    path("client_brief_cont/", views.client_brief_cont, name="client_brief_cont"),

    path("skillas_dashboard/", views.skilla, name="skillas_dashboard"),
    
    path("s_profile/", views.s_profile, name="s_profile"),
    path("wallet/", views.wallet, name="wallet"),
    path("fund_withdrawal/", views.fund_withdrawal, name="fund_withdrawal"),
    path("continue_to_withdrawal/", views.continue_to_withdrawal, name="continue_to_withdrawal"),
    path("success_page/", views.withdraw_success, name="withdraw_success"),

    path("company_dashboard/", views.company, name="company_dashboard"),

    path("logout/", views.log_out, name="logout")
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)