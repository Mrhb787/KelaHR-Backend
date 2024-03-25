"""
URL configuration for kelaHR project.
"""

from django.contrib import admin
from django.urls import path
from .views import auth, contacts


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/user/",
        auth.UserListAPIView.as_view(),
        name="user_list",
    ),
    path(
        "api/contacts/add/",
        contacts.LinkedinAddDataAPI.as_view(),
        name="add_contact_details",
    ),
    path(
        "api/contacts/",
        contacts.LinkedinRetrieveDataAPI.as_view(),
        name="get_contact_details",
    ),
]
