from individual import Individual, generate_individual, evaluate
import random

def default_selection(population, kwargs):
    return population


def truncation_selection(population, kwargs): 
    num_selected = kwargs.setdefault('num_selected', kwargs['pop_size'])
    population.sort(reverse=True)
    survivors = population[:num_selected]
    return survivors


def tournament_selection(population, kwargs):
    tournament_size = kwargs.setdefault('tournament_size', 2)
    num_selected = kwargs.setdefault('num_selected', kwargs['pop_size'])
    survivors = []
    for i in range(num_selected):
        tournament = random.sample(population, tournament_size)
        tournament.sort(reverse=True)
        survivors.append(tournament[0])   
    return survivors
