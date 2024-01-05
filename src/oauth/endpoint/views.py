from rest_framework import viewsets, parsers, permissions

from src.oauth import serializer


class UserView(viewsets.ModelViewSet):
    """ View and edit user data
    """
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializer.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()