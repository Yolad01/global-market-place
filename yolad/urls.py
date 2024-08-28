
from django.contrib import admin
from django.urls import path, include

from main.api import api








urlpatterns = [
    # path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path("", include("main.urls")),
    path("api/", api.urls)
    # path("", include("pwa.urls")),

]
