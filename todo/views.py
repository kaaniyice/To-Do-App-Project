from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from user.models import Task


# Create your views here.
@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user).order_by('deadline')
    return render(request, "todo/index.html", {"tasks": tasks})


@login_required
def add(request):
    if request.method == "POST":
        description = request.POST.get("description")
        deadline = request.POST.get("deadline")  # Get other fields as needed
        priority = request.POST.get("priority")
        # Manual validation (or use model validation methods for convenience)
        if not description:
            # Handle missing description
            return render(request, "todo/index.html", {"error": "Description is required"})
        # Create task instance and assign user
        task = Task(
            user=request.user,
            description=description,
            deadline=deadline,  # Set other fields as needed
            priority=priority
        )
        # Validate using model methods

        task.save()
        return HttpResponseRedirect(reverse("todo:index"))
    return HttpResponseRedirect(reverse("todo:index"))


@login_required
def remove(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        # Retrieve task by description and check ownership
        task = Task.objects.get(id=task_id, user=request.user)
        if request.method == "POST":
            task.delete()
            return HttpResponseRedirect(reverse("todo:index"))  # Redirect to the index page
        else:
            # Handle GET request if needed (e.g., confirmation page)
            return render(request, "todo/confirm_remove.html", {"task": task})
