from web.response import Response
from utils.template import load_template


def render(template_name, context=None):

    html = load_template(template_name)

    context = context or {}

    for key, value in context.items():
        val_str = str(value)
        html = html.replace("{{ " + key + " }}", val_str)
        html = html.replace("{{" + key + "}}", val_str)

    return Response(
        body=html,
        headers={
            "Content-Type": "text/html"
        }
    )