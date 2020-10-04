from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from wall_api.models import User, Post
from wall_api.serializers import UserSerializer, PostSerializer


class UserView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        """
        Custom post function to use a message response insted of
        returning the user data.
        """
        self.create(request, *args, **kwargs)
        return Response({"msg": "User registered succesfully!"}, status=status.HTTP_201_CREATED)


class TokenAuthView(ObtainAuthToken):
    """
    Custom view for getting the user's token with a custom response
    that contains the username and the token.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get(user=user)
        return Response({
            'username': user.username,
            'token': token.key
        })


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Uses the authenticated user data to fill
        the posted_by field.
        """
        serializer.save(posted_by=self.request.user)
