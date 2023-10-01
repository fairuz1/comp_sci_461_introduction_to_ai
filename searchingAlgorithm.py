import heapq, time
from queue import PriorityQueue

def findPath(algorithm, graph, start_city, end_city, depth=None):
    # switch state depanding on user input
    # run the searching algorithm while calculating time needed
    if algorithm == "Breadth First Search (BFS)":
        start = time.perf_counter()
        city_paths = backtracking(bfs(graph, start_city), start_city, end_city)
        end = time.perf_counter()
        
    elif algorithm == "Depth First Search (DFS)":
        start = time.perf_counter()
        city_paths = backtracking(dfs(graph, start_city, depth, end_city), start_city, end_city)
        end = time.perf_counter()
    
    elif algorithm == "ID-DFS":
        start = time.perf_counter()
        city_paths = backtracking(best_first_search(graph, start_city, end_city), start_city, end_city)
        end = time.perf_counter()
    
    elif algorithm == "Best First Search":
        start = time.perf_counter()
        city_paths = backtracking(dfs(graph, start_city), start_city, end_city)
        end = time.perf_counter()
    
    elif algorithm == "A Star Algorithm":
        start = time.perf_counter()
        city_paths = a_star_search(graph, start_city, end_city)
        paths = backtracking(city_paths, start_city, end_city)
        end = time.perf_counter()
        
        # process the results
        time_needed = (end - start)
        estimated_total_distance = totalDistance(graph, paths)
        return [paths, estimated_total_distance, time_needed]
    
    # process the results
    time_needed = (end - start)
    estimated_total_distance = totalDistance(graph, city_paths)
    return [city_paths, estimated_total_distance, time_needed]

def dfs(graph, start_city, depth=None, end_city=None):
    tree = {}
    to_visit = [(None, start_city)]
    if depth == None:
        # normal dfs algorithm
        while to_visit:
            a, b = to_visit.pop()
            if b not in tree:
                tree[b] = a
                for c in graph.getNeighbours(b):
                    to_visit.append((b, c[0]))
    else:
        # dfs with iterative deepening
        curr_depth = 0
        while to_visit:
            a, b = to_visit.pop()
            if b not in tree:
                tree[b] = a
                for c in graph.getNeighbours(b):
                    to_visit.append((b, c[0]))
                    
                if (curr_depth == depth) or (end_city in tree):
                    return tree
                else:
                    curr_depth += 1
    return tree

def bfs(graph, start_city):
    tree = {}
    to_visit = [(None, start_city)]
    while to_visit:
        a, b = to_visit.pop()
        if b not in tree:
            tree[b] = a
            for c in graph.getNeighbours(b):
                to_visit.insert(0, (b,c[0]))
    return tree

def best_first_search(graph, start_city, end_city):
    que = [(0, start_city)]
    came_from = {}
    came_from[start_city] = None
    
    while que:
        _, peak_node  = heapq.heappop(que)
        
        if peak_node == end_city:
            break
            
        for neighbor in graph.getNeighbours(peak_node):
            if neighbor[0] not in came_from:
                heapq.heappush(que, (neighbor[1], neighbor[0]))
                came_from[neighbor[0]] = peak_node
    
    return came_from

def a_star_search(graph, start_city, end_city):
    frontier = PriorityQueue()
    frontier.put(start_city, 0)
    
    came_from = {}
    cost_so_far = {}
    came_from[start_city] = None
    cost_so_far[start_city] = 0
    
    while not frontier.empty():
        current_city = frontier.get()
        if current_city == end_city:
            break
        
        for neighbor in graph.getNeighbours(current_city):
            new_cost = cost_so_far[current_city] + neighbor[1]
            if (neighbor[0] not in cost_so_far) or (new_cost < cost_so_far[neighbor[0]]):
                cost_so_far[neighbor[0]] = new_cost
                priority = new_cost + graph.euclidDistance(graph.getCoordinate(neighbor[0]), graph.getCoordinate(end_city))
                frontier.put(neighbor[0], priority)
                came_from[neighbor[0]] = current_city
    
    return came_from

def a_star_search_1(graph, start_city, end_city):
    # variables to save heuristic values
	G = {}
	F = {}
 
	#Initialize starting values
	G[start_city] = 0 
	F[start_city] = graph.euclidDistance(graph.getCoordinate(start_city), graph.getCoordinate(end_city))
 
    # create open and close state
	closedVertices = set()
	openVertices = set([start_city])
	cameFrom = {}
 
	while len(openVertices) > 0:
		#Get the city with lowes score
		current = None
		currentFscore = None
		for pos in openVertices:
			if current is None or F[pos] < currentFscore:
				currentFscore = F[pos]
				current = pos
 
		#Check if we arrive at the goal state
		if current == end_city:
			# create path
			path = [current]
			while current in cameFrom:
				current = cameFrom[current]
				path.append(current)
			path.reverse()
			return path
 
		# Mark the current city as closed
		openVertices.remove(current)
		closedVertices.add(current)
 
		# update other cities heuristic score near current city
		for neighbour in graph.getNeighbours(current):
			if neighbour[0] in closedVertices: 
				continue
            
            # re-arrange cities based on their heuristic score
			candidateG = G[current] + move_cost(closedVertices, current, neighbour[0])
 
			if neighbour[0] not in openVertices:
				openVertices.add(neighbour[0])
			elif candidateG >= G[neighbour[0]]:
				continue

			cameFrom[neighbour[0]] = current
			G[neighbour[0]] = candidateG
			H = graph.euclidDistance(graph.getCoordinate(neighbour[0]), graph.getCoordinate(end_city))
			F[neighbour[0]] = G[neighbour[0]] + H

def backtracking(graph, start_city, end_city):
    path = []
    if end_city in graph:
        while end_city is not None:
            path.append(end_city)
            end_city = graph[end_city]
        return path
    else:
        return path

def totalDistance(graph, city_paths):
    total_distance = 0
    if len(city_paths) == 0:
        return total_distance
    else:
        end_city = city_paths[-1]
        for i in range(len(city_paths)-1):
            if city_paths[i] != end_city:
                total_distance += graph.euclidDistance(graph.getCoordinate(city_paths[i]), graph.getCoordinate(city_paths[i+1]))
            elif city_paths[i] == end_city:
                total_distance += graph.euclidDistance(graph.getCoordinate(city_paths[i]), graph.getCoordinate(city_paths[i+1]))
                break
    return total_distance
    
def move_cost(graph, vertex_1, vertex_2):
    for city in graph:
        if vertex_2 in city:
            return 100
    return 1
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    