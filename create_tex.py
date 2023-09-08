
from jinja2 import Environment, FileSystemLoader
from iso639 import languages
import json
import sys
import toml
import os


NAME = os.environ["NAME"]
LANG = os.environ["LANG"]
LANGNAME = languages.get(alpha2=LANG).name

class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value


with open("config.toml", "r") as f: cfg = toml.loads(f.read())
config = DotDict(cfg)

os.environ["EXPORT_DEST"] = config.General.export_destination

environment = Environment(loader=FileSystemLoader("templates/"), variable_start_string='<!', variable_end_string='>')
template = environment.get_template("template.tex")

js1 = dict()
js2 = dict()

errmsg_FileNotFound = "File sources/{lang}_{name}.json was not found."

source_destination = os.path.join(config.General.source_destination, NAME)
try:
    with open(os.path.join(source_destination, f"he_{NAME}.json")) as fj1:
        js1 = json.load(fj1)
except FileNotFoundError:
    msg = errmsg_FileNotFound.format(lang="he", name=NAME)
    print(msg)
    sys.exit(1)

try:
    with open(os.path.join(source_destination, f"{LANG}_{NAME}.json")) as fj2:
        js2 = json.load(fj2)
except FileNotFoundError:
    msg = errmsg_FileNotFound.format(lang=LANG, name=NAME)
    print(msg)
    sys.exit(1)


def main():
    new_js = {"heTitle": js1["heTitle"], "text": []}

    for i, chapter_content in enumerate(js1["text"]):
        chapter = []
        for j, verse_content in enumerate(chapter_content):
            chapter += [{"he": verse_content, "pl": js2["text"][i][j].strip()}]
        new_js["text"] += [chapter]

    content = template.render(title=js1["heTitle"], chapters=new_js["text"], config=config, lang=LANGNAME)

    with open(f"tex/{NAME}.tex", "w") as f:
        f.write(content)

    os.system("bash create_pdf.sh")

main()
