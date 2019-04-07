from django import template

import markdown

register = template.Library()


@register.filter
def markdownify(text):
    return markdown.markdown(text.replace('\r\n', '\n'), safe_mode='escape', extensions=['markdown.extensions.extra'])