# from http://stackoverflow.com/a/1112236
import re
import base64
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()

@register.filter
def get_attr(value, arg):
  """Gets an attribute of an object dynamically from a string name"""

  if hasattr(value, str(arg)):
    return getattr(value, arg)
  elif hasattr(value, 'has_key') and value.has_key(arg):
    return value[arg]
  elif numeric_test.match(str(arg)) and len(value) > int(arg):
    return value[int(arg)]
  else:
    return settings.TEMPLATE_STRING_IF_INVALID

@register.filter
def get_image(value):
  """Gets an picture of a user"""
  return base64.b64encode(value)