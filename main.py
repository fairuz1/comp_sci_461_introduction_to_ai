import schedule_data, heapqimport random# retrive all relevant data and store them into a set (except: activities, rooms)activities      = schedule_data.get_activities_data()activities_name = schedule_data.get_activity_names(activities)facilitators    = schedule_data.get_all_facilitators()times           = schedule_data.get_available_times()rooms           = schedule_data.get_all_rooms()# specify population datadesired_generation = 100first_pop_num   = 500population      = schedule_data.initialize_population(len(activities_name), len(rooms), len(times), len(facilitators), first_pop_num)next_population = list()past_population = list()best_solution   = dict()generation      = dict()current_gen     = 1# specify genetics algorithm configurationselitism         = Truecrossover_rate  = 0.7mutation_rate   = 0.7def genetics_algorithm():    global population, current_gen, best_solution        # calculate fitness scores    fitness_array = list()    for solution in population:        solution_fitness = get_fitness_score(solution)        fitness_array.append((solution_fitness, solution))        # store fitness in a minheap and apply elitism if True    heapq.heapify(fitness_array)    past_population.append((current_gen, tuple(fitness_array)))        if (elitism):        best_parent = heapq.nlargest(2, fitness_array)        fitness_array.remove(best_parent[0])        fitness_array.remove(best_parent[1])                heapq.heapify(fitness_array)                # crossover between 2 parents to create an offspring using tournament method        tournament_crossover(fitness_array, crossover_rate, len(population)-2)                heapq.heapify(next_population)        heapq.heappush(next_population, list(best_parent[0][1]))        heapq.heappush(next_population, list(best_parent[1][1]))    else:        # crossover between 2 parents to create an offspring using tournament method        tournament_crossover(fitness_array, crossover_rate, len(population))            # do mutation    mutation(mutation_rate)        # selection for the new generation of population    current_best_solution = heapq.nlargest(1, fitness_array)[0]    if (len(best_solution) == 0) or (current_best_solution[0] > best_solution['fitness']):        best_solution['generation']     = current_gen        best_solution['best_solution']  = current_best_solution[-1]        best_solution['fitness']        = current_best_solution[0]        record_generation(current_gen, current_best_solution)    current_gen += 1        # repeat until desired generation    if current_gen <= desired_generation:        population = next_population[:]        next_population.clear()        genetics_algorithm()    else:        # get best answer and return txt file containing population        save_populations()        get_best_solution()        def get_fitness_score(solution):    fitness = 0    activity_101 = []    activity_191 = []    set_schedule = set(map(tuple, solution))        for schedule in solution:        activity    = activities[activities_name[schedule[0]]] # activity dict data        room        = rooms[schedule[1]] # tuple room data        time        = times[schedule[2]] # time        facilitator = facilitators[schedule[3]] # facilitator name                # check conflicting schedules        fitness += check_conflicting_schedules(schedule, set_schedule)                # check room size        fitness += check_room_size(activity, room)                # check facilitator preferences        fitness += check_facilitator(activity, facilitator)                # check facilitator load        fitness += check_facilitator_load(schedule[3], time, set_schedule)                if ((activity == 'SLA100A') or (activity == 'SLA100B')):            activity_101.append(schedule)                if ((activity == 'SLA191A') or (activity == 'SLA191B')):            activity_191.append(schedule)        # check for specific activity    if (len(activity_101) == 2) and (len(activity_191) == 2):        fitness += check_for_specific_activity(activity_101, activity_191)        return fitness            def check_conflicting_schedules(activity, schedule):    current_room = activity[1]    current_time = activity[2]    for event in schedule:        if (current_room == event[1]) and (current_time == event[2]):            return -0.5    return 0def check_room_size(current_activity, current_room):    current_expected_enrollment = current_activity['expected_enrollment']    if (current_expected_enrollment > current_room[-1]):        return -0.5    elif (current_room[-1] > current_expected_enrollment*3):         return -0.2    elif (current_room[-1] > current_expected_enrollment*6):         return -0.4    else:        return 0.3def check_facilitator(current_activity, current_facilitator):    if (current_facilitator in current_activity['prefered_facilitators']):        return 0.5    elif (current_facilitator in current_activity['other_facilitators']):        return 0.2    else:        return -0.1    def check_facilitator_load(current_facilitator_index, current_time, schedule):    # global facilitators    score = 0    facilitator_count = 0    facilitator_load_at_same_time = 0        for activity in schedule:        if (activity[3] == current_facilitator_index):            facilitator_count += 1                        if (activity[2] == current_time):                facilitator_load_at_same_time += 1    if (facilitator_count == 1):        score += 0.2    elif ((facilitator_count == 1) or (facilitator_count == 2)):        if (facilitators[current_facilitator_index] == 'Tyler'):            pass        else:            score += -0.4    elif (facilitator_count >= 4):        score += -0.5        if (facilitator_load_at_same_time >= 1):        score += -0.2        return scoredef check_for_specific_activity(activity_101, activity_191):    score = 0    time_data_101 = (times[activity_101[0][2]], times[activity_101[1][2]])    time_data_191 = (times[activity_101[0][2]], times[activity_101[1][2]])    rooms_data_101 = (rooms[activity_101[0][3]], rooms[activity_101[1][3]])    rooms_data_191 = (rooms[activity_101[0][3]], rooms[activity_101[1][3]])        # check for 101 schedule    if (abs(time_data_101[0] - time_data_101[1]) >= 4):        score += 0.5    elif (time_data_101[0] == time_data_101[1]):        score += -0.5            # check for 191 schedule    if (abs(time_data_191[0] - time_data_191[1]) >= 4):        score += 0.5    elif (time_data_191[0] == time_data_191[1]):        score += -0.5        # check for concecutive schedule    for index in range(len(time_data_101)):        if time_data_101[index] in time_data_191:            score += -0.25        elif abs(time_data_101[index] - time_data_191[0]) == 1:            score += 0.5            score += check_spcified_room(rooms_data_101[index], rooms_data_191[0])        elif abs(time_data_101[index] - time_data_191[1]) == 1:            score += 0.5            score += check_spcified_room(rooms_data_101[index], rooms_data_191[1])        else:            if abs(time_data_101[index] - time_data_191[0]) == 2:                score += 0.25            elif abs(time_data_101[index] - time_data_191[1]) == 2:                score += 0.25    return score        def check_spcified_room(room1, room2):    score = 0    if ((("Roman") in room1) and ("Roman") not in room2) or ((("Beach") in room1) and ("Beach") not in room2):        score += -0.4    return scoredef tournament_crossover(population, crossover_rate, length):    # remove the lowest fitness score solution    for i in range(length//2):        heapq.heappop(population)        # do crossover    while len(next_population) != length:        parent_a = random.choice(population)        parent_b = random.choice(population)        probability_number = random.random()        if (probability_number >= crossover_rate):            gen_a1, gen_a2  = parent_a[-1][1:5], parent_a[-1][5:]            gen_b1, gen_b2 = parent_b[-1][1:5], parent_b[-1][5:]                        offspring1 = [parent_a[-1][0]] + gen_a1 + gen_b2            offspring2 = [parent_b[-1][0]] + gen_b1 + gen_a2            offspring1_fitness = get_fitness_score(offspring1)            offspring2_fitness = get_fitness_score(offspring2)                        if (offspring1_fitness > offspring2_fitness):                next_population.append(offspring1)            else:                next_population.append(offspring2)     return next_populationdef mutation(mutation_rate):    probability_number = random.random()    for solution in next_population:        if (probability_number >= mutation_rate):            random_solution = random.choice(next_population)            random_chromosome = random.choice(random_solution)            random_allele = random.choice(random_chromosome)                        random_value_index = random_chromosome.index(random_allele)            random_range = 0            if (random_value_index == 0):                random_range = len(activities_name)-1            elif (random_value_index == 1):                random_range = len(rooms)-1            elif (random_value_index == 2):                random_range = len(times)-1            elif (random_value_index == 3):                random_range = len(facilitators)-1            else:                continue                        random_chromosome[random_value_index] = random.randint(0, random_range)def record_generation(current_generation, solution):    global generation    translate = solution[-1]    generation[current_generation] = {        "generation": current_generation,        "best_solution": translate,        "fitness": solution[0]    }        to_string(current_generation, translate, solution[0])def translate_schedule_data(schedule):    for activity in schedule:        current_activity_name = activities_name[activity[0]]        current_room = rooms[activity[1]]        current_times = times[activity[2]]        current_facilitator = facilitators[activity[3]]                activity[0] = current_activity_name        activity[1] = current_room        activity[2] = schedule_data.convert_time_format_12(current_times)        activity[3] = current_facilitator    return scheduledef to_string(current_generation, current_solution, fitness_score):    print(f'Generation: {current_generation}')    for current_activity in current_solution:            print(f'{current_activity[0]} -> Time: {current_activity[2]}, Room: {current_activity[1]}, Facilitator: {current_activity[3]}')            print(f'Fitness: {fitness_score}', end="\n")    print('')        def get_best_solution():    print('\n ----- The best schedule found -----')    to_string(best_solution['generation'], translate_schedule_data(best_solution['best_solution']), best_solution['fitness'])def save_populations():        returngenetics_algorithm()