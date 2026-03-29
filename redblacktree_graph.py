from redblacktree import RedBlackTree #utilizes info from redblacktree.py file


class RBTreeGraph:

    def __init__(self):
        self.adj: dict[int, RedBlackTree] = {}
        self.edge_count: int = 0


#creates red-black tree adjacency list for node u
    def tree(self, u: int) -> RedBlackTree:
        if u not in self.adj:
            self.adj[u] = RedBlackTree()
        return self.adj[u]

    def add_edge(self, u: int, v: int) -> None:
        tu = self.tree(u)
        tv = self.tree(v) #for when graph is undirected or edge does not exist
        if not tu.contains(v):
            tu.insert(v)
            tv.insert(u)
            self.edge_count += 1

    def add_node(self, u: int) -> None:
        self.tree(u) #checks that node u exists in empty red-black tree


#repeats over u's neighbors to make sure it is in sorted order
    #travels tree through inorder traversal
    def neighbors(self, u: int):
        t = self.adj.get(u)
        return iter(t) if t is not None else iter([])

    def has_node(self, u: int) -> bool:
        return u in self.adj

    def has_edge(self, u: int, v: int) -> bool:
        t = self.adj.get(u)
        return t is not None and t.contains(v)

    def all_nodes(self) -> list[int]:
        return list(self.adj.keys())

    @property
    def node_count(self) -> int:
        return len(self.adj)

    def __repr__(self) -> str:
        return (
            f"Red-Black Tree Graph(nodes={self.node_count:,}, "
            f"edges={self.edge_count:,})"
        )
