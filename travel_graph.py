#!/usr/bin/python

import csv

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

def print_usage(args=None, g=None):
    print "Usage:"
    print "\tadd <from> <to> <date> <price> | <id>"
    print ("\tadds a node to the graph. If node was previously removed, re-add"
            " using <id>.\n")
    print "\texport <filename>"
    print "\texports current graph to filename.\n"
    print "\timport <filename>"
    print "\timports a graph from filename.\n"
    print "\tlist [--removed | --all]"
    print "\tlists current edges. "
    print "\tIf --removed option is set, removed edges will be displayed. "
    print "\tIf --all option is set, all edges will be displayed.\n"
    print "\tpath <start> <end>"
    print "\tdisplays shortest path from <start> to <end>.\n"
    print "\tquit"
    print "\tquits the program.\n"
    print "\tremove <from> <to> <date> <price> | <id>"
    print "\tremoves the specified node from the graph."

def import_graph(args, g):
    if len(args) != 2:
        return False
    fname = args[1]
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
    print "Successfully imported graph from %s !"%fname

def export_graph(args, g):
    if len(args) != 2:
        return False
    fname = args[1]
    with open(fname, 'w') as outfile:
        outfile.write(str(g))
        outfile.close()
    print "Successfully wrote graph to %s !"%fname
    return True
    
def add_edge_to_graph(args, g):
    n_args = len(args)
    try:
        if n_args == 2:
            edge_id = int(args[1])
            edge = g.get_edge(edge_id)
            if edge:
                edge[3] = True
                return True
            else:
                return False
        elif n_args == 5:
            from_a = args[1]
            to_b = args[2]
            date = args[3]
            price = float(args[4])
            g.add_edge(from_a, to_b, date, price)
            return True
        else:
            return False
    except ValueError:
        return False

def remove_edge_from_graph(args, g):
    try:
        if len(args) == 2:
            edge_id = int(args[1])
            edge = g.get_edge(edge_id)
            if edge:
                edge[3] = False
                return True
            else:
                return False
        else:
            return False
    except ValueError:
        return False

def find_shortest_path(args, g):
    if len(args) != 3:
        return False
    start = args[1]
    end = args[2]
    shortest_path = g.shortest_path(start, end)
    total_price = g.distance(shortest_path)
    print "%s-->"%start
    for to_b, date, price in shortest_path:
        print "%s\t\t%s\t\t$%.2f"%(to_b, date, price)
    print "TOTAL PRICE:\t$%.2f"%total_price

def list_edges(args, g):
    if len(args) > 2:
        return False
    if len(args) == 1:
        g.list_edges()
    else:
        arg = args[1]
        if arg == '--removed':
            g.list_edges(False, True)
        elif arg == '--all':
            g.list_edges(True, True)
        else:
            return False
    return True

IMPORT = 'import'
PATH = 'path'
ADD = 'add'
REMOVE = 'remove'
LIST = 'list'
EXPORT = 'export'
QUIT = 'quit'
USAGE = 'usage'
CMD_LIST = [USAGE, IMPORT, EXPORT, PATH, LIST, ADD, REMOVE, QUIT] 

def parse_and_execute_cmd(cmd, g):
    args = cmd.split(' ')
    func_dict = {  
        # dictionary containing functions for executing commands.
        # each takes args as its argument and return True or False.
        IMPORT  : import_graph,
        EXPORT  : export_graph,
        ADD     : add_edge_to_graph,
        REMOVE  : remove_edge_from_graph,
        PATH    : find_shortest_path,
        LIST    : list_edges,
        USAGE   : print_usage,
        QUIT    : None
    }
    cmd_func = func_dict.get(args[0], print_usage)
    if cmd_func:
        return cmd_func(args, g)
    else:
        return True

def main():
    g = Graph()
    PROMPT = '"._.)> '
    cmd = ''
    while cmd != QUIT:
        cmd = raw_input(PROMPT)
        if cmd == '':
            continue
        success = parse_and_execute_cmd(cmd, g)
        
if __name__ == '__main__':
    main()
