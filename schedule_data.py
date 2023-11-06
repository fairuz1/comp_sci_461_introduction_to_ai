from datetime import datetime
import pandas as pd
import random

def get_activities_data():
    list_data = pd.read_csv(
        'schedule_data/activities.csv', 
        names=['activity','expected_enrollment','prefered_facilitators','other_facilitators']
    )
    
    data = {}
    for i, row in list_data.iterrows():
        prefered_facilitators = tuple(row['prefered_facilitators'].split(", "))
        other_facilitators = tuple(row['other_facilitators'].split(", "))

        data[row['activity']] = {'expected_enrollment': row['expected_enrollment'],
                                 'prefered_facilitators': prefered_facilitators,
                                 'other_facilitators': other_facilitators}
    return data

def get_all_facilitators():
    list_data = pd.read_csv('schedule_data/facilitators.csv', names=['facilitators'])
    data = tuple(row['facilitators'] for i, row in list_data.iterrows())
    return data

def get_available_times():
    list_data = pd.read_csv('schedule_data/times.csv', names=['times'])
    data = tuple(convert_time_format(row['times']) for i, row in list_data.iterrows())
    return data

def get_all_rooms():
    list_data = pd.read_csv('schedule_data/rooms.csv', names=['rooms','capacity'])
    data = tuple(tuple([row['rooms'],row['capacity']]) for i, row in list_data.iterrows())
    return data

def get_activity_names(activities):
    return tuple(i for i in activities.keys())

def initialize_population(activities_name, rooms, times, facilitators, population_number):
    random_solutions = []
    for i in range(population_number):
        solution = list([
            activity_index, 
            random.randint(0, rooms-1), 
            random.randint(0, times-1), 
            random.randint(0, facilitators-1)] for activity_index in range(11))
        random_solutions.append(solution)
    
    return tuple(random_solutions)

def get_function_inputs(activities_name, rooms, times, facilitators):
    # function_input = list([activity, random.choice(rooms), random.choice(times), random.choice(facilitators)] for activity in activities_name)   
    function_input = list([
        i, 
        random.randint(0, rooms-1), 
        random.randint(0, times-1), 
        random.randint(0, facilitators-1)] for i in range(activities_name))

    return function_input

def get_gene_space(activities_name, rooms, times, facilitators):
    return [list(range(0, activities_name)), list(range(0, rooms)), list(range(0, times)), list(range(0, facilitators))]
    
def convert_time_format(time):
    # convert time to 24 hour format
    new_hour_format = datetime.strptime(time, '%I %p')
    return new_hour_format.strftime('%H')

def convert_time_format_12(time):
    # convert time to 12 hour format
    new_hour_format = datetime.strptime(time, "%H")
    return new_hour_format.strftime('%I %p')


