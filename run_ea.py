import selector 
import replacer 
import variator 
from writer import *
from individual import *
from diversity import calculate_diversity
import os
from datetime import datetime


default_source_path = 'courses.xlsx'
default_results_path = 'results'


def run_ea(**kwargs):

    start_time = datetime.now()

    hour_size = kwargs.setdefault('hour_size', 11)
    day_size = kwargs.setdefault('day_size', 5)

    max_generations = kwargs.setdefault('max_generations', 100)
    pop_size = kwargs.setdefault('pop_size', 20)
    num_offspring = kwargs.setdefault('num_offspring', 100)
    room_size = kwargs.setdefault('room_size', 20)
    mutation_rate = kwargs.setdefault('mutation_rate', 0.1)
    crossover_rate = kwargs.setdefault('crossover_rate', 0.9)

    source_path = kwargs.setdefault('source_path', default_source_path)
    results_path = kwargs.setdefault('results_path', default_results_path)
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    final_schedule_path = results_path+'/final_schedule.xlsx'
    initial_schedule_path = results_path+'/initial_schedule.xlsx'
    final_population_path = results_path+'/final_population.xlsx'
    initial_population_path = results_path+'/initial_population.xlsx'
    best_individual_path = results_path+'/best_individual.xlsx'
    fitness_path = results_path+'/fitness.png'
    diversity_path = results_path+'/diversity.png'
    statistics_path = results_path+'/statisctic.txt'

    selection = getattr(selector, kwargs['selector'] )
    variation = getattr(variator, kwargs['variator'])
    replacement = getattr(replacer, kwargs['replacer'])

    # INITIALIZATION
    print("\nINITIALIZATION...")
    population = initialize_population(kwargs)
    save_population(population, initial_population_path)
    save_schedule(population[0], initial_schedule_path, kwargs)

    # OPTIMIZATION
    '''The general outline of an epoch is selection, variation, evaluation, replacement, migration, archival, and observation'''
    print("\nOPTIMIZATION...\t("+kwargs['selector']+', '+kwargs['variator']+', '+kwargs['replacer']+')')
    iter = 0
    terminate_condition = False
    fitness_list = []
    diversity_list = []
    while iter < max_generations and not terminate_condition:
        parents = selection(population, kwargs)
        offspring = variation(parents, kwargs)
        generation_fitness = evaluate(parents+offspring)
        population = replacement(parents, offspring, kwargs)
        population.sort(reverse=True)
        best_individual = population[0]
        terminate_condition = terminate(best_individual.fitness)
        
        print('Generation: ',(iter+1),'/',max_generations,'\tBest Fitness: ', best_individual.fitness)
        fitness_list.append(generation_fitness)
        diversity_list.append(calculate_diversity(population))
        iter+=1
    
    end_time = datetime.now()
    kwargs['time'] = end_time - start_time

    print('\nTime:', kwargs['time'])

    # SAVE RESULTS
    print('\nSAVING RESULTS...')
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    save_individual(best_individual, best_individual_path)
    save_population(population, final_population_path)
    save_schedule(best_individual, final_schedule_path, kwargs)
    save_fitness(fitness_list, fitness_path)
    save_diversity(diversity_list, diversity_path)
    save_statistics(best_individual, kwargs, statistics_path)
    print('\n\n\n')

    return best_individual, population, fitness_list, diversity_list
