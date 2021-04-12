import itertools as it
import tkinter as tk


def print_graph(g):
    print(len(g))
    for k, v in g.items():
        print(k, ':', v)


def get_lgraph(g):
    n = len(g)
    for order in it.permutations(range(n)):
        for heights in it.permutations(range(n)):
            lengths = try_order_and_heights(order, heights, g)
            if not lengths:
                continue
            paint_lgraph(order, heights, lengths)
            return True
    print('given graph is not an L-graph')
    return False


def try_order_and_heights(order, heights, g):
    n = len(g)

    lengths = []
    for i in range(n):
        lengths.append(i)

    for node_order in range(n):
        end = False
        node = order[node_order]
        for i in range(node_order+1, n):
            other_node = order[i]
            if other_node in g[node]:
                if heights[node_order] < heights[i]:
                    # ok, predlzim ciaru
                    if end:
                        # uz sa neda ist dalej, lebo pretnem ciaru co nemam
                        return False
                    lengths[node_order] = i
                else:
                    # nedaju sa spojit vrcholy
                    return False
            else:
                if heights[node_order] < heights[i]:
                    # nemozem ist dalej, lebo pretnem ciaru co nemam
                    end = True
    return lengths


def paint_lgraph(order, heights, lengths):
    HEIGHT = 500
    WIDTH = HEIGHT
    n = len(order)
    UNIT = HEIGHT/(n+2)
    window = tk.Tk()

    c = tk.Canvas(height=HEIGHT, width=WIDTH, background='white')

    c.create_line(0, UNIT, (n+2)*UNIT, UNIT)

    for i, p in enumerate(zip(order, lengths, heights)):
        (o, l, h) = p
        c.create_text((i+1)*UNIT, UNIT/2, text=str(o))
        c.create_line((i+1)*UNIT, UNIT, (i+1)*UNIT, (h+2)*UNIT)
        c.create_line((i+1)*UNIT, (h+2)*UNIT, (l+1.5)*UNIT, (h+2)*UNIT)

    c.pack()
    window.mainloop()


node_count, edge_count = map(int, input().split())

graph = {}
for i in range(node_count):
    graph[i] = []

for _ in range(edge_count):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

print_graph(graph)
get_lgraph(graph)
