from web.response import Response
from utils.template import load_template


def render(template_name, context=None):

    html = load_template(template_name)

    context = context or {}

    for key, value in context.items():
        html = html.replace(
            "{{ " + key + " }}",
            str(value)
        )

    return Response(
        body=html,
        headers={
            "Content-Type": "text/html"
        }
    )