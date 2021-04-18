import numpy as np
import tkinter as tk


def read_graph():
    '''
    read graph from standard input
    '''
    node_count, edge_count = map(int, input().split())

    graph = {}
    for i in range(node_count):
        graph[i] = []

    for _ in range(edge_count):
        a, b = map(int, input().split())
        graph[a].append(b)
        graph[b].append(a)

    return graph


def random_graph(node_count, edge_count):
    assert edge_count >= 0 and 2*edge_count <= node_count * \
        (node_count -
         1), f'More edges than complete graph.\n\tNodes: {node_count}\n\tEdges: {edge_count}'

    graph = {}
    for i in range(node_count):
        graph[i] = []

    correction = 0
    for i, num in enumerate(np.random.permutation(range(node_count*(node_count-1)))):
        if i >= edge_count + correction:
            break
        a = num // node_count
        b = num % node_count
        if a == b or (b in graph[a]):
            correction += 1
        else:
            graph[a].append(b)
            graph[b].append(a)

    return graph


def paint_lgraph(order, heights, lengths):
    '''
    Funkcia iba vykresli graf ak vie poradie vrcholov a tvary L-iek
    '''

    print(order, heights, lengths)
    HEIGHT = 500
    WIDTH = HEIGHT
    n = len(order)
    UNIT = HEIGHT/(n+2)
    window = tk.Tk()

    c = tk.Canvas(height=HEIGHT, width=WIDTH, background='white')

    c.create_line(0, UNIT, (n+2)*UNIT, UNIT)

    for i, o in enumerate(order):
        l, h = lengths[o], heights[o]
        c.create_text((i+1)*UNIT, UNIT/2, text=str(o))
        c.create_line((i+1)*UNIT, UNIT, (i+1)*UNIT, (h+2)*UNIT)
        c.create_line((i+1)*UNIT, (h+2)*UNIT, (l+1.5)*UNIT, (h+2)*UNIT)

    c.pack()
    window.mainloop()


def print_graph(g):
    print(len(g))
    for k, v in g.items():
        print(k, ':', v)
