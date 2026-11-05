"""Manual check of project URLs; deliberately separate from the daily workflow."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from urllib.request import Request, urlopen


def check(url):
    try:
        with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as response:
            return response.status, url, response.url
    except Exception as error:
        return type(error).__name__, url, str(error)


if __name__ == "__main__":
    profile = json.loads((Path(__file__).resolve().parents[1] / "profile.json").read_text(encoding="utf-8"))
    with ThreadPoolExecutor(max_workers=6) as pool:
        for status, url, final in pool.map(check, (p["url"] for p in profile["projects"])):
            print(status, url, "->", final)
