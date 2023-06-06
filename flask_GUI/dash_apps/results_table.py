import sys, os
current_file_directory = os.path.realpath(__file__)
# adding the statistics_tool folder to path
sys.path.append(os.path.join(os.path.join(os.path.join(current_file_directory, '..'), '..'), '..'))

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import flask_GUI.dash_apps.my_pivot_table as pt
from classes_and_utils.GUI_utils import *
from flask_GUI.dash_apps.results_table_css import css
from flask_GUI.constants import COLOR_GRADIENT_RED_BLUE, COLOR_GRADIENT_RED_WHITE_BLUE
import math
from classes_and_utils.unique_helper import UniqueHelper
import uuid

def get_color_from_gradient(x, gradient):
    if x<0 or x>1:
        print ("values must be between 0-1")
        return 'white'
    
    gradient_len = len(gradient)
    idx = math.ceil(x*(gradient_len-1))
    return gradient[idx]
    
def get_color_by_two_values_diff(ref, main, gradient):

    if type(main)==str or type(ref)==str:
        return 'white'
    
    if ref == 0:
        if main == 0:
            precentage_change = 0
        else:
            precentage_change = 1
    else:
        precentage_change = min(1, (main/ref) - 1) #not allowing more that 100% improvement
    color_presentage = (1 + precentage_change) * 0.5
    return get_color_from_gradient(color_presentage, gradient)

def get_text_color_by_stat(main, gradient):
    ret_val = get_color_from_gradient(main, gradient)
    if ret_val == 'white':
        ret_val = 'black'
    return ret_val


