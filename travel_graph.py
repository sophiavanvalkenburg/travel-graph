#!/usr/bin/python

import csv
from graph import Graph

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
    return True

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
                print "Successfully re-added edge %d."%edge_id
                return True
            else:
                return False
        elif n_args == 5:
            from_a = args[1]
            to_b = args[2]
            date = args[3]
            price = float(args[4])
            g.add_edge(from_a, to_b, date, price)
            print ("Successfully added edge from %s to %s on date %s for $%.2f."
                    %(from_a, to_b, date, price))
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
                print "Successfully removed edge %d."%edge_id
                return True
            else:
                return False
        else:
            return False
    except ValueError:
        return False

def find_paths(args, g):
    n_args = len(args)
    if n_args == 3:
        start = args[1]
        end = args[2]
        find_all_paths(g, start, end)
    elif n_args == 4:
        start = args[2]
        end = args[3]
        if args[1] == '--shortest':
            find_shortest_path(g, start, end)
        elif args[1] == '--ham':
            find_ham_paths(g, start, end)
        else:
            return False
    elif n_args == 5:
        start = args[3]
        end = args[4]
        if '--shortest' in args[1:3] and '--ham' in args[1:3]:
            find_shortest_ham_path(g, start, end)
    else:
        return False
    return True

def find_all_paths(g, start, end):
    all_paths = g.paths(start, end)
    all_paths.sort(key=g.distance)
    for path in all_paths:
        print "%s-->"%start
        print g.path_str(path)
        print "TOTAL PRICE: $%.2f"%g.distance(path)
        print "-----------------------------------"

def find_ham_paths(g, start, end):
    ham_paths = g.ham_paths(start, end)
    ham_paths.sort(key=g.distance)
    for path in ham_paths:
        print "%s-->"%start
        print g.path_str(path)
        print "TOTAL_PRICE: $%.2f"%g.distance(path)
        print "-----------------------------------"

def find_shortest_path(g, start, end):
    shortest_path = g.shortest_path(start, end)
    print "%s-->"%start
    print g.path_str(shortest_path)
    print "TOTAL PRICE: $%.2f"%g.distance(shortest_path)

def find_shortest_ham_path(g, start, end):
    shortest_ham_path = g.shortest_ham_path(start, end)
    print "%s-->"%start
    print g.path_str(shortest_ham_path)
    print "TOTAL PRICE: $%.2f"%g.distance(shortest_ham_path)

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

def parse_and_execute_cmd(cmd, g):
    args = cmd.split(' ')
    func_dict = {  
        # dictionary containing functions for executing commands.
        # each takes args as its argument and return True or False.
        'paths'     : find_paths,
        'import'    : import_graph,
        'export'    : export_graph,
        'add'       : add_edge_to_graph,
        'remove'    : remove_edge_from_graph,
        'list'      : list_edges,
        'usage'     : print_usage,
        'quit'      : None
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
    while cmd != 'quit':
        cmd = raw_input(PROMPT)
        if cmd == '':
            continue
        success = parse_and_execute_cmd(cmd, g)
        if not success:
            print ("Command '%s' did not succeed. "
                    "Was it in the wrong format?"%cmd)
        
if __name__ == '__main__':
    main()
