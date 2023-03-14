import sys, os
current_file_directory = os.path.realpath(__file__)
# adding the statistics_tool folder to path
sys.path.append(os.path.join(os.path.join(os.path.join(current_file_directory, '..'), '..'), '..'))

from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import flask_GUI.dash_apps.my_pivot_table as pt
from classes_and_utils.GUI_utils import *
from flask_GUI.dash_apps.results_table_css import css
from flask import Flask, render_template
from flask_GUI.constants import COLOR_GRADIENT_RED_WHITE_BLUE
import math

MAIN_EXP = 'main'
REF_EXP = 'ref'

def get_color_from_gradient(x, gradient):
    if x<0 or x>1:
        print ("values must be between 0-1")
        return 'white'
    
    gradient_len = len(gradient)
    idx = math.ceil(x*(gradient_len-1))
    return gradient[idx]
    
def get_color_by_two_values_diff(ref, main, gradient):

    if ref ==0 or type(main)==str or type(ref)==str:
        return 'white'
    precentage_change = min(1, (main/ref) - 1) #not allowing more that 100% improvement
    color_presentage = (1 + precentage_change) * 0.5
    return get_color_from_gradient(color_presentage, gradient)



class Results_table():
    def __init__(self, server):

        self.dash_app = Dash(
            __name__,
            server=server,
            url_base_pathname='/dash/',
            external_stylesheets=[dbc.themes.COSMO])

        self.table = None
        self.dash_app.layout = self.get_layout()
        # self.set_callbacks()

    # def set_callbacks(self):
        self.dash_app.callback(
            Output('cols_seg', 'options'),
            Output('rows_seg', 'options'),
            Input('init', 'value')) \
            (lambda x: (self.segmentation_categories, self.segmentation_categories))

    def set_data(self, exp, segmentations):
        self.table = pt.PivotTable(segmentations, data = exp, cell_function=self.get_cell_exp)
        self.segmentation_categories = list(segmentations.keys())

    def get_webpage(self):
        return self.dash_app.index()

    def get_cell_exp(self, all_exps, column_keys, row_keys):  
        '''
        The function that return a single cell
        '''     
        segmentations = [curr_segment for curr_segment in column_keys+row_keys if 'None' not in curr_segment.keys()]

        exp_data = {}
        exp_data[MAIN_EXP] = all_exps[MAIN_EXP].get_cell_data(segmentations)
        if all_exps[REF_EXP] !=[]:
            exp_data[REF_EXP] = all_exps[REF_EXP][0].get_cell_data(segmentations) 

        all_metrics = []
        for k in exp_data[MAIN_EXP].keys():
            
            TDs = [html.Td(k)]
            num_of_exps = len(exp_data.keys())

            for exp_name in exp_data.keys():
                txt = "{}".format(exp_data[exp_name][k])
                if k in ["TP", "FP", "FN"]:
                    link = "/update_list?cell_name={}&stat={}".format(exp_data[exp_name]['cell_name'],k)
                    curr_metric = html.A(txt ,href=link, target="example-list-div")
                    color = 'white'
                else:
                    curr_metric = txt
                    color = 'white' if num_of_exps == 1 else\
                    get_color_by_two_values_diff(exp_data[REF_EXP][k], exp_data[MAIN_EXP][k], COLOR_GRADIENT_RED_WHITE_BLUE)

                TDs.append(html.Td(curr_metric, style={'background-color':color}))

                if k in ["TP", "FP", "FN"]:
                    if self.table.unique_helper != None:
                        unique = self.table.unique_helper.generate_unique_html_dash_element(column_keys,row_keys,k,exp_name)
                        TDs.append(html.Td(unique, style={'background-color':color}))
                    else:
                        TDs.append(html.Td('', style={'background-color':color}))
                else:
                    TDs.append(html.Td('', style={'background-color':color}))

                TDs.append(dbc.Button("Open Offcanvas", id="open-offcanvas", n_clicks=0))                    


            all_metrics.append(html.Tr(TDs))

        cell_content = html.Table(all_metrics)
        to_show = html.Td(cell_content)

        return to_show
    
    def get_layout(self):
        Title_div = html.Div([dbc.Alert("Reporter Page", className="m-1"), html.H6("init_value", id='init')], style=css['title'])

        cols_segmentation_dropdown = html.Div(
                                        dcc.Dropdown([], [],
                                        id='cols_seg', multi=True),
                                        style={'width':'50%'})
        rows_segmentation_dropdown = html.Div(
                                        dcc.Dropdown([], [],
                                        id='rows_seg', multi=True),
                                        style={'width':'50%'})

        table_buttons_div = html.Div([cols_segmentation_dropdown,\
                                      rows_segmentation_dropdown,\
                                      html.H5('Loading Table', id='table-div',
                                                style=css['table-div'])], \
                                      style=css['table-buttons-div'], 
                                      id='table-buttons-div')

        example_list_div = html.Iframe([dbc.Alert('Example_list', color="secondary")],\
                                        name='example-list-div', 
                                        style=css['example-list-div'])

        image_div = html.Iframe([html.H1('Image div')], 
                                name='iframe3', 
                                id='image-div', 
                                style=css['image-div'])
        

        footer = html.Div([dbc.Alert("Reporter Page222",className="m-4")], style=css['footer'])

        offcanvas = html.Div(
            [
                dbc.Button("Open Offcanvas", id="open-offcanvas", n_clicks=0),
                dbc.Offcanvas(
                    html.P(
                        "This is the content of the Offcanvas. "
                        "Close it by clicking on the close button, or "
                        "the backdrop."
                    ),
                    id="offcanvas",
                    title="Title",
                    is_open=False,
                ),
            ]
        )

        
        whole_page = html.Div([offcanvas,footer, Title_div, image_div, table_buttons_div, example_list_div], style=css['whole-reporter'])
        return  whole_page


### Data For Test #######
segmentations_for_test = {\
    'size' :  ['tiny', 'small', 'medium', 'large'],
    'Enviroment'  :  ['Indoor_Enviroment', 'Outdoor_Enviroment'],
    'Location':  ['Room_Location', 'Crowded environment_Location', 'Office_Location', 'Outdoor_Location'],
    'User_Movement_Type': ['Approach_PC_User_Movement_Type', 'None_User_Movement_Type']} 


cols_for_test =  ['Location', 'Light', 'Size', 'Status', 'TP', 'FP', 'FN']

data_for_test =[\
            ['Indoor', 'Day',    'Small', 'approachin',  45, 50, 20],
            ['Indoor', 'Day',    'Small', 'approachin',  20, 88, 270],
            ['Outdoor', 'Day',   'Medium', 'leaving',    100, 66, 420],
            ['Outdoor', 'Night', 'Small', 'approachin',  4, 40, 205],
                ]

df =pd.DataFrame.from_records(data_for_test, columns=cols_for_test)

if __name__ == "__main__":
    server = Flask(__name__)

    rt = Results_table(server)
    # rt.dash_app.run_server()
    
    @server.route('/', methods=['GET', 'POST'])
    def statistics_reporter_dash():
        return rt.get_webpage()

    # server.run()
    rt.dash_app.run_server()
    
    # @rt.dash_app.callback(
    #     Output('table-div', 'children'),
    #     Input('cols_seg', 'value'),
    #     Input('rows_seg', 'value')
    # )
    # def update_results_table(cols_input ,rows_input):
    #     # print("In callback")
    #     if len(cols_input)==0 or len(rows_input)==0:
    #         return html.H1('Empty Table')

    #     table_div = rt.table.get_table(cols_input, rows_input)

    #     return table_div
