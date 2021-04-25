class Node:
    def __init__(self, keys=None, father=None):
        if keys is None:
            keys = []
        elif isinstance(keys, int):
            keys = [keys]
        self.keys = keys
        self.children = []
        self.father = father

    def add(self, char):
        self.keys.append(char)
        self.keys = sorted(self.keys)

    def length(self):
        return len(self.keys)

    def has_children(self):
        return len(self.children)


class BTree:
    def __init__(self, t):
        self.t = t
        self.degree = (2 * t - 1)
        self.root = None

    def search(self, char):
        leaf = True
        if char in self.root.keys:
            return True
        else:
            search_array = self.root.children
            temp_array = []
            while leaf:
                for child in search_array:
                    if char in child.keys:
                        return True
                    if not child.has_children():
                        leaf = False
                    temp_array += child.children
                search_array = temp_array
            return False

    def insert(self, char, node=None):
        if self.root is None:
            self.root = Node(char)

        else:
            if node is None:
                node = self.root

            if node.has_children():
                for key in node.keys:
                    if char < key:
                        self.insert(char, node.children[node.keys.index(key)])
                self.insert(char, node.children[-1])

            else:
                if node.length() < self.degree:
                    node.add(char)

                else:
                    self.split(node)
                    self.insert(char)

    def split(self, node):
        if node.father is None:
            self.root = Node(node.keys[self.t - 1])
            left = Node(node.keys[:self.t - 1], self.root)
            for child in node.children[:self.t]:
                child.father = left
                left.children.append(child)
            right = Node(node.keys[self.t:], self.root)
            for child in node.children[self.t:]:
                child.father = right
                right.children.append(child)
            self.root.children = [left] + [right]

        else:
            if node.father.length() == self.degree:
                self.split(node.father)

            father = node.father
            father.add(node.keys[self.t - 1])
            index = father.keys.index(node.keys[self.t - 1])
            left = Node(node.keys[:self.t - 1], father)
            for child in node.children[:self.t]:
                child.father = left
                left.children.append(child)
            right = Node(node.keys[self.t:], father)
            for child in node.children[self.t:]:
                child.father = right
                right.children.append(child)
            father.children = father.children[:index] + [left] + [right] + father.children[index + 1:]

    def print_tree(self, node=None, line=''):
        if node is None:
            node = self.root

        line += '\t'

        if node.has_children():
            for index in reversed(range(len(node.children))):
                self.print_tree(node.children[index], line)
                if index != 0:
                    print(line + str(node.keys[index - 1]))

        else:
            print(line + str(node.keys))


tree = BTree(3)
for i in range(23):
    tree.insert(i)
tree.print_tree()

if tree.search(5):
    print('Found')
else:
    print('Not found')