class Results_table():
    
    def __init__(self, server):

        self.dash_app = Dash(
            __name__,
            server=server,
            url_base_pathname='/dash/' + str(uuid.uuid4()) + "/",
            external_stylesheets=[dbc.themes.COSMO],suppress_callback_exceptions=True)

        self.table = None
        self.dash_app.layout = self.get_whole_page_layout()
        self.unique_helper = None
        self.main_exp = None
        self.ref_exp = None
       
    
    def set_unique(self,calc_unique):
        self.calc_unique = calc_unique
        if calc_unique and self.unique_helper == None:
            self.unique_helper = UniqueHelper(self.main_exp,self.ref_exp)

    def set_data(self, main_exp, ref_exp, segmentations,calc_unique = False):
        self.main_exp = main_exp
        self.ref_exp = ref_exp

        if main_exp is not None and calc_unique and self.unique_helper is None:
            self.unique_helper = UniqueHelper(main_exp,ref_exp)
       
        self.calc_unique = calc_unique
        self.table = pt.PivotTable(segmentations, main_exp,ref_exp, cell_function=self.get_cell_exp)
        self.segmentation_categories = list(segmentations.keys())

    def get_webpage(self,columns,rows):
        self.dash_app.layout = self.get_table_div_layout(columns,rows)
        return self.dash_app.index()
    
    def make_title(self,column_keys, row_keys):
        columns = ''
        for c in column_keys:
            for key in dict(c):
                if dict(c)[key] == 'None':
                    continue
                if len(columns) > 0:
                    columns += ","
                columns += dict(c)[key]

        rows = ''
        for c in row_keys:
            for key in dict(c):
                if dict(c)[key] == 'None':
                    continue
                if len(rows) > 0:
                    rows += ","
                rows += dict(c)[key]
        if rows == '':
            return columns
        if columns == '':
            return rows
        return rows + "/" + columns
    
    
    def generate_unique_html_dash_element(self,column_keys,row_keys, stat_functions,exp_name, cell_name):
        '''
            stat_func: TP,TN,FN
        '''        
        unique_array,unique_array_ref,_ = self.unique_helper.calc_unique_detections(column_keys,row_keys,stat_functions)
        link_unique = get_link_for_update_list(cell_name=cell_name, 
                                                stat=stat_functions, 
                                                is_ref = exp_name==REF_EXP,
                                                is_unique = True)
        num = 0
        if exp_name == MAIN_EXP:
            num = len(unique_array)
        else:
            num = len(unique_array_ref)

        txt_unique = "(unique: " + str(num) + ")"
        
        return txt_unique,link_unique

    def get_cell_exp(self, main_exp,ref_exp, column_keys, row_keys,row_index):  
        '''
        The function that return a single cell
        '''     
        segmentations = [curr_segment for curr_segment in column_keys+row_keys if 'None' not in curr_segment.keys()]
        
        exp_data = {}
        exp_data[MAIN_EXP] = main_exp.get_cell_data(segmentations, self.unique_helper, False)
        if ref_exp is not None:
            exp_data[REF_EXP] = ref_exp.get_cell_data(segmentations, self.unique_helper, True) 

        all_metrics = []
        if ref_exp is not None:
            TDs = []
            TDs.append(html.Td(''))
            TDs.append(html.Td('MAIN', style={'color':'black','font-weight':'bold','white-space':'nowrap'}))
            if self.unique_helper != None:
                TDs.append(html.Td(''))
            TDs.append(html.Td('REF', style={'color':'black','font-weight':'bold','white-space':'nowrap'}))
            all_metrics.append(html.Tr(TDs,style=css['table-row']))
        
        idx = 0
        for k in exp_data[MAIN_EXP].keys():
            
            if k == 'cell_name':
                continue
            
            TDs = [html.Td(k,style={'white-space':'nowrap'})]
            num_of_exps = len(exp_data.keys())
            
            bg_color = '#ffffff'
            style ={'white-space': 'nowrap', 'color': 'black'}
            if num_of_exps > 1: #if there is more than one report so use backgournd color not text color
                bg_color = get_color_by_two_values_diff(exp_data[REF_EXP][k], exp_data[MAIN_EXP][k], COLOR_GRADIENT_RED_WHITE_BLUE)
                style['background-color'] = bg_color
                
            
            for exp_name in exp_data.keys():
                txt = "{}".format(exp_data[exp_name][k])
                if k in ["TP", "FP", "FN", "TN"]:
                    link = get_link_for_update_list(cell_name=exp_data[exp_name]['cell_name'], 
                                                    stat=k, 
                                                    is_ref = exp_name==REF_EXP)
                    
                    js = json.dumps({'action':'update_list','value': link})
                    msg = "javascript:window.parent.postMessage({});".format(js)
                    cur_style = {'text-decoration':'underline'}
                    #if there is background color so change the text to black and add underline
                    if bg_color != 'white' and bg_color != '#ffffff':
                        cur_style['color'] = 'black'
                    curr_metric = html.A(txt ,href=msg, target="", style=cur_style)                   
                else:
                    curr_metric = txt
                    if bg_color == 'white' or bg_color == '#ffffff':
                        style['color'] = get_text_color_by_stat(1-exp_data[MAIN_EXP][k], COLOR_GRADIENT_RED_BLUE)               
                   
                TDs.append(html.Td(curr_metric,style=style))

                if self.calc_unique == True and k in ["TP", "FP", "FN"]:
                    if self.unique_helper != None:
                        txt_unique, link_unique = self.generate_unique_html_dash_element(column_keys,row_keys,k,exp_name, exp_data[exp_name]['cell_name'])
                        js = json.dumps({'action':'update_list','value': link_unique})
                        msg = "javascript:window.parent.postMessage({});".format(js)
                        a_unique = html.A(txt_unique,href=msg, target="")

                        TDs.append(html.Td(a_unique,style={'white-space': 'nowrap'}))
                    else:
                        if self.unique_helper != None:
                            TDs.append(html.Td('',style={'white-space': 'nowrap'}))
                else:
                    if self.unique_helper != None:
                        TDs.append(html.Td('',style={'white-space': 'nowrap'}))
            
            if idx % 2 == 0:
                if row_index % 2 == 0:
                    all_metrics.append(html.Tr(TDs,style=css['table_row_blue']))
                else:
                    all_metrics.append(html.Tr(TDs,style=css['table_row_green']))
            else:
                all_metrics.append(html.Tr(TDs,style=css['table_row_white']))
            
            idx = idx + 1

        title = self.make_title(column_keys, row_keys)

        cell_content = html.Table(all_metrics,style={'width':'100%'},title=title)
        to_show = html.Td(cell_content,style={'padding':'0px'})

        return to_show    
    
    def get_whole_page_layout(self):
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
                                      html.H5('Loading Table',id='table-div',style=css['table-div'])], \
                                      style=css['table-buttons-div'], 
                                      id='table-buttons-div')

        example_list_div = html.Iframe([dbc.Alert('Example_list', color="secondary")],\
                                        name='example-list-div', 
                                        style=css['example-list-div'])

        image_div = html.Iframe([html.H1('Image div')], 
                                name='iframe-image', 
                                id='image-div', 
                                style=css['image-div'])

        whole_page = html.Div([Title_div, image_div, table_buttons_div, example_list_div], style=css['whole-reporter'])
        return  whole_page
    
    def get_table_div_layout(self,columns,rows):

        t = self.table.get_report_table(columns,rows)
        table_buttons_div = html.Div(id='table-div',children=t,style=css['table-div'])

        whole_page = html.Div([table_buttons_div], style=css['whole-reporter'])
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
