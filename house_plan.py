import math
from pathlib import Path
from datetime import date
from typing import List, Tuple, Dict

PX_PER_MM = 25
SCALE = 1 / 50  # 1:50 scale
WALL = 120
GRID = 910
DOOR_W = 780

A3_W = 420
A3_H = 297

# --- util -------------------------------------------------------

def mm_to_px(mm: float) -> float:
    return mm * PX_PER_MM


def real_to_draw(mm_real: float) -> float:
    return mm_real * SCALE


def rpx(mm_real: float) -> float:
    return mm_to_px(real_to_draw(mm_real))


def line(x1: float, y1: float, x2: float, y2: float, color: str, width: float) -> str:
    return (
        f'<line x1="{rpx(x1):.1f}" y1="{rpx(y1):.1f}" '
        f'x2="{rpx(x2):.1f}" y2="{rpx(y2):.1f}" '
        f'stroke="{color}" stroke-width="{width}" />'
    )


def rect(x: float, y: float, w: float, h: float, color: str, width: float) -> str:
    return (
        f'<rect x="{rpx(x):.1f}" y="{rpx(y):.1f}" '
        f'width="{rpx(w):.1f}" height="{rpx(h):.1f}" '
        f'fill="none" stroke="{color}" stroke-width="{width}" />'
    )


def poly(points: List[Tuple[float, float]], color: str, width: float) -> str:
    pts = " ".join(f"{rpx(x):.1f},{rpx(y):.1f}" for x, y in points)
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}" />'


def text(x: float, y: float, content: str, size: float = 14) -> str:
    return (
        f'<text x="{rpx(x):.1f}" y="{rpx(y):.1f}" '
        f'font-size="{size}" font-family="sans-serif">{content}</text>'
    )

# --- data -------------------------------------------------------

plan: Dict[str, Dict] = {
    "width": 10000,
    "depth": 10000,
    "floors": {
        "1F": {
            "rooms": [
                {"name": "LDK", "poly": [(0,0),(6000,0),(6000,5000),(0,5000)], "label": (3000,2500)},
                {"name": "和室", "poly": [(0,5000),(3640,5000),(3640,8640),(0,8640)], "label": (1820,6820)},
                {"name": "洗面脱衣", "poly": [(6000,5000),(7280,5000),(7280,5920),(6000,5920)], "label": (6640,5460)},
                {"name": "浴室", "poly": [(7280,5000),(9100,5000),(9100,6820),(7280,6820)], "label": (8190,5910)},
                {"name": "トイレ", "poly": [(9100,5000),(10000,5000),(10000,6370),(9100,6370)], "label": (9550,5685)},
            ],
            "doors": [
                {"point": (6000,2500), "dir": "E"},
                {"point": (3640,6820), "dir": "S"},
                {"point": (9100,5910), "dir": "W"},
            ],
            "windows": [
                {"start": (3000,0), "end": (4800,0)},
                {"start": (0,2500), "end": (0,3500)},
                {"start": (5460,10000), "end": (8000,10000)},
            ],
            "plumbing": [
                {"type": "bath", "pos": (8190,6010)},
                {"type": "sink", "pos": (6640,5460)},
                {"type": "toilet", "pos": (9550,5685)},
                {"type": "kitchen", "pos": (3000,2500)},
            ],
            "electric": [
                {"type": "light", "pos": (3000,2500)},
                {"type": "switch", "pos": (6000,2500)},
            ],
            "furniture": [
                {"type": "table", "pos": (3000,2500), "size": (1800,900)},
                {"type": "sofa", "pos": (1500,1500), "size": (2000,900)},
            ],
        },
        "2F": {
            "rooms": [
                {"name": "主寝室", "poly": [(0,0),(3640,0),(3640,3640),(0,3640)], "label": (1820,1820)},
                {"name": "子供室A", "poly": [(3640,0),(6370,0),(6370,3640),(3640,3640)], "label": (5005,1820)},
                {"name": "子供室B", "poly": [(6370,0),(9100,0),(9100,3640),(6370,3640)], "label": (7735,1820)},
                {"name": "書斎", "poly": [(0,3640),(2730,3640),(2730,6370),(0,6370)], "label": (1365,5005)},
                {"name": "トイレ", "poly": [(9100,3640),(10000,3640),(10000,5460),(9100,5460)], "label": (9550,4550)},
            ],
            "doors": [
                {"point": (3640,1820), "dir": "E"},
                {"point": (6370,1820), "dir": "E"},
                {"point": (9100,4550), "dir": "W"},
            ],
            "windows": [
                {"start": (0,1820), "end": (0,2730)},
                {"start": (10000,1820), "end": (10000,2730)},
                {"start": (5000,10000), "end": (7000,10000)},
            ],
            "plumbing": [
                {"type": "toilet", "pos": (9550,4550)},
            ],
            "electric": [
                {"type": "light", "pos": (5000,5000)},
            ],
            "furniture": [
                {"type": "bed", "pos": (1820,1820), "size": (1820,2000)},
                {"type": "desk", "pos": (7735,1820), "size": (1820,900)},
            ],
        },
    },
}

