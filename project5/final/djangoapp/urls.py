from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("welcome", views.welcome, name="welcome"),

    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),

    path("user", views.user, name="user"),
    path("user/<int:user_id>", views.user, name="user"),
    path("followers/<int:user_id>", views.followers, name="followers"),
    path("following/<int:user_id>", views.following, name="following"),
    path("upload", views.upload, name="upload"),
    path("avatar", views.avatar, name="avatar"),
    path("post/<post_id>", views.post, name="post"),
    path("search", views.search, name="search"),

    path("comment", views.new_comment, name="comment"),
    path("like", views.new_like, name="like"),
    path("follow", views.new_follow, name="follow")
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
