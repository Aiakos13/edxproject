from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("allideas/", views.allideas, name="allideas"),
    path("addidea/", views.add_idea, name="addidea"),
    path("deleteidea/<int:id>/", views.delete_idea, name="deleteidea"),
    path("editidea/<int:id>/", views.edit_idea, name="editidea"),
]
