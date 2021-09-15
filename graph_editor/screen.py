import tkinter as tk
from graph import Graph
import random
from tooltip import create_tool_tip

# TODO:
#   premiestnovanie vrcholov (aj hrany sa musia zaroven hybat)
#   squeeze pri printe grafu
#   directed grafy 
#   loadnutie grafu

class Screen:
    def __init__(self, height: float=500, width: float=500, v_diameter: float=10):
        self.w = tk.Tk()
        self.c = tk.Canvas(height=height, width=width, background='white')
        self.height = height
        self.width = width
        self.v_diameter = v_diameter
        self.g = Graph()
        self.remove_mode = False
        self.selected = None
        self.vertex_id = {}
        self.edge_id = {}
        
        self.background = None
        self.moving_edge=None
        self.clear()
        self.init_bindings()
        self.init_buttons()

        self.c.pack(fill="both", expand=True)
        self.w.mainloop()

    def init_buttons(self):
        self.b_mode = tk.Button(
            master=self.w, 
            text='mode [m]', 
            command=self.change_mode
        )
        self.b_mode.place(x=0, y=0)
        create_tool_tip(self.b_mode, text='Switch between remove and add mode')

        self.b_clear = tk.Button(
            master=self.w, 
            text='clear [c]', 
            command=self.clear
        )
        self.b_clear.place(x=0, y=30)
        create_tool_tip(self.b_clear, text='Remove all nodes')
        
        self.b_save = tk.Button(
            master=self.w, 
            text='save [s]', 
            command=self.save
        )
        self.b_save.place(x=0, y=60)
        create_tool_tip(self.b_save, text='Save graph to \'<current_dir>/graph.txt\'')
        
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
            x = random.uniform(self.v_diameter, self.width - self.v_diameter)
        if not y:
            y = random.uniform(self.v_diameter, self.width - self.v_diameter)
        
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

    def save(self):
        file = open('graph.txt', 'w')
        print('-------------------------')
        print(self.g.str())
        file.write(self.g.str())
