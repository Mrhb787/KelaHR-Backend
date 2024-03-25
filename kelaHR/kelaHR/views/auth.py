"""
User Authentication 
"""

from rest_framework import generics
from ..serializers.auth import UserSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        sample_data = {
            "id": 1,
            "email": "testemail@gmail.com",
            "password": "test@1234",
            "username": "test",
            "phoneno": "7890643521",
        }

        return [sample_data]
