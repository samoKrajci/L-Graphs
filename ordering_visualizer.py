from graph_utils import read_graph, draw_lgraph
import tkinter as tk
import argparse

parser = argparse.ArgumentParser(description='Grounded-L graph visualizer')

parser.add_argument(
    '-i', 
    '--input-file', 
    help='File with the input graph. ' 
    'Defauls to empty graph'
)

class Args:
    def __init__(self, input_file=None, output_file=None):
        self.input_file = input_file
        self.output_file = output_file


def try_order(order, g):
    '''
    Pre dane poradie vrcholov vrati najmensie nakreslenie take,
        aby tam boli vsetky prieniky (mozu byt aj navyse).
    Bezi v O(n^2)
    '''
    n = len(g)

    vert_order = []
    lengths = []
    bad_intersections = []
    for _ in range(n):
        lengths.append(0)

    for i, v in enumerate(order):
        min_height, bad_intersections_column = get_min_height(v, i, vert_order, lengths, g)
        vert_order.insert(min_height, v)
        lengths[v] = get_min_length(v, i, order, g)

        bad_intersections += list(map(
            lambda a: (i, a),
            bad_intersections_column
        ))
        
        bad_intersections = list(map(
            lambda pair: (pair[0], pair[1] + 1) if pair[1] > min_height else pair,  
            bad_intersections
        ))

    return flip_array(vert_order), lengths, bad_intersections


def get_min_height(v, v_index, vert_order, lengths, g):
    '''
    pre dany vrchol zisti najmensiu potrebnu vysku
    (tak aby sa pretol s potrebnymi vrcholmi)
    '''
    min_height = 0
    cant_be_longer = False
    bad_intersections = []
    for i, other in enumerate(vert_order):
        if other in g[v]:
            if cant_be_longer:
                return -1
            min_height = i+1
        elif lengths[other] >= v_index:
            bad_intersections.append(i+1)
    bad_intersections = filter(lambda a: a < min_height, bad_intersections)
    return min_height, bad_intersections


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

class Painter:
    def __init__(self, canvas, graph, unit):
        self.graph = graph
        self.n = len(graph)
        self.selected = -1
        
        self.canvas = canvas
        self.unit = unit
        self.order = list(range(self.n))

        self.repaint()

        self.canvas.bind("<Button-1>", self.callback)

        self.canvas.pack()

    def repaint(self):
        heights, lengths, bad_intersections = try_order(self.order, self.graph)
        draw_lgraph(self.canvas, self.unit, self.order, heights, lengths, bad_intersections)

    def change_order(self, a, b):
        removed = self.order.pop(a)
        self.order.insert(b, removed)
        
    def get_clicked_vertex(self, event):
        if event.y > self.unit:
            return -1
        return (event.x - self.unit / 2) // self.unit

    def callback(self, event):
        if self.selected == -1:
            self.selected = int(self.get_clicked_vertex(event))
            self.canvas.create_oval(
                self.selected * self.unit + self.unit * 0.7,
                self.unit * 0.2,
                (self.selected + 1) * self.unit + self.unit * 0.3,
                self.unit * 0.8,
                outline = 'blue'
            )
        else:
            second_selected = int(self.get_clicked_vertex(event))
            self.change_order(self.selected, second_selected)
            self.repaint()
            self.selected = -1




def main(file=None):
    graph = read_graph(file)

    window = tk.Tk()
    HEIGHT = 500
    WIDTH = HEIGHT
    UNIT = HEIGHT/(len(graph)+2)
    
    c = tk.Canvas(height=HEIGHT, width=WIDTH, background='white')

    _ = Painter(c, graph, UNIT)

    window.mainloop()


def paint_lgraph(order, heights, lengths, bad_intersections = []):
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
    
    c.pack()
    window.mainloop()

if __name__ == "__main__":
    args = parser.parse_args(namespace=Args)
    main(file=args.input_file)
