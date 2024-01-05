from django.urls import path

from .endpoint import auth_views


urlpatterns = [
    path('', auth_views.google_login),
    path('google/', auth_views.google_auth),
]