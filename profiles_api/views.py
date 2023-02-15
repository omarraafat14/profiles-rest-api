from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework  import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import HelloSerializer

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