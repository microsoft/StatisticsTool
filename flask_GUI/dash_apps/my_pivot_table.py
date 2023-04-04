import sys, os
# current_file_directory = os.path.realpath(__file__)
# # adding the statistics_tool folder to path
# sys.path.append(os.path.join(current_file_directory, '..'))

from dash import Dash, html, dcc, Input, Output
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

sys.path.append('../classes_and_utils')

def default_get_cell(data, column_keys, row_keys):
    return html.Td("{}\n{}".format(column_keys, row_keys), style={'border':'solid'})

class   PivotTable():

    def __init__(self, segmentations, data, cell_function = default_get_cell):
        self.segmentations = segmentations
        self.get_cell = cell_function
        self.data = data

    def get_row(self, rows_keys, columns_order, horizontal_span_size, all_rows_cats, idx_hist):
        '''
        A function that returns single Dash-Html table row
        '''
        single_row = []

        ## The left size of the row - the titles/ headers
        for i,_ in enumerate(rows_keys):
            segment_name = list(rows_keys[i].values())[0]

            ### TODO: DEbug the next line - do we need it??
            appearnce_number = np.sum([x*y for x,y in zip(idx_hist[i+1:],horizontal_span_size[i+1:])])
            if appearnce_number == 0: 
                # In the first row of a nested category, the cell should be spanned
                single_row.append(html.Td("{}".format(segment_name),\
                    rowSpan=horizontal_span_size[i])) #style={'border':'solid'}

        ## The core of the table
        ## This for-loop goes over all columns of the row, and collect the cells
        for column_keys in columns_order:
            single_row.append(self.get_cell(self.data, column_keys, rows_keys))

        single_row = [html.Tr(single_row)]
        return single_row
        
    def get_cols_of_cat(self, segments_categories:list, i:int = 0, prev_segments_hist:list = []):
        '''
        A recursive function that goes over all current segmented categories (that was asked by the user). 
        For each category it goes over all its possible values.
        segments_categories: a list sorted by appearacne order
        i: the current index (used by the recurcy)
        prev_segments_hist: save the segments history (used by the recurcy)
        '''
        if len(segments_categories)==0:
            yield [{'None':'None'}]
            return

        curr_segment_category = segments_categories[i]
        for segment_name in self.segmentations[curr_segment_category]:
            segments_history = prev_segments_hist + [{curr_segment_category: segment_name}]
            if len(segments_categories) == i+1:
                yield segments_history
            else:
                yield from self.get_cols_of_cat(segments_categories, i+1, prev_segments_hist = segments_history) 


    def get_rows_of_cat(self, rows_segmentation_categories, columns_order,horizontal_span_size,prev_segments_history = [], row_cat_idx=0, idx_hist=[]):
        '''
        A recursive function that returns all rows of table
        '''
        if len(rows_segmentation_categories) == 0:
            segments_history = [{"None": "None"}]
            horizontal_span_size = [0]
            return self.get_row(segments_history, columns_order, horizontal_span_size, rows_segmentation_categories,idx_hist = [0])
        
        list_all_TRs = []

        ## Go over all values in curr category
        curr_segment_category  = rows_segmentation_categories[row_cat_idx]
        for idx, segment_name in enumerate(self.segmentations[curr_segment_category]):
            segments_history = prev_segments_history + [{curr_segment_category: segment_name}]
            idx_hist_ = idx_hist + [idx]
            if len(rows_segmentation_categories) == row_cat_idx+1: ## Bringing a single row
                TRs_curr_cat =  self.get_row(segments_history, columns_order, horizontal_span_size, rows_segmentation_categories,idx_hist = idx_hist_)
            
            else: ## Continue recoursy - bring all rows in this category
                TRs_curr_cat = self.get_rows_of_cat(rows_segmentation_categories, columns_order, horizontal_span_size,prev_segments_history= segments_history, row_cat_idx = row_cat_idx+1, idx_hist = idx_hist_)

            list_all_TRs.extend(TRs_curr_cat)

        return list_all_TRs


    def get_lens_bellow(self, lens_vector):
        span_size = [1]
        for x in lens_vector[::-1]:
            span_size.append(x*span_size[-1])
        return span_size[-2::-1]

    def get_lens_above(self, lens_vector):
        span_size = [1]
        for x in lens_vector:
            span_size.append(x*span_size[-1])
        return span_size[:-1:]

    def get_cols_titles(self, pivot_category_vertical, pivot_category_horizon):
        if len(pivot_category_horizon) == 0:
            pivot_category_horizon = [" "]
        horizontal_headers = [html.Th("{}||".format(hor_cat), scope='col') for hor_cat in pivot_category_horizon]

        if len(pivot_category_vertical) == 0:
            values_th = [html.Th("general", scope='col')]
            cols_titles = [html.Tr(horizontal_headers + values_th)]
            return cols_titles


        lens_vector = [len(self.segmentations[cat]) for cat in pivot_category_vertical]
        span_size = self.get_lens_bellow(lens_vector)
        repetionions = self.get_lens_above(lens_vector)
        
        cols_titles = []
        for curr_cat, cat_len, curr_repeat in zip(pivot_category_vertical, span_size, repetionions):
            
            cat_values = self.segmentations[curr_cat]
            #, style={'border':'solid'}
            values_th = [html.Th(col_name, scope='col', colSpan = cat_len )\
                        for col_name in cat_values] * curr_repeat
            
            cols_titles.append(html.Tr(horizontal_headers + values_th))

        return cols_titles

    def get_keys_permutations(self,colums,rows):
        list1 = ['large','medium','small']
        list2 = ['right','left']
        list3 = ['up','down']
        list4 = ['Recall','Precision','FPR','TOTAL_PRED']
        list5 = ['TP','FP','FN']
        
        res1 = [ (i, j, k,t) for i in list1
                 for j in list2
                 for k in list3
                 for t in list4]
        
        res2 = [ (i, j, k,t) for i in list1
                 for j in list2
                 for k in list3
                 for t in list5]
        
        return res1 + res2

    def get_table(self, all_columns, all_rows):
        '''
        The main function that builds the whole table
        '''
        #hagai
        #unique_stats, unique_stats_ref = self.get_unique(all_columns,all_rows)

        ## Table head ##
        titles_rows = self.get_cols_titles(all_columns, all_rows)
        table_head = html.Thead(titles_rows)

        ## Table Body ##
        columns_order = list(self.get_cols_of_cat(all_columns))
        print(columns_order)
        lens_vector = [len(self.segmentations[cat]) for cat in all_rows]
        horizontal_span_size = self.get_lens_bellow(lens_vector)
        table_rows = self.get_rows_of_cat(all_rows, columns_order,horizontal_span_size)

        table_body = html.Tbody(table_rows)    

        ## Create the table ##
        table = dbc.Table(
                            id="table1",# style={'border':'solid'},\
                            children = [table_head, table_body],
                            bordered=True,
                            dark=False,
                            hover=True,
                            responsive=True,
                            striped=True
                            )

        return table


