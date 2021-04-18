import itertools as it
from graph_utils import paint_lgraph, print_graph, read_graph


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


def main():
    graph = read_graph()

    print_graph(graph)
    get_lgraph(graph)


if __name__ == "__main__":
    main()
