from django import template

register = template.Library()

@register.filter(name='mult')
def mult(arg1,arg2):
    return arg1*arg2

