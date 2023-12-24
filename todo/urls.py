from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "todo"
urlpatterns = [
    path("", login_required(views.index), name="index"),
    path("add", login_required(views.add), name="add"),
    path('remove/', login_required(views.remove), name='remove'),
    path('edit/', login_required(views.edit), name='edit'),
]
