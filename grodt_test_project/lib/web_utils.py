
import json
import re
import sys

from django import template
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string


def _render_error(request, errortpl="error", user_context=None):
    if user_context is None:
        user_context = {}
    return render(
        request, "common/%s.html" % errortpl, user_context
    )


def render_actions(actions):
    t = template.Template("""{% load lib_tags %}
{% for a in actions %}{% render_link a %}{% endfor %}
""")
    return t.render(template.Context({"actions": actions}))


def getctx(status, level=1, callback=None, **kwargs):
    if not callback:
        callername = sys._getframe(level).f_code.co_name
    else:
        callername = callback
    ctx = {"status": status, "callback": callername}
    for kw, v in list(kwargs.items()):
        ctx[kw] = v
    return ctx


def ajax_response(request, status="ok", respmsg=None,
                  url=None, ajaxnav=False, norefresh=False,
                  template=None, **kwargs):
    """Ajax response shortcut

    Simple shortcut that sends an JSON response. If a template is
    provided, a 'content' field will be added to the response,
    containing the result of this template rendering.

    :param request: a Request object
    :param status: the response status ('ok' or 'ko)
    :param respmsg: the message that will displayed in the interface
    :param url: url to display after receiving this response
    :param ajaxnav:
    :param norefresh: do not refresh the page after receiving this response
    :param template: eventual template's path
    :param kwargs: dict used for template rendering
    """
    ctx = {}
    for k, v in list(kwargs.items()):
        ctx[k] = v
    if template is not None:
        content = render_to_string(template, ctx, request)
    elif "content" in kwargs:
        content = kwargs["content"]
    else:
        content = ""
    jsonctx = {"status": status, "content": content}
    if respmsg is not None:
        jsonctx["respmsg"] = respmsg
    if ajaxnav:
        jsonctx["ajaxnav"] = True
    if url is not None:
        jsonctx["url"] = url
    jsonctx["norefresh"] = norefresh
    return JsonResponse(jsonctx)


def render_to_json_response(context, **response_kwargs):
    """Simple shortcut to render a JSON response.

    :param dict context: response content
    :return: ``HttpResponse`` object
    """
    data = json.dumps(context)
    response_kwargs["content_type"] = "application/json"
    return HttpResponse(data, **response_kwargs)


def static_url(path):
    """Returns the correct static url for a given file

    :param path: the targeted static media
    """
    if path.startswith("/"):
        path = path[1:]
    return "%s%s" % (settings.STATIC_URL, path)


def size2integer(value, output_unit="B"):
    """Try to convert a string representing a size to an integer value
    in bytes or megabytes.

    Supported formats:
    * K|k for KB
    * M|m for MB
    * G|g for GB

    :param value: the string to convert
    :param output_unit: result's unit (defaults to Bytes)
    :return: the corresponding integer value
    """
    m = re.match(r"(\d+)\s*([a-zA-Z]+)", value)
    if m is None:
        if re.match(r"\d+", value):
            return int(value)
        return 0
    if output_unit == "B":
        if m.group(2)[0] in ["K", "k"]:
            return int(m.group(1)) * 2 ** 10
        if m.group(2)[0] in ["M", "m"]:
            return int(m.group(1)) * 2 ** 20
        if m.group(2)[0] in ["G", "g"]:
            return int(m.group(1)) * 2 ** 30
    elif output_unit == "MB":
        if m.group(2)[0] in ["K", "k"]:
            return int(int(m.group(1)) / 2 ** 10)
        if m.group(2)[0] in ["M", "m"]:
            return int(m.group(1))
        if m.group(2)[0] in ["G", "g"]:
            return int(m.group(1)) * 2 ** 10
    else:
        raise ValueError("Unsupported output unit {}".format(output_unit))
    return 0
