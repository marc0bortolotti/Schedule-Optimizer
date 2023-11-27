# Schedule-Optimizer

The Schedule-Optimizer aims to design an accademic schedule starting from a table of teachings from different courses of studying. The optimization is made by an Evolutionary Algorithm which explore the space of solutions to find the best ones in terms of fitness. The latter take into consideration different aspects of an accademic schedule. In particular, the fact that a teaching cannot be repeated in the same day or that there cannot be any overlapping of lessons or classrooms. Note that an individual is represented by its candidate solution which is a defined schedule whcih take into account all the teachings present inside the source file. During the evolution phase, it maybe mutate in 'HOUR','DAY', or 'ROOM' to explore different combinations which can improve the individual's fitness value.
## Requiremets
Python packages:   
- pylab
- pandas
- collections
- numpy
- cv2
- operator
- dash
- plotly
- dash_bootstrap_components

## Usage
Before running the optimization, be sure that the variable 'source_path' points to the correct file position.
Note that, to make the script run correctly, the source file **MUST** have the same columns'name as in the example below. 
Then, a single optimization can be simple made by running the following command from the command line:
```
python main.py
```
Furthermore, to better visualize the results of the optimization, a dashboard has been designed. 
Run the following command and open the link that appears to launch the dashboard.
```
python dashboard.py
```
If you want to verify the performance of different sets of parameters, run the multiple optimizations script:
```
python multiple_optimizations.py
```
You can choose among:
- 'mutation_vs_crossover'
- 'different_crossover_rates'
- 'different_mutation_rates'
- 'different_selection'
- 'different_variation'
- 'different_replacement'

## Results
The optimization outputs an excel file as the following:

![Schedule](/example_images/schedule.png)

The number of printed schedules depends on the number of course of studying offered by the department and thus involved in the optimization to be sure that any room won't be occupated at the same time from teachings of different kinds of stydiyng. 
Below an example of the source file is reported. Note that columns' name are pre-defined and cannot be changed. On the other hand, you can add/remove/modify teachings as you prefer.

![Source](/example_images/source.png)

Furthermore, you can also visualize:
- the initial population (initial_population.xlsx)
- the final population (final_population.xlsx)
- the initial schedule (initial_schedule.xlsx)
- the fitness graph (fitness.png)
- the diversity graoh (diversity.png)
- summary of the optimization (statisctics.txt)

If you run multiple optimizations, you can visualize also a boxplot (i.e. Best_Variation in /results/multiple_optimizations/different_variation)
