# Singly linked-list node that wraps a single Block and points to the next one.
class Node:
    data = None  # the Block stored in this node
    next = None  # reference to the following Node (None at the tail)

    def __init__(self,data):
        self.data = data
