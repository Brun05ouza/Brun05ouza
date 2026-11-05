"""Original vector art shared by every scene. No external fonts or images."""
from html import escape

BG = "#0B1020"
BLUE = "#2563FF"
VIOLET = "#7775FF"
ICE = "#A8D4FF"
WHITE = "#F8FAFF"
MUTED = "#A0ADC7"
LINE = "#253452"

# A deliberately small, original 5×7 alphabet, emitted as SVG paths.
FONT = {
    "A": "01110/10001/10001/11111/10001/10001/10001",
    "B": "11110/10001/10001/11110/10001/10001/11110",
    "C": "01111/10000/10000/10000/10000/10000/01111",
    "D": "11110/10001/10001/10001/10001/10001/11110",
    "E": "11111/10000/10000/11110/10000/10000/11111",
    "F": "11111/10000/10000/11110/10000/10000/10000",
    "G": "01111/10000/10000/10111/10001/10001/01111",
    "H": "10001/10001/10001/11111/10001/10001/10001",
    "I": "11111/00100/00100/00100/00100/00100/11111",
    "J": "00111/00010/00010/00010/10010/10010/01100",
    "K": "10001/10010/10100/11000/10100/10010/10001",
    "L": "10000/10000/10000/10000/10000/10000/11111",
    "M": "10001/11011/10101/10101/10001/10001/10001",
    "N": "10001/11001/11001/10101/10011/10011/10001",
    "O": "01110/10001/10001/10001/10001/10001/01110",
    "P": "11110/10001/10001/11110/10000/10000/10000",
    "Q": "01110/10001/10001/10001/10101/10010/01101",
    "R": "11110/10001/10001/11110/10100/10010/10001",
    "S": "01111/10000/10000/01110/00001/00001/11110",
    "T": "11111/00100/00100/00100/00100/00100/00100",
    "U": "10001/10001/10001/10001/10001/10001/01110",
    "V": "10001/10001/10001/10001/10001/01010/00100",
    "W": "10001/10001/10001/10101/10101/11011/10001",
    "X": "10001/10001/01010/00100/01010/10001/10001",
    "Y": "10001/10001/01010/00100/00100/00100/00100",
    "Z": "11111/00001/00010/00100/01000/10000/11111",
    "0": "01110/10001/10011/10101/11001/10001/01110",
    "1": "00100/01100/00100/00100/00100/00100/01110",
    "2": "01110/10001/00001/00010/00100/01000/11111",
    "3": "11110/00001/00001/01110/00001/00001/11110",
    "4": "00010/00110/01010/10010/11111/00010/00010",
    "5": "11111/10000/10000/11110/00001/00001/11110",
    "6": "01110/10000/10000/11110/10001/10001/01110",
    "7": "11111/00001/00010/00100/01000/01000/01000",
    "8": "01110/10001/10001/01110/10001/10001/01110",
    "9": "01110/10001/10001/01111/00001/00001/01110",
    ">": "10000/01000/00100/00010/00100/01000/10000",
    "-": "00000/00000/00000/11111/00000/00000/00000",
    ".": "00000/00000/00000/00000/00000/00110/00110",
    "/": "00001/00001/00010/00100/01000/10000/10000",
    "?": "01110/10001/00001/00010/00100/00000/00100",
    " ": "00000/00000/00000/00000/00000/00000/00000",
}