##############################################################################################
## Bellow is an example of how to use this class ###
def table_page_example(segmentations):
    default_cols_segmentation = [list(segmentations.keys())[0]]
    default_rows_segmentation = [list(segmentations.keys())[1]]


    ######################
    Title_div = html.Div([dbc.Alert("Hello, Bootstrap!", className="m-5")])

    cols_segmentation_dropdown = dcc.Dropdown(list(segmentations.keys()), default_cols_segmentation,
                                       id='cols_seg', multi=True)
    rows_segmentation_dropdown = dcc.Dropdown(list(segmentations.keys()), default_rows_segmentation,
                                       id='rows_seg', multi=True)

    table_div = html.Div([html.H1('Loading Table')], id='table-div')

    return html.Div([Title_div, cols_segmentation_dropdown, rows_segmentation_dropdown, table_div], style={'border':'solid'})

app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
#HAGAI-callback
'''
@app.callback(
    Output('table-div', 'children'),
    Input('cols_seg', 'value'),
    Input('rows_seg', 'value')
)
def update_output(cols_input ,rows_input):
    table_div = table.get_table(cols_input, rows_input)
    return table_div
'''

if __name__ == '__main__':

    segmentations = {\
        'Size' :  ['Small', 'Medium', 'large','mysize'],
        'Location'  :  ['Indoor', 'Outdoor'],
        'Light':  ['Day', 'Night', 'dawn'],
        'Status': ['approachin', 'leaving']} 

    cols =  ['Location', 'Light', 'Size', 'Status', 'TP', 'FP', 'FN']

    data=[\
                ['Indoor', 'Day',    'Small', 'approachin',  45, 50, 20],
                ['Indoor', 'Day',    'Small', 'approachin',  20, 88, 270],
                ['Outdoor', 'Day',   'Medium', 'leaving',    100, 66, 420],
                ['Outdoor', 'Night', 'Small', 'approachin',  4, 40, 205],
                    ]

    df =pd.DataFrame.from_records(data, columns=cols)
    table = PivotTable(segmentations, df)
    app.layout = table_page_example(segmentations)
    app.run_server()
    app.server.debug = True

