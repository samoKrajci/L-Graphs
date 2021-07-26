import itertools as it
from pattern_elimination import num_to_perm
from graph_utils import read_graph, random_graph, paint_lgraph, print_graph
import time
from bruteforce_smarter import try_order
from concurrent.futures import ProcessPoolExecutor, as_completed
from random import shuffle
from math import factorial
from multiprocessing import cpu_count


def permutation_from_number(number, length):
    remaining = list(range(length))
    ret = []
    for i in range(length-1, -1, -1):
        index_remove = number // factorial(i)
        number %= factorial(i)
        ret.append(remaining[index_remove])
        remaining.pop(index_remove)
    return ret


def try_orders(g, order_left, order_right):
    print('start try_order')
    for order_num in range(order_left, order_right):
        order = num_to_perm(order_num, len(g))

        heights, lengths = try_order(order, g)
        if not lengths:
            continue
        print('end try_order')
        return order, heights, lengths
    print('end try_order')
    return False, False, False


def split_permutations(n, groups_count):
    print('start split_permutations')
    p = list(it.permutations(range(n)))
    ret = []
    seg_size = factorial(n)/groups_count
    for i in range(groups_count):
        ret.append(p[round(seg_size*i): round(seg_size*(i+1))])
    print('end split_permutations')
    return ret


def get_lgraph(g):
    # permutations_batches = split_permutations(len(g), cpu_count())

    print('pred ppe')
    executor = ProcessPoolExecutor()
    print('po ppe')
    seg_size = factorial(len(g))/cpu_count()
    processes = map(lambda i: executor.submit(
        try_orders, g, round(seg_size*i), round(seg_size*(i+1))), range(cpu_count()))

    for process in as_completed(processes):
        order, heights, lengths = process.result()
        if order:
            map(lambda p: p.cancel(), processes)
            return order, heights, lengths

    print('given graph is not an L-graph')
    return False, False, False


def main():
    # graph = read_graph()
    graph = random_graph(13, 15)
    print_graph(graph)

    tic = time.perf_counter()
    order, heights, lenghts = get_lgraph(graph)
    toc = time.perf_counter()
    print(f"Finding an ordering took {toc - tic:0.4f} seconds")

    if order:
        paint_lgraph(order, heights, lenghts)


if __name__ == "__main__":
    main()