def rect(x, y, w, h, color, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" {extra}/>'


def text(x, y, value, size=18, color=WHITE, extra=""):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-family="Verdana,DejaVu Sans,sans-serif" {extra}>{escape(str(value))}</text>')


def pixel(x, y, value, unit=2, color=WHITE):
    path = []
    for i, char in enumerate(value.upper()):
        for row, bits in enumerate(FONT[char].split("/")):
            for col, bit in enumerate(bits):
                if bit == "1":
                    px, py = x + (i * 6 + col) * unit, y + row * unit
                    path.append(f'M{px:g} {py:g}h{unit:g}v{unit:g}h-{unit:g}z')
    return f'<path fill="{color}" d="{"".join(path)}" shape-rendering="crispEdges"/>'


STYLE = """
@keyframes float {0%,100% {transform:translateY(0)} 50% {transform:translateY(-4px)}}
@keyframes breathe {0%,100% {transform:translateY(0)} 50% {transform:translateY(-1px)}}
@keyframes twinkle {0%,100% {opacity:.4} 50% {opacity:.9}}
@keyframes frame0 {0%,24.999% {opacity:1} 25%,100% {opacity:0}}
@keyframes frame1 {0%,24.999% {opacity:0} 25%,49.999% {opacity:1} 50%,100% {opacity:0}}
@keyframes frame2 {0%,49.999% {opacity:0} 50%,74.999% {opacity:1} 75%,100% {opacity:0}}
@keyframes frame3 {0%,74.999% {opacity:0} 75%,99.999% {opacity:1} 100% {opacity:0}}
.planet {animation:float 7s cubic-bezier(.77,0,.175,1) infinite}
.idle {animation:breathe 4s cubic-bezier(.77,0,.175,1) infinite}
.star {animation:twinkle 8s cubic-bezier(.77,0,.175,1) infinite}
.frame {opacity:0;animation-duration:.8s;animation-timing-function:steps(1,end);animation-iteration-count:infinite}
.f0 {opacity:1;animation-name:frame0}.f1 {animation-name:frame1}
.f2 {animation-name:frame2}.f3 {animation-name:frame3}
@media (prefers-reduced-motion:reduce) {
 .planet,.idle,.star,.frame {animation:none}
 .star {opacity:.7}.frame {opacity:0}.f0 {opacity:1}
}
"""


def svg(content, height, title, desc="", width=960):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>'
            f'<style>{STYLE}</style>{rect(0, 0, width, height, BG)}{content}</svg>\n')


