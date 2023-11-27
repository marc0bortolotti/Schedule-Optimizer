def calculate_diversity(population):
    diversity = 0
    for individual_i in population:
        for individual_j in population:
            diversity_tmp = 0
            candidate_i = individual_i.candidate.copy()
            candidate_j = individual_j.candidate.copy()
            differences = candidate_i.compare(candidate_j) # see example below
            differences = differences.count() 
            for dif in differences:
                diversity_tmp += dif
            diversity_tmp = diversity_tmp/2 # remove count in column 'other' which is the same of 'self'
            diversity+=int(diversity_tmp)
    return diversity/2 # remove cases individual_j compare to individual_i


'''
EXAMPLE

differences = candidate_i.compare(candidate_j)   
NB: return Nan if the values are equal
                                             
    -> AULA: self other ORA: self  other 
             7    4          [2,3] [4,5]
             Nan  Nan        [7,8] [1,2]    
             2    10         Nan   Nan
             Nan  Nan        [1,2] [6,7]       

differences = differences.count() 
NB: coun non-Nan values in columns     

    -> AULA: self other ORA: self  other 
             2    2          3     3                                 

'''