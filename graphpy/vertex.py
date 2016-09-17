"""
Implementation of a vertex, as used in graphs
"""


################################################################################
#                                                                              #
#                                  Undirected                                  #
#                                                                              #
################################################################################


class UndirectedVertex(object):

    def __init__(self, name=''):
        self._name = name or id(self)
        self._edges = set()
        self._has_self_edge = False

    def __repr__(self):
        display = (self.name, id(self))
        return "Vertex(name=%s, id=%s)" % display

    def __str__(self):
        return "V(%s)" % self.name

    def __contains__(self, e):
        return e in self._edges

    @property
    def name(self):
        return self._name

    @property
    def edges(self):
        return iter(self._edges)

    @property
    def has_self_edge(self):
        return self._has_self_edge

    @property
    def neighbors(self):
        """ Iterator over vertices adjacent to this vertex """
        return iter(set(v for e in self._edges for v in e.vertices
                        if v != self) |
                    (set([self]) if self._has_self_edge else set()))

    @property
    def degree(self):
        """ Number of neighbors this vertex has (+1 if it has a self edge) """
        return sum(1 for _ in self._edges) + (1 if self._has_self_edge else 0)

    def add_edge(self, e):
        """ Adds an edge to this vertex """
        if self not in e.vertices:
            raise VertexNotPartOfEdgeException(self, e)
        if e in self:
            raise VertexAlreadyHasEdgeException(self, e)

        self._edges.add(e)

        if e.is_self_edge:
            self._has_self_edge = True

    def remove_edge(self, e):
        """ Removes an edge from this vertex """
        self._edges.discard(e)

        if e.is_self_edge:
            self._has_self_edge = False


################################################################################
#                                                                              #
#                                   Directed                                   #
#                                                                              #
################################################################################


class DirectedVertex(object):

    def __init__(self, name=''):
        self._name = name
        self._edges = set()

    def __repr__(self):
        display = (self.name, id(self))
        return "Vertex(name=%s, id=%s)" % display

    def __str__(self):
        return "V(%s)" % self.name

    def __contains__(self, e):
        return e in self._edges

    @property
    def name(self):
        return self._name

    @property
    def edges(self):
        return iter(self._edges)

    @property
    def outs(self):
        """ Iterator over vertices into which this vertex has an edge """
        return iter(set(e.v_to for e in self._edges if e.v_from == self))

    @property
    def ins(self):
        """ Iterator over vertices which have an edge into this vertex """
        return iter(set(e.v_from for e in self._edges if e.v_to == self))

    @property
    def out_degree(self):
        """ Number of vertices into which this vertex has an edge """
        return sum(1 for e in self._edges if e.v_from == self)

    @property
    def in_degree(self):
        """ Number of vertices which have an edge into this vertex """
        return sum(1 for e in self._edges if e.v_to == self)

    @property
    def degree(self):
        """ Sum of out degree and in degree """
        return self.out_degree + self.in_degree

    def add_edge(self, e):
        """ Adds an edge to this vertex """
        if self != e.v_from and self != e.v_to:
            raise VertexNotPartOfEdgeException(self, e)
        if e in self:
            raise VertexAlreadyHasEdgeException(self, e)

        self._edges.add(e)

    def remove_edge(self, e):
        """ Removes an edge from this vertex """
        self._edges.discard(e)


################################################################################
#                                                                              #
#                                  Exceptions                                  #
#                                                                              #
################################################################################


class VertexNotPartOfEdgeException(Exception):
    def __init__(self, v, e):
        m = str(v) + " is not part of " + str(e) + "."
        super(VertexNotPartOfEdgeException, self).__init__(m)

class VertexAlreadyHasEdgeException(Exception):
    def __init__(self, v, e):
        m = str(v) + " already has " + str(e) + "."
        super(VertexAlreadyHasEdgeException, self).__init__(m)
