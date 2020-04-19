from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(elem, arg):
    elem.field.widget.attrs.update({'class' : arg})
    return elem
