import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from ..models import AuthUser


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = "Token"

    def authenticate(self, request):
        """
        The 'authenticate' method is called every time, regardless of whether
        the endpoint requires authentication. It has two possible return values:
            1) None - returned if we do not want to authenticate. This usually
            means that we anticipate authentication will fail, for example,
            when the token is not included in the header.
            2) (user, token) - returned when authentication is successful.
            If neither case is met, an AuthenticationFailed exception is raised,
            allowing DRF to handle the rest.
        """
        request.user = None
        print("Hello")

        # 'auth_header' should be an array with two elements:
        # 1) the name of the authentication header (Token in our case)
        # 2) the JWT we need to authenticate against
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            # Incorrect token header, only one element is passed
            return None

        elif len(auth_header) > 2:
            # Incorrect token header, some extra whitespace
            return None

        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")

        if prefix.lower() != auth_header_prefix:
            # Incorrect header prefix - reject
            return None

        # There is a "chance" that authentication will be successful by now.
        # We delegate the actual authentication of credentials to the method below.
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        Attempt to authenticate with the provided credentials. If successful,
        return the user and token; otherwise, raise an exception.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except Exception:
            msg = "Authentication error. Unable to decode the token."
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = AuthUser.objects.get(pk=payload["id"])
        except AuthUser.DoesNotExist:
            msg = "User corresponding to this token not found."
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = "This user is deactivated."
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)
