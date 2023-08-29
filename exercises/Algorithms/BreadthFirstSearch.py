from exercises.Model import Graph


class BreadthFirstSearch:

    def __init__(self):
        self.graph = Graph()
        self.queue = list()
        self.visited = list()

    def add_edge(self, node, edge):
        self.graph.add_edge(node, edge)

    def add_node(self, node):
        self.graph.add_node(node)

    def remove_node(self, node):
        self.graph.remove_node(node)

    def remove_edge(self, node, edge):
        self.graph.remove_edge(node, edge)

    def bfs(self, node):
        self.queue.append(node)
        while self.queue:
            node = self.queue.pop(0)
            if node not in self.visited:
                self.visited.append(node)
                for i in self.graph.graph[node]:
                    self.queue.append(i)
        return self.visited
