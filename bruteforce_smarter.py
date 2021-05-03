import itertools as it
import numpy as np
from graph_utils import read_graph, random_graph, paint_lgraph, print_graph
import time


def get_lgraph(g):
    n = len(g)
    for order in it.permutations(range(n)):
        # Pre kazde mozne poradie skusime skonstruovat nakreslenie
        heights, lengths = try_order(order, g)
        if not lengths:
            continue
        return order, heights, lengths
    print('given graph is not an L-graph')
    return False, False, False


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

    return flip_array(vert_order), lengths


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


def main():
    graph = read_graph()
    # graph = random_graph(11, 20)
    print_graph(graph)

    tic = time.perf_counter()
    order, heights, lenghts = get_lgraph(graph)
    toc = time.perf_counter()
    print(f"Finding an ordering took {toc - tic:0.4f} seconds")

    if order:
        paint_lgraph(order, heights, lenghts)


if __name__ == "__main__":
    main()
