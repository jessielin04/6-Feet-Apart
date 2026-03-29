import time
from collections import deque
from dataclasses import dataclass
from typing import Optional


@dataclass
class BFSResult:
    source: int
    target: int
    struct_name: str
    path: Optional[list[int]]
    nodes_visited: int
    elapsed_ms: float

    @property
    def degrees(self) -> Optional[int]:
        return (len(self.path) - 1) if self.path else None #edges in shortest path

    @property
    def found(self) -> bool:
        return self.path is not None #True if path exists

    def path_str(self) -> str: #produces path separated by arrows
        if not self.path:
            return "No connection found"
        return " -> ".join(str(uid) for uid in self.path)

    def summary(self) -> str: #summarizes data for BFS
        deg = f"{self.degrees} degree(s) of separation" if self.found else "unreachable"
        return (
            f"[{self.struct_name}]\n"
            f"  {deg}\n"
            f"  Path: {self.path_str()}\n"
            f"  Nodes visited: {self.nodes_visited:,}\n"
            f"  BFS time: {self.elapsed_ms:.4f} ms"
        )

    def to_dict(self) -> dict: #connects to flask
        return {
            "source": self.source,
            "target": self.target,
            "struct": self.struct_name,
            "path": self.path,
            "degrees": self.degrees,
            "found": self.found,
            "nodes_visited": self.nodes_visited,
            "elapsed_ms": round(self.elapsed_ms, 4),
        }


def bfs_shortest_path(
    graph,
    source: int,
    target: int,
    struct_name: str = "Graph",
) -> BFSResult:
    t0 = time.perf_counter()

    #if node is non-existent...
    if not graph.has_node(source) or not graph.has_node(target): 
        elapsed = (time.perf_counter() - t0) * 1000
        return BFSResult(source, target, struct_name, None, 0, elapsed)

    if source == target:
        elapsed = (time.perf_counter() - t0) * 1000
        return BFSResult(source, target, struct_name, [source], 1, elapsed)

    parent: dict[int, Optional[int]] = {source: None}
    queue: deque[int] = deque([source])
    nodes_visited = 0
    found = False

    #BFS loop
    while queue:
        current = queue.popleft()
        nodes_visited += 1

        for nbr in graph.neighbors(current):
            if nbr not in parent:
                parent[nbr] = current
                if nbr == target:
                    found = True
                    break
                queue.append(nbr)

        if found:
            break

    elapsed = (time.perf_counter() - t0) * 1000

    if not found:
        return BFSResult(source, target, struct_name, None, nodes_visited, elapsed)

    path: list[int] = []
    node: Optional[int] = target
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    return BFSResult(source, target, struct_name, path, nodes_visited, elapsed)
