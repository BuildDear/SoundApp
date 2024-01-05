from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from src.oauth import serializer
from src.oauth.services.google import check_google_auth


def google_login(request):
    """ Login with google
    """
    return render(request, 'google_login.html')


@api_view(["POST"])
def google_auth(request):
    google_data = serializer.GoogleAuth(data=request.data)
    if google_data.is_valid():
        token = check_google_auth(google_data.data)
        return Response(token)
    else:
        return AuthenticationFailed(code=403, detail='Dad data google')
