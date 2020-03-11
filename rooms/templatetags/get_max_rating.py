from django import template
from rooms import models as room_models
from reviews import models as review_models

register = template.Library()


@register.simple_tag
def get_max_rating(rooms):
    if rooms is not None:
        reviews_count = {}
        all_reviews = review_models.Review.objects.all()
        all_reviews = list(all_reviews)
        for rev in all_reviews:
            if rev.room in reviews_count:
                reviews_count[rev.room] += 1
            else:
                reviews_count[rev.room] = 1
        rating = {}
        all_rooms = room_models.Room.objects.all()
        all_rooms = list(all_rooms)
        for r in all_rooms:
            if r in reviews_count and reviews_count[r] >= 5:
                rating[r] = r.total_rating()

        if len(rating) == 0:
            return "-1"

        top_rating_room = max(rating.keys(), key=(lambda k: rating[k]))

        return top_rating_room

