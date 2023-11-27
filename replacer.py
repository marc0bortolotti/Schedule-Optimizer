def default_replacement(parents, offspring, kwargs):
    population = parents + offspring
    return population


def plus_replacement(parents, offspring, kwargs):
    population = parents+offspring
    pop_size = kwargs.setdefault('pop_size',len(population))
    population.sort(reverse=True)
    population = population[:pop_size]
    return population