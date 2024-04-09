
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views








urlpatterns = [
    # path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path("", include("main.urls")),

    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("reset_password_sent/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]
