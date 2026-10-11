from web.response import Response
from utils.template import load_template


def render(template_name, context=None, request=None):

    html = load_template(template_name)

    context = dict(context) if context else {}

    # Automatically provide auth_nav context based on request.user
    if "auth_nav" not in context:
        user = getattr(request, "user", None) if request else None
        if user:
            context["auth_nav"] = f'<span style="color: var(--text-secondary); margin-right: 0.5rem;">👤 {user.username}</span><a href="/logout">Logout</a>'
        else:
            context["auth_nav"] = '<a href="/login">Login</a>'

    user = getattr(request, "user", None) if request else None
    if "current_user" not in context:
        context["current_user"] = user.username if user else ""

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