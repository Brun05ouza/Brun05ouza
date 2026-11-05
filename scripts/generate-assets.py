"""Generate original README art with Python's standard library."""
import json
import textwrap
from pathlib import Path
from art import BG, BLUE, ICE, LINE, MUTED, VIOLET, WHITE
from art import astronaut, pixel, planet, rect, stars, svg, text, trail, walking

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def save(name, content):
    target = ASSETS / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def hero():
    s = stars()
    s += rect(40, 34, 24, 3, BLUE)
    s += pixel(76, 30, "BRUNO UNIVERSE", 1.5, ICE)
    s += text(920, 41, "A DEVELOPER'S JOURNEY", 11, MUTED, 'text-anchor="end" letter-spacing="1.2"')
    s += astronaut(64, 132, 3.5)
    s += pixel(242, 113, "BRUNO", 7)
    s += pixel(242, 178, "SOUZA", 7)
    s += text(244, 260, "Creative Developer", 23, ICE)
    s += text(244, 292, "Full Stack  /  UI & Motion", 19, MUTED)
    s += planet(788, 101, 4)
    # The trail starts under Bruno's boots, reaches the right edge, and continues below.
    s += f'<path d="M128 322h42v18h750v52" fill="none" stroke="{LINE}" stroke-width="2" stroke-dasharray="4 8"/>'
    s += rect(124, 318, 8, 8, BLUE)
    s += pixel(40, 360, "PRESS START", 1.6, ICE)
    s += text(920, 367, "CÓDIGO, DESIGN E MOVIMENTO.", 11, MUTED, 'text-anchor="end" letter-spacing="1"')
    return svg(s, 392, "Bruno Souza — Creative Developer",
               "Bruno Universe. Astronauta loiro de olhos azuis e traje azul e branco, com a letra B no peito, inicia uma jornada espacial. Full Stack, UI e Motion.")


def hero_mobile():
    s = rect(24, 27, 18, 3, BLUE) + pixel(54, 24, "BRUNO UNIVERSE", 1.5, ICE)
    s += astronaut(28, 104, 3.3)
    s += pixel(174, 113, "BRUNO", 6) + pixel(174, 174, "SOUZA", 6)
    s += text(28, 302, "Creative Developer", 24, ICE)
    s += text(28, 338, "Full Stack / UI & Motion", 20, MUTED)
    s += planet(384, 60, 2)
    s += trail(376, 28, 452) + pixel(28, 402, "PRESS START", 1.7, ICE)
    return svg(s, 448, "Bruno Souza — Creative Developer", "Astronauta loiro de olhos azuis. Full Stack, UI e Motion.", width=480)


def section(label, position, pose="walk", mobile=False):
    width = 480 if mobile else 960
    s = pixel(32 if mobile else 40, 30 if mobile else 38, "> " + label, 2.5)
    s += trail(122, 0, width)
    s += (walking(position, 56, 1.5) if pose == "walk" else astronaut(position, 56, 1.5, pose))
    if pose == "sit":
        sx = position + 55
        s += rect(sx, 72, 46, 32, LINE) + rect(sx+3, 75, 40, 26, ICE)
        s += rect(sx+6, 78, 34, 20, BG) + pixel(sx+10, 83, ">", 1, ICE)
        s += rect(sx+20, 91, 8, 2, BLUE) + rect(sx+19, 104, 8, 11, LINE)
        s += rect(sx+9, 115, 29, 3, LINE) + rect(sx-2, 119, 52, 3, VIOLET)
    return svg(s, 144, label, "Bruno continua sua jornada em pixel art.", width)


