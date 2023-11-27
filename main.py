from run_ea import run_ea
import cv2


if __name__ == "__main__":

    kwargs = {} 
    
    # PATH
    kwargs['source_path'] = 'courses.xlsx'   
    kwargs['results_path'] = 'results/single_optimization'

    # PARAMETERS
    kwargs['num_offspring'] = 2
    kwargs['pop_size'] = 3
    kwargs['max_generations'] = 2
    kwargs['room_size'] = 40
    kwargs['mutation_rate'] = 0.1
    kwargs['crossover_rate'] = 0.9
    kwargs['selector'] = 'tournament_selection'
    kwargs['variator'] = 'variation_4'
    kwargs['replacer'] = 'plus_replacement'
    # kwargs['mixing_number'] = 2 # for variation_4()
    # kwargs['tournament_size'] = 5 # for tournament_selection()
    # kwargs['num_selected'] = 10 # for truncation_selection()

    best_individual, population, fitness_list, diversity_list = run_ea(**kwargs)

    print('Best Fitness:', best_individual.fitness)
    print('Overlaps in rooms:', best_individual.room_overlap)
    print('Overlaps of lessons:', best_individual.hour_overlap)
    print('Overlaps in mandatory teachings:', best_individual.type_overlap)

    
    # SHOW FITNESS and DIVERSITY
    fitness = cv2.imread(kwargs['results_path']+'/fitness.png')
    diversity = cv2.imread(kwargs['results_path']+'/diversity.png')
    cv2.imshow("Fitness", fitness)
    cv2.imshow("Diversity", diversity)
    cv2.waitKey(0)





        