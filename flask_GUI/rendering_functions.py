#TODO: Need to move all rendering function to this file
from flask import Flask, render_template
from classes_and_utils.GUI_utils import *

def show_stats_render(request, exp, comp_exp):
    statistics_dict, wanted_seg, seg_num, wanted_statistics_names, columns, sub_rows, rows, primary, secondary, tertiary, save_path,unique = manage_stats_request(request, exp)
    cur_stats = None
    exp.unique = None
    unique_stats = None
    unique_stats_ref = None
    if len(comp_exp) > 0:
        cur_exp = comp_exp[0]
        cur_stats, _, _, _, _, _, _, _, _, _, _, calc_unique = manage_stats_request(request, cur_exp)
        #statistics_dict, wanted_statistics_names = update_statistics_with_comp_data(stats=statistics_dict, names=wanted_statistics_names, comp_stats=cur_stats)#, exp=exp, cur_exp=cur_exp)
        if calc_unique and exp.main_ref_dict == None:
            exp.main_ref_dict, exp.ref_main_dict = match_main_ref_predictions(exp, comp_exp[0])
        
        if exp.main_ref_dict != None and exp.ref_main_dict != None:
            keys = [x for x in statistics_dict.keys()]
            unique, unique_ref, unique_stats, unique_stats_ref =calc_unique_detections(keys, exp, cur_exp, exp.main_ref_dict, exp.ref_main_dict)
            exp.unique = unique
            cur_exp.unique = unique_ref

    return render_template('table.html', stats=statistics_dict, stats_ref=cur_stats, 
                    wanted_seg=wanted_seg, seg_num=seg_num, 
                    statistics_names=wanted_statistics_names, 
                    columns=columns, sub_rows=sub_rows, rows=rows, 
                    primary=primary, 
                    secondary=secondary, tertiary=tertiary,
                    unique_stats = unique_stats,
                    unique_stats_ref = unique_stats_ref, 
                    save_path=save_path)

