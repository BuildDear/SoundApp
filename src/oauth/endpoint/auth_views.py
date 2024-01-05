from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed

from src.oauth import serializer


def google_login(request):
    """ Login with google
    """
    return render(request, 'google_login.html')


@api_view(["POST"])
def google_auth(request):
    google_data = serializer.GoogleAuth(data=request.data)
    if google_data.is_valid():
        pass
    else:
        return AuthenticationFailed(code=403, detail='Dad data google')
