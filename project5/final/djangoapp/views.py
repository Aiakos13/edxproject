import base64
import uuid
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Comment, Post, UserExtended


def _get_datetime(dt):
    result = str(datetime.strftime(dt, "%B %d, %Y, %I:%M %p").replace('PM', 'p.m.').replace('AM', 'a.m.'))

    split = result.split(":")
    if split[0][-2] == "0":
        result = split[0][:-2] + split[0][-1] + ":" + split[1]

    return result


def index(request):
    if request.user.id is None:
        return HttpResponseRedirect(reverse("welcome"))

    user = User.objects.get(id=request.user.id)
    user_ex = UserExtended.objects.get(user__id=user.id)
    context = {
        "posts": [],
        "following": False
    }

    if user_ex.following.count() > 0:
        context["following"] = True

    for following in user_ex.following.all():
        context["posts"].extend(Post.objects.filter(author__id=following.id))
    context["posts"].sort(key=lambda x: x.created, reverse=True)

    return render(request, "djangoapp/index.html", context)


def welcome(request):
    if request.method == "POST":
        return HttpResponseNotAllowed(["GET"])

    return render(request, "djangoapp/welcome.html")


def login_view(request):
    if request.method == "GET":
        return HttpResponseNotAllowed(["POST"])

    user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
    if user is None:
        return HttpResponseRedirect(reverse("welcome"))

    login(request, user)
    return HttpResponseRedirect(reverse("index"))


def logout_view(request):
    if request.method == "POST":
        return HttpResponseNotAllowed(["GET"])

    logout(request)
    return HttpResponseRedirect(reverse("welcome"))


def register_view(request):
    if request.method == "GET":
        return HttpResponseNotAllowed(["POST"])

    user = User.objects.create_user(
        username=request.POST["username"],
        email=request.POST["email"],
        password=request.POST["password1"]
    )
    user_extended = UserExtended.objects.create(
        user=User.objects.get(
            id=user.id
        )
    )

    login(request, user)
    return HttpResponseRedirect(reverse("index"))


def user(request, user_id=None):
    if request.method == "POST":
        return HttpResponseNotAllowed(["GET"])

    if user_id is None:
        if request.user.id is None:
            return HttpResponseRedirect(reverse("welcome"))

        user_id2 = request.user.id
    else:
        user_id2 = user_id

    user_ex = UserExtended.objects.get(user__id=user_id2)

    show_follow_button = False
    if user_id is not None and user_id != request.user.id:
        show_follow_button = True

    already_follow = False
    if show_follow_button:
        already_follow = user_id in [x.user.id for x in UserExtended.objects.get(user__id=request.user.id).following.all()]

    context = {
        "user_ex": user_ex,
        "posts": Post.objects.filter(author__user__id=user_id2).order_by("-created"),
        "show_follow_button": show_follow_button,
        "already_follow": already_follow,
        "following": user_ex.following.count(),
        "followers": user_ex.followers.count()
    }
    context["dummies"] = range(4 - context["posts"].count() % 4)
    return render(request, "djangoapp/user.html", context)


def followers(request, user_id):
    user_ex = UserExtended.objects.get(user__id=user_id)

    context = {
        "user_ex": user_ex,
        "followers": user_ex.followers.all()
    }
    return render(request, "djangoapp/followers.html", context)


def following(request, user_id):
    user_ex = UserExtended.objects.get(user__id=user_id)

    context = {
        "user_ex": user_ex,
        "following": user_ex.following.all()
    }
    return render(request, "djangoapp/following.html", context)


def post(request, post_id):
    if request.method == "POST":
        return HttpResponseNotAllowed(["GET"])

    context = {
        "post": Post.objects.get(id=post_id),
        "comments": Comment.objects.filter(post__id=post_id).order_by("-created")
    }
    user_id = request.user.id
    user_liked = False
    if user_id is not None and user_id in [x.user.id for x in context["post"].liked.all()]:
        user_liked = True
    context["user_liked"] = user_liked

    return render(request, "djangoapp/post.html", context)


def search(request):
    if request.method == "POST":
        return HttpResponseNotAllowed(["GET"])

    query = request.GET["q"]

    context = {
        "users": UserExtended.objects.filter(user__username__icontains=query),
        "posts": Post.objects.filter(description__icontains=query)
    }
    return render(request, "djangoapp/search.html", context)


@login_required
@csrf_exempt
def new_follow(request):
    if request.method == "GET":
        return HttpResponseNotAllowed(["POST"])

    user_following = UserExtended.objects.get(user__id=request.user.id)
    user_to_follow = UserExtended.objects.get(user__id=request.POST["user_to_follow"])

    user_following.following.add(user_to_follow)

    return JsonResponse({"followers": user_to_follow.followers.count()})


@login_required
def new_comment(request):
    if request.method == "GET":
        return HttpResponseNotAllowed(["POST"])

    comment_text = request.POST["comment"]
    post_id = request.POST["post_id"]

    comment = Comment.objects.create(
        author=UserExtended.objects.get(user__id=request.user.id),
        post=Post.objects.get(id=post_id),
        text=comment_text
    )
    post = Post.objects.get(id=post_id)
    post.comments.add(comment)

    comments = [{"author_name": x.author.user.username,
                 "author_id": x.author.user.id,
                 "created": _get_datetime(x.created),
                 "text": x.text} for x in Comment.objects.filter(post__id=post_id).order_by("-created")]
    return JsonResponse({"comments": comments})


@login_required
@csrf_exempt
def new_like(request):
    if request.method == "GET":
        return HttpResponseNotAllowed(["POST"])

    post_id = request.POST["post_id"]
    user_id = request.user.id

    post = Post.objects.get(id=post_id)
    post.liked.add(UserExtended.objects.get(user__id=user_id))

    return JsonResponse({"liked": post.liked.count()})


@login_required
@csrf_exempt
def avatar(request):
    if request.method == "GET":
        return HttpResponseNotAllowed(["POST"])

    image_data = request.POST["image"]
    format, imgstr = image_data.split(';base64,')
    ext = format.split('/')[-1]

    data = ContentFile(base64.b64decode(imgstr))
    file_name = f"{str(uuid.uuid4())}.{ext}"

    user_ex = UserExtended.objects.get(user__id=request.user.id)
    if user_ex.avatar != user_ex.avatar.field.default:
        user_ex.avatar.delete(save=True)
    user_ex.avatar.save(file_name, data, save=True)

    return JsonResponse({"message": "success"})


@login_required
@csrf_exempt
def upload(request):
    if request.method == "GET":
        return render(request, "djangoapp/upload.html")

    description = request.POST["description"]

    image_data = request.POST['image']
    format, imgstr = image_data.split(';base64,')
    ext = format.split('/')[-1]

    data = ContentFile(base64.b64decode(imgstr))
    file_name = f"{str(uuid.uuid4())}.{ext}"

    post = Post.objects.create(
        author=UserExtended.objects.get(user__id=request.user.id),
        description=description
    )
    post.image.save(file_name, data, save=True)

    return HttpResponseRedirect(reverse("user"))
