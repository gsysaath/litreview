from django.conf import settings
from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from reviews_tickets.views import (
    UserReviewTicketView,
    ReviewTicketView,
    ReviewCreateView,
    ReviewCreateAllView,
    ReviewUpdateView,
    TicketCreateView,
    TicketUpdateView,
    ticket_delete_view,
    review_delete_view,
)


app_name = "reviews_tickets"
urlpatterns = [
    path(
        ('my-feed/'), login_required(UserReviewTicketView.as_view()), name="user-feed"
    ),
    path(
        ('feed/'), login_required(ReviewTicketView.as_view()), name="feed"
    ),
    path(
        ('ticket/new/'), login_required(TicketCreateView.as_view()), name="ticket-create"
    ),
    re_path(
        r'^ticket/(?P<ticket_id>[0-9]+)/$', login_required(TicketUpdateView.as_view()), name="ticket-update"
    ),
    re_path(
        r'^ticket/(?P<ticket_id>[0-9]+)/review/new/$', login_required(ReviewCreateView.as_view()), name="review-to-ticket-create"
    ),
    path(
        ('review/new/'), login_required(ReviewCreateAllView.as_view()), name="review-create"
    ),
    re_path(
        r'^review/(?P<review_id>[0-9]+)$', login_required(ReviewUpdateView.as_view()), name="review-update"
    ),
    re_path(
        r'^ticket/(?P<ticket_id>[0-9]+)/delete/$', login_required(ticket_delete_view), name="ticket-delete"
    ),
    re_path(
        r'^review/(?P<review_id>[0-9]+)/delete/$', login_required(review_delete_view), name="review-delete"
    ),
]