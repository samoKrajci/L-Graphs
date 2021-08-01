from graph_utils import random_graph
import bruteforce_smarter as bs
import pattern_elimination as pe
import parallelization
import time


def compare(get_lgraph_a, label_a, get_lgraph_b, label_b):
    '''
    compares two methods on a random graph
    '''
    graph = random_graph(11, 15)

    tic = time.perf_counter()
    get_lgraph_a(graph)
    toc = time.perf_counter()
    print(
        f"Finding an ordering with {label_a} took {toc - tic:0.4f} seconds")

    tic = time.perf_counter()
    get_lgraph_b(graph)
    toc = time.perf_counter()
    print(f"Finding an ordering with {label_b} took {toc - tic:0.4f} seconds")


if __name__ == "__main__":
    compare(lambda g: parallelization.get_lgraph_parallel(
        g, pe.try_order), 'parallel', pe.get_lgraph, 'bruteforce')
