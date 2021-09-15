class Graph:
    def __init__(self, directed: bool=False):
        self.vertices = dict()
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
        v_map = dict()
        next_available = 0
        for v in self.vertices.keys():
            v_map[v]=next_available
            next_available += 1

        for key, value in self.vertices.items():
            for v in value:
                if key > v or self.directed:
                    s += f'\n{v_map[key]} {v_map[v]}'
        return s
