from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Idea

# how can i do JsonResponse with Django?


# Create your views here.


def index(req):
    return render(req, "index.html")


def allideas(req):
    idea = Idea.objects.order_by("created_at")
    data = serializers.serialize("json", idea)
    return HttpResponse(data, content_type="application/json")


def add_idea(req):
    if req.method == "POST":
        title = req.POST.get("title")
        description = req.POST.get("description")
        user = req.POST.get("user")
        Idea.objects.create(title=title, description=description, user=user)
        return HttpResponseRedirect("/")
    return render(req, "add_idea.html")


def edit_idea(req, id):
    if req.method == "POST":
        title = req.POST.get("title")
        description = req.POST.get("description")
        user = req.POST.get("user")
        Idea.objects.filter(id=id).update(
            title=title, description=description, user=user
        )
        return HttpResponseRedirect("/")
    return render(req, "edit_idea.html", {"id": id})


def delete_idea(req, id):
    if req.method == "DELETE":
        Idea.objects.filter(id=id).delete()
        return HttpResponseRedirect("/")
    return HttpResponseRedirect("/")


def edit_idea(req, id):
    if req.method == "POST":
        title = req.POST.get("title")
        description = req.POST.get("description")
        user = req.POST.get("user")
        Idea.objects.filter(pk=id).update(
            title=title, description=description, user=user
        )
        return HttpResponseRedirect("/")
    idea = Idea.objects.get(pk=id)
    print(idea.description)
    data = {
        "title": idea.title,
        "description": idea.description,
        "user": idea.user,
        "id": id,
    }
    return JsonResponse(data)
