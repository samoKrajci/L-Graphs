import tkinter as tk
from typing import Callable
from graph import Graph, read_graph
import random
from tooltip import create_tool_tip
import os

# TODO:
#   loadnutie grafu
#   olabelovat vrcholy
#   directed grafy 

class Screen:
    def __init__(
        self, 
        height: float=500, 
        width: float=500, 
        v_diameter: float=10, 
        output_file: str='graph.txt', 
        input_file: str=None, 
        verbose: bool=True,
        submit_fn: Callable[[str, any], any]=None,
        submit_button_text: str='Submit',
        submit_button_tooltip: str=''
    ):
        self.output_file = output_file
        self.verbose = verbose
        self.submit_fn = submit_fn
        self.sumbit_button_text = submit_button_text
        self.submit_button_tooltip = submit_button_tooltip
        self.w = tk.Tk()
        self.c = tk.Canvas(height=height, width=width, background='white')
        self.height = height
        self.width = width
        self.v_diameter = v_diameter
        self.remove_mode = False
        self.selected = None
        self.vertex_id = {}
        self.edge_id = {}
        
        self.background = None
        self.moving_edge=None
        self.clear()
        self.g = Graph() if not input_file else read_graph(input_file)
        self.init_bindings()
        self.init_buttons()

        self.c.pack(fill="both", expand=True)
        if input_file:
            self.random_paint_graph()
        self.w.mainloop()

    def init_buttons(self):
        # Mode button
        self.b_mode = tk.Button(
            master=self.w, 
            text='mode [m]', 
            command=self.change_mode
        )
        self.b_mode.place(x=0, y=0)
        create_tool_tip(self.b_mode, text='Switch between remove and add mode')
        # Clear button
        self.b_clear = tk.Button(
            master=self.w, 
            text='clear [c]', 
            command=self.clear
        )
        self.b_clear.place(x=0, y=30)
        create_tool_tip(self.b_clear, text='Remove all nodes')
        # Save button
        self.b_save = tk.Button(
            master=self.w, 
            text='save [s]', 
            command=self.save
        )
        self.b_save.place(x=0, y=60)
        create_tool_tip(self.b_save, text='Save graph to \'<current_dir>/graph.txt\'')
        # Randomize button
        self.b_randomize = tk.Button(
            master=self.w, 
            text='randomize', 
            command=self.random_paint_graph
        )
        self.b_randomize.place(x=0, y=90)
        create_tool_tip(self.b_randomize, text='Randomly shuffle vertices')
        # Submit button
        if self.submit_fn:
            self.b_submit = tk.Button(
                master=self.w, 
                text=self.sumbit_button_text, 
                command=self.submit_pipeline
            )
            self.b_submit.place(x=0, y=120)
            create_tool_tip(self.b_submit, text=self.submit_button_tooltip)

    def submit_pipeline(self):
        temp_file_name = '_temp_graph.txt'
        self.save(output_file=temp_file_name)
        new_window = tk.Toplevel(self.w)
        self.submit_fn(temp_file_name, master=new_window)
        os.remove(temp_file_name)

    def init_bindings(self):
        self.c.tag_bind('vertex', '<Button-1>', self.click_vertex)
        self.c.tag_bind('vertex', '<B1-Motion>', self.move_vertex)
        self.c.tag_bind('edge', '<Button-1>', self.click_edge)
        self.c.tag_bind('moving_edge', '<Button-1>', self.click_moving_edge)
        self.c.tag_bind('background', '<Button-1>', self.click_background)
        self.w.bind('m', lambda _: self.b_mode.invoke())
        self.w.bind('c', lambda _: self.b_clear.invoke())
        self.w.bind('s', lambda _: self.b_save.invoke())
        self.w.bind('<Escape>', lambda _: self.unselect_vertex())
        self.w.bind('<Configure>', self.on_resize)
        self.w.bind('<Motion>', self.on_mouse_move)

    def on_mouse_move(self, event):
        if self.selected:
            m_coords = self.c.coords('moving_edge')
            self.c.coords(self.moving_edge, m_coords[0], m_coords[1], event.x, event.y)


    def on_resize(self, event):
        self.height = event.height
        self.width = event.width
        self.c.coords(self.background, 0, 0, self.width, self.height)

    def clear(self):
        self.change_mode(remove_mode=False)
        self.unselect_vertex()
        self.g = Graph()
        self.c.delete('all')
        self.background = self.c.create_rectangle(
            0, 
            0, 
            self.width, 
            self.height, 
            fill='white', 
            tags='background',
            width=0,
            outline='red'
        )

    def random_paint_graph(self):
        old_g_str = self.g.str()
        lines = old_g_str.split('\n')
        self.clear()
        l = lines[0].split()
        n, m = int(l[0]), int(l[1])
        v_map = dict()
        for i in range(n):
            v_map[i] = self.add_vertex()
        for line_i in range(1, m+1):
            l = lines[line_i].split()
            self.add_edge(v_map[int(l[0])], v_map[int(l[1])])
        


    def change_mode(self, remove_mode: bool=None):
        if self.remove_mode != remove_mode:
            self.remove_mode = not self.remove_mode
            self.unselect_vertex()
            if self.remove_mode:
                self.c.itemconfig(self.background, width=10)
            else:
                self.c.itemconfig(self.background, width=0)

    def move_vertex(self, event):
        if not self.remove_mode:
            self.unselect_vertex()
            v = event.widget.find_withtag('current')[0]
            self.c.coords(
                v, 
                event.x - self.v_diameter,
                event.y - self.v_diameter,
                event.x + self.v_diameter,
                event.y + self.v_diameter,
            )
            for id, e in self.edge_id.items():
                if e[0] == v or e[1] == v:
                    a, b = e[0], e[1]
                    coord_a = self.c.coords(a)
                    coord_b = self.c.coords(b)
                    mid_a = ((coord_a[0] + coord_a[2]) / 2, (coord_a[1] + coord_a[3]) / 2)
                    mid_b = ((coord_b[0] + coord_b[2]) / 2, (coord_b[1] + coord_b[3]) / 2)
                    self.c.coords(
                        id,
                        mid_a[0],
                        mid_a[1],
                        mid_b[0],
                        mid_b[1]
                    )

    def click_vertex(self, event):
        v = event.widget.find_withtag('current')[0]
        if self.remove_mode:
            self.remove_vertex(v)
        
        elif not self.remove_mode:
            if not self.selected:
                self.select_vertex(v)
            else:
                self.add_edge(self.selected, v)

    def click_edge(self, event):
        if self.remove_mode:
            e = event.widget.find_withtag("current")[0]
            self.remove_edge(e)

    def click_moving_edge(self, event):
        v = self.add_vertex(event.x, event.y)
        self.add_edge(self.selected, v)
        self.unselect_vertex()

    def click_background(self, event):
        if self.remove_mode:
            pass
        else:
            self.add_vertex(event.x, event.y)
            if self.selected:
                pass

    def add_vertex(self, x: float=None, y: float=None):
        if not x:
            x = random.uniform(100, self.width - self.v_diameter)
        if not y:
            y = random.uniform(100, self.height - self.v_diameter)
        
        v = self.c.create_oval(
            x - self.v_diameter, 
            y - self.v_diameter, 
            x + self.v_diameter, 
            y + self.v_diameter,
            width=5,
            fill='blue',
            outline='blue',
            activeoutline='red',
            tags='vertex'
        )
        self.vertex_id[v] = self.g.add_vertex()
        return v
    
    def remove_vertex(self, v_canvas_id):
        self.c.delete(v_canvas_id)
        self.g.remove_vertex(self.vertex_id[v_canvas_id])
        for e, p in list(self.edge_id.items()):
            if p[0] == v_canvas_id or p[1] == v_canvas_id:
                self.c.delete(e)
                del self.edge_id[e]
        del self.vertex_id[v_canvas_id]

    def add_edge(self, a_canvas_id: int, b_canvas_id: int):
        self.unselect_vertex()
        a_coords = self.c.coords(a_canvas_id)
        b_coords = self.c.coords(b_canvas_id)
        successful = self.g.add_edge(self.vertex_id[a_canvas_id], self.vertex_id[b_canvas_id])
        if not successful:
            return None
        e = self.c.create_line(
            (a_coords[0] + a_coords[2]) / 2,
            (a_coords[1] + a_coords[3]) / 2,
            (b_coords[0] + b_coords[2]) / 2,
            (b_coords[1] + b_coords[3]) / 2,
            width=5,
            activefill='red',
            tags='edge'
        )
        self.c.tag_lower(e, 'vertex')
        self.edge_id[e] = (a_canvas_id, b_canvas_id)

        return e

    def remove_edge(self, edge):
        self.c.delete(edge)
        a, b = self.vertex_id[self.edge_id[edge][0]], self.vertex_id[self.edge_id[edge][1]]
        self.g.remove_edge(a, b)
        del self.edge_id[edge]

    def select_vertex(self, v_canvas_id: int):
        self.selected = v_canvas_id
        self.c.itemconfig(v_canvas_id, fill='cyan', outline='cyan')
        v_coords = self.c.coords(v_canvas_id)
        self.moving_edge = self.c.create_line(
            (v_coords[0] + v_coords[2]) / 2,
            (v_coords[1] + v_coords[3]) / 2,
            (v_coords[0] + v_coords[2]) / 2,
            (v_coords[1] + v_coords[3]) / 2,
            width=5,
            tags='moving_edge'
        )
        self.c.tag_lower(self.moving_edge, 'vertex')

    def unselect_vertex(self):
        self.c.itemconfig(self.selected, fill='blue', outline='blue')
        self.c.delete('moving_edge')
        self.moving_edge = None
        self.selected = None

    def save(self, output_file: str=None):
        if not output_file:
            output_file = self.output_file
        file = open(output_file, 'w')
        if self.verbose:
            print('------------ Graph saved -------------')
            print(self.g.str())
            file.write(self.g.str())
