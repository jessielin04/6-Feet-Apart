import csv
import sys
import time
from pathlib import Path

from hash_map_graph import HashMapGraph
from redblacktree_graph import RBTreeGraph
from BFS import bfs_shortest_path

def load_graphs(path: str, skip_header: bool = False) -> tuple[HashMapGraph, RBTreeGraph, float, float]:
    hm = HashMapGraph()
    rbt = RBTreeGraph()
    edges: list[tuple[int, int]] = []

    with open(path, newline="") as f:
        reader = csv.reader(f)
        if skip_header:
            next(reader, None)
        for row in reader:
            if len(row) < 2:
                continue
            try:
                u, v = int(row[0].strip()), int(row[1].strip())
                edges.append((u, v))
            except ValueError:
                continue

    t0=time.perf_counter()
    for u, v in edges:
        hm.add_edge(u, v)
    hm_ms=(time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    for u, v in edges:
        rbt.add_edge(u, v)
    rbt_ms = (time.perf_counter() - t0) * 1000

    return hm, rbt, hm_ms, rbt_ms


DEMO_EDGES = [
    (1, 2), (1, 3), (2, 4), (3, 4), (4, 5),
    (5, 6), (6, 7), (7, 8), (8, 9), (9, 10),
    (3, 7), (2, 8), (1, 10), (5, 10), (6, 3),
]

def build_demo_graphs() -> tuple[HashMapGraph, RBTreeGraph]:
    hm = HashMapGraph()
    rbt = RBTreeGraph()
    for u, v in DEMO_EDGES:
        hm.add_edge(u, v)
        rbt.add_edge(u, v)
    return hm, rbt


def run_bfs_comparison(hm: HashMapGraph, rbt: RBTreeGraph, source: int, target: int) -> None:
    hm_result = bfs_shortest_path(hm, source, target, struct_name="Hash Map Graph")
    rbt_result = bfs_shortest_path(rbt, source, target, struct_name="Red-Black Tree Graph")

    sep = "-" * 100
    print(sep)
    print(f"BFS: source={source}-> target={target}")
    print(sep)
    print(hm_result.summary())
    print()
    print(rbt_result.summary())
    print(sep)

    if hm_result.degrees != rbt_result.degrees:
        print("WARNING: the path lengths will differ between structures")
    else:
        status = "reachable" if hm_result.found else "unreachable"
        print(f"Both structures agree; The node pair is {status}.")

    if hm_result.elapsed_ms > 0 and rbt_result.elapsed_ms > 0:
        faster_name = "Hash Map" if hm_result.elapsed_ms <= rbt_result.elapsed_ms else "Red-Black Tree"
        faster_ms = hm_result.elapsed_ms if faster_name == "Hash Map" else rbt_result.elapsed_ms
        slower_ms = rbt_result.elapsed_ms if faster_name == "Hash Map" else hm_result.elapsed_ms
        ratio = slower_ms / faster_ms
        print(f"{faster_name} BFS was {ratio:.2f}x faster ({faster_ms:.4f} ms vs {slower_ms:.4f} ms)")
    print(sep)
    print()


def print_build_summary(hm: HashMapGraph, rbt: RBTreeGraph, hm_ms: float = 0.0, rbt_ms: float = 0.0) -> None:
    print("\nSUMMARY OF GRAPHS")
    print("~" * 60)
    print(f"{hm!r}")
    if hm_ms:
        print(f"Build time: {hm_ms:,.2f} ms")
    print(f"  {rbt!r}")
    if rbt_ms:
        print(f"Build time: {rbt_ms:,.2f} ms")
    print("=" * 60)
    print()


def main() -> None:
    args = sys.argv[1:]
    skip_header = "--skip-header" in args
    args = [a for a in args if not a.startswith("--")]

    if not args:
        hm, rbt = build_demo_graphs()
        print_build_summary(hm, rbt)
        for src, tgt in [(1, 9), (1, 5), (2, 7), (10, 4), (1, 99)]:
            run_bfs_comparison(hm, rbt, src, tgt)
        return

    csv_path = args[0]
    if not Path(csv_path).exists():
        print(f"Error: file not found — {csv_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Graph loading from: {csv_path}")
    hm, rbt, hm_ms, rbt_ms = load_graphs(csv_path, skip_header=skip_header)
    print_build_summary(hm, rbt, hm_ms, rbt_ms)

    nodes = hm.all_nodes()
    if not nodes:
        print("Check your format, no nodes loaded.")
        sys.exit(1)

    if len(args) >= 3:
        try:
            source = int(args[1])
            target = int(args[2])
        except ValueError:
            print("Error: Integers must be utilized.", file=sys.stderr)
            sys.exit(1)
    else:
        source, target = nodes[0], nodes[min(len(nodes) - 1, 500)]
        print(f"[No source/target given — using nodes {source} and {target}]\n")

    run_bfs_comparison(hm, rbt, source, target)

    if len(nodes) >= 10:
        import random
        random.seed(42)
        print("Additional sampled BFS queries:")
        for _ in range(3):
            run_bfs_comparison(hm, rbt, random.choice(nodes), random.choice(nodes))


if __name__ == "__main__":
    main()
