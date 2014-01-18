import sys
import csv

class Graph():
    def __init__(self):
        self.graph = {}
    def add_edge(self, from_a, to_b, date, price):
        if from_a not in self.graph:
            self.graph[from_a] = {}
        self.graph[from_a][to_b] = (date, price)
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
                date, price = val
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

g = Graph()
fname = sys.argv[1]
start = sys.argv[2]
end = sys.argv[3]
with open(fname, 'rb') as gfile:
    reader = csv.reader(gfile)
    for row in reader:
        if len(row) != 4:
            continue
        from_a = row[0]
        to_b = row[1]
        date = row[2]
        price = float(row[3])
        g.add_edge(from_a, to_b, date, price)
shortest_path = g.shortest_path(start, end)
for node in shortest_path:
    print "%s %s $%.2f"%node
total_price = g.distance(shortest_path)
print "total price: $%.2f"%total_price

