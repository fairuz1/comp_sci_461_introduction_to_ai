import pandas as pd

def get_activities_data():
    list_data = pd.read_csv(
        'schedule_data/activities.csv', 
        names=['activity','expected_enrollment','prefered_facilitators','other_facilitators']
    )
    
    data = {}
    for i, row in list_data.iterrows():
        prefered_facilitators = row['prefered_facilitators'].split(", ")
        other_facilitators = row['other_facilitators'].split(", ")

        data[row['activity']] = {'expected_enrollment': row['expected_enrollment'],
                                 'prefered_facilitators': prefered_facilitators,
                                 'other_facilitators': other_facilitators}
    return data

def get_all_facilitators():
    list_data = pd.read_csv('schedule_data/facilitators.csv', names=['facilitators'])
    data = {row['facilitators'] for i, row in list_data.iterrows()}
    return data

def get_available_times():
    list_data = pd.read_csv('schedule_data/times.csv', names=['times'])
    data = {row['times'] for i, row in list_data.iterrows()}
    return data

def get_all_rooms():
    list_data = pd.read_csv('schedule_data/rooms.csv', names=['rooms','capacity'])
    data = {}
    for i, row in list_data.iterrows():
        data[row['rooms']] = row['capacity']
    return data

def get_activity_names(activities):
    return {i for i in activities.keys()}