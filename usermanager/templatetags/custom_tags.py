from django import template

register = template.Library()


@register.filter(name="email_ma")
def email_masker(value, arg):
    email_split = value.split("@")
    return f"{email_split[0]}@******.***" if arg % 2 == 0 else value
