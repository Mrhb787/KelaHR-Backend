"""
User Authentication 
"""

import json
from rest_framework import generics
from rest_framework.response import Response
from django import http
from ..serializers.contacts import LinkedinUserSerializer, LinkedinAddUserSerializer
from ..service.google_sheets_data import GoogleWorksheetDB, TransformDataStructure


keladb: GoogleWorksheetDB = GoogleWorksheetDB()


class LinkedinRetrieveDataAPI(generics.RetrieveAPIView):
    serializer_class = LinkedinUserSerializer
    queryset = keladb.worksheet_data_list

    def get_object(self):
        linkedin_url = self.request.query_params.get("linkedin_url")
        linkedin_id = linkedin_url.split("/")[-2]
        item = next(
            (item for item in self.queryset if item["linkedin_id"] == linkedin_id), None
        )
        if item is None:
            raise http.Http404
        return item

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class LinkedinAddDataAPI(generics.CreateAPIView):
    serializer_class = LinkedinAddUserSerializer
    queryset = keladb.worksheet_data_list

    def post(self, request, *args, **kwargs):
        body = json.loads(self.request.body.decode(encoding="utf-8"))
        data = TransformDataStructure(
            id=-1,
            linkedin_id=body["linkedin_url"].split("/")[-2],
            email=body["email"],
            phoneno=body["phoneno"],
        )
        response = keladb.add_data(data)
        if response:
            return Response(
                data={"message": "Contact Added Successfully!"},
            )
        return Response(
            data={"error": "Failed to add the value"},
            status=http.HttpResponseBadRequest.status_code,
        )