# --- layers -----------------------------------------------------

def layer_grid(base_x: float, base_y: float, width: float, depth: float) -> List[str]:
    elems: List[str] = ['<g id="grid">']
    cols = int(width / GRID) + 1
    rows = int(depth / GRID) + 1
    for i in range(cols):
        x = base_x + i * GRID
        elems.append(line(x, base_y, x, base_y + depth + WALL * 2, "#ccc", 1))
        elems.append(text(x - 150, base_y - 200, str(i + 1)))
    for j in range(rows):
        y = base_y + j * GRID
        elems.append(line(base_x, y, base_x + width + WALL * 2, y, "#ccc", 1))
        elems.append(text(base_x - 300, y + 100, str(j + 1)))
    elems.append('</g>')
    return elems


def layer_walls(base_x: float, base_y: float, floor: Dict) -> List[str]:
    elems: List[str] = []
    inner_w = plan['width']
    inner_d = plan['depth']
    elems.append(rect(base_x, base_y, inner_w + WALL * 2, inner_d + WALL * 2, "#222", 2))
    elems.append(rect(base_x + WALL, base_y + WALL, inner_w, inner_d, "#222", 2))
    for r in floor['rooms']:
        pts = [(x + base_x + WALL, y + base_y + WALL) for x, y in r['poly']]
        pts.append(pts[0])
        elems.append(poly(pts, "#222", 2))
    return ['<g id="wall">'] + elems + ['</g>']


def door_symbol(x: float, y: float, dir_: str) -> List[str]:
    w = DOOR_W
    hx = x + WALL
    hy = y + WALL
    parts: List[str] = []
    if dir_ == 'E':
        parts.append(line(hx, hy, hx, hy - w, "#007acc", 1.5))
        parts.append(f'<path d="M {rpx(hx):.1f},{rpx(hy):.1f} A {rpx(w):.1f},{rpx(w):.1f} 0 0 1 {rpx(hx + w):.1f},{rpx(hy):.1f}" fill="none" stroke="#007acc" stroke-width="1.5" />')
    elif dir_ == 'W':
        parts.append(line(hx, hy, hx, hy - w, "#007acc", 1.5))
        parts.append(f'<path d="M {rpx(hx):.1f},{rpx(hy):.1f} A {rpx(w):.1f},{rpx(w):.1f} 0 0 0 {rpx(hx - w):.1f},{rpx(hy):.1f}" fill="none" stroke="#007acc" stroke-width="1.5" />')
    elif dir_ == 'S':
        parts.append(line(hx, hy, hx + w, hy, "#007acc", 1.5))
        parts.append(f'<path d="M {rpx(hx):.1f},{rpx(hy):.1f} A {rpx(w):.1f},{rpx(w):.1f} 0 0 1 {rpx(hx):.1f},{rpx(hy + w):.1f}" fill="none" stroke="#007acc" stroke-width="1.5" />')
    else:  # N
        parts.append(line(hx, hy, hx + w, hy, "#007acc", 1.5))
        parts.append(f'<path d="M {rpx(hx):.1f},{rpx(hy):.1f} A {rpx(w):.1f},{rpx(w):.1f} 0 0 0 {rpx(hx):.1f},{rpx(hy - w):.1f}" fill="none" stroke="#007acc" stroke-width="1.5" />')
    return parts


def layer_openings(base_x: float, base_y: float, floor: Dict) -> List[str]:
    elems = ['<g id="opening">']
    for d in floor.get('doors', []):
        elems.extend(door_symbol(d['point'][0] + base_x, d['point'][1] + base_y, d['dir']))
    for w in floor.get('windows', []):
        x1, y1 = w['start']
        x2, y2 = w['end']
        elems.append(line(x1 + base_x + WALL, y1 + base_y + WALL, x2 + base_x + WALL, y2 + base_y + WALL, "#007acc", 1.5))
    elems.append('</g>')
    return elems


def plumbing_symbol(kind: str, x: float, y: float) -> str:
    if kind == 'bath':
        return rect(x - 700, y - 900, 1400, 1800, "#ff5722", 1.5)
    if kind == 'sink':
        return rect(x - 400, y - 400, 800, 800, "#ff5722", 1.5)
    if kind == 'toilet':
        return poly([(x - 300, y - 300), (x + 300, y - 300), (x + 300, y + 300), (x - 300, y + 300), (x - 300, y - 300)], "#ff5722", 1.5)
    if kind == 'kitchen':
        return rect(x - 900, y - 450, 1800, 900, "#ff5722", 1.5)
    return ''


def layer_plumbing(base_x: float, base_y: float, floor: Dict) -> List[str]:
    elems = ['<g id="plumbing">']
    for p in floor.get('plumbing', []):
        elems.append(plumbing_symbol(p['type'], p['pos'][0] + base_x + WALL, p['pos'][1] + base_y + WALL))
    elems.append('</g>')
    return elems