def about(profile, mobile=False):
    width, margin, size = (480, 32, 22) if mobile else (960, 40, 20)
    lines = textwrap.wrap(profile["about"], 34 if mobile else 78)
    s = pixel(margin, 34, "> ABOUT", 2.5)
    for i, line in enumerate(lines):
        s += text(margin, 110 + i * 32, line, size, ICE if i == 0 else WHITE)
    metadata_y = 110 + (len(lines) - 1) * 32 + 48
    s += rect(margin, metadata_y - 10, 5, 5, BLUE)
    s += text(margin + 17, metadata_y, profile["location"], 19 if mobile else 17, ICE)
    if mobile:
        for i, line in enumerate(textwrap.wrap(profile["education"], 34)):
            s += text(margin, metadata_y + 34 + i * 28, line, 19, MUTED)
        last_line = metadata_y + 34 + i * 28
    else:
        s += text(320, metadata_y, profile["education"], 17, MUTED)
        last_line = metadata_y
    height = last_line + 110
    s += trail(height - 20, 0, width)
    s += walking(325 if mobile else 810, height - 86, 1.5)
    alt = f'{profile["about"]} {profile["location"]}. {profile["education"]}.'
    return svg(s, height, "About — Bruno Souza", alt, width)


def icon(kind, x, y):
    if kind == 0:
        p = '<path d="m8 0-8 8 8 8M22 0l8 8-8 8M18-2l-6 20" fill="none" stroke="#A8D4FF" stroke-width="3"/>'
    elif kind == 1:
        p = rect(0, 0, 28, 6, ICE) + rect(0, 9, 28, 6, VIOLET) + rect(0, 18, 28, 6, BLUE)
    elif kind == 2:
        p = '<path d="M0 20h6V10h6v6h6V0h6v8h6" fill="none" stroke="#A8D4FF" stroke-width="3"/>'
    else:
        p = rect(5, 0, 18, 28, ICE) + rect(8, 4, 12, 18, BG) + rect(12, 24, 4, 2, BLUE)
    return f'<g transform="translate({x} {y})" shape-rendering="crispEdges">{p}</g>'


