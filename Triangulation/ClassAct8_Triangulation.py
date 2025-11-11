import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ============================================================================
# PROBLEM 1: Points and Triangles
# ============================================================================

def create_super_triangle(points):
    if not points:
        return [(0, 0), (1, 0), (0, 1)]
    
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    
    dx = max_x - min_x
    dy = max_y - min_y
    delta_max = max(dx, dy)
    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2
    
    margin = delta_max * 10
    
    p1 = (mid_x - margin, mid_y - margin)
    p2 = (mid_x + margin, mid_y - margin)
    p3 = (mid_x, mid_y + margin * 1.732)  
    
    return [p1, p2, p3]

# ============================================================================
# PROBLEM 2: The Circumscribed Circle
# ============================================================================

def calculate_circumcircle(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    ax = x2 - x1
    ay = y2 - y1
    bx = x3 - x1
    by = y3 - y1
    
    d = 2 * (ax * by - ay * bx)
    
    if abs(d) < 1e-10:
        return None
    
    ux = (by * (ax * ax + ay * ay) - ay * (bx * bx + by * by)) / d
    uy = (ax * (bx * bx + by * by) - bx * (ax * ax + ay * ay)) / d
    
    center_x = x1 + ux
    center_y = y1 + uy
    
    radius = math.sqrt(ux * ux + uy * uy)
    
    return (center_x, center_y, radius)


# ============================================================================
# PROBLEM 3: Points Inside Circles
# ============================================================================

def point_in_circumcircle(point, triangle):
    circle = calculate_circumcircle(triangle[0], triangle[1], triangle[2])
    
    if circle is None:
        return False
    
    center_x, center_y, radius = circle
    px, py = point
    
    dist = math.sqrt((px - center_x) ** 2 + (py - center_y) ** 2)
    
    return dist < radius + 1e-10


def find_bad_triangles(point, triangles):
    bad_triangles = []
    for triangle in triangles:
        if point_in_circumcircle(point, triangle):
            bad_triangles.append(triangle)
    return bad_triangles


# ============================================================================
# PROBLEM 4: Non-shared Sides
# ============================================================================

def get_edges(triangle):
    return [
        (triangle[0], triangle[1]),
        (triangle[1], triangle[2]),
        (triangle[2], triangle[0])
    ]


def normalize_edge(edge):
    p1, p2 = edge
    if p1 < p2:
        return (p1, p2)
    else:
        return (p2, p1)


def find_unique_edges(triangles):
    edge_count = {}
    
    for triangle in triangles:
        edges = get_edges(triangle)
        for edge in edges:
            normalized = normalize_edge(edge)
            edge_count[normalized] = edge_count.get(normalized, 0) + 1
    
    # Return edges that appear exactly once
    unique_edges = [edge for edge, count in edge_count.items() if count == 1]
    return unique_edges


# ============================================================================
# PROBLEM 5: Graphics
# ============================================================================

def plot_super_triangle(points, super_triangle, filename=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    
    xs = [super_triangle[0][0], super_triangle[1][0], super_triangle[2][0], super_triangle[0][0]]
    ys = [super_triangle[0][1], super_triangle[1][1], super_triangle[2][1], super_triangle[0][1]]
    ax.plot(xs, ys, 'g-', linewidth=2, label='Super Triangle')
    ax.fill(xs, ys, alpha=0.1, color='green')
    
    if points:
        pts_x, pts_y = zip(*points)
        ax.scatter(pts_x, pts_y, c='red', s=50, zorder=5, label='Input Points')
        
        for i, (x, y) in enumerate(points, 1):
            ax.annotate(f'P{i}', (x, y), xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    ax.set_aspect('equal')
    ax.set_title('Problem 1: Super Triangle Containing All Points', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    if filename:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"  Saved: {filename}")
    plt.close()


def plot_circumcircle(triangle, filename=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    
    xs = [triangle[0][0], triangle[1][0], triangle[2][0], triangle[0][0]]
    ys = [triangle[0][1], triangle[1][1], triangle[2][1], triangle[0][1]]
    ax.plot(xs, ys, 'b-', linewidth=2, label='Triangle')
    ax.fill(xs, ys, alpha=0.2, color='blue')
    
    for i, (x, y) in enumerate(triangle, 1):
        ax.scatter(x, y, c='blue', s=100, zorder=5)
        ax.annotate(f'P{i}', (x, y), xytext=(5, 5), textcoords='offset points', fontsize=10, fontweight='bold')
    
    circle_data = calculate_circumcircle(triangle[0], triangle[1], triangle[2])
    if circle_data:
        center_x, center_y, radius = circle_data
        circle = Circle((center_x, center_y), radius, fill=False, 
                       edgecolor='red', linewidth=2, label='Circumcircle')
        ax.add_patch(circle)
        
        ax.scatter(center_x, center_y, c='red', s=100, marker='x', linewidths=3, zorder=6, label='Center')
        ax.annotate(f'Center\n({center_x:.2f}, {center_y:.2f})\nR={radius:.2f}', 
                   (center_x, center_y), xytext=(10, -20), textcoords='offset points', 
                   fontsize=9, bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
    
    ax.set_aspect('equal')
    ax.set_title('Problem 2: Circumscribed Circle', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    if filename:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"  Saved: {filename}")
    plt.close()


def plot_point_in_circle(triangle, test_points, filename=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    
    xs = [triangle[0][0], triangle[1][0], triangle[2][0], triangle[0][0]]
    ys = [triangle[0][1], triangle[1][1], triangle[2][1], triangle[0][1]]
    ax.plot(xs, ys, 'b-', linewidth=2, label='Triangle')
    ax.fill(xs, ys, alpha=0.2, color='blue')
    
    for i, (x, y) in enumerate(triangle, 1):
        ax.scatter(x, y, c='blue', s=100, zorder=5)
        ax.annotate(f'P{i}', (x, y), xytext=(5, 5), textcoords='offset points', fontsize=10, fontweight='bold')
    
    circle_data = calculate_circumcircle(triangle[0], triangle[1], triangle[2])
    if circle_data:
        center_x, center_y, radius = circle_data
        circle = Circle((center_x, center_y), radius, fill=False, 
                       edgecolor='purple', linewidth=2, linestyle='--', label='Circumcircle')
        ax.add_patch(circle)
        
        ax.scatter(center_x, center_y, c='purple', s=100, marker='x', linewidths=3, zorder=6)
    
    for i, point in enumerate(test_points, 4):
        is_inside = point_in_circumcircle(point, triangle)
        color = 'green' if is_inside else 'red'
        marker = 'o' if is_inside else 's'
        label = 'Inside' if is_inside else 'Outside'
        
        ax.scatter(point[0], point[1], c=color, s=150, marker=marker, 
                  zorder=7, edgecolors='black', linewidths=2,
                  label=label if i == 4 or (i == 5 and not is_inside) else '')
        ax.annotate(f'P{i}\n({label})', point, xytext=(5, 5), textcoords='offset points', 
                   fontsize=9, bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.3))
    
    ax.set_aspect('equal')
    ax.set_title('Problem 3: Points Inside/Outside Circumcircle', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    if filename:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"  Saved: {filename}")
    plt.close()


def plot_unique_edges(triangles, unique_edges, filename=None):
    """Visualize Problem 4: Non-shared edges."""
    fig, ax = plt.subplots(figsize=(10, 10))
    
    all_points = set()
    for triangle in triangles:
        xs = [triangle[0][0], triangle[1][0], triangle[2][0], triangle[0][0]]
        ys = [triangle[0][1], triangle[1][1], triangle[2][1], triangle[0][1]]
        ax.plot(xs, ys, 'lightblue', linewidth=1, alpha=0.5)
        all_points.update(triangle)
    
    for edge in unique_edges:
        xs = [edge[0][0], edge[1][0]]
        ys = [edge[0][1], edge[1][1]]
        ax.plot(xs, ys, 'r-', linewidth=3, label='Unique Edge' if edge == unique_edges[0] else '')
    
    if all_points:
        pts_x, pts_y = zip(*all_points)
        ax.scatter(pts_x, pts_y, c='blue', s=50, zorder=5)
    
    ax.set_aspect('equal')
    ax.set_title(f'Problem 4: Non-Shared Edges ({len(unique_edges)} edges)', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    if filename:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"  Saved: {filename}")
    plt.close()


def plot_triangulation(points, triangles, title="Delaunay Triangulation", 
                       show_circles=False, filename=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    
    for triangle in triangles:
        xs = [triangle[0][0], triangle[1][0], triangle[2][0], triangle[0][0]]
        ys = [triangle[0][1], triangle[1][1], triangle[2][1], triangle[0][1]]
        ax.plot(xs, ys, 'b-', linewidth=0.5)
    
    if show_circles:
        for triangle in triangles:
            circle_data = calculate_circumcircle(triangle[0], triangle[1], triangle[2])
            if circle_data:
                center_x, center_y, radius = circle_data
                circle = Circle((center_x, center_y), radius, fill=False, 
                              edgecolor='lightblue', linestyle='--', linewidth=0.5)
                ax.add_patch(circle)
    
    if points:
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        ax.scatter(xs, ys, c='red', s=30, zorder=5)
    
    ax.set_aspect('equal')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    
    if filename:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Saved plot to {filename}")
    else:
        plt.show()
    
    plt.close()


# ============================================================================
# PROBLEM 6: Delaunay Triangulation
# ============================================================================

def bowyer_watson(points):
    if len(points) < 3:
        return []
    
    super_triangle = create_super_triangle(points)
    triangles = [super_triangle]
    
    for point in points:
        bad_triangles = find_bad_triangles(point, triangles)
        
        unique_edges = find_unique_edges(bad_triangles)
        
        for bad_tri in bad_triangles:
            triangles.remove(bad_tri)
        
        for edge in unique_edges:
            new_triangle = [edge[0], edge[1], point]
            triangles.append(new_triangle)
    
    final_triangles = []
    for triangle in triangles:
        if not any(vertex in super_triangle for vertex in triangle):
            final_triangles.append(triangle)
    
    return final_triangles

# ============================================================================
# EXAMPLE USAGE AND TESTING
# ============================================================================

def generate_random_points(n, seed=42):
    import random
    random.seed(seed)
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]


def read_points_from_file(filename):
    points = []
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
        n = int(lines[0].strip())
        
        for i in range(1, n + 1):
            line = lines[i].strip()
            parts = line.split()
            x = float(parts[0])
            y = float(parts[1])
            points.append((x, y))
    
    return points


def main():
    print("=" * 70)
    print("Delaunay Triangulation - Bowyer-Watson Algorithm")
    print("=" * 70)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_file = os.path.join(script_dir, "puntos-n11_2.txt")
    print(f"\nReading points from: {input_file}")
    points = read_points_from_file(input_file)
    
    print(f"Loaded {len(points)} points:")
    for i, (x, y) in enumerate(points, 1):
        print(f"  Point {i}: ({x}, {y})")
    
    print("\n[Problem 1] Creating super triangle...")
    super_tri = create_super_triangle(points)
    print(f"Super triangle vertices:")
    for i, vertex in enumerate(super_tri, 1):
        print(f"  Vertex {i}: ({vertex[0]:.2f}, {vertex[1]:.2f})")
    
    plot_super_triangle(points, super_tri, 
                       filename=os.path.join(script_dir, "problem1_super_triangle.png"))
    
    print("\n[Problem 2] Calculating circumcircle for first 3 points...")
    if len(points) >= 3:
        circle = calculate_circumcircle(points[0], points[1], points[2])
        if circle:
            print(f"  Center: ({circle[0]:.4f}, {circle[1]:.4f})")
            print(f"  Radius: {circle[2]:.4f}")
        
        test_triangle = [points[0], points[1], points[2]]
        plot_circumcircle(test_triangle, 
                         filename=os.path.join(script_dir, "problem2_circumcircle.png"))
    
    print("\n[Problem 3] Checking if points are inside circumcircle...")
    test_triangle = [points[0], points[1], points[2]] if len(points) >= 3 else []
    if test_triangle and len(points) > 3:
        test_pts = []
        for i in range(3, min(6, len(points))):
            is_inside = point_in_circumcircle(points[i], test_triangle)
            print(f"  Point {i+1} {points[i]} is {'INSIDE' if is_inside else 'OUTSIDE'} the circumcircle")
            test_pts.append(points[i])
        
        plot_point_in_circle(test_triangle, test_pts,
                           filename=os.path.join(script_dir, "problem3_point_in_circle.png"))
    
    print("\n[Problem 4] Non-shared edges will be identified during triangulation...")
    
    if len(points) >= 5:
        sample_triangles = [
            [points[0], points[1], points[2]],
            [points[0], points[2], points[3]],
            [points[2], points[3], points[4]]
        ]
        unique = find_unique_edges(sample_triangles)
        print(f"  Example: {len(sample_triangles)} triangles have {len(unique)} unique (non-shared) edges")
        
        plot_unique_edges(sample_triangles, unique,
                         filename=os.path.join(script_dir, "problem4_unique_edges.png"))
    
    print("\n[Problem 6] Computing Delaunay triangulation...")
    triangles = bowyer_watson(points)
    print(f"Generated {len(triangles)} triangles")
    
    print("\nTriangles (vertex indices):")
    for i, triangle in enumerate(triangles, 1):
        indices = []
        for vertex in triangle:
            if vertex in points:
                indices.append(points.index(vertex) + 1)
            else:
                indices.append(-1)
        print(f"  Triangle {i}: vertices {indices}")
    
    # Problem 5: Visualize results
    print("\n[Problem 5] Creating visualizations...")
    
    # Basic triangulation
    plot_triangulation(points, triangles, 
                      title=f"Problem 5: Delaunay Triangulation ({len(points)} points)",
                      show_circles=False,
                      filename=os.path.join(script_dir, "problem5_delaunay_basic.png"))
    
    # With circumcircles
    plot_triangulation(points, triangles, 
                      title=f"Problem 5: Delaunay with Circumcircles ({len(points)} points)",
                      show_circles=True,
                      filename=os.path.join(script_dir, "problem5_delaunay_circles.png"))
    
    # Verify Delaunay property
    print("\n[Verification] Checking Delaunay property...")
    violations = 0
    for tri_idx, triangle in enumerate(triangles):
        circle = calculate_circumcircle(triangle[0], triangle[1], triangle[2])
        if circle:
            for pt_idx, point in enumerate(points):
                if point not in triangle:
                    if point_in_circumcircle(point, triangle):
                        violations += 1
                        print(f"  WARNING: Point {pt_idx+1} violates triangle {tri_idx+1}")
    
    if violations == 0:
        print("  ✓ All triangles satisfy the Delaunay property!")
        print("  ✓ No points lie inside any circumcircle (except triangle vertices)")
    else:
        print(f"  ✗ Found {violations} violations of Delaunay property")
    
    print("\n" + "=" * 70)
    print("All problems solved successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()