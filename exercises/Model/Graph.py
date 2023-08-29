class Graph(object):
    def __init__(self):
        self.graph = {}
        self.queue = list()

    def add_edge(self, node, edge):
        if node not in self.graph:
            self.graph[node] = [edge]
        else:
            self.graph[node].append(edge)

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def remove_node(self, node):
        if node in self.graph:
            del self.graph[node]
        for i in self.graph:
            if node in self.graph[i]:
                self.graph[i].remove(node)

    def remove_edge(self, node, edge):
        if node in self.graph:
            if edge in self.graph[node]:
                self.graph[node].remove(edge)
