import re

from django import template
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def check_active_menu(url):
    if "mynewapp" in url:
        return 1
    elif "xxx" in url:
        return 2

    return 0


@register.filter
def colorize_level(level):
    """A simple filter a text using a boostrap color."""
    classes = {
        "INFO": "text-info",
        "WARNING": "text-warning",
        "CRITICAL": "text-danger"
    }
    if level not in classes:
        return level
    return "<p class='%s'>%s</p>" % (classes[level], level)


@register.filter
def tohtml(message):
    """Simple tag to format a text using HTML."""
    return re.sub(r"'(.*?)'", r"<strong>\g<1></strong>", message)


@register.simple_tag
def visirule(field):
    if not hasattr(field, "form") or not hasattr(field.form, "visirules") or field.html_name not in field.form.visirules:
        return ""
    rule = field.form.visirules[field.html_name]
    return mark_safe(" data-visibility-field='{}' data-visibility-value='{}' ".format(rule["field"], rule["value"]))


@register.simple_tag
def display_messages(msgs):
    text = ""
    level = "info"
    for m in msgs:
        level = m.tags
        text += smart_text(m) + "\\\n"

    if level == "info":
        level = "success"
        timeout = "2000"
    else:
        timeout = "undefined"

    return mark_safe("""
<script type="text/javascript">
    $(document).ready(function() {
        $('body').notify('%s', '%s', %s);
    });
</script>
""" % (level, text, timeout))
