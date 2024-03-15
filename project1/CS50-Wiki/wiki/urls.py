
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("encyclopedia.urls")),
]

handler404 = "encyclopedia.views.handler_404"
