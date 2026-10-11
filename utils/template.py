import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

TAG_RE = re.compile(r'(\{\{.*?\}\}|\{%.*?%\})', re.DOTALL)


def load_template(filename):
    template_path = os.path.join(TEMPLATES_DIR, filename)
    with open(template_path, "r", encoding="utf-8") as file:
        return file.read()


def resolve_value(expr, context):
    expr = expr.strip()
    if not expr:
        return ""
    parts = expr.split(".")
    val = context.get(parts[0])
    for p in parts[1:]:
        if val is None:
            return None
        if isinstance(val, dict):
            val = val.get(p)
        elif hasattr(val, p):
            attr = getattr(val, p)
            val = attr() if callable(attr) else attr
        elif hasattr(val, "__getitem__"):
            try:
                val = val[p]
            except Exception:
                return None
        else:
            return None
    return val


def eval_condition(condition, context):
    cond = condition.strip()
    is_not = False
    if cond.startswith("not "):
        is_not = True
        cond = cond[4:].strip()
    val = resolve_value(cond, context)
    truthy = bool(val)
    return not truthy if is_not else truthy


class TextNode:
    def __init__(self, text):
        self.text = text

    def render(self, context):
        return self.text


class VarNode:
    def __init__(self, expr):
        self.expr = expr

    def render(self, context):
        val = resolve_value(self.expr, context)
        return "" if val is None else str(val)


class IfNode:
    def __init__(self, condition, true_nodes, false_nodes):
        self.condition = condition
        self.true_nodes = true_nodes
        self.false_nodes = false_nodes

    def render(self, context):
        if eval_condition(self.condition, context):
            return "".join(n.render(context) for n in self.true_nodes)
        else:
            return "".join(n.render(context) for n in self.false_nodes)


class ForNode:
    def __init__(self, var_name, iter_expr, loop_nodes, empty_nodes):
        self.var_name = var_name
        self.iter_expr = iter_expr
        self.loop_nodes = loop_nodes
        self.empty_nodes = empty_nodes

    def render(self, context):
        items = resolve_value(self.iter_expr, context)
        if not items:
            return "".join(n.render(context) for n in self.empty_nodes)
        out = []
        for item in items:
            ctx = dict(context)
            ctx[self.var_name] = item
            out.append("".join(n.render(ctx) for n in self.loop_nodes))
        return "".join(out)


class IncludeNode:
    def __init__(self, filename):
        self.filename = filename

    def render(self, context):
        raw_tmpl = load_template(self.filename)
        return render_template(raw_tmpl, context)


def parse_nodes(tokens, stop_tags=None):
    stop_tags = stop_tags or []
    nodes = []
    while tokens:
        token = tokens[0]
        if token.startswith("{%") and token.endswith("%}"):
            tag_content = token[2:-2].strip()
            parts = tag_content.split()
            if not parts:
                tokens.pop(0)
                continue
            tag_name = parts[0]
            if tag_name in stop_tags:
                return nodes
            tokens.pop(0)

            if tag_name == "if":
                condition = " ".join(parts[1:])
                true_nodes = parse_nodes(tokens, ["else", "endif"])
                false_nodes = []
                if tokens and tokens[0].strip().startswith("{% else"):
                    tokens.pop(0)
                    false_nodes = parse_nodes(tokens, ["endif"])
                if tokens and tokens[0].strip().startswith("{% endif"):
                    tokens.pop(0)
                nodes.append(IfNode(condition, true_nodes, false_nodes))

            elif tag_name == "for":
                # {% for item in items %}
                var_name = parts[1]
                iter_expr = parts[3]
                loop_nodes = parse_nodes(tokens, ["empty", "else", "endfor"])
                empty_nodes = []
                if tokens and (tokens[0].strip().startswith("{% empty") or tokens[0].strip().startswith("{% else")):
                    tokens.pop(0)
                    empty_nodes = parse_nodes(tokens, ["endfor"])
                if tokens and tokens[0].strip().startswith("{% endfor"):
                    tokens.pop(0)
                nodes.append(ForNode(var_name, iter_expr, loop_nodes, empty_nodes))

            elif tag_name == "include":
                filename = parts[1].strip("\"'")
                nodes.append(IncludeNode(filename))

        elif token.startswith("{{") and token.endswith("}}"):
            tokens.pop(0)
            nodes.append(VarNode(token[2:-2].strip()))
        else:
            tokens.pop(0)
            nodes.append(TextNode(token))

    return nodes


def render_template(template_str, context):
    tokens = [t for t in TAG_RE.split(template_str) if t]
    nodes = parse_nodes(tokens)
    return "".join(n.render(context) for n in nodes)