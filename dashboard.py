import pandas as pd
import dash
from dash import Dash, html, dcc, dash_table, callback, ctx
import pandas as pd
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
from run_ea import run_ea
import variator
import selector
import replacer

kwargs = {}

# PATH
results_path = 'results/single_optimization'
final_schedule_path = results_path+'/final_schedule.xlsx'
kwargs['results_path'] = results_path
kwargs['source_path'] = 'source/courses.xlsx'

# DEFAULT OPTIMIZATION PARAMETERS 
stop_interrupt = False
default_max_generations = 50
default_pop_size = 20
default_num_offspring = 100
default_room_size = 5
default_crossover_rate = 0.9
default_mutation_rate = 0.1
selectors = [var for var in dir(selector) if 'selection' in var]
variators = [var for var in dir(variator) if 'variation' in var]
replacers = [var for var in dir(replacer) if 'replacement' in var]
courses = pd.read_excel(kwargs['source_path'])['COURSE OF STUDYING'].unique()
last_selected_course = None
fitness_list = None

# DASHBOARD
theme = dbc.themes.BOOTSTRAP
css = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
app = dash.Dash(external_stylesheets=[theme, css])

'''for style consult Cascading Style Sheets(CSS)'''

title = dbc.Row(dbc.Col([html.Br(),
                         html.H1("SCHEDULE OPTIMIZER"),
                         html.Br(),
                         html.H5("Course Project: Bio-Inspired AI"),
                         html.Br()]),
                className="text-center",
                style={'color': 'Black', 'background-color': 'White'})  # 'color': 'AliceBlue', 'background-color': 'Teal'}

input_1 = html.Div([html.H6('Max Generations',style={'display':'inline-block','margin-right':47, 'color': 'black'}),
                    dcc.Input(id='max_generations',type='text',placeholder=str(default_max_generations),style={'display':'inline-block', 'width':'40px', 'textAlign': 'center'})])
input_2 = html.Div([html.H6('Population Size',style={'display':'inline-block','margin-right':58, 'color': 'black'}),
                    dcc.Input(id='pop_size',type='text',placeholder=str(default_pop_size),style={'display':'inline-block', 'width':'40px', 'textAlign': 'center'})])
input_3 = html.Div([html.H6('Number of offspring',style={'display':'inline-block','margin-right':20, 'color': 'black'}),
                    dcc.Input(id='num_offspring',type='text',placeholder=str(default_num_offspring),style={'display':'inline-block', 'width':'40px', 'textAlign': 'center'})])
input_4 = html.Div([html.H6('Available Rooms',style={'display':'inline-block','margin-right':50, 'color': 'black'}),
                    dcc.Input(id='room_size',type='text',placeholder=str(default_room_size),style={'display':'inline-block', 'width':'40px', 'textAlign': 'center'})])
input_5 = html.Div([html.H6('Crossover Rate',style={'display':'inline-block','margin-right':60, 'color': 'black'}),
                    dcc.Input(id='crossover_rate',type='text',placeholder=str(default_crossover_rate),style={'display':'inline-block', 'width':'40px', 'textAlign': 'center'})])
input_6 = html.Div([html.H6('Mutation Rate',style={'display':'inline-block','margin-right':64, 'color': 'black'}),
                    dcc.Input(id='mutation_rate',type='text',placeholder=str(default_mutation_rate),style={'display':'inline-block', 'width':'40px', 'textAlign': 'center'})])

dropdown_selector = html.Div([html.H6("Selector",style={'display':'inline-block', 'color': 'black', 'margin-right':16, 'margin-top':10}),
                              dcc.Dropdown(selectors, id='dropdown_selector', placeholder=selectors[-2], style={'display':'inline-block', 'width': '200px', 'textAlign': 'center',  'vertical-align': 'middle'})])

dropdown_replacer = html.Div([html.H6("Replacer",style={'display':'inline-block', 'color': 'black', 'margin-right':13, 'margin-top':10}),
                              dcc.Dropdown(replacers, id='dropdown_replacer', placeholder=replacers[-1], style={'display':'inline-block', 'width': '200px', 'textAlign': 'center', 'vertical-align': 'middle'})])

