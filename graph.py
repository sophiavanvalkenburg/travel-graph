from datetime import datetime

class Graph():
    def __init__(self):
        self.graph = {}
        self.next_id = 0
        self.EARLIEST_DATE = datetime(2014, 1, 1)
        self.YEAR = 2014
    def edges(self):
        for from_a, to_b_dict in self.graph.items():
            for to_b, edges in to_b_dict.items():
                for i, edge in enumerate(edges):
                    yield self.graph[from_a][to_b][i]
    def clear(self):
        self.graph = {}
        self.next_id = 0
    def list_edges(self, show_enabled=True, show_disabled=False):
        for edge in self.edges():
            edge_id, from_a, to_b, raw_date, price, enabled = edge
            date = datetime.strftime(raw_date, '%m/%d')
            enabled_str = 'enabled' if enabled else 'disabled'
            edge_str = "%d:\t%s->%s\t%s\t$%.2f\t%s"%(edge_id, from_a, 
                    to_b, date, price, enabled_str)
            if enabled and show_enabled:
                print edge_str
            elif not enabled and show_disabled:
                print edge_str
    def get_edge(self, target_edge_id):
        for edge in self.edges():
            edge_id, from_a, to_b, date, price, enabled = edge
            if edge_id == target_edge_id:
                return edge
    def add_edge(self, from_a, to_b, date, price):
        if from_a not in self.graph:
            self.graph[from_a] = {}
        if to_b not in self.graph[from_a]:
            self.graph[from_a][to_b] = []
        date = datetime.strptime(date, '%m/%d')
        date = date.replace(year=self.YEAR)
        self.graph[from_a][to_b].append([self.next_id, from_a, to_b, date,
            price, True])
        self.next_id += 1
    def remove_edge(self, edge):
        edge_id, from_a, to_b, date, price, enabled = edge
        self.graph[from_a][to_b].remove(edge)
    def disable_edge(self, edge):
        edge[5] = False
    def enable_edge(self, edge):
        edge[5] = True
    def neighbors(self, from_a):
        if from_a not in self.graph:
            return {}
        else:
            return self.graph[from_a]
    def path_contains(self, path, from_stops, to_stops):
        path_from_stops = []
        path_to_stops = []
        for edge in path:
            from_a = edge[1]
            to_b = edge[2]
            path_from_stops.append(from_a)
            path_to_stops.append(to_b)
        return (sorted(path_from_stops) == sorted(from_stops)
                and sorted(path_to_stops) == sorted(to_stops))
    def ham_paths(self, from_a, to_b, from_stops=None, to_stops=None):
        """
        brute-force method for computing hamiltonian paths from a to b
        """
        if from_stops is None:
            from_stops = self.graph.keys()
        if to_stops is None:
            to_stops = self.graph.keys()
            to_stops.append(to_b)
            to_stops.remove(from_a)
        # every path from a to b
        paths = self.paths(from_a, to_b)
        # filter paths that contain all stops
        ham_paths = [ p for p in paths 
                if self.path_contains(p, from_stops, to_stops) ]
        return ham_paths
    def paths(self, from_a, to_b):
        def helper(from_a, to_b, all_paths, seen_edges, last_date):
            if from_a not in all_paths:
                all_paths[from_a] = []
            neighbors = self.neighbors(from_a)
            if neighbors == {}:
                return []
            for n, edges in neighbors.items():
                for edge in edges:
                    _, _, _, date, price, enabled = edge
                    if not enabled or date <= last_date:
                        continue
                    if edge not in seen_edges:
                        seen_edges.append(edge)
                        if n != to_b:
                            new_paths = helper(n, to_b, all_paths, seen_edges, 
                                    date)
                        else:
                            new_paths = [[]]
                        paths_from_a_to_b = [ [edge] + p for p in new_paths ]
                        all_paths[from_a].extend(paths_from_a_to_b)
            return all_paths[from_a]
        return helper(from_a, to_b, {}, [], self.EARLIEST_DATE)
    def shortest_ham_path(self, from_a, to_b):
        ham_paths = self.ham_paths(from_a, to_b)
        if ham_paths == []:
            return []
        return min(ham_paths, key=self.distance)
    def shortest_path(self, from_a, to_b):
        def helper(from_a, to_b, current_path, last_date):
            paths = []
            neighbors = self.neighbors(from_a)
            if neighbors == {}:
                return []
            for n, edges in neighbors.items():
                for edge in edges:
                    _, _, _, date, price, enabled = edge
                    if not enabled or date <= last_date:
                        continue
                    if edge not in current_path:
                        new_path = current_path + [edge]
                        if n != to_b:
                            new_path = helper(n, to_b, new_path, date)
                        if new_path != []:
                            paths.append(new_path)
            if paths == []:
                return []
            else:
                return min(paths, key=self.distance)
        return helper(from_a, to_b, [], self.EARLIEST_DATE)
    def distance(self, path):
        return sum( p[4] for p in path )
    def path_str(self,path):
        path_str = ''
        for edge in path:
            _, from_a, to_b, date, price, _ = edge
            date = datetime.strftime(date, '%m/%d')
            path_str += "%s->%s\t%s\t$%.2f\n"%(from_a, to_b, date, price)
        path_str += "\nTOTAL PRICE: $%.2f"%self.distance(path)
        return path_str 
    def __str__(self):
        graph_str = ''
        for edge in self.edges():
            edge_id, from_a, to_b, raw_date, price, enabled = edge
            date = datetime.strftime(raw_date, '%m/%d')
            if enabled:
                graph_str += "%s,%s,%s,%.2f\n"%(from_a, to_b, date, price)
        return graph_str


