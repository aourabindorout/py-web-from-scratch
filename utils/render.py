from utils.template import load_template, render_template
from web.response import Response


def render(template_name, context=None, request=None):
    template_str = load_template(template_name)
    context = dict(context) if context else {}

    # Provide current authenticated user to all templates cleanly
    if "user" not in context:
        context["user"] = getattr(request, "user", None) if request else None

    html = render_template(template_str, context)
    return Response(
        body=html,
        headers={
            "Content-Type": "text/html"
        }
    )