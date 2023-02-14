from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class HelloView(APIView):
    """Test API View"""

    def get(self, request):
        """Return a list of APIView features"""
        return Response(
            data = {'message': "Hello World!"}
        )

