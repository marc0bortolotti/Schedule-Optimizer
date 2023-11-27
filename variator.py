import numpy as np
from operator import add
from individual import Individual, generate_individual
import random as rdm


def default_variation(parents,kwargs):
    return parents


def variation_1(parents, kwargs):
    '''
    For each parent generate 'num_offspring'/'num_parents' offspring
    Variation on hour, day and room with +-1. When the bound is reached, turn back.
    Crossover between 2 parents implemented selecting:
        parent_1.candidate[:random_index] rows 
        parent_2.candidate[random_index:] rows
    '''

    offspring = []
    num_offspring = kwargs['num_offspring']
    mutation_rate = kwargs['mutation_rate']
    crossover_rate = kwargs['crossover_rate']
    hour_size = kwargs['hour_size']
    day_size = kwargs['day_size']
    room_size= kwargs['room_size']


    # CROSSOVER 
    for parent_1 in parents:
        for i in range(round(num_offspring/len(parents))):
            candidate=parent_1.candidate.copy()
            individual = Individual(candidate=candidate) 
            
            random=np.random.uniform(0,1)
            if(random<crossover_rate and len(parents)>1):
                possible_parents = parents.copy()
                possible_parents.remove(parent_1)
                parent_2 = rdm.sample(possible_parents, 1)[0]
                crossover_point = np.random.choice(range(len(individual.candidate)))
                individual.candidate[crossover_point:]=parent_2.candidate[crossover_point:]
            offspring.append(individual)

    # MUTATION
    for individual in offspring:
        for i in range(len(individual.candidate)):
            
            # HOUR MUTATION
            random=np.random.uniform(0,1)
            mutation_type=np.random.randint(0,2)
            if (random<mutation_rate):
                if(mutation_type==0 and (np.array(individual.candidate.at[i,'HOUR'])<hour_size).all()):
                        individual.candidate.at[i,'HOUR']=list(map(add,individual.candidate.at[i,'HOUR'],np.ones(len(individual.candidate.at[i,'HOUR']),int)))
                elif(mutation_type==0 and (np.array(individual.candidate.at[i,'HOUR'])==hour_size).any()):
                        individual.candidate.at[i,'HOUR']=list(map(lambda a, b: a - b,individual.candidate.at[i,'HOUR'],np.ones(len(individual.candidate.at[i,'HOUR']),int)))
                elif(mutation_type==1 and np.array(individual.candidate.at[i,'HOUR'])>1).all():
                        individual.candidate.at[i,'HOUR']=list(map(lambda a, b: a - b,individual.candidate.at[i,'HOUR'],np.ones(len(individual.candidate.at[i,'HOUR']),int)))
                elif(mutation_type==1 and np.array(individual.candidate.at[i,'HOUR'])==1).any():
                        individual.candidate.at[i,'HOUR']=list(map(add,individual.candidate.at[i,'HOUR'],np.ones(len(individual.candidate.at[i,'HOUR']),int)))
            
            # DAY MUTATION
            random=np.random.uniform(0,1)
            mutation_type=np.random.randint(0,2)
            if (random<mutation_rate):
                if(mutation_type==0):
                    if(individual.candidate.at[i,'DAY']<day_size):
                        individual.candidate.at[i,'DAY']+=1
                    else:
                        individual.candidate.at[i,'DAY']-=1
                elif(mutation_type==1):
                    if(individual.candidate.at[i,'DAY']>1):
                        individual.candidate.at[i,'DAY']-=1
                    else:
                        individual.candidate.at[i,'DAY']+=1
            
            # ROOM MUTATION
            mutation_type=np.random.randint(0,2)
            random=np.random.uniform(0,1)
            if (random<mutation_rate):
                if(mutation_type==0):
                    if(individual.candidate.at[i,'ROOM']<room_size):
                        individual.candidate.at[i,'ROOM']+=1
                    else:
                        individual.candidate.at[i,'ROOM']-=1
                elif(mutation_type==1):
                    if(individual.candidate.at[i,'ROOM']>1):
                        individual.candidate.at[i,'ROOM']-=1
                    else:
                        individual.candidate.at[i,'ROOM']+=1
    return offspring


