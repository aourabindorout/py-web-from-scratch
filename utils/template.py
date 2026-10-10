import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")


def load_template(filename):
    template_path = os.path.join(TEMPLATES_DIR, filename)
    with open(template_path, "r", encoding="utf-8") as file:
        return file.read()