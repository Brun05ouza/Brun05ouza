"""Check deliverables, XML safety, image alternatives and local references."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = "{http://www.w3.org/2000/svg}"


class Images(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img":
            assert attrs.get("alt"), "An image is missing its text alternative"
        for attr in ["src", "srcset"]:
            if attr in attrs:
                assert (ROOT / attrs[attr]).is_file(), f"Broken local image: {attrs[attr]}"


def main():
    count, largest = 0, 0
    for path in sorted((ROOT / "assets").rglob("*.svg")):
        source = path.read_text(encoding="utf-8")
        node = ET.fromstring(source)
        assert node.tag == NS + "svg", f"Invalid SVG: {path}"
        assert node.get("viewBox") and node.find(NS + "title") is not None
        for item in node.iter():
            assert item.tag not in {NS + "script", NS + "foreignObject", NS + "image"}
            assert not any(k.lower().startswith("on") for k in item.attrib)
            assert not any("http" in v for k,v in item.attrib.items() if k.endswith("href"))
        assert "prefers-reduced-motion" in source
        assert path.stat().st_size < 250_000, f"Oversized SVG: {path}"
        largest = max(largest, path.stat().st_size)
        count += 1
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    Images().feed(readme)
    for target in re.findall(r'\]\(([^)]+)\)', readme):
        if not re.match(r"https?://|mailto:", target):
            assert (ROOT / target.split("#")[0]).is_file(), f"Broken local link: {target}"
    assert readme.count("<picture>") == readme.count("</picture>")
    assert readme.count("<a ") == readme.count("</a>")
    profile = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
    assert len(profile["projects"]) == 6
    assert profile["projects"][-1]["personal"] is True
    assert "projeto pessoal" in readme.lower()
    print(f"Valid: {count} SVGs; largest {largest:,} bytes; all local references and image alternatives present.")


if __name__ == "__main__":
    main()
