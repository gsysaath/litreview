from itertools import chain

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()

from reviews_tickets.models import Ticket, Review
from follows.models import UserFollows
from reviews_tickets.forms import ReviewForm, TicketForm


class UserReviewTicketView(ListView):
    template_name = "reviews_tickets/user_reviews_tickets_list.html"

    def get_queryset(self, request):
        user = request.user
        reviews = Review.objects.filter(user=user)
        tickets = Ticket.objects.filter(user=user)
        reviews_tickets_list = sorted(
            chain(reviews, tickets),
            key=lambda x: x.time_created, 
            reverse=True
        )
        
        return reviews_tickets_list

    def get(self,request, *args, **kwargs):
        self.object_list = self.get_queryset(request)
        context = self.get_context_data()
        return self.render_to_response(context)


class ReviewTicketView(ListView):
    template_name = "reviews_tickets/reviews_tickets_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context[""] = 
        return context

    def get_queryset(self, request):
        user = request.user
        followed_users = UserFollows.objects.filter(followed_user=user).values('user')
        reviews = Review.objects.filter(Q(user__in=followed_users) | Q(user=user))
        tickets = Ticket.objects.filter(Q(user__in=followed_users) | Q(user=user))
        reviews_tickets_list = sorted(
            chain(reviews, tickets),
            key=lambda x: x.time_created,
            reverse=True
        )
        return reviews_tickets_list[0:20]

    def get(self,request, *args, **kwargs):
        self.object_list = self.get_queryset(request)
        context = self.get_context_data()
        return self.render_to_response(context)


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews_tickets/create_review_view.html"
    success_url = reverse_lazy("reviews_tickets:feed")

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = context['view'].kwargs.get('ticket_id')
        context['ticket_id'] = ticket_id
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        user = self.request.user
        ticket_id = self.kwargs.get('ticket_id')
        ticket = Ticket.objects.get(id=ticket_id)
        self.object = form.save(commit=False)
        self.object.user = user
        self.object.ticket = ticket
        self.object.save()
        response = HttpResponseRedirect(self.get_success_url())
        return response

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class ReviewCreateAllView(TemplateView):
    template_name = "reviews_tickets/create_review_and_ticket_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket_form'] = TicketForm
        context['review_form'] = ReviewForm
        return context

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        user = request.user
        ticket = TicketForm(request.POST, request.FILES).save(commit=False)
        review = ReviewForm(request.POST).save(commit=False)
        ticket.user = user
        ticket.save()
        review.user = user
        review.ticket = ticket
        review.save()
        url = reverse_lazy("reviews_tickets:feed")
        return HttpResponseRedirect(url)


class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews_tickets/edit_review_view.html"
    success_url = reverse_lazy("reviews_tickets:user-feed")

    def setup(self, request, review_id, *args, **kwargs):
        super().setup(request, review_id)
        self.review_id = review_id

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['review_id'] = self.review_id
        return context

    def get_object(self, queryset=None):
        review = Review.objects.get(id=self.review_id)
        if self.request.user != review.user:
            messages.warning(self.request, "Not allowed")
            return HttpResponseRedirect(reverse_lazy("reviews_tickets:feed"))
        return review


class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "reviews_tickets/create_ticket_view.html"
    success_url = reverse_lazy("reviews_tickets:feed")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        user = self.request.user
        self.object = form.save(commit=False)
        self.object.user = user
        self.object.save()
        response = HttpResponseRedirect(self.get_success_url())
        return response

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = "reviews_tickets/edit_ticket_view.html"
    success_url = reverse_lazy("reviews_tickets:user-feed")

    def setup(self, request, ticket_id, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        super().setup(request, ticket_id)
        self.ticket_id = ticket_id

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['ticket_id'] = self.ticket_id
        return context
    
    def get_object(self, queryset=None):
        ticket = Ticket.objects.get(id=self.ticket_id)
        if self.request.user != ticket.user:
            messages.warning(self.request, "Not allowed")
            return HttpResponseRedirect(reverse_lazy("reviews_tickets:feed"))
        return ticket


def ticket_delete_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if ticket.user != request.user:
        messages.warning(request, "Not allowed")
        return HttpResponseRedirect(reverse_lazy("reviews_tickets:feed"))
    ticket.delete()
    url = reverse_lazy("reviews_tickets:user-feed")
    messages.success(request, 'Ticket has been deleted')
    return HttpResponseRedirect(url)

def review_delete_view(request, review_id):
    review = Review.objects.get(id=review_id)
    if review.user != request.user:
        messages.warning(request, "Not allowed")
        return HttpResponseRedirect(reverse_lazy("reviews_tickets:feed"))
    review.delete()
    url = reverse_lazy("reviews_tickets:user-feed")
    messages.success(request, 'Review has been deleted')
    return HttpResponseRedirect(url)