def skill_scenes(profile):
    for mobile in [False, True]:
        width, height = (480, 780) if mobile else (960, 428)
        s = pixel(32 if mobile else 40, 32, "> SKILLS", 2.5)
        for i, (label, tech) in enumerate(profile["skills"].items()):
            x = 32 if mobile else 40 + (i % 2) * 468
            y = 106 + i * 148 if mobile else 106 + (i // 2) * 132
            s += icon(i, x, y - 18)
            s += text(x + 46, y, label, 23 if mobile else 21, WHITE)
            for j, line in enumerate(textwrap.wrap(" · ".join(tech), 34 if mobile else 38)):
                s += text(x, y + 37 + j * 28, line, 18 if mobile else 17, MUTED)
        baseline = height - 18
        s += trail(baseline, 0, width)
        s += rect(width // 2 - 55, baseline - 4, 112, 4, BLUE)
        s += walking(width // 2 - 25, baseline - 66, 1.5)
        save("skills-mobile.svg" if mobile else "skills.svg", svg(s, height, "Skills — tecnologias", "; ".join(f'{k}: {", ".join(v)}' for k,v in profile["skills"].items()), width))


def mission_scenes(profile):
    for n, project in enumerate(profile["projects"], 1):
        for mobile in [False, True]:
            width, height = (480, 244) if mobile else (960, 164)
            s = pixel(28 if mobile else 40, 28, f"0{n}", 2.3, VIOLET)
            x = 28 if mobile else 112
            y = 80 if mobile else 43
            s += text(x, y, project["name"], 25 if mobile else 24)
            if project.get("personal"):
                s += text(x, y + 28, "PROJETO PESSOAL", 12, ICE, 'letter-spacing="1"')
                y += 29
            description_lines = textwrap.wrap(project["description"], 41 if mobile else 86)
            for j, line in enumerate(description_lines):
                s += text(x, y + 36 + j * 27, line, 18 if mobile else 17, MUTED)
            if project.get("technologies"):
                tech_y = y + 36 + (len(description_lines) - 1) * 27 + 31
                tech_lines = textwrap.wrap(" · ".join(project["technologies"]), 40 if mobile else 90)
                for j, line in enumerate(tech_lines):
                    s += text(x, tech_y + j * 24, line, 16 if mobile else 15, ICE)
                height = max(height, tech_y + (len(tech_lines) - 1) * 24 + 65)
            s += text(width - 28, height - 26, "EXPLORAR >", 12, ICE, 'text-anchor="end" letter-spacing="1"')
            s += trail(height - 9, 0, width)
            if n == 3:
                s += walking(width - 196, height - 75, 1.5)
            save(f'missions/{n:02d}{"-mobile" if mobile else ""}.svg', svg(s, height, project["name"], project["description"], width))


def contact(mobile=False):
    width, height = (480, 312) if mobile else (960, 248)
    s = pixel(32 if mobile else 40, 34, "> CONTINUE?", 2.5)
    lines = ["Tem uma ideia interessante?", "Vamos transformar isso em algo real."]
    for i, line in enumerate(lines):
        s += text(32 if mobile else 40, 105 + 32 * i, line, 20 if mobile else 21, ICE if i == 0 else MUTED)
    portal_x, portal_y = (374 if mobile else 860), height - 126
    s += trail(height - 54, 0, width)
    s += astronaut(portal_x - 70, height - 133, 1.8)
    portal = ('<path d="M4 0h12v2h4v4h2v24h-2v4h-4v2H4v-2H0v-4h-2V6h2V2h4z" fill="#253452"/>'
              '<path d="M4 2h12v2h2v4h2v20h-2v4h-2v2H4v-2H2v-4H0V8h2V4h2z" fill="#7775FF"/>'
              '<path d="M6 5h8v2h2v4h1v14h-1v4h-2v2H6v-2H4v-4H3V11h1V7h2z" fill="#0B1020"/>'
              '<g class="star"><path d="M8 8h4v4h2v12h-2v4H8v-4H6V12h2z" fill="#2563FF"/>'
              '<path d="M9 12h2v12H9z" fill="#A8D4FF"/></g>')
    s += f'<g transform="translate({portal_x} {portal_y}) scale(2)" shape-rendering="crispEdges">{portal}</g>'
    s += pixel(32 if mobile else 40, height - 27, "MISSION COMPLETE", 1.6, ICE)
    if not mobile:
        s += pixel(626, height - 27, "READY FOR THE NEXT ONE.", 1.6, MUTED)
    return svg(s, height, "Continue? — Vamos criar algo juntos", "Bruno chega a um portal espacial. Mission complete — ready for the next one.", width)


def picture(name, alt, link=None):
    from html import escape
    tag = (f'<picture>\n  <source media="(max-width: 600px)" srcset="assets/{name}-mobile.svg">\n'
           f'  <img src="assets/{name}.svg" width="100%" alt="{escape(alt, quote=True)}">\n</picture>')
    return f'<a href="{escape(link, quote=True)}">\n{tag}\n</a>' if link else tag


def readme(profile):
    parts = ["<!-- Generated by scripts/generate-assets.py. Edit profile.json and the generator. -->",
             picture("hero", profile["name"] + " — " + profile["headline"], profile["portfolio"]),
             navigation(profile),
             picture("about", f'{profile["about"]} {profile["location"]}. {profile["education"]}.'),
             picture("skills", "; ".join(f'{k}: {", ".join(v)}' for k,v in profile["skills"].items())),
             picture("missions", "Missions — seis projetos para explorar")]
    for n, p in enumerate(profile["projects"], 1):
        alt = p["name"] + (" — projeto pessoal" if p.get("personal") else "") + ". " + p["description"]
        parts.append(picture(f"missions/{n:02d}", alt, p["url"]))
    parts += [picture("log", "Exploration log — atividade no GitHub"),
              picture("github-stats", "Estatísticas reais do GitHub: repositórios públicos, estrelas, contribuições e linguagens."),
              navigation(profile, statistics=True),
              picture("contact", "Continue? Tem uma ideia interessante? Vamos transformar isso em algo real."),
              navigation(profile)]
    (ROOT / "README.md").write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def character_sheet():
    s = pixel(36, 30, "MEET BRUNO", 2.5)
    s += text(36, 78, "O mesmo explorador. Cada etapa da jornada.", 16, MUTED)
    poses = [(52, "IDLE", "idle", 0), (252, "WALK 01", "walk", 0),
             (440, "WALK 02", "walk", 1), (628, "WALK 03", "walk", 2),
             (816, "WALK 04", "walk", 3)]
    for x, label, pose, frame in poses:
        s += astronaut(x, 114, 2.7, pose, frame)
        s += pixel(x, 258, label, 1.5, ICE)
    s += trail(298, 36, 920)
    s += astronaut(68, 324, 3, "sit")
    s += text(244, 362, "Loiro. Olhos azuis. Traje azul e branco.", 21, WHITE)
    s += text(244, 399, "Capacete em pixels, sorriso e uma pequena letra B.", 17, MUTED)
    s += text(244, 431, "Quatro quadros de caminhada; uma identidade em todas as cenas.", 16, MUTED)
    return svg(s, 492, "Bruno — sprites originais", "Pose inicial, quatro quadros de caminhada e pose sentado.")


def buttons():
    # Links belong to the surrounding Markdown anchors, never inside SVG images.
    for name, label in [("portfolio", "PORTFOLIO"), ("github", "GITHUB"),
                        ("linkedin", "LINKEDIN"), ("email", "E-MAIL"),
                        ("repositories", "REPOS"), ("statistics", "DADOS")]:
        w, h, unit = 156, 52, 1.8
        content = (f'<path d="M4 1h148v3h3v44h-3v3H4v-3H1V4h3z" '
                   f'fill="{BG}" stroke="{LINE}" stroke-width="2" shape-rendering="crispEdges"/>')
        label_w = (len(label) * 6 - 1) * unit
        content += pixel((w - label_w) / 2, 20, label, unit, ICE)
        content += rect(12, 12, 3, 3, BLUE)
        save(f"links/{name}.svg", svg(content, h, label, width=w))


def navigation(profile, statistics=False):
    from html import escape
    links = [
        ("portfolio", profile["portfolio"], "Visitar meu portfólio"),
        ("github", f'https://github.com/{profile["username"]}', "Meu perfil no GitHub"),
        ("linkedin", profile["linkedin"], "Conectar no LinkedIn"),
        ("email", f'mailto:{profile["email"]}', "Conversar por e-mail"),
    ]
    if statistics:
        links = [("repositories", f'https://github.com/{profile["username"]}?tab=repositories', "Explorar meus repositórios"),
                 ("statistics", "docs/maintenance.md#estatísticas", "Como as estatísticas são calculadas")]
    anchors = [f'<a href="{escape(url, quote=True)}"><img src="assets/links/{name}.svg" width="156" height="52" alt="{escape(label, quote=True)}"></a>'
               for name, url, label in links]
    return '<p align="center">\n  ' + '\n  '.join(anchors) + '\n</p>'


def main():
    profile = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
    save("hero.svg", hero())
    save("hero-mobile.svg", hero_mobile())
    save("character/sheet.svg", character_sheet())
    for pose in ["idle", "walk", "sit"]:
        content = walking(8, 8, 4) if pose == "walk" else astronaut(8, 8, 4, pose)
        save(f"character/{pose}.svg", svg(content, 192, f"Bruno — {pose}", width=144))
    buttons()
    save("about.svg", about(profile))
    save("about-mobile.svg", about(profile, mobile=True))
    save("missions.svg", section("MISSIONS", 630))
    save("missions-mobile.svg", section("MISSIONS", 280, mobile=True))
    save("log.svg", section("EXPLORATION LOG", 810, "sit"))
    save("log-mobile.svg", section("EXPLORATION LOG", 280, "sit", mobile=True))
    skill_scenes(profile)
    mission_scenes(profile)
    save("contact.svg", contact())
    save("contact-mobile.svg", contact(True))
    readme(profile)
    print("Generated README and all original scene/character assets.")


if __name__ == "__main__":
    main()
