from math import factorial
from graph_utils import read_graph, paint_lgraph, print_graph, random_graph, num_to_perm
from bruteforce_smarter import try_order
from itertools import combinations
import numpy as np
import time


def get_lgraph(g):
    '''
    skusame vsetky permutacie iterovanim cez n! "cisel permutacie",
        v kazdej najdeme prvy zakazany pattern a zahodime vsetky moznosti
        v ktorych sa nachadza
    '''
    n = len(g)
    perm_num = 0
    perms_visited = 0
    first_distinct_index = 0
    while perm_num < factorial(n):
        perms_visited += 1
        order = num_to_perm(perm_num, n)

        # zakazane patterny nam staci pozerat od `first_distinct_index`, tie pred tym sme uz pozreli
        next_perm_num = get_next_perm_num(perm_num, first_distinct_index, g)

        if not next_perm_num:
            # ak get_next_perm_num vratilo False, tak v usporiadani nie je zakazany pattern
            #   a nasli sme teda dobre usporiadanie
            print(f'visited/all: {perms_visited / perm_num:0.6f}')
            heights, lengths = try_order(order, g)
            return order, heights, lengths

        if next_perm_num >= factorial(n):
            # presli sme vsetky permutacie
            break
        # prvy rozny index aktualnej a nasledujucej permutacie
        first_distinct_index = get_first_distinct_index(
            order, num_to_perm(next_perm_num, n))
        perm_num = next_perm_num
    print('given graph is not an L-graph')
    return False, False, False


def get_first_distinct_index(la, lb):
    '''
    vrati prvy odlisny index dvoch arrayov
    '''
    index = 0
    for a, b in zip(la, lb):
        if not (a == b):
            return index
        index += 1


def get_next_perm_num(perm_num, start_index, g):
    '''
    postupne pozera vsetky vrcholy od `start_index` a zistuje, 
        ci sa tam nachadza forbidden pattern.
        Ak nie, vrati false,
        ak ano, zmeni prvy index na ktorom nejaky pattern konci 
        a vrati cislo danej permutacie
    '''
    n = len(g)
    perm = num_to_perm(perm_num, n)
    for i in range(start_index, n):
        if forbidden_pattern(perm, i, g):
            # print(i)
            return perm_num + factorial(n-i-1)
    return False


def forbidden_pattern(perm, index, g):
    '''
    checkne, ci vrchol na danom indexe tvori zakazany pattern
        s nejakou trojicou vrcholov nalavo 
    '''
    for comb in combinations(perm[:index], 3):
        comb_full = np.append(np.asarray(comb), perm[index])
        # print(comb_full)
        a = is_pattern_a(g, comb_full)
        b = is_pattern_b(g, comb_full)
        if a or b:
            return True
    return False


def is_pattern_a(g, vl):
    '''
    checkne, ci vrcholy vl tvoria "prvy" zakazany pattern
    '''
    return (
        vl[2] in g[vl[0]] and
        vl[3] in g[vl[1]] and
        not (vl[1] in g[vl[0]]) and
        not (vl[2] in g[vl[1]])
    )


def is_pattern_b(g, vl):
    '''
    checkne, ci vrcholy vl tvoria "druhy" zakazany pattern
    '''
    return (
        vl[1] in g[vl[0]] and
        vl[2] in g[vl[1]] and
        vl[3] in g[vl[0]] and
        not (vl[2] in g[vl[0]])
    )


def main():
    graph = read_graph()
    print_graph(graph)

    tic = time.perf_counter()
    order, heights, lenghts = get_lgraph(graph)
    toc = time.perf_counter()
    print(f"Finding an ordering took {toc - tic:0.4f} seconds")

    if order:
        paint_lgraph(order, heights, lenghts)


if __name__ == "__main__":
    main()
