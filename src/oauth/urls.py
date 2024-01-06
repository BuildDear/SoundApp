from django.urls import path

from .endpoint import auth_views, views

urlpatterns = [
    path('', auth_views.google_login),
    path('google/', auth_views.google_auth),

    path('me/', views.UserView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('author/', views.AuthorView.as_view({'get': 'list'})),
    path('author/<int:pk>', views.AuthorView.as_view({'get': 'retrieve'})),
]