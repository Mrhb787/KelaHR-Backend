"""
Contacts Serializer
"""

from rest_framework import serializers


class LinkedinUserSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Linkedin User Serializer
    """

    id = serializers.IntegerField()
    linkedin_id = serializers.CharField(
        allow_null=True,
        required=False,
    )
    email = serializers.ListField(
        allow_null=True,
        required=False,
    )
    phoneno = serializers.ListField(
        allow_null=True,
        required=False,
    )


class LinkedinAddUserSerializer(
    serializers.Serializer
):  # pylint: disable=abstract-method
    """
    Linkedin Add User Serializer
    """

    linkedin_url = serializers.URLField(
        allow_null=True,
        required=False,
    )
    email = serializers.ListField(
        allow_null=True,
        required=False,
    )
    phoneno = serializers.ListField(
        allow_null=True,
        required=False,
    )
