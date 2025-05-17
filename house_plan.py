import math
from pathlib import Path

def mm_to_px(mm: float) -> float:
    """Convert drawing millimeters to pixels (1 mm = 4 px)."""
    return mm * 4

def real_to_draw(mm_real: float) -> float:
    """Convert real millimeters to drawing millimeters at 1:100 scale."""
    return mm_real / 100


def line(x1: float, y1: float, x2: float, y2: float, color: str, width: float) -> str:
    return (
        f'<line x1="{mm_to_px(x1):.1f}" y1="{mm_to_px(y1):.1f}" '
        f'x2="{mm_to_px(x2):.1f}" y2="{mm_to_px(y2):.1f}" '
        f'stroke="{color}" stroke-width="{mm_to_px(width):.1f}" />'
    )


def rect(x: float, y: float, w: float, h: float, color: str, width: float) -> str:
    return (
        f'<rect x="{mm_to_px(x):.1f}" y="{mm_to_px(y):.1f}" '
        f'width="{mm_to_px(w):.1f}" height="{mm_to_px(h):.1f}" '
        f'fill="none" stroke="{color}" stroke-width="{mm_to_px(width):.1f}" />'
    )


def polyline(points: list[tuple[float, float]], color: str, width: float, dash: str | None = None) -> str:
    pts = " ".join(f"{mm_to_px(x):.1f},{mm_to_px(y):.1f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{mm_to_px(width):.1f}"{dash_attr} />'


def door(x: float, y: float, w: float, inward: bool, color: str = "#007acc") -> str:
    """Draw L-shaped door."""
    if inward:
        pts = [(x, y), (x + w, y), (x + w, y + w)]
    else:
        pts = [(x, y), (x - w, y), (x - w, y - w)]
    return polyline(pts, color, 0.5)


def window(x: float, y: float, length: float, horizontal: bool = True) -> str:
    if horizontal:
        return "\n".join([
            line(x, y, x + length, y, "#007acc", 0.5),
            line(x, y - 0.5, x + length, y - 0.5, "#007acc", 0.5),
        ])
    return "\n".join([
        line(x, y, x, y + length, "#007acc", 0.5),
        line(x - 0.5, y, x - 0.5, y + length, "#007acc", 0.5),
    ])


def furniture(x: float, y: float, w: float, d: float, label: str) -> list[str]:
    return [
        rect(x, y, w, d, "#795548", 0.3),
        text(x + w / 2 - 5, y + d / 2, label, 2.5),
    ]


def grid(base_x: float, base_y: float, w: float, d: float, spacing: float, elements: list[str]) -> None:
    """Add light grid lines inside a rectangle."""
    count_x = int(w / spacing)
    count_y = int(d / spacing)
    for i in range(1, count_x):
        x = base_x + i * spacing
        elements.append(line(x, base_y, x, base_y + d, "#ccc", 0.1))
        elements.append(text(x - 1, base_y - 2, str(i)))
    for j in range(1, count_y):
        y = base_y + j * spacing
        elements.append(line(base_x, y, base_x + w, y, "#ccc", 0.1))
        elements.append(text(base_x - 4, y + 1, str(j)))


def text(x: float, y: float, content: str, size: float = 3.5) -> str:
    return (
        f'<text x="{mm_to_px(x):.1f}" y="{mm_to_px(y):.1f}" '
        f'font-size="{mm_to_px(size):.1f}" font-family="sans-serif">{content}</text>'
    )


def draw_floor(base_x: float, base_y: float, elements: list[str]) -> None:
    """Draw detailed first floor."""
    BW = real_to_draw(12000)
    BD = real_to_draw(10000)
    t = real_to_draw(150)
    # exterior wall with thickness
    elements.append(rect(base_x, base_y, BW, BD, "#222", t))
    elements.append(rect(base_x + t, base_y + t, BW - 2 * t, BD - 2 * t, "#222", 0.5))

    # porch
    porch_w = real_to_draw(2500)
    porch_d = real_to_draw(1500)
    elements.append(rect(base_x + real_to_draw(1000), base_y + BD, porch_w, porch_d, "#222", 1.5))

    # partitions
    pw = 0.9
    elements.append(line(base_x + real_to_draw(5000), base_y + t, base_x + real_to_draw(5000), base_y + BD - t, "#666", pw))
    elements.append(line(base_x + t, base_y + real_to_draw(3000), base_x + real_to_draw(5000), base_y + real_to_draw(3000), "#666", pw))
    elements.append(line(base_x + real_to_draw(2700), base_y + real_to_draw(3000), base_x + real_to_draw(2700), base_y + real_to_draw(7000), "#666", pw))
    elements.append(line(base_x + real_to_draw(2700), base_y + real_to_draw(7000), base_x + real_to_draw(5000), base_y + real_to_draw(7000), "#666", pw))

    # doors (simple L-shape polylines)
    dsize = real_to_draw(800)
    elements.append(door(base_x + real_to_draw(5000), base_y + real_to_draw(3000), dsize, inward=True))
    elements.append(window(base_x + real_to_draw(1000), base_y + t, real_to_draw(1800)))

    # sanitary symbols
    sx = base_x + real_to_draw(500)
    sy = base_y + real_to_draw(3500)
    elements.extend([
        rect(sx, sy, real_to_draw(800), real_to_draw(1200), "#ff4d00", 0.5),
        line(sx, sy, sx + real_to_draw(800), sy + real_to_draw(1200), "#ff4d00", 0.5),
    ])

    # piping lines
    elements.append(polyline([
        (sx + real_to_draw(400), sy + real_to_draw(1200)),
        (sx + real_to_draw(400), base_y + BD - t),
        (base_x + real_to_draw(11000), base_y + BD - t),
    ], "#2196f3", 0.4))
    elements.append(polyline([
        (sx + real_to_draw(400), sy + real_to_draw(1200)),
        (sx + real_to_draw(400), base_y + BD),
    ], "#6d4c41", 0.4, dash="2,2"))

    # electric symbols and wiring
    ex = base_x + real_to_draw(6000)
    ey = base_y + real_to_draw(2000)
    elements.append(polyline([
        (ex, base_y + t),
        (ex, base_y + BD - t),
    ], "#9c27b0", 0.3, dash="1,2"))
    elements.append(line(ex - 1, ey - 1, ex + 1, ey + 1, "#9c27b0", 0.5))
    elements.append(line(ex - 1, ey + 1, ex + 1, ey - 1, "#9c27b0", 0.5))

    # furniture
    elements.extend(furniture(base_x + real_to_draw(6000), base_y + real_to_draw(3500), real_to_draw(2000), real_to_draw(900), "テーブル"))
    elements.extend(furniture(base_x + real_to_draw(6500), base_y + real_to_draw(1000), real_to_draw(1800), real_to_draw(800), "ソファ"))

    # room names
    elements.append(text(base_x + real_to_draw(2500), base_y + real_to_draw(1500), "LDK 20畳"))
    elements.append(text(base_x + real_to_draw(1500), base_y + real_to_draw(8000), "和室 4.5畳"))

    # dimension lines around building
    dim_off = 5
    elements.append(line(base_x - dim_off, base_y, base_x - dim_off, base_y + BD, "#000", 0.3))
    elements.append(line(base_x - dim_off * 2, base_y, base_x - dim_off, base_y, "#000", 0.3))
    elements.append(line(base_x - dim_off * 2, base_y + BD, base_x - dim_off, base_y + BD, "#000", 0.3))
    elements.append(text(base_x - dim_off * 4, base_y + BD / 2, f"{int(BD * 10)}") )
    elements.append(line(base_x, base_y - dim_off, base_x + BW, base_y - dim_off, "#000", 0.3))
    elements.append(line(base_x, base_y - dim_off * 2, base_x, base_y - dim_off, "#000", 0.3))
    elements.append(line(base_x + BW, base_y - dim_off * 2, base_x + BW, base_y - dim_off, "#000", 0.3))
    elements.append(text(base_x + BW / 2, base_y - dim_off * 4, f"{int(BW * 10)}"))

    # light grid lines every 0.25m
    grid(base_x, base_y, BW, BD, real_to_draw(250), elements)
    # additional grid for detail
    grid(base_x, base_y, BW, BD, real_to_draw(250), elements)


def draw_floor2(base_x: float, base_y: float, elements: list[str]) -> None:
    BW = real_to_draw(12000)
    BD = real_to_draw(10000)
    t = real_to_draw(150)
    elements.append(rect(base_x, base_y, BW, BD, "#222", t))
    elements.append(rect(base_x + t, base_y + t, BW - 2 * t, BD - 2 * t, "#222", 0.5))

    pw = 0.9
    elements.append(line(base_x + real_to_draw(4000), base_y + t, base_x + real_to_draw(4000), base_y + BD - t, "#666", pw))
    elements.append(line(base_x + real_to_draw(8000), base_y + t, base_x + real_to_draw(8000), base_y + BD - t, "#666", pw))
    elements.append(line(base_x + t, base_y + real_to_draw(5000), base_x + BW - t, base_y + real_to_draw(5000), "#666", pw))

    dsize = real_to_draw(800)
    elements.append(door(base_x + real_to_draw(4000), base_y + real_to_draw(5000), dsize, inward=True))

    # simple beds and desks
    elements.extend(furniture(base_x + real_to_draw(2200), base_y + real_to_draw(3200), real_to_draw(1800), real_to_draw(900), "ベッド"))
    elements.extend(furniture(base_x + real_to_draw(6200), base_y + real_to_draw(3200), real_to_draw(1800), real_to_draw(900), "ベッド"))
    elements.extend(furniture(base_x + real_to_draw(2200), base_y + real_to_draw(8200), real_to_draw(1800), real_to_draw(900), "ベッド"))
    elements.extend(furniture(base_x + real_to_draw(9200), base_y + real_to_draw(8200), real_to_draw(1000), real_to_draw(700), "机"))

    elements.append(text(base_x + real_to_draw(2000), base_y + real_to_draw(3000), "子供室 6畳"))
    elements.append(text(base_x + real_to_draw(6000), base_y + real_to_draw(3000), "子供室 6畳"))
    elements.append(text(base_x + real_to_draw(2000), base_y + real_to_draw(8000), "主寝室 8畳"))
    elements.append(text(base_x + real_to_draw(9000), base_y + real_to_draw(8000), "書斎 4畳"))

    dim_off = 5
    elements.append(line(base_x - dim_off, base_y, base_x - dim_off, base_y + BD, "#000", 0.3))
    elements.append(line(base_x - dim_off * 2, base_y, base_x - dim_off, base_y, "#000", 0.3))
    elements.append(line(base_x - dim_off * 2, base_y + BD, base_x - dim_off, base_y + BD, "#000", 0.3))
    elements.append(text(base_x - dim_off * 4, base_y + BD / 2, f"{int(BD * 10)}"))
    elements.append(line(base_x, base_y - dim_off, base_x + BW, base_y - dim_off, "#000", 0.3))
    elements.append(line(base_x, base_y - dim_off * 2, base_x, base_y - dim_off, "#000", 0.3))
    elements.append(line(base_x + BW, base_y - dim_off * 2, base_x + BW, base_y - dim_off, "#000", 0.3))
    elements.append(text(base_x + BW / 2, base_y - dim_off * 4, f"{int(BW * 10)}"))


def main() -> None:
    width_px = mm_to_px(420)
    height_px = mm_to_px(297)
    elements: list[str] = []
    elements.append('<g id="wall">')
    draw_floor(real_to_draw(1000), real_to_draw(1000), elements)
    draw_floor2(real_to_draw(1000) + real_to_draw(13000), real_to_draw(1000), elements)
    elements.append('</g>')

    elements.append('<g id="legend">')
    lx = real_to_draw(34000)
    ly = real_to_draw(23000)
    elements.append(rect(lx, ly, real_to_draw(7000), real_to_draw(5000), "#000", 0.3))
    elements.append(text(lx + real_to_draw(500), ly + real_to_draw(1000), "凡例"))
    elements.append(text(lx + real_to_draw(500), ly + real_to_draw(2000), "外壁 #222"))
    elements.append(text(lx + real_to_draw(500), ly + real_to_draw(3000), "間仕切 #666"))
    elements.append(text(lx + real_to_draw(500), ly + real_to_draw(4000), "建具 #007acc"))
    elements.append(text(lx + real_to_draw(3500), ly + real_to_draw(1000), "北"))
    elements.append(polyline([
        (lx + real_to_draw(3500), ly + real_to_draw(1500)),
        (lx + real_to_draw(3500), ly + real_to_draw(500)),
        (lx + real_to_draw(3400), ly + real_to_draw(600)),
        (lx + real_to_draw(3500), ly + real_to_draw(500)),
        (lx + real_to_draw(3600), ly + real_to_draw(600))
    ], "#000", 0.3))
    elements.append('</g>')

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 {width_px} {height_px}">'
    ]
    svg.extend(elements)
    svg.append('</svg>')

    Path("house_plan.svg").write_text("\n".join(svg), encoding="utf-8")
    print("\u2705 house_plan.svg generated")
    size = Path("house_plan.svg").stat().st_size
    assert size >= 20 * 1024
    assert Path("house_plan.svg").is_file()

if __name__ == "__main__":
    main()
