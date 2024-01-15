import os.path

from django.http import FileResponse, Http404, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, parsers, views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

from src.audio_lib import models, serializer
from src.audio_lib.models import Track
from src.base.classes import MixedSerializer, Pagination
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
    permission_classes = [AllowAny, ]

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


class TrackView(MixedSerializer, viewsets.ModelViewSet):
    """ CRUD tracks
    """
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_class = serializer.CreateAuthorTrackSerializer
    serializer_classes_by_action = {
        'list': serializer.AuthorTrackSerializer
    }

    def get_queryset(self):
        return models.Track.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        delete_old_file(instance.file.path)
        instance.delete()


class PlayListView(MixedSerializer, viewsets.ModelViewSet):
    """ CRUD playlists
    """
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_class = serializer.CreatePlayListSerializer
    serializer_classes_by_action = {
        'list': serializer.PlayListSerializer
    }

    def get_queryset(self):
        return models.PlayList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class TrackListView(generics.ListAPIView):
    """ List of all tracks
    """
    queryset = models.Track.objects.filter(album__private=False, private=False)
    serializer_class = serializer.AuthorTrackSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'user__display_name', 'album__name', 'genre__name']


class AuthorTrackListView(generics.ListAPIView):
    """ List of all author`s tracks
    """
    serializer_class = serializer.AuthorTrackSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'album__name', 'genre__name']

    def get_queryset(self):
        return models.Track.objects.filter(
            user__id=self.kwargs.get('pk'), album__private=False, private=False
        )


class CommentAuthorView(viewsets.ModelViewSet):
    """ CRUD author`s comments
    """
    serializer_class = serializer.CommentAuthorSerializer
    permission_classes = [IsAuthor,]

    def get_queryset(self):
        return models.Comment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentView(viewsets.ModelViewSet):
    """ Track`s comments
    """
    serializer_class = serializer.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(track_id=self.kwargs.get('pk'))


class StreamingFileView(views.APIView):
    """ Running track
    """
    def set_play(self, track: Track) -> None:
        track.plays_count += 1
        track.save()

    def get(self, request, pk):
        """ Handle GET requests for streaming a track """
        # Get the track or return a 404 response if not found
        self.track = get_object_or_404(Track, id=pk, private=False)

        # Check if the file exists on the server
        if os.path.exists(self.track.file.path):
            # Increment the play count
            self.set_play(self.track)

            # Prepare the response with appropriate headers
            response = HttpResponse('', content_type="audio/mpeg", status=206)

            # Use X-Accel-Redirect header to stream the file through Nginx
            response['X-Accel-Redirect'] = f"/mp3/{self.track.file.name}"

            return response
        else:
            # Raise a 404 exception if the file is not found
            raise Http404("File not found")


class DownloadTrackView(views.APIView):
    """ Downloading track
    """

    def set_download(self) -> None:
        self.track.download += 1
        self.track.save()

    def get(self, request, pk):
        """ Handle GET requests for downloading a track """
        # Get the track or return a 404 response if not found
        self.track = get_object_or_404(models.Track, id=pk, private=False)

        # Check if the file exists on the server
        if os.path.exists(self.track.file.path):
            # Increment the download count
            self.set_download()

            # Prepare the response with appropriate headers
            response = HttpResponse('', content_type="audio/mpeg", status=206)
            response["Content-Disposition"] = f"attachment; filename={self.track.file.name}"

            # Use X-Accel-Redirect header to serve the file through Nginx
            response['X-Accel-Redirect'] = f"/media/{self.track.file.name}"

            return response
        else:
            # Raise a 404 exception if the file is not found
            raise Http404("File not found")


class StreamingFileAuthorView(views.APIView):
    """ Running author`s track
    """
    permission_classes = [IsAuthor]

    def get(self, request, pk):
        """ Handle GET requests for streaming an author's track """
        # Get the track or return a 404 response if not found
        self.track = get_object_or_404(Track, id=pk, user=request.user)

        # Check if the file exists on the server
        if os.path.exists(self.track.file.path):
            # Prepare the response with appropriate headers
            response = HttpResponse('', content_type="audio/mpeg", status=206)

            # Use X-Accel-Redirect header to stream the file through Nginx
            response['X-Accel-Redirect'] = f"/mp3/{self.track.file.name}"

            return response
        else:
            # Raise a 404 exception if the file is not found
            raise Http404("File not found")

