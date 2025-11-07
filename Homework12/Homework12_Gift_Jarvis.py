# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 3
# Luis Salomón Flores Ugalde

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925

# ------- HW 12: Convex Hull: Graham Scan and Jarvis March -------

from math import atan2
import sys
import os
import glob
from typing import List, Tuple, Iterable
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

Point = Tuple[float, float]


def read_points(path: str) -> List[Point]:
    pts: List[Point] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.replace(",", " ").split()
            if len(parts) < 2:
                continue
            x, y = float(parts[0]), float(parts[1])
            pts.append((x, y))
    return pts

def unique_points(points: Iterable[Point]) -> List[Point]:
    seen = set()
    out = []
    for p in points:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out

def cross(o: Point, a: Point, b: Point) -> float:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def dist2(a: Point, b: Point) -> float:
    dx, dy = a[0] - b[0], a[1] - b[1]
    return dx*dx + dy*dy

def leftmost_lowest(points: List[Point]) -> Point:
    return min(points, key=lambda p: (p[1], p[0]))

# ---------- Graham Scan ----------

def graham_scan(points: Iterable[Point]) -> List[Point]:
    pts = unique_points(points)
    n = len(pts)
    if n <= 1:
        return pts[:]
    anchor = leftmost_lowest(pts)

    def angle_key(p: Point):
        return (atan2(p[1] - anchor[1], p[0] - anchor[0]), -dist2(p, anchor))

    sorted_pts = sorted((p for p in pts if p != anchor), key=angle_key)

    filtered: List[Point] = []
    last_angle = None
    last_best = None
    for p in sorted_pts:
        ang = atan2(p[1] - anchor[1], p[0] - anchor[0])
        if last_angle is None or abs(ang - last_angle) > 1e-15:
            if last_best is not None:
                filtered.append(last_best)
            last_angle = ang
            last_best = p
        else:
            if dist2(anchor, p) > dist2(anchor, last_best):
                last_best = p
    if last_best is not None:
        filtered.append(last_best)

    if not filtered:
        return [anchor]

    hull: List[Point] = [anchor]
    for p in filtered:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)

    if len(hull) >= 3 and all(abs(cross(hull[i-2], hull[i-1], hull[i])) < 1e-15 for i in range(2, len(hull))):
        ends = [anchor, max(filtered, key=lambda q: dist2(q, anchor))]
        ends = unique_points(sorted(ends))
        return ends
    return hull

# ---------- Jarvis March ----------

def jarvis_march(points: Iterable[Point]) -> List[Point]:
    pts = unique_points(points)
    n = len(pts)
    if n <= 1:
        return pts[:]

    start = leftmost_lowest(pts)
    hull: List[Point] = []
    p = start
    while True:
        hull.append(p)
        q = pts[0] if pts[0] != p else pts[1]
        for r in pts:
            if r == p or r == q:
                continue
            ori = cross(p, q, r)
            if ori > 0:
                q = r
            elif abs(ori) < 1e-15 and dist2(p, r) > dist2(p, q):
                q = r
        p = q
        if p == start:
            break

    if len(hull) > 2 and all(abs(cross(hull[0], hull[1], r)) < 1e-15 for r in hull[2:]):
        a = min(pts, key=lambda x: (x[0], x[1]))
        b = max(pts, key=lambda x: (x[0], x[1]))
        return [a, b] if a != b else [a]
    return hull

def format_points(pts: Iterable[Point]) -> str:
    return "[" + ", ".join(f"({x:.6g}, {y:.6g})" for x, y in pts) + "]"

def plot_convex_hull(points: List[Point], hull: List[Point], title: str, filename: str):
    fig, ax = plt.subplots(figsize=(10, 8))

    if points:
        px, py = zip(*points)
        ax.scatter(px, py, c='blue', s=50, alpha=0.6, label='Points', zorder=3)

    if len(hull) >= 2:
        hx, hy = zip(*hull)
        ax.plot(list(hx)+[hx[0]], list(hy)+[hy[0]], 'r-', linewidth=2, label='Convex Hull', zorder=2)
        ax.scatter(hx, hy, c='red', s=100, marker='^', label='Hull Vertices', zorder=4)
        ax.add_patch(Polygon(hull, alpha=0.2, facecolor='red', edgecolor='none', zorder=1))
    elif len(hull) == 1:
        ax.scatter([hull[0][0]], [hull[0][1]], c='red', s=100, marker='^', label='Hull Vertex', zorder=4)

    ax.set_xlabel('X'); ax.set_ylabel('Y')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best'); ax.grid(True, alpha=0.3); ax.axis('equal')

    if points:
        x_min, x_max = min(p[0] for p in points), max(p[0] for p in points)
        y_min, y_max = min(p[1] for p in points), max(p[1] for p in points)
        mx = (x_max - x_min) * 0.1 or 1
        my = (y_max - y_min) * 0.1 or 1
        ax.set_xlim(x_min - mx, x_max + mx)
        ax.set_ylim(y_min - my, y_max + my)

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"  Graph saved as: {filename}")
    plt.close()


def discover_txt_files(default_dir: str, pattern: str | None) -> list[str]:
    if pattern:  
        return sorted(glob.glob(pattern))
    return sorted(glob.glob(os.path.join(default_dir, "*.txt")))

def main():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()
    pattern = sys.argv[1] if len(sys.argv) >= 2 else None
    txt_files = discover_txt_files(script_dir, pattern)

    if not txt_files:
        where = pattern or os.path.join(script_dir, "*.txt")
        print(f"No input files found for: {where}")
        sys.exit(1)

    print(f"Found {len(txt_files)} file(s).")
    print("=" * 80)

    for file_path in txt_files:
        filename = os.path.basename(file_path)
        base = os.path.splitext(filename)[0]
        print(f"\nProcessing: {filename}")
        print("-" * 80)

        pts = read_points(file_path)
        if not pts:
            print(f"  No points found in {filename}")
            continue

        print(f"\nPoints (n={len(pts)}): {format_points(pts)}")

        print("\n--- Graham Scan ---")
        hull_g = graham_scan(pts)
        print(f"Hull (h={len(hull_g)}): {format_points(hull_g)}")
        plot_convex_hull(pts, hull_g, f"Graham Scan - {filename}", os.path.join(script_dir, f"{base}_graham_scan.png"))

        print("\n--- Jarvis March ---")
        hull_j = jarvis_march(pts)
        print(f"Hull (h={len(hull_j)}): {format_points(hull_j)}")
        plot_convex_hull(pts, hull_j, f"Jarvis March - {filename}", os.path.join(script_dir, f"{base}_jarvis_march.png"))

        print("=" * 80)

if __name__ == "__main__":
    main()