dropdown_variator = html.Div([html.H6("Variator",style={'display':'inline-block', 'color': 'black', 'margin-right':18, 'margin-top':10}),
                              dcc.Dropdown(variators, id='dropdown_variator', placeholder=variators[-1], style={'display':'inline-block', 'width': '200px', 'textAlign': 'center', 'vertical-align': 'middle'})])

dropdown_courses =  html.Div([html.H6("Course of Study",style={'color': 'black', 'margin-top':60}),
                              dcc.Dropdown(courses, id='dropdown_courses', style={'display':'inline-block', 'width': '200px', 'textAlign': 'center'})])

start_button = dbc.Button("Run Optimization", color="primary", id="run_optimization", style={'width': '300px','textAlign': 'center'})

input_arguments = html.Div([html.H6("Insert other parameters (i.e. mixing_number=3)",style={'color': 'black', 'margin-top':20}),
                            dcc.Input(id="input_arguments", type="text", placeholder="", debounce=True)])

selection = dbc.Row([dbc.Col([html.Br(),input_1, input_2, input_3, input_4, input_5, input_6, input_arguments], width=3),
                     dbc.Col([html.Br(), start_button, dropdown_courses], width=4, style={'background-color': 'White'}),
                     dbc.Col([html.Br(),dropdown_selector, dropdown_variator, dropdown_replacer], width=3)],
                    className="text-center",
                    justify="center",  
                    style={'color': 'gray'})

output = dbc.Row([dcc.Loading(children=dbc.Container(id='output_img_table'),id="loading",type="dot")],
                 className="text-center",
                 style={'color': 'gray'})     

app.layout = dbc.Container(fluid=True, 
                           children=[title,
                                     selection,
                                     html.Br(),
                                     output])

def output():
    table = dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns],
                                 style_cell = {'font_family': 'sans-serif',
                                               'font_size': '15px',
                                               'text_align': 'center'},
                                 style_header={'fontWeight': 'bold'},                                     
                                 id = 'tbl')
  
    graph_fit = dcc.Graph(id="graph", figure=fig_fit)
    graph_div = dcc.Graph(id="graph", figure=fig_div)

    title_1 = html.H5("Schedule",style={'color': 'black'})
    statistics_1 = []
    statistics_1.append(html.H6("Statisctics:",style={'color': 'black', 'text-align': 'left'}))
    statistics_1.append(html.H6("Best Fitness Value: "+str(best_individual.fitness),style={'color': 'gray', 'text-align': 'left'}))
    statistics_1.append(html.H6("Number of lessons overlapped: "+str(best_individual.hour_overlap),style={'color': 'gray', 'text-align': 'left'}))
    statistics_1.append(html.H6("Number of mandatory teachings overlapped: "+str(best_individual.type_overlap),style={'color': 'gray', 'text-align': 'left'}))

    statistics_2 = []
    statistics_2.append(html.H6("Rooms overlapped: ",style={'color': 'black', 'text-align': 'left'}))

    if len(best_individual.room_overlap) == 0:
        statistics_2.append(html.H6('No rooms overlapped', style={'color': 'gray', 'text-align': 'left'}))
    else:
        days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        for overlap in best_individual.room_overlap:
            day = days[overlap['DAY']-1]
            hour = str(7+overlap['HOUR'])+':30 - '+str(8+overlap['HOUR'])+':30'
            room = 'ROOM '+str(overlap['ROOM']) 
            str_tmp = room+': '+day+', '+hour
            statistics_2.append(html.H6(str_tmp, style={'color': 'gray', 'text-align': 'left'}))

    children = dbc.Container([title_1,
                              html.Br(),
                              dbc.Col(table),
                              html.Br(),html.Br(),
                              dbc.Row([dbc.Col(statistics_1, width=4), dbc.Col(statistics_2, width=4)], justify="center", style={'margin-left':150}),
                              dbc.Row([dbc.Col(graph_fit), dbc.Col(graph_div)])])
    return children


