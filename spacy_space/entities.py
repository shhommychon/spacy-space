class DependencyEdge:
    def __init__(self, length:int, parent_index:int, child_index:int):
        self.length = length
        self.parent_index = parent_index
        self.child_index = child_index
    
    def __repr__(self):
        return f"DependencyEdge(length={self.length}, " \
               f"parent_index={self.parent_index}, " \
               f"child_index={self.child_index})"

    def __lt__(self, other):
        if self.length != other.length:
            return self.length > other.length
        elif self.parent_index != other.parent_index:
            return self.parent_index < other.parent_index
        else:
            return self.child_index < other.child_index