def astronaut(x=0, y=0, scale=1, pose="idle", frame=0):
    """32×44 pixel master; shared head guarantees identity between poses."""
    s = []
    r = lambda *args: s.append(rect(*args))
    # Backpack, collar, torso. Dark pixels isolate the silhouette.
    r(2, 25, 8, 13, LINE); r(3, 26, 5, 9, BLUE); r(3, 27, 2, 4, ICE)
    r(8, 23, 19, 15, LINE); r(9, 24, 17, 12, BLUE)
    r(10, 24, 14, 3, WHITE); r(12, 27, 12, 7, WHITE)
    s.append(pixel(16, 27, "B", 1, BLUE))
    r(10, 35, 15, 2, ICE); r(16, 35, 3, 2, WHITE)
    # Gloves and boots each use genuinely distinct positions in the walk cycle.
    arm_offset = [0, -2, 0, 2][frame]
    if pose == "sit":
        r(24, 27, 6, 4, BLUE); r(28, 27, 4, 3, WHITE)
        r(9, 37, 10, 4, BLUE); r(17, 38, 7, 3, WHITE)
        r(20, 36, 10, 4, BLUE); r(27, 37, 4, 5, WHITE)
        r(8, 40, 3, 4, LINE)
    else:
        r(6, 26 - arm_offset, 4, 8, BLUE); r(6, 33 - arm_offset, 4, 4, WHITE)
        r(25, 26 + arm_offset, 4, 8, BLUE); r(25, 33 + arm_offset, 4, 4, WHITE)
        legs = [(10, 37, 7, 5), (20, 37, 7, 5)]
        if pose == "walk":
            legs = [[(8, 37, 7, 5), (22, 35, 7, 5)],
                    [(12, 37, 7, 5), (19, 37, 7, 5)],
                    [(10, 35, 7, 5), (22, 37, 7, 5)],
                    [(12, 37, 7, 5), (19, 37, 7, 5)]][frame]
        for lx, ly, lw, lh in legs:
            r(lx, ly, lw, lh, BLUE); r(lx - 1, ly + lh - 1, lw + 2, 2, LINE)
            r(lx, ly + lh - 2, lw + 1, 2, WHITE)
    # Stepped helmet outline; never rounded rectangles or vector ellipses.
    s.append('<path fill="#253452" d="M10 0h14v2h5v4h3v14h-3v4h-5v2H10v-2H5v-4H2V6h3V2h5z"/>')
    s.append('<path fill="#F8FAFF" d="M10 1h14v2h4v4h3v12h-3v4h-4v2H10v-2H6v-4H3V7h3V3h4z"/>')
    r(5, 8, 2, 11, ICE); r(7, 19, 20, 3, ICE)
    s.append('<path fill="#182A4A" d="M11 4h13v2h3v3h2v8h-2v3H10v-2H8V8h3z"/>')
    # Blonde hair with a stepped fringe, bright blue irises, warm skin.
    r(12, 8, 13, 10, "#F0C4A0"); r(14, 18, 9, 2, "#F0C4A0")
    r(12, 6, 11, 3, "#D69E3A"); r(11, 8, 14, 3, "#EAC05A")
    r(12, 7, 8, 2, "#F6D77D"); r(11, 10, 2, 4, "#D69E3A")
    r(18, 9, 3, 2, "#F6D77D"); r(23, 9, 2, 3, "#D69E3A")
    r(14, 12, 3, 3, WHITE); r(21, 12, 3, 3, WHITE)
    r(15, 12, 2, 3, "#398BFF"); r(22, 12, 2, 3, "#398BFF")
    r(16, 13, 1, 1, "#182A4A"); r(23, 13, 1, 1, "#182A4A")
    r(18, 16, 4, 1, "#965D49"); r(19, 17, 2, 1, "#965D49")
    r(8, 7, 2, 5, ICE); r(10, 5, 5, 1, ICE)
    r(28, 11, 3, 5, BLUE); r(29, 12, 1, 2, ICE)
    cls = ' class="idle"' if pose == "idle" else ""
    return (f'<g transform="translate({x} {y}) scale({scale})" shape-rendering="crispEdges">'
            f'<g{cls}>{"".join(s)}</g></g>')


def walking(x, y, scale):
    return ''.join(f'<g class="frame f{i}">{astronaut(x,y,scale,"walk",i)}</g>' for i in range(4))


def planet(x, y, unit=4):
    p = ('<path fill="#7775FF" d="M8 0h8v1h3v2h2v3h1v8h-1v3h-2v2h-3v1H8v-1H5v-2H3v-3H2V6h1V3h2V1h3z"/>'
         '<path fill="#A8D4FF" d="M8 1h7v1H9v2H6v3H4V6h1V4h1V2h2z"/>'
         '<path fill="#494A9E" d="M19 5h2v9h-1v3h-2v2h-3v1H8v-1h6v-2h3v-3h2z"/>'
         '<path fill="#5259BB" d="M8 7h4v2h3v3h-4v-2H8zM17 3h2v3h-3V5h1z"/>'
         '<path fill="#A8D4FF" d="M0 12h5v-1h5v-1h6V9h6V8h4v2h-4v1h-5v1h-6v1H6v1H0z"/>'
         '<path fill="#0B1020" d="M0 14h6v1H0zM22 6h4v2h-2V7h-2z"/>')
    return f'<g transform="translate({x} {y}) scale({unit})"><g class="planet" shape-rendering="crispEdges">{p}</g></g>'


def stars():
    return (rect(56, 58, 3, 3, ICE) + rect(178, 96, 3, 3, VIOLET) +
            rect(720, 60, 3, 3, ICE) + rect(886, 260, 3, 3, ICE) +
            '<g class="star">' + rect(802, 246, 6, 2, VIOLET) +
            rect(804, 244, 2, 6, VIOLET) + '</g>')


def trail(y, start=0, end=960):
    return f'<path d="M{start} {y}H{end}" fill="none" stroke="{LINE}" stroke-width="2" stroke-dasharray="4 8"/>'
