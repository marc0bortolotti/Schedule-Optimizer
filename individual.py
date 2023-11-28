
from collections import Counter
import numpy as np
from writer import *


class Individual(object):
    """Represents an individual in an evolutionary computation.
    
    An individual is defined by its candidate solution and the
    fitness (or value) of that candidate solution. Individuals
    can be compared with one another by using <, <=, >, and >=.
    In all cases, such comparisons are made using the individuals'
    fitness values. The ``maximize`` attribute is respected in all
    cases, so it is better to think of, for example, < (less-than)
    to really mean "worse than" and > (greater-than) to mean
    "better than". For instance, if individuals a and b have fitness
    values 2 and 4, respectively, and if ``maximize`` were ``True``,
    then a < b would be true. If ``maximize`` were ``False``, then 
    a < b would be false (because a is "better than" b in terms of
    the fitness evaluation, since we're minimizing).    
    """
    def __init__(self, candidate=None):
        self.candidate = candidate
        self.fitness = None
        self.maximize = False
        self.hour_overlap = None
        self.room_overlap = None
        self.type_overlap = None
        
    def __str__(self):
        return '{0} \nFITNESS: {1}'.format(str(self.candidate), str(self.fitness))
        
    def __lt__(self, other):
        if self.fitness is not None and other.fitness is not None:
            if self.maximize: 
                return self.fitness < other.fitness
            else:
                return self.fitness > other.fitness

    def __le__(self, other):
        return self < other or not other < self
            
    def __gt__(self, other):
        if self.fitness is not None and other.fitness is not None:
            return other < self

    def __ge__(self, other):
        return other < self or not self < other
        
    def __eq__(self, other):
        return self.fitness == other.fitness and self.candidate.equals(other.candidate)
                
    def __ne__(self, other):
        return not (self == other)
    


def new_row(candidate, row_index):

    cfu = candidate.at[row_index, "CFU"]

    if cfu == 6:
        temp = np.random.randint(1, hour_size) 
        hours = [temp,temp+1]
    else: 
        temp = np.random.randint(1, hour_size-1)
        hours = [temp,temp+1,temp+2] 

    row = {'TEACHING':candidate.at[row_index, "TEACHING"], 
           'ID':candidate.at[row_index, "ID"], 
           'COURSE OF STUDYING':candidate.at[row_index, "COURSE OF STUDYING"], 
           'CFU':candidate.at[row_index, "CFU"], 
           'TYPE':candidate.at[row_index, "TYPE"], 
           'ROOM':np.random.randint(room_size), 
           'DAY':np.random.randint(day_size)+1,
           'HOUR': hours}   
    return row


def generate_individual(kwargs):
    
    source_df =  kwargs['source_df']
    candidate = source_df.copy() # NB: copy()!!!

    for row_index in candidate.index:
        candidate.loc[row_index] = new_row(candidate, row_index)
        if(candidate.at[row_index, "CFU"]==12): 
            candidate = candidate.append(new_row(candidate, row_index), ignore_index=True) 
            candidate = candidate.append(new_row(candidate, row_index), ignore_index=True) 
        else: candidate = candidate.append(new_row(candidate, row_index), ignore_index=True) 
    candidate = candidate.sort_values(by=['ID'])
    candidate = candidate.reset_index(drop=True)
    individual = Individual(candidate=candidate)
    return individual


def initialize_population(kwargs):
    global hour_size, day_size, pop_size, room_size
    hour_size = kwargs['hour_size']
    day_size = kwargs['day_size']
    pop_size = kwargs['pop_size']
    room_size = kwargs['room_size']

    source_df = pd.read_excel(kwargs['source_path'])
    kwargs['source_df'] = source_df
    source_df["ROOM"] = None
    source_df["DAY"] = None
    source_df["HOUR"] = None

    population = []
    pop_tmp = 0
    while(pop_tmp<pop_size):
        individual = generate_individual(kwargs)
        population.append(individual)
        pop_tmp+=1
    return population


def terminate(best_fitness):
    return best_fitness < 1


def evaluate(population):
    return fitness(population)


def fitness(population):

    generation_fitness = []
    p1 = 1 # penalty for room overlap
    p2 = 1 # penalty for mandatory courses overlap
    p3 = 10 # penalty for lessons' overlap
    p4 = 1 # penalty for teachings' repetition in the same day
    p5 = 1 # penalty for excess of hours of lesson in a day 
    max_daily_hours = 8 # max number of hours of lesson in a day

  
    for individual in population:

        fit = 0
        candidate = individual.candidate.copy()
        room_overlap = []
        hour_overlap = 0
        type_overlap = []
        teaching_repetition = 0
        exceeding_hours = 0

        for day in candidate['DAY'].unique():
            
            df_day = candidate[candidate['DAY']==day]
            ore = df_day['HOUR'].to_list()
            ore = list(np.concatenate(ore).flat)
            counter = Counter(ore)
            ore_overlapp = [x for x in counter if counter[x]>1] # Counter gives dict of [element:value], value = occurence
            
            for hour in ore_overlapp:
                
                # select lessons which are overlapped in the schedule 
                rows = []
                for i, row in df_day.iterrows():
                    if any(row['HOUR']==hour): rows.append(row)
                df_overlap = pd.DataFrame(rows)


                # overlap in rooms
                counter_aule = Counter(df_overlap['ROOM'].to_list())    
                for room in counter_aule: 
                    occurrence = counter_aule[room]
                    if occurrence>1: 
                        room_overlap.append({'DAY' : day, 'HOUR': hour, 'ROOM' : room, 'OCCURRENCE' : occurrence})
                            
                            
                for course_of_studying in df_overlap['COURSE OF STUDYING'].unique():

                    df_course_of_studying = df_overlap[df_overlap['COURSE OF STUDYING'] == course_of_studying]

                    # overlap of lessons
                    if len(df_course_of_studying)>1 : hour_overlap += len(df_course_of_studying)-1
                    
                    # overlap of mandatory teachings
                    df_obbligatorio = df_course_of_studying[df_course_of_studying['TYPE'] == 'MANDATORY']
                    if len(df_obbligatorio) > 0: type_overlap.append(len(df_obbligatorio)-1)

            
            for course_of_studying in df_day['COURSE OF STUDYING'].unique():
                    df_course_of_studying = df_day[df_day['COURSE OF STUDYING'] == course_of_studying]  
                    
                    # check if there are lessons of the same teaching in the same day
                    IDs = df_course_of_studying['ID'].to_list()
                    occurences_ID = Counter(IDs).values()
                    occurences_ID = [x for x in occurences_ID if x>1]
                    teaching_repetition += sum(occurences_ID)
                
                    # fix a max number of hours of lesson in a day
                    hours = df_course_of_studying['HOUR'].to_list()
                    hours = list(np.concatenate(hours).flat)
                    num_hours = len(hours)
                    if(num_hours>max_daily_hours):
                        exceeding_hours+=(num_hours-max_daily_hours)
                
                
        fit = len(room_overlap)*p1 + sum(type_overlap)*p2 + hour_overlap*p3 + teaching_repetition*p4 + exceeding_hours*p5 
        individual.fitness = fit
        individual.type_overlap = sum(type_overlap)
        individual.room_overlap = room_overlap
        individual.hour_overlap = hour_overlap
        generation_fitness.append(individual.fitness)
        
    return generation_fitness