def variation_2(parents,kwargs):
    '''
    For each parent generate 'num_offspring'/'num_parents' offspring
    Variation on hour, day and room with +-1. When the bound is reached, restart from the other side.
    Crossover between two parents implemented selecting:
        parent_1.candidate[:random_index] rows 
        parent_2.candidate[random_index:] rows
    '''
    offspring = []
    num_offspring = kwargs['num_offspring']
    mutation_rate = kwargs['mutation_rate']
    crossover_rate = kwargs['crossover_rate']
    hour_size = kwargs['hour_size']
    day_size = kwargs['day_size']
    room_size= kwargs['room_size']

    # CROSSOVER 
    for parent_1 in parents:
        for i in range(round(num_offspring/len(parents))):
            candidate=parent_1.candidate.copy()
            individual = Individual(candidate=candidate) 

            random=np.random.uniform(0,1)
            if(random<crossover_rate and len(parents)>1):
                possible_parents = parents.copy()
                possible_parents.remove(parent_1)
                parent_2 = rdm.sample(possible_parents, 1)[0]
                crossover_point = np.random.choice(range(len(individual.candidate)))
                individual.candidate[crossover_point:]=parent_2.candidate[crossover_point:]
            offspring.append(individual)

    # MUTATION
    for individual in offspring:
        for i in range(len(individual.candidate)):

            # HOUR MUTATION
            random=np.random.uniform(0,1)
            mutation_type=np.random.randint(0,2)
            if (random<mutation_rate):
                if(mutation_type==0):
                    if((np.array(individual.candidate.at[i,'HOUR'])==hour_size).any()):
                        if(len(individual.candidate.at[i,'HOUR'])==3):
                            individual.candidate.at[i,'HOUR']==[1,2,3]
                        else:
                            individual.candidate.at[i,'HOUR']==[1,2]
                    else:
                        individual.candidate.at[i,'HOUR']=list(map(add,individual.candidate.at[i,'HOUR'],np.ones(len(individual.candidate.at[i,'HOUR']),int)))
                elif(mutation_type==1):
                    if(np.array(individual.candidate.at[i,'HOUR'])==1).any():
                        if(len(individual.candidate.at[i,'HOUR'])==3):
                            individual.candidate.at[i,'HOUR']=[hour_size-2,hour_size-1,hour_size]
                        else:
                            individual.candidate.at[i,'HOUR']=[hour_size-1,hour_size]
                    else:
                        individual.candidate.at[i,'HOUR']=list(map(lambda a, b: a - b,individual.candidate.at[i,'HOUR'],np.ones(len(individual.candidate.at[i,'HOUR']),int)))
            
            # DAY MUTATION
            random=np.random.uniform(0,1)
            mutation_type=np.random.randint(0,2)
            if (random<mutation_rate):
                if(mutation_type==0):
                    if(individual.candidate.at[i,'DAY']<day_size):
                        individual.candidate.at[i,'DAY']=individual.candidate.at[i,'DAY']+1
                    else:
                        individual.candidate.at[i,'DAY']==1
                elif(mutation_type==1):
                    if(individual.candidate.at[i,'DAY']>1):
                        individual.candidate.at[i,'DAY']=individual.candidate.at[i,'DAY']-1
                    else:
                        individual.candidate.at[i,'DAY']==day_size
            
            #  ROOM MUTATION
            random=np.random.uniform(0,1)
            mutation_type=np.random.randint(0,2)
            if (random<mutation_rate):
                if(mutation_type==0):
                    if(individual.candidate.at[i,'ROOM']<room_size):
                        individual.candidate.at[i,'ROOM']=individual.candidate.at[i,'ROOM']+1
                    else:
                        individual.candidate.at[i,'ROOM']==1
                elif(mutation_type==1):
                    if(individual.candidate.at[i,'ROOM']>1):
                        individual.candidate.at[i,'ROOM']=individual.candidate.at[i,'ROOM']-1
                    else:
                        individual.candidate.at[i,'ROOM']==room_size
    return offspring


