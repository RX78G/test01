import math

COS30 = math.cos(math.radians(30))
SIN30 = math.sin(math.radians(30))

# Dimensions in millimeters
WIDTH = 10000  # 10 m
DEPTH = 8000   # 8 m
HEIGHT = 6000  # 6 m (top of second floor)
ROOF_HEIGHT = 2000  # ridge height above second floor

SCALE = 0.05  # drawing scale (px per mm)
MARGIN = 20   # margin around drawing (px)


def iso(x: float, y: float, z: float) -> tuple[float, float]:
    """Return isometric projection coordinates."""
    u = (x - y) * COS30
    v = (x + y) * SIN30 - z
    return u, v


def project(point: tuple[float, float, float],
            min_x: float, max_y: float) -> tuple[float, float]:
    u, v = iso(*point)
    x = (u - min_x) * SCALE + MARGIN
    y = (max_y - v) * SCALE + MARGIN
    return x, y


def main() -> None:
    # Base box edges
    box = [
        ((0, 0, 0), (WIDTH, 0, 0)),
        ((WIDTH, 0, 0), (WIDTH, DEPTH, 0)),
        ((WIDTH, DEPTH, 0), (0, DEPTH, 0)),
        ((0, DEPTH, 0), (0, 0, 0)),

        ((0, 0, HEIGHT), (WIDTH, 0, HEIGHT)),
        ((WIDTH, 0, HEIGHT), (WIDTH, DEPTH, HEIGHT)),
        ((WIDTH, DEPTH, HEIGHT), (0, DEPTH, HEIGHT)),
        ((0, DEPTH, HEIGHT), (0, 0, HEIGHT)),

        ((0, 0, 0), (0, 0, HEIGHT)),
        ((WIDTH, 0, 0), (WIDTH, 0, HEIGHT)),
        ((WIDTH, DEPTH, 0), (WIDTH, DEPTH, HEIGHT)),
        ((0, DEPTH, 0), (0, DEPTH, HEIGHT)),
    ]

    # Roof edges
    ridge_front = (WIDTH / 2, 0, HEIGHT + ROOF_HEIGHT)
    ridge_back = (WIDTH / 2, DEPTH, HEIGHT + ROOF_HEIGHT)
    roof = [
        ((0, 0, HEIGHT), ridge_front),
        ((WIDTH, 0, HEIGHT), ridge_front),
        ((0, DEPTH, HEIGHT), ridge_back),
        ((WIDTH, DEPTH, HEIGHT), ridge_back),
        (ridge_front, ridge_back),
    ]

    all_lines = [(line, "#333") for line in box] + [(line, "#900") for line in roof]

    points = [p for line, _ in all_lines for p in line]
    proj = [iso(*p) for p in points]
    min_x = min(u for u, _ in proj)
    max_y = max(v for _, v in proj)
    max_x = max(u for u, _ in proj)
    min_y = min(v for _, v in proj)

    view_w = (max_x - min_x) * SCALE + 2 * MARGIN
    view_h = (max_y - min_y) * SCALE + 2 * MARGIN

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_w:.2f} {view_h:.2f}">',
        '<text x="10" y="20" font-size="16" fill="#000">Simple 3D-Isometric House</text>',
    ]

    for (start, end), color in all_lines:
        x1, y1 = project(start, min_x, max_y)
        x2, y2 = project(end, min_x, max_y)
        svg.append(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{color}" stroke-width="2" />'
        )

    svg.append('</svg>')

    with open("house.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print("\u2705 house.svg \u3092\u751f\u6210\u3057\u307e\u3057\u305f")


if __name__ == "__main__":
    main()
