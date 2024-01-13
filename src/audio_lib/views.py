from rest_framework import generics, viewsets, parsers
from rest_framework.permissions import AllowAny

from src.audio_lib import models, serializer
from src.base.permissions import IsAuthor
from src.base.services import delete_old_file


class GenreView(generics.ListAPIView):
    """ List of genre
    """
    queryset = models.Genre.objects.all()
    serializer_class = serializer.GenreSerializer


class LicenseView(viewsets.ModelViewSet):
    """ CRUD of author`s license
    """
    serializer_class = serializer.LicenseSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.License.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AlbumView(viewsets.ModelViewSet):
    """ CRUD author`s albums
    """
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializer.AlbumSerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        return models.Album.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class PublicAlbumView(generics.ListAPIView):
    """ List of public author`s albums
    """
    serializer_class = serializer.AlbumSerializer

    def get_queryset(self):
        return models.Album.objects.filter(user__id=self.kwargs.get('pk'), private=False)