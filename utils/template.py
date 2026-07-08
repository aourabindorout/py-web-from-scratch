def load_template(filename):

    with open(f"templates/{filename}", "r") as file:
        return file.read()