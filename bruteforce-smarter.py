import itertools as it
import tkinter as tk
import numpy as np


def print_graph(g):
    print(len(g))
    for k, v in g.items():
        print(k, ':', v)


def get_lgraph(g):
    n = len(g)
    for order in it.permutations(range(n)):
        # Pre kazde mozne poradie skusime skonstruovat nakreslenie
        heights, lengths = try_order(order, g)
        if not lengths:
            continue
        paint_lgraph(order, heights, lengths)
        return True
    print('given graph is not an L-graph')
    return False


def try_order(order, g):
    '''
    Pre dane poradie vrcholov skusi skonstruovat nakreslenie
    rovnakym sposobom ako je v paperi.
    Bezi v O(n^2)
    '''
    n = len(g)

    # toto by mal byt linked list, ale nic take v Pythone nie je a aj tak to nebude omnoho rychlejsie...
    vert_order = []
    lengths = []
    for _ in range(n):
        lengths.append(0)

    for i, v in enumerate(order):
        min_height = get_min_height(v, i, vert_order, lengths, g)
        if min_height == -1:
            return False, False
        vert_order.insert(min_height, v)
        lengths[v] = get_min_length(v, i, order, g)

    return vert_order, lengths


def get_min_height(v, v_index, vert_order, lengths, g):
    '''
    pre dany vrchol zisti najmensiu potrebnu vysku
    (tak aby sa pretol s potrebnymi vrcholmi)
    '''
    min_height = 0
    cant_be_longer = False
    for i, other in enumerate(vert_order):
        if other in g[v]:
            if cant_be_longer:
                return -1
            min_height = i+1
        elif lengths[other] >= v_index:
            cant_be_longer = True
    return min_height


def get_min_length(v, v_index, order, g):
    '''
    pre dany vrchol zisti najmensiu potrebnu dlzku
    '''
    min_length = v_index
    for i, other in enumerate(order[v_index+1:]):
        if other in g[v]:
            min_length = v_index + i + 1
    return min_length


def flip_array(array):
    '''
    pomocna funkcia ktora z array[i] = j vyrobi array[j] = i
    '''
    f_array = []
    for _ in range(len(array)):
        f_array.append(0)

    for i, a in enumerate(array):
        f_array[a] = i
    return f_array


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

    flipped_heights = flip_array(heights)

    c = tk.Canvas(height=HEIGHT, width=WIDTH, background='white')

    c.create_line(0, UNIT, (n+2)*UNIT, UNIT)

    for i, o in enumerate(order):
        l, h = lengths[o], flipped_heights[o]
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
