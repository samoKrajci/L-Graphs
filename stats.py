from bruteforce_smarter import try_order
from graph_utils import random_graph
import matplotlib.pyplot as plt
import itertools as it


def good_order_ratio(g, verbose=False):
    '''
    vrati pocet dobrych a zlych usporiadani grafu
    pripadne aj vypise vsetky dobre usporiadania
    '''
    n = len(g)
    good = 0
    bad = 0
    good_orderings = []
    for order in it.permutations(range(n)):
        # Pre kazde mozne poradie skusime skonstruovat nakreslenie
        heights, lengths = try_order(order, g)
        if not lengths:
            bad += 1
        else:
            good += 1
            good_orderings.append(order)

    if verbose:
        for ordering in good_orderings:
            print(ordering)
    return good, bad


def stats_for_size(node_count, measurements):
    '''
    pre dany pocet vrcholov vrati array pomerov pre kazdy pocet hran
    pre kazdy pocet hran je vykonanych `measurement` merani
    '''
    averages = []
    for edge_count in range(1, (node_count*(node_count-1))//2+1):
        good_total = 0
        bad_total = 0
        for _ in range(measurements):
            graph = random_graph(node_count, edge_count)
            good, bad = good_order_ratio(graph)
            good_total += good
            bad_total += bad
        ratio = good_total / (good_total + bad_total)
        averages.append(ratio)
    return averages


def stats_up_to_size(max_node_count, measurements):
    '''
    zavola funkciu stats_for_size pre grafy velkosti od 3 po `max_node_count`
    '''
    averagess = []
    for node_count in range(3, max_node_count+1):
        print(node_count)
        stats = stats_for_size(node_count, measurements)
        averagess.append(stats)
    return averagess


def plot_multiple(data):
    '''
    plotne array kriviek
    '''
    for i, ar in enumerate(data):
        plt.plot(ar, label=str(i+3))

    plt.ylim([0, 1.1])
    plt.xlabel('number of edges')
    plt.ylabel('good/all ratio')
    plt.show()


def main():
    plot_multiple(stats_up_to_size(5, 100))

    # good_order_ratio(random_graph(7, 10), True)


if __name__ == "__main__":
    main()
