from django import template
from reservations import models as reservation_models

register = template.Library()


@register.simple_tag
def get_guest_reservation(user):
    guest_reservations = []
    all_reservations = reservation_models.Reservation.objects.all()
    all_reservations = list(all_reservations)
    for r in all_reservations:
        if r.room.host == user and r.guest != user:
            guest_reservations.append(r)

    if len(guest_reservations) == 0:
        return "-1"

    return guest_reservations
