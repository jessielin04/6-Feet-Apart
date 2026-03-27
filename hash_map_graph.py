from collections import defaultdict


class HashMapGraph:

    def __init__(self):
        self.adj: dict[int, set[int]] = defaultdict(set)
        self.edge_count: int = 0

    def add_edge(self, u: int, v: int) -> None:
        if v not in self.adj[u]:
            self.adj[u].add(v)
            self.adj[v].add(u)
            self.edge_count += 1

    def add_node(self, u: int) -> None:
        _ = self.adj[u]

    def neighbors(self, u: int):
        return self.adj.get(u, frozenset())

    def has_node(self, u: int) -> bool:
        return u in self.adj

    def has_edge(self, u: int, v: int) -> bool:
        s = self.adj.get(u)
        return s is not None and v in s

    def all_nodes(self) -> list[int]:
        return list(self.adj.keys())

    @property
    def node_count(self) -> int:
        return len(self.adj)

    def __repr__(self) -> str:
        return (
            f"HashMapGraph(nodes={self.node_count:,}, "
            f"edges={self.edge_count:,})"
        )
