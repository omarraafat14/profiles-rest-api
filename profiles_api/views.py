from django.shortcuts import render

from rest_framework  import viewsets
from rest_framework import status
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import HelloSerializer, UserProfileSerializer, ProfileFeedItemSerializer
from .models import UserProfile, ProfileFeedItem
from .permissions import UpdateOwnProfile, UpdateOwnStatus

# Create your views here.
class HelloAPIView(APIView):
    """Test API View"""
    serializer_class = HelloSerializer

    def get(self, request):
        """Return a list of APIView features"""
        return Response(
            data = {'message': "Hello World!"}
        )

    def post(self, request):
        """create a hello message"""
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data['name']
            message = f'Hello, {name}'
            return Response({"message":message})
        
        return Response(
            serializer.errors, 
            status = status.HTTP_400_BAD_REQUEST
        )
    
    def put(self,request,pk=None):
        """Handle updating an object"""
        return Response({"message":"PUT"})

    def patch(self,request,pk=None):
        """Handle a partial updating an object"""
        return Response({"message":"PATCH"})

    def delete(self,request,pk=None):
        """Delete an object"""
        return Response({"message":"Delete"})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    serializer_class = HelloSerializer

    def list(self,request):
        """Return a list of ViewSet features"""
        
        a_viewset = [
            'Uses actions instead of HTTP Methods',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response({
            "message":"List",
            'a_viewset': a_viewset,
        })

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            message = f'Hello, {name}'
            return Response({'message': message})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk = None):
        """Handle getting an object by its ID"""
        return Response(
            {
                "message": 'GET'
            }
        )

    def update(self, request, pk = None):
        """Handle updating an object"""
        return Response(
            {
                "message": 'PUT'
            }
        )

    def partial_update(self,request,pk = None):
        """Handle updating part of an object"""
        return Response(
            {
                "message": 'PATCH'
            }
        )

    def destroy(self,request,pk = None):
        """Handle removing an object"""
        return Response(
            {
                "message": 'DELETE'
            }
        )


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [UpdateOwnProfile]
    authentication_classes = [TokenAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']

    def create(self,request):
        """Create and return a new user"""
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            user = UserProfile.objects.create_user(
                email = serializer.validated_data['email'],
                name = serializer.validated_data['name'],
                password = serializer.validated_data['password']
            )
            return Response(
                data = serializer.data,
                status=status.HTTP_201_CREATED
            )


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = ProfileFeedItemSerializer
    queryset = ProfileFeedItem.objects.all()
    permission_classes = (
        UpdateOwnStatus,
        IsAuthenticatedOrReadOnly
    )

    #override the behaviour for creating objects through ModelViewSet 
    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile = self.request.user)