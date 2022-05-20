from django.db import IntegrityError
from django.shortcuts import  render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import RedirectView, TemplateView, ListView
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import get_user_model
from users.forms import NewUserForm
from follows.forms import FollowForm
from follows.models import UserFollows

User = get_user_model()


def user_redirect_view(request):
    if request.user.is_authenticated:
        return redirect("reviews_tickets:feed")
    else:
        return redirect("/accounts/login/")

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("reviews_tickets:feed")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request=request, template_name="registration/register.html", context={"register_form":form})


def add_follower(request):
    if request.method == "POST":
        form = FollowForm(request.POST)
        if form.is_valid():
            following_user_username = form.cleaned_data['username']
            following_user = User.objects.filter(username=following_user_username)
            if following_user and not UserFollows.objects.filter(followed_user=request.user, user=following_user[0]):
                if following_user[0] == request.user:
                    messages.error(request, "You can't follow yourself")
                else:
                    follow = UserFollows(user=following_user[0], followed_user=request.user)
                    follow.save()
                    messages.success(request, f"You are now following {following_user_username}")
            else:
                messages.error(request, "User does not exist or you are already following him/her")
    return redirect("users:all")


def delete_follower(request, user_id):
    user = User.objects.get(id=user_id)
    userfollows = UserFollows.objects.get(user=user, followed_user=request.user)
    userfollows.delete()
    messages.success(request, f"You have successfully unfollowed {user.username}")
    return redirect("users:all")



class UsersListView(TemplateView):
    template_name = "users/followers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FollowForm()
        return context

    def get(self,request, *args, **kwargs):
        context = self.get_context_data()
        context['following'] = UserFollows.objects.filter(followed_user=request.user)
        context['followed_by'] = UserFollows.objects.filter(user=request.user)
        return self.render_to_response(context)

