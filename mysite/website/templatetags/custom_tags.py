from django import template
from datetime import datetime
from django.utils.safestring import mark_safe
import json


register = template.Library()

@register.filter
def get_at_index(object_list, index):
	return object_list[index]

@register.filter
def replace_entity(value):
	return value.replace('&#8220;','"').replace('&#44;',',').replace('None', '')

@register.filter
def js(obj):
	return mark_safe(json.dumps(obj))
