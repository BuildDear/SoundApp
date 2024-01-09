from rest_framework import generics, viewsets

from src.audio_lib import models, serializer
from src.base.permissions import IsAuthor


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