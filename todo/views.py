import datetime

from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from user.models import Task


# Create your views here.
@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user).order_by('deadline')
    print(tasks)
    try:
        error = request.session["error"]
    except:
        error = ""
    date = datetime.date.today()
    return render(request, "index.html", {
        "tasks": tasks,
        "error": error,
        "date": date,
    })


@login_required
def add(request):
    if request.method == "POST":
        request.session["error"] = ""
        description = request.POST.get("description")
        deadline = request.POST.get("deadline")  # Get other fields as needed
        priority = request.POST.get("priority")
        # Manual validation (or use model validation methods for convenience)
        if not description:
            # Handle missing description
            request.session["error"] = "Description is required"
            return HttpResponseRedirect(reverse("todo:index"))
        # Create task instance and assign user
        if deadline:
            deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
            if deadline_date < datetime.date.today():
                request.session["error"] = "The deadline can't be a past time"
                return HttpResponseRedirect(reverse("todo:index"))
        else:
            deadline = None
        try:
            task = Task(
                user=request.user,
                description=description,
                deadline=deadline,
                priority=priority
            )
            task.save()
        except Exception as error:
            print(error)
            request.session["error"] = error
            return HttpResponseRedirect(reverse("todo:index"))
        # Validate using model methods
        return HttpResponseRedirect(reverse("todo:index"))
    else:

        return HttpResponseRedirect(reverse("todo:index"))


@login_required
def remove(request):
    if request.method == "POST":
        request.session["error"] = ""
        task_id = request.POST.get("task_id")
        # Retrieve task by description and check ownership
        task = Task.objects.get(id=task_id, user=request.user)
        if task:
            task.delete()
            return HttpResponseRedirect(reverse("todo:index"))  # Redirect to the index page
        else:
            # Handle GET request if needed (e.g., confirmation page)
            return HttpResponseRedirect(reverse("todo:index"))


@login_required
def edit(request):
    if request.method == "POST":
        request.session["error"] = ""
        task_id = request.POST.get("task_id")
        task = Task.objects.get(id=task_id, user=request.user)  # Retrieve task and check ownership
        task.description = request.POST.get("description")
        task.due_date = request.POST.get("due_date")
        task.priority = request.POST.get("priority")
        task.save()
        return HttpResponseRedirect(reverse("todo:index"))  # Redirect to index
    else:
        return HttpResponseRedirect(reverse("todo:index"))
