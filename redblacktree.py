RED = True
BLACK = False


class Node:
    __slots__ = ("key", "color", "left", "right", "parent")

    def __init__(self, key, color=RED):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:


#ALWAYS BLACK
    def __init__(self):
        self.NIL = Node(key=None, color=BLACK)
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL
        self.root = self.NIL
        self.size = 0

    def insert(self, key) -> None:
        if self.contains(key): #SKIPS KEYS THAT MAY REPEAT
            return

        z = Node(key) #CREATES RED node with empty children
        z.left = self.NIL
        z.right = self.NIL
        z.parent = self.NIL

        y = self.NIL #for insertion...
        x = self.root
        while x is not self.NIL:
            y = x
            x = x.left if z.key < x.key else x.right

        z.parent = y #empty
        if y is self.NIL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        self.size += 1 #post insertion
        self.insert_fixup(z)

    def contains(self, key) -> bool:
        return self.search(self.root, key) is not self.NIL

    def delete(self, key) -> None:
        z = self.search(self.root, key)
        if z is self.NIL:
            return
        self.delete_node(z)
        self.size -= 1

    def min(self):
        if self.root is self.NIL:
            return None
        return self.minimum(self.root).key

    def max(self):
        if self.root is self.NIL:
            return None
        return self.maximum(self.root).key

    def __len__(self) -> int:
        return self.size

    def __bool__(self) -> bool:
        return self.size > 0

    def __iter__(self):
        yield from self.inorder(self.root) #inorder traversal

    def __repr__(self) -> str:
        return f"RedBlackTree(size={self.size})"

    def search(self, node, key):
        while node is not self.NIL and node.key != key:
            node = node.left if key < node.key else node.right
        return node #key not found, returns "NIL"--> BST search


#below is inorder traversal
    def inorder(self, node):
        if node is not self.NIL:
            yield from self.inorder(node.left)
            yield node.key
            yield from self.inorder(node.right)

    def minimum(self, node): #leftmost node= min key
        while node.left is not self.NIL:
            node = node.left
        return node

    def maximum(self, node): #rightmost node=max key
        while node.right is not self.NIL:
            node = node.right
        return node

    def left_rotate(self, x): #for left rotation
        y = x.right
        x.right = y.left
        if y.left is not self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is self.NIL:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y): #right rotation
        x = y.left
        y.left = x.right
        if x.right is not self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is self.NIL:
            self.root = x
        elif y is y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def insert_fixup(self, z): #for violations/mistakes
        while z.parent.color is RED:
            if z.parent is z.parent.parent.left:
                uncle = z.parent.parent.right
                if uncle.color is RED:
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.right_rotate(z.parent.parent)
            else:
                uncle = z.parent.parent.left
                if uncle.color is RED:
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.left_rotate(z.parent.parent)

        self.root.color = BLACK #REMEMBER ROOT IS ALWAYS BLACK

    def transplant(self, u, v):
        if u.parent is self.NIL:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_node(self, z):
        y = z
        y_original_col = y.color

        if z.left is self.NIL: # NO LEFT child
            x = z.right
            self.transplant(z, z.right)
        elif z.right is self.NIL: #NO RIGHT child
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right) #2 children
            y_original_col = y.color
            x = y.right
            if y.parent is z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_col is BLACK:
            self.delete_fixup(x)

    def delete_fixup(self, x):
        while x is not self.root and x.color is BLACK:
            if x is x.parent.left:
                w = x.parent.right
                if w.color is RED: #sibling=red
                    w.color = BLACK
                    x.parent.color = RED
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color is BLACK and w.right.color is BLACK:
                    w.color = RED #siblings children=black
                    x = x.parent
                else:
                    if w.right.color is BLACK: #sibling right child=black
                        w.left.color = BLACK
                        w.color = RED
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color is RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color is BLACK and w.left.color is BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color is BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = BLACK
