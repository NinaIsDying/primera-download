from django.urls import include, path

from . import views


urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path("", views.home, name="home"),
    path("download/", views.download_apk, name="download_apk"),
    path("qr/", views.download_qr, name="download_qr"),
]