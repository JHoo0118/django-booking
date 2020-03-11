from django import template

register = template.Library()


@register.simple_tag
def get_in_progress(reservations):
    reservations_list = list(reservations)
    cnt = 0
    for r in reservations_list:
        if r.is_finished():
            cnt += 1

    if cnt == 0:
        return True
    else:
        return False

