from django.urls import path
from django.contrib.auth.decorators import login_required

from users.views import (
    register_request,
    add_follower,
    delete_follower,
    UsersListView,
)


app_name = "users"
urlpatterns = [
    path(
        ("all"),
        view=login_required(UsersListView.as_view()),
        name="all"
    ),
    path("register/", register_request, name="register"),
    path("add-follower", login_required(add_follower), name="add-follower"),
    path("delete-follower/<int:user_id>/", login_required(delete_follower), name="delete-follower"),
]
