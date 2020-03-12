import datetime
from django import template
from reservations import models as reservation_models

register = template.Library()


@register.simple_tag
def check_day_change(l_d):
    l_d_list = list(map(int, l_d.split(" ")))
    now = datetime.datetime.today()
    year = now.year
    month = now.month
    day = now.day
    if year != l_d_list[0] or month != l_d_list[1] or day != l_d_list[2]:
        return True

    return False
