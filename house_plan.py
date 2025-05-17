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


def polyline(points: list[tuple[float, float]], color: str, width: float) -> str:
    pts = " ".join(f"{mm_to_px(x):.1f},{mm_to_px(y):.1f}" for x, y in points)
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{mm_to_px(width):.1f}" />'


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
    BW = real_to_draw(12000)  # building width 12m -> 120mm
    BD = real_to_draw(10000)  # building depth 10m -> 100mm
    # exterior wall
    elements.append(rect(base_x, base_y, BW, BD, "#222", 1.5))

    # porch
    porch_w = real_to_draw(2500)
    porch_d = real_to_draw(1500)
    elements.append(rect(base_x + real_to_draw(1000), base_y + BD, porch_w, porch_d, "#222", 1.5))

    # partitions
    pw = 0.9
    elements.append(line(base_x + real_to_draw(5000), base_y, base_x + real_to_draw(5000), base_y + BD, "#666", pw))
    elements.append(line(base_x, base_y + real_to_draw(3000), base_x + real_to_draw(5000), base_y + real_to_draw(3000), "#666", pw))
    elements.append(line(base_x + real_to_draw(2700), base_y + real_to_draw(3000), base_x + real_to_draw(2700), base_y + real_to_draw(7000), "#666", pw))
    elements.append(line(base_x + real_to_draw(2700), base_y + real_to_draw(7000), base_x + real_to_draw(5000), base_y + real_to_draw(7000), "#666", pw))

    # doors (simple L-shape polylines)
    dsize = real_to_draw(800)
    elements.append(polyline([
        (base_x + real_to_draw(5000), base_y + real_to_draw(3000)),
        (base_x + real_to_draw(5000) - dsize, base_y + real_to_draw(3000)),
        (base_x + real_to_draw(5000) - dsize, base_y + real_to_draw(3000) - dsize)
    ], "#007acc", 0.5))

    # sanitary symbols
    sx = base_x + real_to_draw(500)
    sy = base_y + real_to_draw(3500)
    elements.append(rect(sx, sy, real_to_draw(800), real_to_draw(1200), "#ff4d00", 0.5))
    elements.append(line(sx, sy, sx + real_to_draw(800), sy + real_to_draw(1200), "#ff4d00", 0.5))

    # electric symbols
    ex = base_x + real_to_draw(6000)
    ey = base_y + real_to_draw(2000)
    elements.append(line(ex - 1, ey - 1, ex + 1, ey + 1, "#9c27b0", 0.5))
    elements.append(line(ex - 1, ey + 1, ex + 1, ey - 1, "#9c27b0", 0.5))

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

    # light grid lines every 0.25m
    grid(base_x, base_y, BW, BD, real_to_draw(250), elements)


def draw_floor2(base_x: float, base_y: float, elements: list[str]) -> None:
    BW = real_to_draw(12000)
    BD = real_to_draw(10000)
    elements.append(rect(base_x, base_y, BW, BD, "#222", 1.5))

    pw = 0.9
    elements.append(line(base_x + real_to_draw(4000), base_y, base_x + real_to_draw(4000), base_y + BD, "#666", pw))
    elements.append(line(base_x + real_to_draw(8000), base_y, base_x + real_to_draw(8000), base_y + BD, "#666", pw))
    elements.append(line(base_x, base_y + real_to_draw(5000), base_x + BW, base_y + real_to_draw(5000), "#666", pw))

    dsize = real_to_draw(800)
    elements.append(polyline([
        (base_x + real_to_draw(4000), base_y + real_to_draw(5000)),
        (base_x + real_to_draw(4000) - dsize, base_y + real_to_draw(5000)),
        (base_x + real_to_draw(4000) - dsize, base_y + real_to_draw(5000) - dsize)
    ], "#007acc", 0.5))

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
