from rest_framework import generics

from src.audio_lib import models, serializer


class GenreView(generics.ListAPIView):
    """ List of genre
    """
    queryset = models.Genre.objects.all()
    serializer_class = serializer.GenreSerializer