
from django.contrib import admin
from django.urls import path, include, re_path






urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path("", include("main.urls")),
    re_path('^', include('django.contrib.auth.urls')),
]
