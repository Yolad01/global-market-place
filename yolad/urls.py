
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views








urlpatterns = [
    # path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path("", include("main.urls")),
    # path("", include("pwa.urls")),

]
