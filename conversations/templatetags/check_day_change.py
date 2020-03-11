from django import template
from reservations import models as reservation_models

register = template.Library()


@register.simple_tag
def check_day_change(l_d, r_s_d):
    if int(l_d) - int(r_s_d) >= 1:
        return True
    else:
        return False
