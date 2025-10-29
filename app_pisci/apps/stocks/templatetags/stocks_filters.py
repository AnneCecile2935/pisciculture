from django import template

register = template.Library()

@register.filter(name='widget_type')
def widget_type(field):
    return field.field.widget.__class__.__name__

@register.filter(name='add_class')
def add_class(field, css_class):
    if hasattr(field, 'widget') and isinstance(field.widget, Widget):
        if 'class' in field.widget.attrs:
            field.widget.attrs['class'] += f' {css_class}'
        else:
            field.widget.attrs['class'] = css_class
    return field
