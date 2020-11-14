from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

@register.filter(name='domain')
@stringfilter
def domain(url): 
    """ Extracts the domain of an URL """
    match = re.search(r'^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)', url)
    match = re.sub(r'((^https?:\/\/(www)?)|(^www.))', '', match.group()) 
    return match
    
    