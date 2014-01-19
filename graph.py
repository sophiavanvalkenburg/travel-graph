from datetime import datetime

class Graph():
    def __init__(self):
        self.graph = {}
        self.next_id = 0
        self.EARLIEST_DATE = datetime(2014, 1, 1)
        self.YEAR = 2014
    def list_edges(self, show_enabled=True, show_disabled=False):
        for from_a, to_b_dict in self.graph.items():
            for to_b, edges in to_b_dict.items():
                for edge in edges:
                    edge_id, raw_date, price, enabled = edge
                    date = datetime.strftime(raw_date, '%m/%d')
                    enabled_str = 'enabled' if enabled else 'disabled'
                    edge_str = "%d:\t%s->%s\t%s\t$%.2f\t%s"%(edge_id, from_a, 
                            to_b, date, price, enabled_str)
                    if enabled and show_enabled:
                        print edge_str
                    elif not enabled and show_disabled:
                        print edge_str
    def get_edge(self, target_edge_id):
        for from_a, to_b_dict in self.graph.items():
            for to_b, edges in to_b_dict.items():
                for edge in edges:
                    edge_id, date, price, enabled = edge
                    if edge_id == target_edge_id:
                        return edge
    def add_edge(self, from_a, to_b, date, price):
        if from_a not in self.graph:
            self.graph[from_a] = {}
        if to_b not in self.graph[from_a]:
            self.graph[from_a][to_b] = []
        date = datetime.strptime(date, '%m/%d')
        date = date.replace(year=self.YEAR)
        self.graph[from_a][to_b].append([self.next_id, date, price, True])
        self.next_id += 1
    def neighbors(self, from_a):
        if from_a not in self.graph:
            return {}
        else:
            return self.graph[from_a]
    def path_contains(self, path, stops):
        path_stops = []
        for n, date, price in path:
            path_stops.append(n)
        return sorted(path_stops) == sorted(stops)
    def ham_paths(self, from_a, to_b, stops=None):
        """
        brute-force method for computing hamiltonian paths from a to b
        """
        if stops is None:
            stops = self.graph.keys()
            stops.append(to_b)
        # have to remove the start
        stops = [ s for s in stops if s != from_a ]
        # every path from a to b
        paths = self.paths(from_a, to_b)
        # filter paths that contain all stops
        ham_paths = [ p for p in paths if self.path_contains(p, stops) ]
        return ham_paths
    def paths(self, from_a, to_b):
        def helper(from_a, to_b, all_paths, seen_edges, last_date):
            if from_a not in all_paths:
                all_paths[from_a] = []
            neighbors = self.neighbors(from_a)
            if neighbors == {}:
                return []
            for n, vals in neighbors.items():
                for val in vals:
                    edge_id, date, price, enabled = val
                    if not enabled or date <= last_date:
                        continue
                    edge = (n, date, price)
                    if edge not in seen_edges:
                        seen_edges.append(edge)
                        if n != to_b:
                            new_paths = helper(n, to_b, all_paths, seen_edges, date)
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
            for n, vals in neighbors.items():
                for val in vals:
                    edge_id, date, price, enabled = val
                    if not enabled or date <= last_date:
                        continue
                    edge = (n, date, price)
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
        return helper(from_a, to_b, [], self.EARLIST_DATE)
    def distance(self, path):
        # path is list of (to_b, date, price)
        return sum( price for to_b, date, price in path )
    def path_str(self,path):
        path_str = ''
        for edge in path:
            n, date, price = edge
            date = datetime.strftime(date, '%m/%d')
            path_str += "%s\t%s\t$%.2f\n"%(n, date, price)
        return path_str 
    def __str__(self):
        graph_str = ''
        for from_a, to_b_edges in self.graph.items():
            for to_b, edges in to_b_edges.items():
                for edge in edges:
                    edge_id, raw_date, price, enabled = edge
                    date = datetime.strftime(raw_date, '%m/%d')
                    if enabled:
                        graph_str += "%s,%s,%s,%.2f\n"%(from_a, to_b, date, price)
        return graph_str


