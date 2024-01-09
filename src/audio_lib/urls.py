from django.urls import path

from src.audio_lib import views

urlpatterns = [

    path('genre/', views.GenreView.as_view()),

    path('license/', views.LicenseView.as_view({'get': 'list', 'post': 'create'})),
    path('license/<int:pk>', views.LicenseView.as_view({'put': 'update', 'delete': 'destroy'})),

]