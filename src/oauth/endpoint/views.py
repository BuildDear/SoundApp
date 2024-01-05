from rest_framework import viewsets, parsers

class UserView(viewsets.ModelViewSet):
    """ View and edit user data
    """
    parser_classes = (parsers.MultiPartParser,)
    serializer_class =