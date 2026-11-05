"""Local visual QA; optional dependency: playwright and installed Microsoft Edge."""
from html import escape
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".preview"


def main():
    OUT.mkdir(exist_ok=True)
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    # Keep images, native paragraphs and anchors; minimal Markdown rendering for QA.
    import re
    body = readme.replace('src="assets/', 'src="../assets/').replace('srcset="assets/', 'srcset="../assets/')
    body = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', body)
    body = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', body)
    body = '\n'.join(f'<p>{block}</p>' if not block.lstrip().startswith('<') else block for block in body.split('\n\n'))
    page_source = f'''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bruno Universe — preview local</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#0d1117;color:#d1d9e0;font:16px/1.65 Verdana,sans-serif}}
main{{max-width:1026px;margin:32px auto;padding:32px;border:1px solid #30363d;border-radius:6px}}
a{{color:#a8d4ff;text-decoration:none}}p{{margin:16px 0 24px}}img{{max-width:100%;height:auto}}picture{{display:block}}picture>img{{display:block;width:100%}}p[align="center"]{{text-align:center;line-height:1;margin:16px 0 32px}}p[align="center"] a{{display:inline-block;margin:0 0 4px}}a:focus-visible{{outline:2px solid #7775ff;outline-offset:4px}}
@media(max-width:600px){{main{{margin:0;padding:40px;border:0}}body{{font-size:15px}}}}
</style><main>{body}</main></html>'''
    (OUT / "index.html").write_text(page_source, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        page = browser.new_page(viewport={"width": 1100, "height": 900}, device_scale_factor=1)
        page.goto((OUT / "index.html").as_uri())
        page.wait_for_function('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)')
        page.screenshot(path=str(OUT / "desktop.png"), full_page=True)
        page.locator('img[src$="hero.svg"]').screenshot(path=str(OUT / "hero.png"))
        for scene in ["skills", "contact", "github-stats"]:
            page.locator(f'img[src$="{scene}.svg"]').screenshot(path=str(OUT / f"{scene}.png"))
        page.goto((ROOT / "assets/character/sheet.svg").as_uri())
        page.locator("svg").screenshot(path=str(OUT / "character.png"))
        page.set_viewport_size({"width": 390, "height": 844})
        page.goto((OUT / "index.html").as_uri())
        page.wait_for_function('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)')
        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'), 'Mobile page overflows'
        assert page.locator('img[src$="hero.svg"]').evaluate('i=>i.currentSrc.endsWith("hero-mobile.svg")')
        page.screenshot(path=str(OUT / "mobile.png"), full_page=True)
        page.locator('img[src$="hero.svg"]').screenshot(path=str(OUT / "hero-mobile.png"))
        page.locator('img[src$="github-stats.svg"]').screenshot(path=str(OUT / "stats-mobile.png"))
        page.emulate_media(reduced_motion="reduce")
        page.screenshot(path=str(OUT / "reduced-motion.png"), full_page=True)
        page.goto((ROOT / "assets/character/walk.svg").as_uri())
        assert page.locator(".f0").evaluate('e=>getComputedStyle(e).opacity') == "1"
        for i in [1, 2, 3]:
            assert page.locator(f".f{i}").evaluate('e=>getComputedStyle(e).opacity') == "0"
        assert page.locator(".f0").evaluate('e=>getComputedStyle(e).animationName') == "none"
        page.emulate_media(reduced_motion="no-preference")
        frames = []
        for i in range(4):
            page.locator("svg").evaluate('''(s,i)=>s.querySelectorAll('.frame').forEach(e=>{e.style.animationPlayState='paused';e.style.animationDelay=`-${i*.2+.05}s`})''', i)
            page.locator("svg").screenshot(path=str(OUT / f"walk-{i}.png"))
            frames.append(page.locator(".frame").evaluate_all('es=>es.map(e=>getComputedStyle(e).opacity)'))
        assert frames == [["1","0","0","0"],["0","1","0","0"],["0","0","1","0"],["0","0","0","1"]], frames
        browser.close()
    print("Desktop, mobile, reduced-motion and all four animation frames passed. Previews: .preview/")


if __name__ == "__main__":
    main()