@app.callback(Output('output_img_table', 'children'),
              Input('run_optimization', 'n_clicks'),
              Input('max_generations', 'value'),
              Input('pop_size', 'value'),
              Input('num_offspring', 'value'),
              Input('room_size', 'value'),
              Input('crossover_rate', 'value'),
              Input('mutation_rate', 'value'),
              Input('dropdown_courses', 'value'),
              Input('input_arguments', 'value'),
              Input('dropdown_selector', 'value'),
              Input('dropdown_variator', 'value'),
              Input('dropdown_replacer', 'value'))

def update_output(run_optimization, max_generations , pop_size, num_offspring, room_size, crossover_rate, mutation_rate, selected_course, new_argument, selected_selector, selected_variator, selected_replacer):
    
    global best_individual, fitness_list, last_selected_course, fig_fit, fig_div, df, stop_interrupt
    triggered_id = ctx.triggered_id

    if new_argument is not None:
        new_argument = new_argument.replace(" ", "") # remove eventual spaces
        key_word = new_argument.split('=')[0]
        value =  new_argument.split('=')[1] 
        if value.isdigit(): 
            value = int(value)
        kwargs[key_word] = value

    if triggered_id == 'run_optimization':

        if(selected_course == None): selected_course = courses[0]
        if(num_offspring==None): num_offspring = default_num_offspring
        if(pop_size==None): pop_size = default_pop_size
        if(max_generations==None): max_generations = default_max_generations
        if(room_size==None): room_size = default_room_size
        if(crossover_rate==None): crossover_rate = default_crossover_rate
        if(mutation_rate==None): mutation_rate = default_mutation_rate
        if(selected_selector==None): selected_selector = selectors[-2]
        if(selected_variator==None): selected_variator = variators[-1]
        if(selected_replacer==None): selected_replacer = replacers[-1]

        last_selected_course = selected_course

        kwargs['num_offspring'] = int(num_offspring)
        kwargs['pop_size'] = int(pop_size)
        kwargs['max_generations'] = int(max_generations)
        kwargs['room_size'] = int(room_size)
        kwargs['crossover_rate'] = float(crossover_rate)
        kwargs['mutation_rate'] = float(mutation_rate)
        kwargs['selector'] = selected_selector
        kwargs['variator'] = selected_variator
        kwargs['replacer'] = selected_replacer

        best_individual, population, fitness_list, diversity_list = run_ea(**kwargs)

        df = pd.read_excel(final_schedule_path, sheet_name=selected_course) 

        # FITNESS GRAPH
        max_fitness = []
        min_fitness = []
        mean_fitness = []
        for generattion_fitness in fitness_list:
            generattion_fitness.sort()
            max_fitness.append(generattion_fitness[-1])
            min_fitness.append(generattion_fitness[0])
            mean_fitness.append(sum(generattion_fitness)/len(generattion_fitness))
        x = [i for i, fit in enumerate(max_fitness)]
        fig_fit = go.Figure(data=[go.Scatter(x=x, y=max_fitness, marker = {'color' : 'red'}, name = 'Worst'),
                                  go.Scatter(x=x, y=min_fitness, marker = {'color' : 'green'}, name = 'Best'),
                                  go.Scatter(x=x, y=mean_fitness, marker = {'color' : 'orange'}, name = 'Mean')],
                            layout = go.Layout(title={'text':'<b>Fitness</b>', 'xanchor': 'center', 'y':0.9, 'x':0.5, 'yanchor': 'top'}, title_font_color='black')) 
        
        # DIVERSITY GRAPH
        x = [i for i, fit in enumerate(diversity_list)]
        fig_div = go.Figure(data=go.Scatter(x=x, y=diversity_list, marker = {'color' : 'orange'}),
                            layout = go.Layout(title={'text':'<b>Diversity</b>', 'xanchor': 'center', 'y':0.9, 'x':0.5, 'yanchor': 'top'}, title_font_color='black'))
    
        return output()
    
    if selected_course!=last_selected_course and fitness_list is not None:
        if selected_course is None: 
            selected_course = last_selected_course
            last_selected_course = None
        else: last_selected_course = selected_course
        df = pd.read_excel(final_schedule_path, sheet_name=selected_course) 
        return output()
    

# MAIN
if __name__ == '__main__':
    app.run_server()


