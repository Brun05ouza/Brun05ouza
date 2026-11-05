"""Fetch real GitHub data and render self-hosted SVGs; never store credentials.

Authentication: GH_TOKEN/GITHUB_TOKEN in Actions, or gh's OS keychain locally.
Only PUBLIC owned repositories are queried. Languages exclude forks/archives.
The calendar is exactly the contribution calendar returned by GitHub.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

from art import BG, BLUE, ICE, LINE, MUTED, VIOLET, WHITE, pixel, rect, svg, text

ROOT = Path(__file__).resolve().parents[1]
QUERY = """
query($login: String!, $cursor: String) {
  user(login: $login) {
    login
    followers { totalCount }
    repositories(first:100,after:$cursor,privacy:PUBLIC,ownerAffiliations:OWNER) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        isFork isArchived stargazerCount
        languages(first:100) { edges { size node { name } } }
      }
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel weekday } }
      }
    }
  }
}
"""


def github(login):
    repos, cursor, first = [], None, None
    while True:
        args = ["gh", "api", "graphql", "-f", f"query={QUERY}", "-f", f"login={login}"]
        if cursor:
            args += ["-f", f"cursor={cursor}"]
        result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", timeout=90)
        if result.returncode:
            # Do not print subprocess stderr: remote error text is not needed to diagnose auth.
            raise RuntimeError("GitHub API failed. Check gh auth status or the workflow token permissions.")
        data = json.loads(result.stdout)
        if data.get("errors") or not data.get("data", {}).get("user"):
            raise RuntimeError("GitHub GraphQL returned no complete user data; previous assets are preserved.")
        user = data["data"]["user"]
        first = first or user
        repos.extend(user["repositories"]["nodes"])
        pagination = user["repositories"]["pageInfo"]
        if not pagination["hasNextPage"]:
            break
        cursor = pagination["endCursor"]
    languages = Counter()
    for repo in repos:
        if not repo["isFork"] and not repo["isArchived"]:
            for language in repo["languages"]["edges"]:
                languages[language["node"]["name"]] += language["size"]
    calendar = first["contributionsCollection"]["contributionCalendar"]
    return {
        "username": first["login"],
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "public_repositories": first["repositories"]["totalCount"],
        "public_original_stars": sum(r["stargazerCount"] for r in repos if not r["isFork"]),
        "followers": first["followers"]["totalCount"],
        "languages_bytes": dict(languages.most_common()),
        "calendar": calendar,
    }


def number(value):
    return f"{value:,}".replace(",", ".")


def render(data, mobile=False):
    width, height = (480, 730) if mobile else (960, 530)
    left = 32 if mobile else 40
    metrics = [(data["public_repositories"], "Repositórios públicos"),
               (data["public_original_stars"], "Estrelas recebidas"),
               (data["calendar"]["totalContributions"], "Contribuições / 12 meses"),
               (data["followers"], "Seguidores no GitHub")]
    s = ""
    for i, (value, label) in enumerate(metrics):
        x = left + (i % 2) * 224 if mobile else left + i * 226
        y = 34 + (i // 2) * 100 if mobile else 34
        s += text(x, y + 18, number(value), 36, WHITE)
        s += text(x, y + 51, label, 13 if mobile else 14, MUTED)
    lang_y = 258 if mobile else 162
    s += pixel(left, lang_y, "LANGUAGES", 1.8, ICE)
    languages = data["languages_bytes"]
    total = sum(languages.values())
    top = list(languages.items())[:5]
    remainder = total - sum(v for _, v in top)
    if remainder:
        top.append(("Outras", remainder))
    colors = [BLUE, VIOLET, ICE, "#536DAE", "#A0ADC7", LINE]
    if not total:
        s += text(left, lang_y + 50, "Nenhuma linguagem pública disponível.", 16, MUTED)
    else:
        bar_x, bar_width = left, width - 2 * left
        for i, (_, count) in enumerate(top):
            segment = count / total * bar_width
            s += rect(round(bar_x, 3), lang_y + 34, round(segment, 3), 8, colors[i])
            bar_x += segment
        for i, (label, count) in enumerate(top):
            x = left if mobile else left + (i % 3) * 300
            y = lang_y + 82 + i * 30 if mobile else lang_y + 82 + (i // 3) * 31
            s += rect(x, y - 10, 7, 7, colors[i])
            s += text(x + 17, y, f"{label}  {100 * count / total:.1f}%", 17 if mobile else 16, MUTED)
    cal_y = 560 if mobile else 326
    s += pixel(left, cal_y, "CONTRIBUTIONS", 1.8, ICE)
    weeks = data["calendar"]["weeks"]
    pitch = (width - 2 * left) / max(len(weeks), 1)
    square = max(2, pitch - 2)
    level_colors = {"NONE": "#17233B", "FIRST_QUARTILE": "#253D79", "SECOND_QUARTILE": BLUE,
                    "THIRD_QUARTILE": VIOLET, "FOURTH_QUARTILE": ICE}
    for w, week in enumerate(weeks):
        for day in week["contributionDays"]:
            x, y = left + w * pitch, cal_y + 32 + day["weekday"] * (square + 2)
            cell = rect(round(x, 2), round(y, 2), round(square, 2), round(square, 2),
                        level_colors[day["contributionLevel"]])
            s += cell[:-2] + f'><title>{day["date"]}: {day["contributionCount"]} contribuições</title></rect>'
    footer = height - 22
    date = data["fetched_at"][:10].split("-")
    date_label = "/".join(reversed(date))
    s += text(left, footer, f"GitHub API · atualizado em {date_label}", 12, MUTED)
    if not mobile:
        s += text(width-left, footer, "Linguagens por bytes de código público", 12, MUTED, 'text-anchor="end"')
    desc = "; ".join(f"{label}: {value}" for value, label in metrics)
    return svg(s, height, f"Exploration log — {data['username']}", desc, width)


def validate(data):
    for key in ["public_repositories", "public_original_stars", "followers"]:
        if not isinstance(data[key], int) or data[key] < 0:
            raise ValueError(f"Invalid statistic: {key}")
    days = [d for w in data["calendar"]["weeks"] for d in w["contributionDays"]]
    if not days or sum(d["contributionCount"] for d in days) != data["calendar"]["totalContributions"]:
        raise ValueError("Contribution calendar total does not match its days.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cached", action="store_true", help="Render the last valid snapshot without network access.")
    args = parser.parse_args()
    profile = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
    snapshot = ROOT / "assets" / "github-data.json"
    data = json.loads(snapshot.read_text(encoding="utf-8")) if args.cached else github(profile["username"])
    validate(data)
    # Build and validate everything before replacing the previous good result.
    from xml.etree import ElementTree
    outputs = {"github-stats.svg": render(data), "github-stats-mobile.svg": render(data, True)}
    for content in outputs.values():
        ElementTree.fromstring(content)
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    if not args.cached:
        snapshot.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for name, content in outputs.items():
        (snapshot.parent / name).write_text(content, encoding="utf-8")
    print(f"Updated real GitHub statistics for {data['username']}.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
