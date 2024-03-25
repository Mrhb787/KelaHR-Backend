"""
Auth Serializer
"""

from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    """
    User Serializer
    """

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(max_length=100)
    phoneno = serializers.CharField(max_length=20)
