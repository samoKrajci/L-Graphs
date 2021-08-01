import numpy as np
import tkinter as tk
from math import factorial


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


def draw_lgraph(canvas, unit, order, heights, lengths, bad_intersections=[]):
    n = len(order)
    canvas.delete('all')

    canvas.create_line(0, unit, (n+2)*unit, unit)

    for i, o in enumerate(order):
        l, h = lengths[o], heights[o]
        canvas.create_text((i+1)*unit, unit/2, text=str(o))
        canvas.create_line((i+1)*unit, unit, (i+1)*unit, (h+2)*unit)
        canvas.create_line((i+1)*unit, (h+2)*unit, (l+1.5)*unit, (h+2)*unit)

    for point in bad_intersections:
        canvas.create_oval(
            (point[0]+1)*unit-unit*0.1,
            (point[1]+1)*unit-unit*0.1,
            (point[0]+1)*unit+unit*0.1,
            (point[1]+1)*unit+unit*0.1,
            fill='red'
        )

    canvas.pack()


def paint_lgraph(order, heights, lengths, bad_intersections=[]):
    '''
    Funkcia iba vykresli graf ak vie poradie vrcholov a tvary L-iek
    '''

    HEIGHT = 500
    WIDTH = HEIGHT
    n = len(order)
    UNIT = HEIGHT/(n+2)
    window = tk.Tk()

    c = tk.Canvas(height=HEIGHT, width=WIDTH, background='white')

    draw_lgraph(c, UNIT, order, heights, lengths, bad_intersections)

    window.mainloop()


def print_graph(g):
    print(len(g))
    for k, v in g.items():
        print(k, ':', v)

def num_to_perm(num, n):
    '''
    prevedie cislo do faktorialovej sustavy a vrati zodpovedajucu permutaciu
    '''
    available = list(range(n))
    out = []
    i = n-1
    while i > 0:
        temp = num // factorial(i)
        out.append(available[temp])
        available.pop(temp)
        num %= factorial(i)
        i -= 1
    out.append(available[0])
    return out


