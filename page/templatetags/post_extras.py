# post_extras.py
from django import template

register = template.Library()

@register.filter
def in_profiles(profiles, author):
    return profiles.filter(user=author)