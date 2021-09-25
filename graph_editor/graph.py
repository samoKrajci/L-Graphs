class Graph:
    def __init__(self, directed: bool=False):
        self.vertices = dict()
        self.labels = dict()
        self.directed = directed
        self.n = 0
        self.m = 0
        self.next_id = 0
    
    def add_vertex(self) -> int:
        '''
        adds a vertex with next index
        returns id of added vertex
        '''
        self.vertices[self.next_id] = set()
        self.labels[self.next_id] = self.n
        self.n += 1
        self.next_id += 1
        return self.next_id - 1

    def remove_vertex(self, a: int) -> bool:
        '''
        removes a vertex.
        does not maintain id ordering. 
        returns False if such vertex is not present
        '''
        if a not in self.vertices:
            return False
        self.n -= 1
        self.m -= len(self.vertices[a])
        del self.vertices[a]
        for adj in self.vertices.values():
            if a in adj:
                adj.remove(a)
        self.relabel()
        return True

    def add_edge(self, a: int, b: int) -> bool:
        '''
        raises an exception if such vertices do not exist
        returns False if already exists, True 
        '''
        if a not in self.vertices:
            raise KeyError(f'There is no vertex with index {a}')
        if b not in self.vertices:
            raise KeyError(f'There is no vertex with index {b}')
        if a == b or b in self.vertices[a]:
            return False

        self.vertices[a].add(b)
        self.m += 1
        if not self.directed:
            self.vertices[b].add(a)
        return True

    def remove_edge(self, a: int, b: int) -> bool:
        '''
        returns False if there is no such edge,
        True otherwise
        '''
        if a in self.vertices and b in self.vertices:
            if b in self.vertices[a]:
                self.vertices[a].remove(b)
            if not self.directed:
                if a in self.vertices[b]:
                    self.vertices[b].remove(a)
                    self.m -= 1
            return True
        else:
            return False

    def relabel(self):
        '''
        Relabels vertices so the labels are unique integers in [0, n)
        '''
        self.labels = dict()
        next_available = 0
        for v in self.vertices.keys():
            self.labels[v]=next_available
            next_available += 1

    def str(self):
        '''
        Serializes graph to standard graph format:
        <n_vertex> <n_edge>
        <...
            n_edge lines in format:
            <out_vert> <in_vert>
        ...>
        No newline at the end.
        '''
        s = ''
        s += f'{self.n} {self.m}'
        self.relabel()

        for key, value in self.vertices.items():
            for v in value:
                if key > v or self.directed:
                    s += f'\n{self.labels[key]} {self.labels[v]}'
        return s


def read_graph(file: str, directed: bool=False) -> Graph:
    g = Graph(directed=directed)
    f = open(file, 'r')
    l = f.readline().split()
    n, m = int(l[0]), int(l[1])
    for _ in range(n):
        g.add_vertex()
    for _ in range(m):
        l = f.readline().split()
        a, b = int(l[0]), int(l[1])
        g.add_edge(a, b)
    return g


