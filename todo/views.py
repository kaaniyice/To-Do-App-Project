import datetime
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from user.models import Task


# Create your views here.
@login_required
def index(request):
    # Get the tasks of the currently logged user
    tasks = Task.objects.filter(user=request.user).order_by('deadline')
    # if there is an error message display the error message
    try:
        error = request.session["error"]
    except:
        error = ""
    # Get the current time of the day
    date = datetime.date.today()
    # render the index.html with these values
    context = {
        "tasks": tasks,
        "error": error,
        "date": date,
    }
    return render(request, "index.html", context=context)


@login_required
def add(request):
    if request.method == "POST":
        # Reset the errors
        request.session["error"] = ""
        # Get the form values posted
        description = request.POST.get("description")
        deadline = request.POST.get("deadline")
        priority = request.POST.get("priority")
        # Manual validation-check for the description and if empty display error message
        if not description:
            # Handle missing description
            request.session["error"] = "Description is required"
            return HttpResponseRedirect(reverse("todo:index"))

        if deadline:
            # If the deadline is pass-date display error message
            deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
            if deadline_date < datetime.date.today():
                request.session["error"] = "The deadline can't be a past time"
                return HttpResponseRedirect(reverse("todo:index"))
        else:
            deadline = None
        # Create task instance and assign user
        try:
            task = Task(
                user=request.user,
                description=description,
                deadline=deadline,
                priority=priority
            )
            task.save()
        except Exception as error:
            request.session["error"] = error
            return HttpResponseRedirect(reverse("todo:index"))

        return HttpResponseRedirect(reverse("todo:index"))
    else:
        return HttpResponseRedirect(reverse("todo:index"))


@login_required
def remove(request):
    if request.method == "POST":
        # Reset the errors
        request.session["error"] = ""
        task_id = request.POST.get("task_id")
        # Retrieve task by task.id and check ownership
        task = Task.objects.get(id=task_id, user=request.user)
        # If there is a task delete it from database
        if task:
            task.delete()
            return HttpResponseRedirect(reverse("todo:index"))  # Redirect to the index page
        else:
            # Handle GET request if needed (e.g., confirmation page)
            return HttpResponseRedirect(reverse("todo:index"))


@login_required
def edit(request):
    if request.method == "POST":
        # Reset the errors
        request.session["error"] = ""
        task_id = request.POST.get("task_id")
        # Retrieve task by task.id and check ownership
        task = Task.objects.get(id=task_id, user=request.user)
        task.description = request.POST.get("description")
        task.deadline = request.POST.get("due_date")
        task.priority = request.POST.get("priority")
        # Handle missing description
        if not task.description:
            request.session["error"] = "Description is required"
            return HttpResponseRedirect(reverse("todo:index"))
        if task.deadline:
            # If the deadline is pass-date display error message
            deadline_date = datetime.datetime.strptime(task.deadline, "%Y-%m-%d").date()
            if deadline_date < datetime.date.today():
                request.session["error"] = "The deadline can't be a past time"
                return HttpResponseRedirect(reverse("todo:index"))
        # save the task to database
        task.save()
        # Redirect to index
        return HttpResponseRedirect(reverse("todo:index"))
    else:
        return HttpResponseRedirect(reverse("todo:index"))
