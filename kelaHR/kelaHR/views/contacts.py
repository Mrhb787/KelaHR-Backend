"""
User Authentication 
"""

import json
from typing import Optional
from rest_framework import generics
from rest_framework.response import Response
from django import http
from django.http import HttpResponseBadRequest
from ..serializers.contacts import LinkedinUserSerializer, LinkedinAddUserSerializer
from ..service.google_sheets_data import GoogleWorksheetDB, TransformDataStructure
from ..service.utils import linkedin_id_from_linkedin_url, find_item_with_key_in_list

keladb: GoogleWorksheetDB = GoogleWorksheetDB()


class LinkedinRetrieveDataAPI(generics.RetrieveAPIView):
    serializer_class = LinkedinUserSerializer
    queryset = keladb.worksheet_data_list

    def get_object(self):
        linkedin_url = self.request.query_params.get("linkedin_url")
        if linkedin_url is None:
            raise ValueError()
        linkedin_id = linkedin_id_from_linkedin_url(linkedin_url)
        item = find_item_with_key_in_list(self.queryset, "linkedin_id", linkedin_id)
        return item

    def retrieve(self, request, *args, **kwargs):
        keladb.refresh_instance()
        self.queryset = keladb.worksheet_data_list
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception:  # pylint: disable=broad-except
            return Response(
                data={"error": "linkedin_url not found!"},
                status=HttpResponseBadRequest.status_code,
            )


class LinkedinAddDataAPI(generics.CreateAPIView):
    serializer_class = LinkedinAddUserSerializer
    queryset = keladb.worksheet_data_list

    def post(self, request, *args, **kwargs):
        body = json.loads(self.request.body.decode(encoding="utf-8"))
        data = TransformDataStructure(
            id=-1,
            linkedin_id=linkedin_id_from_linkedin_url(body["linkedin_url"]),
            email=body["email"],
            phoneno=body["phoneno"],
        )
        keladb.refresh_instance()
        self.queryset = keladb.worksheet_data_list
        response = keladb.add_data(data)
        if response:
            keladb.refresh_instance()
            return Response(data=data)
        item = item = find_item_with_key_in_list(
            self.queryset,
            "linkedin_id",
            linkedin_id_from_linkedin_url(body["linkedin_url"]),
        )
        data["id"] = item["id"]
        response = keladb.update_data(data)
        if response:
            keladb.refresh_instance()
            return Response(data=data)
        return Response(
            data={"error": "Failed to add the value"},
            status=http.HttpResponseBadRequest.status_code,
        )
