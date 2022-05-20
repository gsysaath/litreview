
from django.template import Library

from reviews_tickets.models import Review


register = Library()


@register.filter
def classname(obj):
    return obj.__class__.__name__

@register.filter
def check_review_exist(obj):
    review = Review.objects.filter(ticket=obj)
    return True if len(review) > 0 else False

@register.filter
def show_star(obj):
    result = ""
    missing_stars_num = 5 - obj.rating
    for _ in range(obj.rating):
        result += '★'
    for _ in range(missing_stars_num):
        result += '☆'
    return result