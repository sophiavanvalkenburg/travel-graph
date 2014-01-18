
class Graph():
    def __init__(self):
        self.graph = {}
        self.next_id = 0
    def list_edges(self, show_enabled=True, show_disabled=False):
        for from_a, edges in self.graph.items():
            for to_b, edge in edges.items():
                edge_id, date, price, enabled = edge
                enabled_str = 'enabled' if enabled else 'disabled'
                edge_str = "%d:\t%s->%s\t\t%s\t$%.2f\t%s"%(edge_id, from_a, to_b,
                        date, price, enabled_str)
                if enabled and show_enabled:
                    print edge_str
                elif not enabled and show_disabled:
                    print edge_str
    def get_edge(self, target_edge_id):
        for from_a, edges in self.graph.items():
            for to_b, edge in edges.items():
                edge_id, date, price, enabled = edge
                if edge_id == target_edge_id:
                    return edge
    def add_edge(self, from_a, to_b, date, price):
        if from_a not in self.graph:
            self.graph[from_a] = {}
        self.graph[from_a][to_b] = [self.next_id, date, price, True]
        self.next_id += 1
    def neighbors(self, from_a):
        if from_a not in self.graph:
            return {}
        else:
            return self.graph[from_a]
    def shortest_path(self, from_a, to_b):
        def helper(from_a, to_b, current_path):
            paths = []
            neighbors = self.neighbors(from_a)
            if neighbors == {}:
                return []
            for n, val in neighbors.items():
                edge_id, date, price, enabled = val
                if not enabled:
                    continue
                node = (n, date, price)
                if node not in current_path:
                    new_path = current_path + [node]
                    if n != to_b:
                        new_path = helper(n, to_b, new_path)
                    if new_path != []:
                        paths.append(new_path)
            if paths == []:
                return []
            else:
                return min(paths, key=self.distance)
        return helper(from_a, to_b, [])
    def distance(self, path):
        # path is list of (to_b, date, price)
        return sum( price for to_b, date, price in path )
    def __str__(self):
        graph_str = ''
        for from_a, edges in self.graph.items():
            for to_b, edge in edges.items():
                edge_id, date, price, enabled = edge
                if enabled:
                    graph_str += "%s,%s,%s,%.2f\n"%(from_a, to_b, date, price)
        return graph_str


