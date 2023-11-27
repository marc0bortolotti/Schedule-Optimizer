# Schedule-Optimizer

The Schedule-Optimizer aims to design an accademic schedule starting from a table of teachings from different courses of studying. The optimization is made by an Evolutionary Algorithm which explore the space of solutions to find the best ones in terms of fitness. The latter take into consideration different aspects of an accademic schedule. In particular, the fact that a teaching cannot be repeated in the same day or that there cannot be any overlapping of lessons or classrooms.
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
To verify the performance of different sets of parameters, run the multiple optimizations script:
```
python multiple_optimizations.py
```
You can choose among:
- 

## Results
![Tux, the Linux mascot](/example_images/schedule.png)
![Tux, the Linux mascot](/example_images/source.png)