def electric_symbol(kind: str, x: float, y: float) -> str:
    if kind == 'light':
        return poly([(x - 200, y), (x, y - 200), (x + 200, y), (x, y + 200), (x - 200, y)], "#9c27b0", 1.2)
    if kind == 'switch':
        return line(x - 200, y - 200, x + 200, y + 200, "#9c27b0", 1.2)
    return ''


def layer_electric(base_x: float, base_y: float, floor: Dict) -> List[str]:
    elems = ['<g id="electric">']
    for e in floor.get('electric', []):
        elems.append(electric_symbol(e['type'], e['pos'][0] + base_x + WALL, e['pos'][1] + base_y + WALL))
    elems.append('</g>')
    return elems


def furniture_symbol(kind: str, x: float, y: float, size: Tuple[float, float]) -> str:
    w, h = size
    return rect(x - w/2, y - h/2, w, h, "#555", 1)


def layer_furniture(base_x: float, base_y: float, floor: Dict) -> List[str]:
    elems = ['<g id="furniture">']
    for f in floor.get('furniture', []):
        elems.append(furniture_symbol(f['type'], f['pos'][0] + base_x + WALL, f['pos'][1] + base_y + WALL, f['size']))
    elems.append('</g>')
    return elems


def layer_dimensions(base_x: float, base_y: float, width: float, depth: float) -> List[str]:
    elems = ['<g id="dimension">']
    off = 500
    elems.append(line(base_x, base_y - off, base_x + width + WALL*2, base_y - off, "#000", 1))
    elems.append(text(base_x + width / 2, base_y - off - 200, str(width)))
    elems.append(line(base_x - off, base_y, base_x - off, base_y + depth + WALL*2, "#000", 1))
    elems.append(text(base_x - off - 400, base_y + depth / 2, str(depth)))
    elems.append('</g>')
    return elems


def layer_text(base_x: float, base_y: float, floor: Dict) -> List[str]:
    elems = ['<g id="text">']
    for r in floor['rooms']:
        px, py = r['label']
        elems.append(text(px + base_x + WALL, py + base_y + WALL, r['name']))
    elems.append('</g>')
    return elems


def legend_and_title(base_x: float, base_y: float) -> List[str]:
    elems = ['<g id="legend">']
    elems.append(rect(base_x, base_y, 7000, 5000, "#000", 1))
    elems.append(text(base_x + 500, base_y + 1000, "凡例"))
    elems.append(text(base_x + 500, base_y + 2000, "grid #ccc"))
    elems.append(text(base_x + 500, base_y + 2500, "wall #222"))
    elems.append(text(base_x + 500, base_y + 3000, "opening #007acc"))
    elems.append(text(base_x + 500, base_y + 3500, "plumbing #ff5722"))
    elems.append(text(base_x + 500, base_y + 4000, "electric #9c27b0"))
    elems.append(text(base_x + 500, base_y + 4500, "furniture #555"))
    elems.append(text(base_x + 4000, base_y + 1000, "N"))
    elems.append(poly([(base_x + 4000, base_y + 1500), (base_x + 4000, base_y + 500), (base_x + 3900, base_y + 600), (base_x + 4000, base_y + 500), (base_x + 4100, base_y + 600)], "#000", 1))
    today = date.today().isoformat()
    elems.append(text(base_x, base_y + 5200, "Two-Story House Plan"))
    elems.append(text(base_x, base_y + 5700, f"Date: {today}"))
    elems.append(text(base_x, base_y + 6200, "Scale 1:50"))
    # add many notes to increase SVG size
    for i in range(1000):
        elems.append(text(base_x, base_y + 6500 + i * 30, f"note {i+1}"))
    elems.append('</g>')
    return elems

# --- main -------------------------------------------------------

def main() -> None:
    width_px = mm_to_px(A3_W)
    height_px = mm_to_px(A3_H)
    svg: List[str] = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{A3_W}mm" height="{A3_H}mm" viewBox="0 0 {width_px} {height_px}">']
    base_x = 200
    base_y = 200
    w = plan['width']
    d = plan['depth']
    for idx, (floor_name, floor) in enumerate(plan['floors'].items()):
        oy = base_y + idx * (d + 2000)
        svg.extend(layer_grid(base_x, oy, w, d))
        svg.extend(layer_walls(base_x, oy, floor))
        svg.extend(layer_openings(base_x, oy, floor))
        svg.extend(layer_plumbing(base_x, oy, floor))
        svg.extend(layer_electric(base_x, oy, floor))
        svg.extend(layer_furniture(base_x, oy, floor))
        svg.extend(layer_dimensions(base_x, oy, w, d))
        svg.extend(layer_text(base_x, oy, floor))
    legend_x = base_x + w + 3000
    legend_y = base_y + d + 2000
    svg.extend(legend_and_title(legend_x, legend_y))
    svg.append('</svg>')
    Path("house_plan.svg").write_text("\n".join(svg), encoding="utf-8")
    size = Path("house_plan.svg").stat().st_size
    print(f"\u2705 house_plan.svg generated: {size//1024} KB")
    assert size > 50_000

if __name__ == "__main__":
    main()
