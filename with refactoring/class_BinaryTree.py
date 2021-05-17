from random import randint
class Node:
    def __init__(self, node,number):
        self.node = node
        self.left = None
        self.right = None
        self.number = number


    def add(self, value,number):
        if value < self.node:
            if self.left is None:
                self.left = Node(value,number)
            else:
                self.left.add(value,number)
        elif value > self.node:
            if self.right is None:
                self.right = Node(value,number)
            else:
                self.right.add(value,number)


def printTree(tree, level=0,rec=1):
    try:
        if tree.node is not None:
            printTree(tree.left, level + 1,rec+1)
            print(' ' * 4 * level + str(rec) + "№:" + str(tree.number) + ' ->' + str(tree.node))
            printTree(tree.right, level + 1,rec+1)
    except AttributeError:
        pass


