from django.shortcuts import render
from django import forms



# Create your views here.
def index(request):
    if "tasks" not in request.session or request.session["tasks"] is None:
        request.session["tasks"] = []
    return render(request, "todo/index.html", {
        "tasks": request.session["tasks"]
    })

def add(request):
    return render(request, "todo/index.html",)


def remove(request):
    return render(request, "todo/index.html",)

