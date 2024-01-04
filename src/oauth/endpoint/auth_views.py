from django.shortcuts import render


def google_login(request):
    """ Login with google
    """
    return render(request, 'google_login.html')