
from django.urls import path, re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.db.models.query import QuerySet





app_name = "main"


urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),    
    path("sign_in/", views.sign_in, name="sign_in"),
    path("login/", views.login, name="login"),
    path("about/", views.about, name="about"),
    path("terms_condition/", views.terms_condition, name="terms_condition"),
    path("service_policy/", views.service_policy, name="service_policy"),
    path("s_identity/", views.s_identity, name="s_identity"),
    path("identity_details/", views.identity_details, name="identity_details"),
    path("review/", views.review, name="review"),
    path("compliance/", views.compliance, name="compliance"),
    path("guide_one/", views.guide_one, name="guide_one"),
    path("guide_two/", views.guide_two, name="guide_two"),
    path("guide_three/", views.guide_three, name="guide_three"),
    path("guide_four/", views.guide_four, name="guide_four"),
    path("guide_five/", views.guide_five, name="guide_five"),
    path("frequently_asked_questions/", views.frequently_asked_questions, name="frequently_asked_questions"),
    
    path("skilla_profile/", views.skilla_profile, name="skilla_profile"),
    path("client_profile/", views.client_profile, name="client_profile"),
    path("company_profile/", views.company_profile, name="company_profile"),
    
    path("client_dashboard/", views.client_dashboard, name="client_dashboard"),
    path("create_brief/", views.create_brief, name="create_brief"),
    path("applications/", views.applications, name="applications"),

    path("view_skilla_profile/<int:pk>/", views.profile_view, name="profile_view"),

    path("skillas_dashboard/", views.skilla, name="skillas_dashboard"),
    
    path("s_profile/", views.s_profile, name="s_profile"),
    path("wallet/", views.wallet, name="wallet"),
    path("fund_withdrawal/", views.fund_withdrawal, name="fund_withdrawal"),
    path("continue_to_withdrawal/", views.continue_to_withdrawal, name="continue_to_withdrawal"),
    path("success_page/", views.payment_success, name="payment_success"),

    path("company_dashboard/", views.company, name="company_dashboard"),

    path("chat/<str:username>/", views.thread_view, name="chat"),
    
    path("inbox/", views.inbox, name="inbox"),

    path("quotes/", views.quotes, name="quotes"),
    
    path("orders/", views.orders , name="orders"),

    path("create_gigs/", views.create_gigs , name="create_gigs"),
    path("skillas_gigs/", views.skillas_gigs , name="skillas_gigs"),

    path("skillas_gigs_details/<int:id>", views.skillas_gigs_details , name="skillas_gigs_details"),
    path("view_skills/", views.view_skills , name="view_skills"),

    path("view_brief/", views.view_brief , name="view_brief"),
    path("edit_brief/<int:id>", views.edit_brief , name="edit_brief"),

    path("search_results/<str:param>/", views.search_results , name="search_results"),

    path("skilla_search/<str:param>/", views.skilla_search , name="skilla_search"),
    
    # path("skill_detail/", views.skill_detail , name="skill_detail"),

    path("logout/", views.log_out, name="logout"),

    path("password_reset/", views.password_reset_request, name="password_reset_request"),
    path("password_reset/done/", views.password_reset_done, name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.password_reset_confirm, name="password_reset_confirm"),
    path("reset/done/", views.password_reset_complete, name="password_reset_complete"),
    
    path("make-payment/<int:order_no>/<int:price>/", views.make_payment, name="make_payment"),
    path("paid-order-history/", views.paid_order_history, name="paid_order_history"),

    path("rate-user/", views.rate_user, name="rate_user"),

    path("manage-gigs/", views.manage_gigs, name="manage_gigs"),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)