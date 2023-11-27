
from run_ea import *
from writer import *
from individual import *
from pylab import *
import cv2

default_results_path = 'results'
default_sources_path = 'courses.xlsx' 

if __name__ == '__main__':

    kwargs = {} 
    
    # PATH
    kwargs['source_path'] = default_sources_path 
    kwargs['results_path'] = default_results_path

    # TYPE
    kwargs['analisy_type']='different_variation'  #'mutation_vs_crossover','different_crossover_rates', 'different_mutation_rates','different_selection' ,'different_variation', 'different_replacement'

    # PARAMETERS
    kwargs['num_runs'] = 10
    kwargs['num_offspring'] = 20
    kwargs['pop_size'] = 20
    kwargs['max_generations'] = 10
    kwargs['room_size'] = 40
    kwargs['mutation_rate'] = 0.1
    kwargs['crossover_rate'] = 0.9
    kwargs['selector'] = 'tournament_selection'
    kwargs['variator'] = 'variation_4'
    kwargs['replacer'] = 'plus_replacement'
    # kwargs['mixing_number'] = 2 # for variation_5()
    kwargs['tournament_size'] = 8 # for tournament_selection()
    # kwargs['num_selected'] = 10 # for truncation_selection()


    num_runs=kwargs['num_runs']
    

    #----------------MUTATION-VS CROSSOVER---------------
    if kwargs['analisy_type']=='mutation_vs_crossover':

        print('\n\nMUTATION VS CROSSOVER\n\n')
            
        best_fitness_mutation_only_list=[]
        kwargs['experiment_type']='mutation_only'
        for i in range(num_runs):
            print('\nMUTATION ONLY\tRUN', i+1,'/',num_runs)
            kwargs['crossover_rate']=0
            kwargs['mutation_rate']=1
            kwargs['results_path'] = default_results_path+'/'+kwargs['analisy_type']+'/'+kwargs['experiment_type']+'/run_'+str(i)
            best_individual, population, fitness_list, diversity_list = run_ea(**kwargs)
            best_fitness_mutation_only_list.append(best_individual.fitness)
            
        best_fitness_crossover_only_list=[]
        kwargs['experiment_type']='crossover_only'
        for i in range(num_runs):
            print('\nCROSSOVER ONLY\tRUN', i+1,'/',num_runs)
            kwargs['crossover_rate']=1
            kwargs['mutation_rate']=0
            kwargs['results_path'] = default_results_path+'/'+kwargs['analisy_type']+'/'+kwargs['experiment_type']+'/run_'+str(i)
            best_individual, population, fitness_list, diversity_list = run_ea(**kwargs)
            best_fitness_crossover_only_list.append(best_individual.fitness)
            
        fig = figure('Mutation only V/S crossover only')
        ax = fig.gca()
        ax.boxplot([best_fitness_mutation_only_list, best_fitness_crossover_only_list], notch=False)
        ax.set_xticklabels(['Mutation only', 'Crossover only'])
        ax.set_yscale('log')
        ax.set_xlabel('Condition')
        ax.set_ylabel('Best fitness')
        fig_path = default_results_path+'/'+kwargs['analisy_type']+'/only_mutation_VS_only_crossover.png'
        fig.savefig(fig_path)
        close(fig)

    
    #---------------------------DIFFERENT-CROSSOVER-RATES-----------------------------
    elif(kwargs['analisy_type']=='different_crossover_rates'):

        print('\n\nDIFFERENT CROSSOVER RATES\n\n')

        best_fitnesses=[]
        crossover_rates = [0, 0.25, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        for crossover_rate in crossover_rates :
            kwargs['crossover_rate']=crossover_rate
            kwargs['experiment_type']=crossover_rate
            best_fitness_single_crossover=[]
            for i in range(num_runs):
                print('\nCROSSOVER RATE =',kwargs['crossover_rate'],'\tRUN', i+1,'/',num_runs)
                kwargs['results_path'] =  default_results_path+'/'+kwargs['analisy_type']+'/'+kwargs['experiment_type']+'/run_'+str(i)
                best_individual, population, fitness_list, diversity_list = run_ea(**kwargs)
                best_fitness_single_crossover.append(best_individual.fitness)
            best_fitnesses.append(best_fitness_single_crossover)
            
        fig = figure('Best Crossover rate')
        ax = fig.gca()
        ax.boxplot(best_fitnesses,notch=False)
        ax.set_xticklabels(crossover_rates)
        ax.set_xlabel('Crossover rate')
        ax.set_ylabel('Best fitness')
        fig_path = default_results_path+'/'+kwargs['analisy_type']+'/Best_Mutation_Rate.png'
        fig.savefig(fig_path)
        close(fig)
    
    
    #---------------------------DIFFERENT-MUTATION-RATES-----------------------------
    elif(kwargs['analisy_type']=='different_mutation_rates'):
        
        print('\n\nDIFFERENT MUTATION RATES\n\n')
        
        best_fitnesses=[]
        mutation_rates = [0, 0.25, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

        for mutation_rate in mutation_rates :
            kwargs['mutation_rate']=mutation_rate
            kwargs['experiment_type']='mutation_rate='+str(mutation_rate)
            best_fitness_single_mutation=[]
            for i in range(num_runs):
                print('\nMUTATION RATE =',kwargs['mutation_rate'],'\tRUN', i+1,'/',num_runs)
                kwargs['results_path'] = default_results_path+'/'+kwargs['analisy_type']+'/'+kwargs['experiment_type']+'/run_'+str(i)
                best_individual, population, fitness_list, diversity_list = run_ea(**kwargs)
                best_fitness_single_mutation.append(best_individual.fitness)
            best_fitnesses.append(best_fitness_single_mutation)
            
        fig = figure('Best Mutation rate')
        ax = fig.gca()
        ax.boxplot(best_fitnesses,notch=False)
        ax.set_xticklabels(mutation_rates)
        ax.set_xlabel('Mutation Rate')
        ax.set_ylabel('Best fitness')
        fig_path = default_results_path+'/'+kwargs['analisy_type']+'/Best_Mutation_Rate.png'
        fig.savefig(fig_path)
        close(fig)
    
    
    #---------------------------DIFFERENT-VARIATOR----------------------------- 
    elif(kwargs['analisy_type']=='different_variation'):

        print('\n\nDIFFERENT VARIATIONS\n\n')

        variators=[var for var in dir(variator) if 'variation' in var]

        best_fitnesses=[]
        for var in variators :
            kwargs['variator']=var
            kwargs['experiment_type']=var
            best_fitness=[]
            for i in range(num_runs):
                print('\nVARIATOR =',kwargs['variator'],'\tRUN', i+1,'/',num_runs)
                kwargs['results_path'] = default_results_path+'/'+kwargs['analisy_type']+'/'+kwargs['experiment_type']+'/run_'+str(i)
                best_individual, population, fitness_list, diversity_list = run_ea(**kwargs)
                best_fitness.append(best_individual.fitness)
            best_fitnesses.append(best_fitness)
            
        fig = figure('Best Variation')
        ax = fig.gca()
        ax.boxplot(best_fitnesses,notch=False)
        ax.set_xticklabels(variators)
        ax.set_xlabel('Variation')
        ax.set_ylabel('Best fitness')
        fig_path = default_results_path+'/'+kwargs['analisy_type']+'/Best_Variation.png'
        fig.savefig(fig_path)
        close(fig)
            
    #---------------------------DIFFERENT-SELECTION-----------------------------
    elif(kwargs['analisy_type']=='different_selection'):

        print('\n\nDIFFERENT SELECTIONS\n\n')
        selectors=[sel for sel in dir(selector) if 'selection' in sel]
        best_fitnesses=[]
        for sel in selectors :
            kwargs['selector']=sel
            kwargs['experiment_type']=sel
            best_fitness=[]
            for i in range(num_runs):
                print('\nSELECTOR =',kwargs['selector'],'\tRUN', i+1,'/',num_runs)
                kwargs['results_path'] = default_results_path+'/'+kwargs['analisy_type']+'/'+kwargs['experiment_type']+'/run_'+str(i)
                best_individual, population, fitness_list, diversity_list = run_ea(**kwargs)
                best_fitness.append(best_individual.fitness)
            best_fitnesses.append(best_fitness)
            
        fig = figure('Best Selection')
        ax = fig.gca()
        ax.boxplot(best_fitnesses,notch=False)
        ax.set_xticklabels(selectors)
        ax.set_xlabel('Selection')
        ax.set_ylabel('Best fitness')
        fig_path = default_results_path+'/'+kwargs['analisy_type']+'/Best_Variation.png'
        fig.savefig(fig_path)
        close(fig)
    
    
    #---------------------------DIFFERENT-REPLACER-----------------------------        
    elif(kwargs['analisy_type']=='different_replacement'):

        print('\n\nDIFFERENT REPLACEMENTS\n\n')

        replacers=[rep for rep in dir(replacer) if 'replacement' in rep]
        
        best_fitnesses=[]
        for rep in replacers :
            kwargs['replacer']=rep
            kwargs['experiment_type']=rep 
            best_fitness=[]
            for i in range(num_runs):
                print('\nREPLACER =',kwargs['replacer'],'\tRUN', i+1,'/',num_runs)
                kwargs['results_path'] = default_results_path+'/'+kwargs['analisy_type']+'/'+kwargs['experiment_type']+'/run_'+str(i)
                best_individual, population, fitness_list, diversity_list = run_ea(**kwargs)
                best_fitness.append(best_individual.fitness)
            best_fitnesses.append(best_fitness)
            
        fig = figure('Best Replacement')
        ax = fig.gca()
        ax.boxplot(best_fitnesses,notch=False)
        ax.set_xticklabels(replacers)
        ax.set_xlabel('Replacement')
        ax.set_ylabel('Best fitness')
        fig_path = default_results_path+'/'+kwargs['analisy_type']+'/Best_Replacement.png'
        fig.savefig(fig_path)
        close(fig)


    # SHOW BOXPLOT
    fig = cv2.imread(fig_path)
    cv2.imshow(" ", fig)
    cv2.waitKey(0)
    