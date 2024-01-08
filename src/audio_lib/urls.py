from django.urls import path

from src.audio_lib import views

urlpatterns = [

    path('genre/', views.GenreView.as_view()),

]