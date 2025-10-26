from django import template

register = template.Library()

@register.filter(name='widget_type')
def widget_type(field):
    return field.field.widget.__class__.__name__

@register.filter(name='add_class')
def add_class(field, css_class):
    if hasattr(field, 'widget') and hasattr(field.widget, 'attrs'):
        existing_classes = field.widget.attrs.get('class', '')
        field.widget.attrs['class'] = f"{existing_classes} {css_class}".strip()
    return field
