from web.response import Response
from utils.template import load_template


def render(template_name):

    html = load_template(template_name)

    return Response(
        body=html,
        headers={
            "Content-Type": "text/html"
        }
    )