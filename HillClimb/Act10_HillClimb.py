# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 1
# Luis Salomón Flores Ugalde

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925

# ------- Class Activity 10 - Hill Climber_ISL_SA -------

import random
import math
import matplotlib.pyplot as plt
import os

def load_graph(filename):
    n = None
    edges = []

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                a = int(parts[0])
                b = int(parts[1])
            except ValueError:
                continue
            if n is None:
                n = a
            else:
                u, v = a, b
                edges.append((u, v))

    if n is None:
        raise ValueError("Could not find a valid 'n m' header line in the file.")

    return n, edges


def bandwidth(perm, edges):
    n = len(perm)
    pos = [0] * (n + 1)
    for i, v in enumerate(perm):
        pos[v] = i

    bw = 0
    for u, v in edges:
        d = abs(pos[u] - pos[v])
        if d > bw:
            bw = d
    return bw

def random_swap_neighbor(perm):
    n = len(perm)
    i, j = random.sample(range(n), 2)
    neighbor = perm[:]
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

def local_search_hc(perm, edges, max_evals, evals_used, no_improve_limit_factor=10):
    n = len(perm)
    no_improve_limit = no_improve_limit_factor * n

    if evals_used >= max_evals:
        return perm, float("inf"), evals_used

    current_perm = perm[:]
    current_cost = bandwidth(current_perm, edges)
    evals_used += 1

    best_perm = current_perm[:]
    best_cost = current_cost

    no_improve = 0

    while evals_used < max_evals and no_improve < no_improve_limit:
        neighbor = random_swap_neighbor(current_perm)
        neighbor_cost = bandwidth(neighbor, edges)
        evals_used += 1

        if neighbor_cost <= current_cost:
            current_perm = neighbor
            current_cost = neighbor_cost

            if current_cost < best_cost:
                best_cost = current_cost
                best_perm = current_perm[:]

            no_improve = 0
        else:
            no_improve += 1

    return best_perm, best_cost, evals_used

def hill_climber(n, edges, max_evals=100_000):
    perm = list(range(1, n + 1))
    random.shuffle(perm)

    evals_used = 0
    best_perm, best_cost, evals_used = local_search_hc(
        perm, edges, max_evals, evals_used, no_improve_limit_factor=10
    )

    return best_cost

def perturb_solution(perm, num_swaps=3):
    perturbed = perm[:]
    n = len(perturbed)
    for _ in range(num_swaps):
        i, j = random.sample(range(n), 2)
        perturbed[i], perturbed[j] = perturbed[j], perturbed[i]
    return perturbed


def iterated_local_search(n, edges, max_evals=100_000):
    current = list(range(1, n + 1))
    random.shuffle(current)

    evals_used = 0
    current, current_cost, evals_used = local_search_hc(
        current, edges, max_evals, evals_used, no_improve_limit_factor=5
    )

    best_perm = current[:]
    best_cost = current_cost

    while evals_used < max_evals:
        candidate = perturb_solution(best_perm, num_swaps=3)

        candidate, candidate_cost, evals_used = local_search_hc(
            candidate, edges, max_evals, evals_used, no_improve_limit_factor=5
        )

        if candidate_cost < best_cost:
            best_cost = candidate_cost
            best_perm = candidate[:]

    return best_cost

def simulated_annealing(n, edges, max_evals=100_000,
                        T0=10.0, alpha=0.995, Tmin=1e-6):
    current_perm = list(range(1, n + 1))
    random.shuffle(current_perm)

    current_cost = bandwidth(current_perm, edges)
    evals_used = 1

    best_cost = current_cost
    best_perm = current_perm[:]

    T = T0

    while evals_used < max_evals:
        neighbor = random_swap_neighbor(current_perm)
        neighbor_cost = bandwidth(neighbor, edges)
        evals_used += 1

        delta = neighbor_cost - current_cost

        if delta <= 0:
            current_perm = neighbor
            current_cost = neighbor_cost

            if current_cost < best_cost:
                best_cost = current_cost
                best_perm = current_perm[:]
        else:
            if T > 0:
                prob = math.exp(-delta / T)
            else:
                prob = 0.0

            if random.random() < prob:
                current_perm = neighbor
                current_cost = neighbor_cost

        # Cool down
        T = max(Tmin, T * alpha)

    return best_cost

def run_experiments(filename, runs=50, max_evals=100_000):
    # Load instance
    n, edges = load_graph(filename)
    print(f"Loaded graph with {n} vertices and {len(edges)} edges from {filename}")

    hc_costs = []
    ils_costs = []
    sa_costs = []

    # Hill-Climber runs
    print("Running Hill-Climber...")
    for r in range(runs):
        cost = hill_climber(n, edges, max_evals=max_evals)
        hc_costs.append(cost)
        print(f"  HC run {r + 1}/{runs}: cost = {cost}")

    # ILS runs
    print("Running Iterated Local Search...")
    for r in range(runs):
        cost = iterated_local_search(n, edges, max_evals=max_evals)
        ils_costs.append(cost)
        print(f"  ILS run {r + 1}/{runs}: cost = {cost}")

    # SA runs
    print("Running Simulated Annealing...")
    for r in range(runs):
        cost = simulated_annealing(n, edges, max_evals=max_evals)
        sa_costs.append(cost)
        print(f"  SA run {r + 1}/{runs}: cost = {cost}")

    def summarize(name, values):
        avg = sum(values) / len(values)
        print(f"{name}: min = {min(values)}, mean = {avg:.2f}, max = {max(values)}")

    print("\n=== Summary (final bandwidth costs over runs) ===")
    summarize("Hill-Climber", hc_costs)
    summarize("ILS", ils_costs)
    summarize("SA", sa_costs)

    # Boxplot
    plt.figure()
    plt.boxplot([hc_costs, ils_costs, sa_costs],
                labels=["HC", "ILS", "SA"])
    plt.ylabel("Bandwidth (cost)")
    plt.title(f"Bandwidth comparison over {runs} runs\n(max_evals = {max_evals})")
    plt.grid(True, axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    FILENAME = os.path.join(script_dir, "ash85.txt")
    run_experiments(FILENAME, runs=50, max_evals=100_000)
