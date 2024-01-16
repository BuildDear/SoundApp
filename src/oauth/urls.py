from django.urls import path

from .endpoint import auth_views, views

urlpatterns = [
    path('', auth_views.google_login, name='google-login'),
    path('google/', auth_views.google_auth),

    # path('users/', views.RegistrationView.as_view()), # Custom registration
    # path('users/login/', views.LoginAPIView.as_view()), # Custom login

    path('me/', views.UserView.as_view(
        {
            'get': 'retrieve', 'put': 'update'
        })),

    path('social/', views.SocialLinkView.as_view(
        {
            'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'
        })),
    path('social/<int:pk>', views.SocialLinkView.as_view(
        {
            'put': 'update', 'delete': 'destroy'
        })),

    path('author/', views.AuthorView.as_view({'get': 'list'})),
    path('author/<int:pk>', views.AuthorView.as_view({'get': 'retrieve'})),
]