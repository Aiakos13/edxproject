from django.urls import path, re_path

from django.conf.urls import handler400, handler403, handler404, handler500
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.wiki_entry, name="wiki_entry"),
    re_path(r"^wiki/(?P<title>).*[\s\w]*/$", views.wiki_entry, name="wiki_entry"),
    re_path(
        r"^update-entry/$",
        views.create_update,
        name="create_update",
    ),
    re_path(
        r"^update-entry/?/(?P<title>.*\s*)/$",
        views.create_update,
        name="create_update",
    ),
    re_path(
        r"^delete-entry/(?P<title>)/?(?P<deletion>.*)/$",
        views.delete_entry,
        name="delete_entry",
    ),
    path("delete-entry/<title>/<deletion>", views.delete_entry, name="delete_entry"),
    path("delete-entry/<title>", views.delete_entry, name="delete_entry"),
    path("random-entry/", views.random_entry, name="random_entry"),
    re_path(r"^page-not-found/$", views.notFound, name="notFound"),
]
