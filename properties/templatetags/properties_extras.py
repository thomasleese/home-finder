from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def format_distance(value):
    if value >= 500:
        return mark_safe(f"{round(value / 1000, 2)}&nbsp;km")
    else:
        return mark_safe(f"{value}&nbsp;m")


@register.filter
def format_duration(value):
    if value >= 60:
        mins = value // 60
        secs = value - (mins * 60)
        if secs == 0:
            return mark_safe(f"{mins}&nbsp;mins")
        else:
            return mark_safe(f"{mins}&nbsp;mins&nbsp;{secs}&nbsp;secs")
    else:
        return mark_safe(f"{value}&nbsp;secs")