def variation_3(parents,kwargs):
    '''
    For each parent generate 'num_offspring'/'num_parents' offspring
    Variation on hour, day and room with +-random_number(1, hout/day/room_size). 
    Crossover between two parents implemented selecting:
        parent_1.candidate[:random_index] rows 
        parent_2.candidate[random_index:] rows
    '''

    offspring = []
    num_offspring = kwargs['num_offspring']
    mutation_rate = kwargs['mutation_rate']
    crossover_rate = kwargs['crossover_rate']
    hour_size = kwargs['hour_size']
    day_size = kwargs['day_size']
    room_size= kwargs['room_size']

    # CROSSOVER 
    for parent_1 in parents:
        for i in range(round(num_offspring/len(parents))):
            candidate=parent_1.candidate.copy()
            individual = Individual(candidate=candidate) 
            
            random=np.random.uniform(0,1)
            if(random<crossover_rate and len(parents)>1):
                possible_parents = parents.copy()
                possible_parents.remove(parent_1)
                parent_2 = rdm.sample(possible_parents, 1)[0]
                crossover_point = np.random.choice(range(len(individual.candidate)))
                individual.candidate[crossover_point:]=parent_2.candidate[crossover_point:]
            offspring.append(individual)

    # MUTATION
    for individual in offspring:
        for i in range(len(individual.candidate)):

            # HOUR MUTATION
            delta_giono=np.random.randint(1,day_size)
            delta_ore=np.random.randint(1,hour_size)
            delta_ROOM=np.random.randint(1,room_size)
            random=np.random.uniform(0,1)
            if (random<mutation_rate):
                if(any(np.mod(np.array(individual.candidate.at[i,'HOUR'])+delta_ore, hour_size)==0)):
                    if(len(individual.candidate.at[i,'HOUR'])==2):
                        individual.candidate.at[i,'HOUR']=[1,2]
                    else:
                        individual.candidate.at[i,'HOUR']=[1,2,3]
                else:
                    individual.candidate.at[i,'HOUR'] = list(np.mod(np.array(individual.candidate.at[i,'HOUR'])+delta_ore, hour_size))

            # DAY MUTATION
            random=np.random.uniform(0,1)
            if (random<mutation_rate):
                if((individual.candidate.at[i,'DAY'])+delta_giono==day_size):
                    (individual.candidate.at[i,'DAY'])=(individual.candidate.at[i,'DAY']+delta_giono)
                else:
                    (individual.candidate.at[i,'DAY'])=np.mod(individual.candidate.at[i,'DAY']+delta_giono, day_size)

            #  ROOM MUTATION
            random=np.random.uniform(0,1)
            if (random<mutation_rate):
                if((individual.candidate.at[i,'ROOM'])+delta_ROOM==room_size):
                    (individual.candidate.at[i,'ROOM'])=(individual.candidate.at[i,'ROOM']+delta_ROOM)
                else:
                    (individual.candidate.at[i,'ROOM'])=np.mod(individual.candidate.at[i,'ROOM']+delta_ROOM, room_size)
    return offspring


def variation_4(parents,kwargs):
    '''
    Variation on hour, day and room with new random_number(1, hout/day/room_size). 
    Crossover between 'mixing_number' parents implemented selecting random rows from parents.
    '''

    mixing_number = kwargs.setdefault('mixing_number', 1)
    num_offspring = kwargs['num_offspring']
    mutation_rate = kwargs['mutation_rate']
    crossover_rate = kwargs['crossover_rate']
    hour_size = kwargs['hour_size']
    day_size = kwargs['day_size']
    room_size= kwargs['room_size']

    offspring = []

    while len(offspring) < num_offspring:

        parents_tmp = rdm.sample(parents, mixing_number)
        individual = Individual(candidate= parents_tmp[0].candidate.copy())

        # CROSSOVER 
        random = np.random.uniform(0,1)
        if(random<crossover_rate and mixing_number>1):
            candidates_tmp = [parent.candidate.copy() for parent in parents_tmp]
            for row_index in range(len(candidates_tmp[0])):
                row_tmp = rdm.sample(candidates_tmp, 1)[0].iloc[row_index]
                individual.candidate.iloc[row_index] = row_tmp

        # MUTATION
        candidate_tmp = individual.candidate
        for i in range(len(candidate_tmp)):

            # HOUR MUTATION
            random=np.random.uniform(0,1)
            if (random<mutation_rate):
                if(len(candidate_tmp.at[i,'HOUR'])>2):
                    random=np.random.randint(1,hour_size-1)
                    candidate_tmp.at[i,'HOUR'] = [random,random+1,random+2]
                else: 
                    random=np.random.randint(1,hour_size)
                    candidate_tmp.at[i,'HOUR'] = [random,random+1]

            # DAY MUTATION
            random=np.random.uniform(0,1)
            if (random<mutation_rate):
                candidate_tmp.at[i,'DAY'] = np.random.randint(1,day_size)

            #  ROOM MUTATION
            random=np.random.uniform(0,1)
            if (random<mutation_rate):
                candidate_tmp.at[i,'ROOM'] = np.random.randint(0,room_size)
 
        offspring.append(individual)

    return offspring