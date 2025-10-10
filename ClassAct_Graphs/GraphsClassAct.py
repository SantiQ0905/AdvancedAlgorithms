import heapq

# ----------- GRAPH READING -----------
def read_graph(filename, directed=False):
    with open(filename, "r") as f:
        n = int(f.readline().strip())
        edges = []
        for line in f:
            u, v, w = map(int, line.strip().split())
            edges.append((u, v, w))
    # Build adjacency list
    graph = {i: [] for i in range(n)}
    for u, v, w in edges:
        graph[u].append((v, w))
        if not directed:
            graph[v].append((u, w))
    return n, edges, graph


# ----------- PRIM'S ALGORITHM -----------
def prim(graph, start=0):
    visited = set([start])
    edges = [(w, start, v) for v, w in graph[start]]
    heapq.heapify(edges)
    mst = []
    total_cost = 0

    while edges and len(visited) < len(graph):
        w, u, v = heapq.heappop(edges)
        if v not in visited:
            visited.add(v)
            mst.append((u, v, w))
            total_cost += w
            for next_v, next_w in graph[v]:
                if next_v not in visited:
                    heapq.heappush(edges, (next_w, v, next_v))

    return mst, total_cost


# ----------- KRUSKAL'S ALGORITHM -----------
def find(parent, i):
    if parent[i] != i:
        parent[i] = find(parent, parent[i])
    return parent[i]

def union(parent, rank, x, y):
    root_x, root_y = find(parent, x), find(parent, y)
    if root_x != root_y:
        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_y] = root_x
            rank[root_x] += 1

def kruskal(n, edges):
    edges.sort(key=lambda x: x[2])
    parent = [i for i in range(n)]
    rank = [0] * n
    mst = []
    total_cost = 0

    for u, v, w in edges:
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            mst.append((u, v, w))
            total_cost += w

    return mst, total_cost


# ----------- DIJKSTRA'S ALGORITHM -----------
def dijkstra(graph, start=0):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, u = heapq.heappop(pq)
        if current_distance > distances[u]:
            continue
        for v, w in graph[u]:
            distance = current_distance + w
            if distance < distances[v]:
                distances[v] = distance
                heapq.heappush(pq, (distance, v))

    return distances


# ----------- MAIN -----------
if __name__ == "__main__":
    print("== Undirected Graph (MST) ==")
    n, edges, graph = read_graph("ClassAct_Graphs/grafo-no-dirigido.txt", directed=False)

    prim_mst, prim_cost = prim(graph)
    print("\nPrim's MST:", prim_mst)
    print("Total cost:", prim_cost)

    kruskal_mst, kruskal_cost = kruskal(n, edges)
    print("\nKruskal's MST:", kruskal_mst)
    print("Total cost:", kruskal_cost)

    print("\n== Directed Graph (Dijkstra) ==")
    n2, edges2, graph2 = read_graph("ClassAct_Graphs/grafo-dirigido.txt", directed=True)
    dist = dijkstra(graph2, start=0)
    print("\nDijkstra (from node 0):")
    for node, d in dist.items():
        print(f"0 → {node}: {d}")