from django import template

register = template.Library()


@register.simple_tag
def get_reservation_false(reservations):
    reservations_list = list(reservations)
    if len(reservations_list) == 0:
        return True
    else:
        for r in reservations_list:
            if r.is_finished():
                continue
            return False

    return False

