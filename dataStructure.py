class weightedBidirectionalGraph:
    def __init__(self, edges, adjacencies):
        self.graph = dict()
        self.city_coordinate = dict((row['city'], (row['longitude'], row['latitude'])) for i, row in edges.iterrows())
        
        # seeding graph with city adjacencies
        self.seedingGraph(edges, adjacencies)

    def addEdge(self, vertex1, vertex2, weight):
        # add vertecies if not present in the graph
        if vertex1 not in self.graph:
            self.graph[vertex1] = []
        if vertex2 not in self.graph:
            self.graph[vertex2] = []
        
        # add adjacencies to the vertecies
        self.graph[vertex1].append((vertex2, float(weight)))
        self.graph[vertex2].append((vertex1, float(weight)))
    
    # get heuristic value from euclidian distance
    def euclidDistance(self, start_city, end_city):
        return ((start_city[0] - end_city[0])**2 + (start_city[1] - end_city[1])**2)**0.5
    
    # get city coordinates
    def getCoordinate(self, city):
        return self.city_coordinate[city]
    
    # get city's neighbours
    def getNeighbours(self, vertex):
        return self.graph[vertex]
    
    # seeds the city graph with cities
    def seedingGraph(self, edges, adjacencies):
        for i in adjacencies:
            start_city, end_city = i.split()
            self.addEdge(start_city, end_city, self.euclidDistance(self.city_coordinate[start_city], self.city_coordinate[end_city]))