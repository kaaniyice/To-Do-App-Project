from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms


# Create your views here.
@login_required
def index(request):
    if "tasks" not in request.session or request.session["tasks"] is None:
        request.session["tasks"] = []
    return render(request, "todo/index.html", {
        "tasks": request.session["tasks"]
    })


@login_required
def add(request):
    request.session.modified = True
    if request.method == "POST":
        task = request.POST["add_name"]
        date = request.POST["add_date"]
        try:
            request.session["tasks"] += [task]
        except:
            pass
    return HttpResponseRedirect(reverse("todo:index"))


@login_required
def remove(request):
    if request.method == "POST":
        name = request.POST.get("task_value", "")
        if name in request.session["tasks"]:
            # The django session object can only save when its modified. But because you are modifying an object within
            # session, the session object doesn't know its being modified and hence it cant save.
            # To let the session object know its modified use:
            # request.session.modified = True
            request.session.modified = True
            request.session["tasks"].remove(name)
            print(request.session["tasks"])
    return HttpResponseRedirect(reverse("todo:index"))
