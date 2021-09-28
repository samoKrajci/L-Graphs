from graph_utils import random_graph, paint_lgraph, print_graph, num_to_perm, read_graph
import bruteforce_smarter as bs
import pattern_elimination as pe

from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from math import factorial
import signal
import psutil
import os
import time


def kill_child_processes(parent_pid, sig=signal.SIGTERM):
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)
    for process in children:
        process.send_signal(sig)


def try_orders_in_range(g, order_left, order_right, try_order_func):
    for order_num in range(order_left, order_right):
        order = num_to_perm(order_num, len(g))

        heights, lengths = try_order_func(order, g)
        if not lengths:
            continue
        return order, heights, lengths
    return False, False, False


def get_lgraph_parallel(g, try_order_func):
    if len(g) == 0:
        return [], [], []
    executor = ProcessPoolExecutor()
    seg_size = factorial(len(g))/cpu_count()
    processes = map(lambda i: executor.submit(
        try_orders_in_range, g, round(seg_size*i), round(seg_size*(i+1)), try_order_func), range(cpu_count()))

    for process in as_completed(processes):
        order, heights, lengths = process.result()
        if order:
            map(lambda p: p.cancel(), processes)
          
            kill_child_processes(os.getpid())

            return order, heights, lengths

    print('given graph is not an L-graph')
    return False, False, False


def paint_lgraph_from_file(file: str='./graph.txt', master: any=None, verbose: bool=False):
    graph = read_graph(file=file)
    if verbose:
        print_graph(graph)

    tic = time.perf_counter()
    order, heights, lenghts = get_lgraph_parallel(graph, pe.try_order)
    toc = time.perf_counter()
    if verbose:
        print(f"Finding an ordering took {toc - tic:0.4f} seconds")

    if order:
        paint_lgraph(order, heights, lenghts, master=master)


if __name__ == "__main__":
    paint_lgraph_from_file()
