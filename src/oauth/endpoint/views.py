from rest_framework import viewsets, parsers, permissions

from src.base.permissions import IsAuthor
from src.oauth import serializer, models


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


class AuthorView(viewsets.ReadOnlyModelViewSet):
    """ View and edit author data
    """
    queryset = models.AuthUser.objects.all()
    serializer_class = serializer.AuthorSerializer


class SocialLinkView(viewsets.ModelViewSet):
    """ CRUD Social Link
    """
    serializer_class = serializer.SocialLinkSerializer
    permission_classes = [IsAuthor]
