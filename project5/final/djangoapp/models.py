from django.contrib.auth.models import User
from django.db import models


def get_avatar_upload_path(instance, filename):
    return "user_{0}/{1}".format(instance.id, filename)


def get_image_upload_path(instance, filename):
    return "user_{0}/{1}".format(instance.author.id, filename)


class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=get_avatar_upload_path, default="no_avatar.png")
    following = models.ManyToManyField("self", symmetrical=False, related_name="followers")


class Post(models.Model):
    author = models.ForeignKey(UserExtended, on_delete=models.CASCADE, related_name="user_posts")
    image = models.ImageField(upload_to=get_image_upload_path)
    description = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(UserExtended, related_name="liked_posts")
    comments = models.ManyToManyField("Comment", related_name="commented_posts")


class Comment(models.Model):
    author = models.ForeignKey(UserExtended, on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")
    text = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)
