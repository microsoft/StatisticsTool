from datetime import datetime
import sys, os

sys.path.append(os.path.join(os.path.join(os.path.realpath(__file__), '..'), '..'))
from user_defined_functions import ReadingFunctions, EvalutationFunctions, OverlapFunctions, PartitioningFunctions, \
    PartitioningFunctions, StatisticsFunctions, TransformFunctions
from classes_and_utils.ParallelExperiment import *
from classes_and_utils.VideoEvaluation import run_multiple_Videos, VideoEvaluation
from inspect import getmembers, isfunction
from classes_and_utils.utils import loading_json, save_json
import re, pickle
import numpy as np
import json


def save_object(obj, filename):
    """
    Saves an object using pickle in a certain path
    :param obj: any python object (in this project we use it to save an instance of  class ParallelExperiment)
    :param filename: full path to the saved object
    """
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    """
    Loads a pickle file from a path
    :param filename: the path from which the function loads the pickle file
    :return: the loaded file
    """
    with open(filename, 'rb') as input:
        return pickle.load(input)


def serial_num(file_name):
    """
    This function acts as a key value in python's built in function sort(),
    its goal is to make the sort() function sort according to the serial number of the files which use the form:
    **name**_serialnumber.file_type
    :param file_name: the file's name
    :return: serial_number as an int
    """

    # remove file extension from file name (name.png >>> name)
    file_name = os.path.splitext(file_name)[0]
    # find all indices of dot occurrences in the file name
    dot_occurrences = [i.start() for i in re.finditer("\.", file_name)]
    assert len(
        dot_occurrences) == 0, "file name: " + file_name + " file names are not allowed to have dots in them please change that"
    # find all indices of under line occurrences in the file name
    line_occurrences = [i.start() for i in re.finditer("_", file_name)]
    #assert len(line_occurrences) > 0, "file name: " + file_name + " does not include a serial of the form _xxxx"
    # the serial number should be after the last underline
    if len(line_occurrences) == 0:
        return int(file_name)
    last_line_occ = line_occurrences[-1]
    return int(file_name[last_line_occ + 1:])


def folder_func(output_dir):
    """
    Checks that the output directory folder is empty and then opens the appropriate sub folders
    :param output_dir: path to output directory
    :return: Boolean, indicates whether the folder was empty or not
    """
    try:
        # check that output dir is empty
        if len(os.listdir(output_dir)) > 0:
            empty = False
        # assert len(os.listdir(output_dir)) == 0, 'output directory should be empty'
        else:
            empty = True
            # opening the needed sub-folders
            single_video_hash_saving_dir = os.path.join(output_dir, "intermediate results")
            os.makedirs(single_video_hash_saving_dir)
            save_stats_dir = os.path.join(output_dir, "saved by user")
            os.makedirs(save_stats_dir)
            # opening the needed sub-sub-folders
            save_images_dir = os.path.join(save_stats_dir, "saved images")
            save_lists_dir = os.path.join(save_stats_dir, "saved lists")
            save_tables_dir = os.path.join(save_stats_dir, "saved tables")
            os.makedirs(save_images_dir)
            os.makedirs(save_lists_dir)
            os.makedirs(save_tables_dir)
        return empty
    except FileNotFoundError:
        return "FileNotFound"


def options_for_funcs():
    """
    Create lists of all the optional functions in the modules that the user needs to choose from
    :return: lists of all the optional functions
    """
    file_reading_funcs = [mem[0] for mem in getmembers(ReadingFunctions, isfunction) if
                          mem[1].__module__ == ReadingFunctions.__name__]
    Evaluation_funcs = [mem[0] for mem in getmembers(EvalutationFunctions, isfunction) if
                        mem[1].__module__ == EvalutationFunctions.__name__]
    overlap_funcs = [mem[0] for mem in getmembers(OverlapFunctions, isfunction) if
                     mem[1].__module__ == OverlapFunctions.__name__]
    partition_funcs = [mem[0] for mem in getmembers(PartitioningFunctions, isfunction) if
                       mem[1].__module__ == PartitioningFunctions.__name__]
    statistics_funcs = [mem[0] for mem in getmembers(StatisticsFunctions, isfunction) if
                        mem[1].__module__ == StatisticsFunctions.__name__]
    transformation_funcs = [mem[0] for mem in getmembers(TransformFunctions, isfunction) if
                        mem[1].__module__ == TransformFunctions.__name__]
    transformation_funcs.append('None')
    return file_reading_funcs, Evaluation_funcs, overlap_funcs, partition_funcs, statistics_funcs, transformation_funcs


def manage_new_report_page(request, current_file_directory):
    """
    Accepts request from multiple pages and show the available configuration files
    adds a new configuration file if request came from new_task_config.html

    :param request: request that was sent to '/create_new_report' route
    :param current_file_directory: full path to flask_GUI.py
    :return: list of available configuration files
    """

    # if a new config is added in the GUI
    if "add_config" in request.url:
        # unpack the fields in the request and concentrate it in a configuration dictionary
        new_config, new_config_name = unpack_new_config(request)
        path_to_save = current_file_directory.replace(os.path.join('flask_GUI', 'flask_GUI.py'),
                                                      os.path.join('configs', new_config_name))
        # save the dictionary in the config folder as a json file
        save_json(path_to_save + '.json', new_config)
    # check what are the available config files in the config folder
    path_to_configs = current_file_directory.replace(os.path.join('flask_GUI', 'flask_GUI.py'), 'configs')
    if not os.path.exists(path_to_configs):
        os.makedirs(path_to_configs)
    possible_configs = os.listdir(path_to_configs)
    return possible_configs


def unpack_new_config(request):
    """
    extracts the configurations names from the request and place them in a dictionary
    :param request: request that was sent to '/create_new_report' route
    :return: a dictionary with the selected configurations names
    """
    new_config_name = request.form.get('name')
    threshold = request.form.get('Threshold')
    image_width = request.form.get('image_width')
    image_height = request.form.get('image_height')
    reading_func_name = request.form.get('Reading_func')
    transform_func_name = request.form.get('transform_func')
    overlap_func_name = request.form.get('overlap_func')
    evaluation_func_name = request.form.get("evaluation_func")
    statistics_func_name = request.form.get('statistics_func')
    partitioning_func_name = request.form.get('partitioning_func')
    new_config = [
        {"File Reading Function": reading_func_name, "Overlap Function": overlap_func_name, "Threshold": threshold,
         "Evaluation Function": evaluation_func_name, "Image Width": image_width, "Image Height": image_height,
         "Statistics Functions": statistics_func_name, "Partitioning Functions": partitioning_func_name,
         "Transformation Function":transform_func_name}]
    return new_config, new_config_name


def unpack_calc_request(request, current_file_directory):
    """
    Accepts request from new_report.html and unpack the parameters for a new report as variables

    :param request: request that was sent to '/calculating_page' route
    :param current_file_directory: full path to flask_GUI.py
    :return: parameters needed for a new report
    """
    # receiving the wanted configuration file name from the form
    config_file_name = request.form.get('Configuration')
    # receiving the wanted directories names from the form
    prd_dir = request.form.get('Predictions Directory')
    GT_dir = request.form.get('Ground Truth Directory')
    output_dir = request.form.get('Reporter Output Directory')
    
    output_dir=os.path.join(output_dir, datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
    os.makedirs(output_dir)
    
    single_video_hash_saving_dir = os.path.join(output_dir, "intermediate results")
    save_stats_dir = os.path.join(output_dir, "saved by user")
    images_dir = request.form.get('Images Directory')
    # finding the wanted configuration file location and loading it
    config_path = current_file_directory.replace(os.path.join('flask_GUI', 'flask_GUI.py'),
                                                 os.path.join('configs', config_file_name))
    config_file = loading_json(config_path)
    config_dict = config_file[0]
    return config_file_name, prd_dir, GT_dir, output_dir, single_video_hash_saving_dir, save_stats_dir, images_dir, config_dict


def unpack_calc_config_dict(config_dict):
    """
    Accepts a dictionary with configuration names and returns the correct functions and variables
    :param config_dict: a dictionary with the selected configuration for the report
    :return: the functions mentioned in the configuration dictionary
    """
    # extracting the configuration from the config file (which is a dictionary at this point)
    transform_func_name = 'None'
    if 'Transformation Function' in config_dict:
        transform_func_name = config_dict['Transformation Function']
    reading_func_name = config_dict["File Reading Function"]
    overlap_func_name = config_dict["Overlap Function"]
    evaluation_func_name = config_dict["Evaluation Function"]
    threshold = config_dict["Threshold"]
    if "Image Width" in config_dict.keys():
        image_width = config_dict["Image Width"]
        image_height = config_dict["Image Height"]
    # Case Image width and height weren't supplied in the JSON
    else:
        # Set default size 500x500
        image_width = 500
        image_height = 500
    statistics_func_name = config_dict["Statistics Functions"]
    partitioning_func_name = config_dict["Partitioning Functions"]

    # loading the wanted functions from their modules
    reading_func = getattr(ReadingFunctions, reading_func_name)
    overlap_func = getattr(OverlapFunctions, overlap_func_name)
    evaluation_func = getattr(EvalutationFunctions, evaluation_func_name)
    statistics_func = getattr(StatisticsFunctions, statistics_func_name)
    partitioning_func = getattr(PartitioningFunctions, partitioning_func_name)
    transform_func = None
    if transform_func_name != 'None':
        transform_func = getattr(TransformFunctions, transform_func_name)
    return reading_func, overlap_func, evaluation_func, statistics_func, partitioning_func, transform_func, threshold, image_width, image_height


def get_path_lists(prd_dir, GT_dir, images_dir):
    """
    Accepts a path to the predictions, labels and image and returns matching lists of predictions, labels and images
    :param prd_dir: path to prediction files
    :param GT_dir:  path to GT files
    :param images_dir:  path to images files
    :return: lists of matching ordered absolute paths of predictions, labels and images files
    """
    # setting 3 lists of matching predictions GT and images files and folders (for images) - the matching is made by
    # the serial number at the end of the each file (prd_0001 will match GT_0001 and images_0001)
    prd_list = os.listdir(prd_dir)
    GT_list = os.listdir(GT_dir)
    images_folders_list = os.listdir(images_dir)
    # sort the lists by serial number
    prd_list.sort()
    GT_list.sort()
    images_folders_list.sort()
    images_folders_list_base = [os.path.basename(k).split('.')[0] for k in images_folders_list]
    # get absolute path
    prd_list_abs = []
    for name in prd_list:
        if name in GT_list:
            prd_list_abs.append(os.path.join(prd_dir, name))
    GT_list_abs=[]
    for name in GT_list:
        if name in prd_list:
            GT_list_abs.append(os.path.join(GT_dir, name))
    images_folders_list_abs = []
    new_images_folder_list = []
    for name in prd_list:
        if name not in GT_list:
            continue
        if name in images_folders_list_base:
            images_folders_list_abs.append(os.path.join(images_dir, images_folders_list[images_folders_list_base.index(name)]))
            new_images_folder_list.append(name)
        else:
            images_folders_list_abs.append('no_video')
            new_images_folder_list.append('no_video')

    return GT_list_abs, prd_list_abs, new_images_folder_list, images_folders_list_abs


def manage_video_analysis(config_file_name, prd_dir, GT_dir, single_video_hash_saving_dir, save_stats_dir, images_dir,
                          config_dict):
    """

    :param config_file_name: the name of the selected configurations file
    :param prd_dir: the folder that contains the predictions
    :param GT_dir: the folder that contains the GT
    :param single_video_hash_saving_dir: the folder in which to save the intermediate results to (and load them in combine_video_results())
    :param save_stats_dir: the folder in which to save the final results to (e.g report, example images and tables etc. )
    :param images_dir: the folder that contains the images
    :param config_dict: a dictionary with the selected configuration for the report
    :return:
    """

    # extract the functions specified in the configuration file
    reading_func, overlap_func, evaluation_func, statistics_funcs, partitioning_func, transform_func, threshold, image_width, image_height = unpack_calc_config_dict(
        config_dict)
    # extract matching lists of absolute paths for the predictions, labels and images
    GT_list_abs, prd_list_abs, images_folders_list, images_folders_list_abs = get_path_lists(prd_dir, GT_dir,
                                                                                             images_dir)
    video_annotation_dict = {}
    for gt, pred, vid in zip(GT_list_abs, prd_list_abs, images_folders_list_abs):
        video_annotation_dict[vid]={"pred":pred+".json","gt":gt+".json"}

    try:
        # extract all the intermediate results from the raw prediction-label files
        run_multiple_Videos(GT_path_list=GT_list_abs, pred_path_list=prd_list_abs, images_folders_list=images_folders_list,
                            image_folder_fullpath_list=images_folders_list_abs, overlap_function=overlap_func,
                            readerFunction=reading_func, transform_func=transform_func, save_stats_dir=single_video_hash_saving_dir,
                            evaluation_func=evaluation_func)
    except TypeError:
        return 'TypeError'

    # combine the intermediate results for further statistics and example extraction
    exp = combine_video_results(save_stats_dir=save_stats_dir, statistic_funcs=statistics_funcs,
                                files_dir=single_video_hash_saving_dir, segmentation_funcs=partitioning_func,
                                threshold=threshold, image_width=image_width, image_height=image_height,video_annotation_dict=video_annotation_dict, evaluation_function = evaluation_func, overlap_function = overlap_func)

    save_object(exp, os.path.join(save_stats_dir, 'report_' + config_file_name.replace('.json', '') + '.pkl'))
    return exp


def unpack_stats_request(request):
    """
    Accepts requests for /stats route from multiple pages and returns the partition names that were selected and a save Boolean
    :param request: request from either Reporter_page.html or table.html
    :return: partition names that were selected and a save Boolean
    """
    unique = request.form.get('unique')
    if request.form.get('partition0'):
        # request to show statistics from Reporter_page.html
        primary = request.form.get('partition0') if request.form.get('partition0') != 'N/A' else None
        secondary = request.form.get('partition1') if (
                request.form.get('partition1') != 'N/A' and primary is not None) else None
        tertiary = request.form.get('partition2') if (
                request.form.get('partition2') != 'N/A' and secondary is not None) else None
        save = False
    else:
        # request to save the statistics from table.html
        primary = request.args.get('primary') if request.args.get('primary') != 'None' else None
        secondary = request.args.get('secondary') if (
                request.args.get('secondary') != 'None' and primary is not None) else None
        tertiary = request.args.get('tertiary') if (
                request.args.get('tertiary') != 'None' and secondary is not None) else None
        save = True
    return primary, secondary, tertiary, save, unique


def save_tables(statistics_df, state_df, save, primary, secondary, tertiary, save_stats_dir):
    """

    :param statistics_df: pandas dataframe of the partitioned statistics (e.g precision - recall) (multi index)
    :param state_df: pandas dataframe of the partitioned states (e.g TP/FP/FN) (multi index)
    :param save: Boolean, indicates whether or not to save the statistics
    :param primary: #1 partition selected
    :param secondary: #2 partition selected
    :param tertiary: #3 partition selected
    :param save_stats_dir: folder to which the data will be saved
    :return: the path to which the data was saved
    """
    save_path = None
    if save == True:
        save_path = os.path.join(os.path.join(save_stats_dir, 'saved tables'), "segmented_statistics")
        # adding the partitions to the name of the saved file
        for name in [primary, secondary, tertiary]:
            if name:
                partition_name = "_" + name
                save_path += partition_name
        save_path += '.xlsx'
        writer = pd.ExcelWriter(save_path, engine='xlsxwriter')
        statistics_df.to_excel(writer, sheet_name='statistics', startcol=3)
        state_df.to_excel(writer, sheet_name='state_count', startcol=3)
        writer.save()
    return save_path


def stats_4_html(primary, secondary, tertiary, masks):
    """
    Accepts the partitions needed and returns their arrangement in a table as rows, columns etc.

    :param primary: #1 partition selected
    :param secondary: #2 partition selected
    :param tertiary: #3 partition selected
    :param masks: the exp.masks dictionary that contains the boolean masks for the partitions
    :return: titles of the rows, sub-rows, column etc. of the statistical table to be shown to the user
    """
    wanted_seg = {}
    # extract the partition options for each partition (example: for the partition "vehicles" the options could be 'car' and 'bus')
    for partition in [primary, secondary, tertiary]:
        if partition:
            wanted_seg[partition] = masks[partition]['possible partitions']
    # the number of partitions that was asked for by the user will determine the arrangement of the table
    seg_num = len(wanted_seg)
    columns, sub_rows, rows = [], [], []
    # if there is one or more partitions the row's titles will be the 1st partition
    if seg_num > 0:
        rows += wanted_seg[primary]
    # if there are two or more partitions the column's titles will be the second partition
    if seg_num > 1:
        columns += wanted_seg[secondary]
    # if there are three partitions the sub rows will be the 3rd partition
    if seg_num == 3:
        sub_rows += wanted_seg[tertiary]
    return columns, sub_rows, rows, wanted_seg, seg_num


def manage_stats_request(request, exp):
    """
    Manages all the procedures needed when a request is received by /stats route
    :param request: request from either Reporter_page.html or table.html
    :param exp: the ParallelExperiment instance
    :return: all the parameters needed for displaying the statistics results on table.html
    """
    # unpack the values of the request from different pages
    primary, secondary, tertiary, save, unique = unpack_stats_request(request)
    # get the partitioned statistics

   
    statistics_df, state_df, statistics_dict, state_dict = exp.statistics_visualization(primary_segmentation=primary,
                                                                                        secondary_segmentation=secondary,
                                                                                        tertiary_segmentation=tertiary)
    # if asked to save the stats save_tables will do that
    save_path = save_tables(statistics_df, state_df, save, primary, secondary, tertiary, exp.save_stats_dir)
    # combined names and dictionaries of the statistics (e.g precision/recall) and states (e.g FP/FN/TP)
    wanted_statistics_names = list(set([index[-1] for index in statistics_dict])) + ['TP', 'FP', 'FN']
    statistics_dict.update(state_dict)
    
    # get the values of the rows, columns etc. for the html table if those values exists
    columns, sub_rows, rows, wanted_seg, seg_num = stats_4_html(primary, secondary, tertiary, exp.masks)
    return statistics_dict, wanted_seg, seg_num, wanted_statistics_names, columns, sub_rows, rows, primary, secondary, tertiary, save_path, unique


def unpack_list_request(request, main_exp, comp_exp):
    """
    Accepts a request to /update_list route and the masks boolean dictionary and return parameters for
    extraction or saving of an example list

    :param request: request from either table.html (link writen in macros.html) or in examples_list.html
    :param masks: exp.masks (exp is an instance of ParallelExperiment)
    :return: parameters that allow the extraction or saving of an example list
    """
    total, primary, secondary, tertiary = None, None, None, None
    save = False
   
    if "save_list" in request.args:
        save = True
    # mytup is a tuple that varies in size and include the names of the selected
    # row, sub row, column (partitions) if exists, and the name of the state chosen from the table.
    # mytup is a match to a key in the statistics/state dictionary
    if "tup" in request.args:
        mytup = request.args.get('tup')
    # request came from examples_list.html to save the example list
    else:
        mytup = request.args.get('mytup')
    
    mytup = eval(mytup)
    # the statistics chosen for example list (such as TP/FP/FN)
    state = mytup[-1]

    
    state = mytup[-1]
    exp = main_exp
    comp_index=-1
    if 'ref' in request.args and len(comp_exp)>0:
        exp=comp_exp[0]
        comp_index = 0
    
    masks = exp.masks

    show_unique = False
    if 'unique' in request.args:
        show_unique = True

    # The options for possible partitions available 'time of day' 'vehicles'
    opt = [seg for seg in masks.keys() if seg != 'total_stats']
    # a dictionary that will hold the "class" of partition and the choice, for example {'vehicle': 'bus'}
    cl_and_choice = {}
    # if the length of mytup is only 1, it only holds the name of the state/statistics (no partitions)
    if len(mytup) == 1:
        total = True
    else:
        # when the length of mytup is larger than 1 the primary segmentation is 1st object in mytup
        if len(mytup) > 1:
            primary = mytup[0]
            # checking which "class" of partition matches this " partition option"
            # like matching which class does 'bus' match to in {'time of day', 'vehicles'}
            for cl in opt:
                if primary in masks[cl]['possible partitions']:
                    cl_and_choice[cl] = primary
        if len(mytup) > 2:
            secondary = mytup[1]
            for cl in opt:
                if secondary in masks[cl]['possible partitions']:
                    cl_and_choice[cl] = secondary
        if len(mytup) > 3:
            tertiary = mytup[2]
            for cl in opt:
                if tertiary in masks[cl]['possible partitions']:
                    cl_and_choice[cl] = tertiary

    export_sheldon = False
    if 'sheldon' in request.args:
        export_sheldon = True
    return comp_index, show_unique, state, total, primary, secondary, tertiary, save, cl_and_choice, mytup, export_sheldon


def parameters_4_collapsing_list(arr_of_examples, cl_and_choice, save, save_stats_dir, state):
    """

    :param arr_of_examples: nd array, an array of nd arrays of the form: (video_name, Index, frame)
    :param cl_and_choice: dictionary of the form: {'partition class': 'partition option'}, example: {'time of day': 'night'}
    :param save: Boolean, indicates whether to save the list of examples or not
    :param save_stats_dir: folder to 'saved by user'
    :param state: the state (TP/FP/FN) of the requested example
    :return:
    """
    # removing the .json for display
    # for example in arr_of_examples:
    #     example[0] = example[0].replace(".json", "")
    save_path = None
    if len(arr_of_examples) < 1:
        return {}, None
    # saving the examples as a list of lists
    if save:
        list_of_examples = []
        for i in range(len(arr_of_examples)):
            list_of_examples.append(list(arr_of_examples[i, :]))
        # adding the partitions to name of the file
        save_path = os.path.join(os.path.join(save_stats_dir, 'saved lists'), 'example_list_' + state)
        for key in cl_and_choice:
            choice = '_' + cl_and_choice[key]
            save_path += choice
        save_path += '.json'
        save_json(save_path, list_of_examples)
    # unique video names (image folder names) and an array with values corresponds to the index of certain video
    video_names, v_idx_arr = np.unique(arr_of_examples[:, 0], return_inverse=True)
    per_video_example_hash = {}
    # getting the list in a hierarchy of the form:  1. video 2. frame 3. bouding box index
    per_video_example_hash = dict.fromkeys(video_names)
    for key in per_video_example_hash.keys():
        per_video_example_hash[key] = {}
    
    start_index = -1
    start_frame = -1
    prev_frame = -999
    prev_vid = ''
    for ind, example in enumerate(arr_of_examples):
        if example[1] - prev_frame > 1 or prev_vid != example[0]:
            prev_vid = example[0]
            start_index = example[1]
            start_frame = example[2]
            
        prev_frame = example[1]
        if start_frame not in per_video_example_hash[example[0]]:
            start_index = example[1]
            start_frame = example[2]
            per_video_example_hash[example[0]][start_frame] = {}
            (((per_video_example_hash[example[0]])[start_frame]))['frames']  = []

        
        (((per_video_example_hash[example[0]])[start_frame])['frames']).append(example)
        ((per_video_example_hash[example[0]])[start_frame])['end_frame'] = example[3]

    return per_video_example_hash, save_path


def manage_list_request(request, main_exp, comp_exp):
    """
    Accepts a the requests to /update_list route and returns all the parameter needed to show and save the list of examples asked by the user
    :param request: request from either table.html (link writen in macros.html) or in examples_list.html
    :param exp: exp is an instance of ParallelExperiment
    :return: all the parameter needed to show and save the list of examples asked by the user
    """
     # request came from table.html (the actual link is writen in macros.html)
    
    
    # get the names of requested states and partitions, a save boolean and a dictionary of {partition_class: selected_option} (example {"vehicles":"bus"})
    comp_index,show_unique, state, total, primary, secondary, tertiary, save, cl_and_choice, mytup, export_sheldon = unpack_list_request(request, main_exp, comp_exp)
    
    if comp_index > -1:
        exp = comp_exp[comp_index]
    else:
        exp = main_exp

    # extracting the example list for requested partitions and state
    list_of_examples = exp.get_ids(show_unique=show_unique, state=state, total=total, primary=primary, secondary=secondary, tertiary=tertiary)
    # caculate a per_video_example_hash for a collapsing list of examples and a save path for the user to see
    per_video_example_hash, save_path = parameters_4_collapsing_list(list_of_examples, cl_and_choice, save,
                                                                     exp.save_stats_dir, state)

    saved_sheldon = None
    if export_sheldon:
        saved_sheldon = export_list_to_sheldon(per_video_example_hash, exp.video_annotation_dict, exp.save_stats_dir, mytup)
    return comp_index, show_unique, state, cl_and_choice, mytup, save_path, per_video_example_hash, saved_sheldon


def export_list_to_sheldon(images_list, video_annotation_dict,output_dir, states):
    sheldon_list = []
    header = {}
    header['header']={}
    list(video_annotation_dict.values())[0]['pred']
    header['header']['primary_metadata'] = os.path.dirname(list(video_annotation_dict.values())[0]['pred'])
    header['header']['secondary_metadata'] = os.path.dirname(list(video_annotation_dict.values())[0]['gt'])
    header['header']['segmentation']=list(states)
    sheldon_list.append(json.dumps(header))
    for file in images_list:
        for event in images_list[file]:
            sheldon_link={}
            sheldon_link['keys']={}
            sheldon_link['keys']['type']='debug'
            sheldon_link['message']={}
            sheldon_link['message']['IsChecked']='False'
            vid = images_list[file][event]['frames'][0][0]
            sheldon_link['message']['Video Location']=vid
            sheldon_link['message']['Frame Number']= images_list[file][event]['frames'][0][2]
            sheldon_link['message']['end_frame'] = images_list[file][event]['end_frame']
            sheldon_list.append(json.dumps(sheldon_link))
    
    name = ''

    saved_file = output_dir+"/"+'-'.join(list(states)) +".json"
    with open(saved_file, 'w') as f:
        for event in sheldon_list:
            f.write(event+'\n')
        
    return saved_file





def manage_image_request(request, main_exp, comp_exp):
    """
    Accepts the requests to /show_im route and returns an encoded image and the path where the image was saved (if it was saved)

    :param request: request from either example_image (to save) or in examples_list.html
    :param exp: exp is an instance of ParallelExperiment
    :return: an encoded image and the path where the image was saved (if it was saved)
    """
    save_path = False
    # request came from examples_list.html to show an example image
    exp = main_exp
    comp_ind=eval(request.args.get('comp_index'))
    if comp_ind>-1:
        exp = comp_exp[comp_ind]

    if request.args.get('example_name'):
        example_id = request.args.get('example_name')
        example_id = eval(example_id.replace(" ", ","))
        example_id[0] += ".json"
        global last_example_id
        last_example_id = example_id
        data, fig = exp.visualize(bb_id=example_id)
    # request came from examples_image.html to show an save an example image (an keep showing it)
    else:
        data, fig = exp.visualize(bb_id=last_example_id)
        name = last_example_id[0].replace('.json', '') + str(last_example_id[1]) + '.png'
        save_path = os.path.join(os.path.join(exp.save_stats_dir, 'saved images'), name)
        fig.savefig(save_path)
    return data, save_path


#create dictionsary for main/ref report with matched bounding box in ref/main if there is any
def match_main_ref_detections(exp, ref_exp):
        main_ref = {}
        ref_main = {}
        
        for vid in exp.comp_data['video'].unique():
            #set frame_id as index, and keep the original index as another column
            ref_cur_video_df = ref_exp.comp_data[ref_exp.comp_data['video'] == vid].reset_index().reset_index().set_index('frame_id')
            main_cur_video_df = exp.comp_data[exp.comp_data['video'] == vid].reset_index().reset_index().set_index('frame_id')

            main_cur_video_list = main_cur_video_df.to_dict('records')
            ref_cur_video_list = ref_cur_video_df.to_dict('records')

            frames = np.unique(np.concatenate([ref_cur_video_df.index.unique(),main_cur_video_df.index.unique()]))
            for frame in frames:
                #level_0 is the index in the list
                main_ind =  main_cur_video_df['level_0'][main_cur_video_df.index==frame]
                ref_ind =  ref_cur_video_df['level_0'][ref_cur_video_df.index==frame]

                predictions =[main_cur_video_list[i] for i in main_ind]
                ref_predictions =[ref_cur_video_list[i] for i in ref_ind]
                
                if not len(ref_predictions) or not len(predictions):
                    mat=[]
                else:
                    mat = np.zeros((len(predictions), len(ref_predictions)))
                
                for i, pred in enumerate(predictions):
                    for j, label in enumerate(ref_predictions):
                    
                        if not pred['detection'] or not label['detection']:
                            continue
                        
                        overlap = exp.overlap_function(pred, label)
                        mat[i, j] = round(overlap, 2)
            
                exp.evaluation_function(predictions, mat)

                #'index' is the location in the original dataframe of all the videos (exp.comp_data)
                for ind, x in enumerate(predictions): 
                    if 'matching' in x:
                        main_ref[x['index']]=ref_predictions[x['matching']]['index']
                        ref_main[ref_predictions[x['matching']]['index']] = x['index']
            
        return main_ref, ref_main

def calc_unique_detections(partitions, exp, ref_exp, main_ref_dict, ref_main_dict):
   
    if main_ref_dict is None or ref_main_dict is None:
        return

    unique_out = {}
    unique_stats = {}
    unique_ref_out = {}
    unique_stats_ref = {}
    unique = unique_out
    unique_ref = unique_ref_out

    #iterate over all selected partitions
    for cur_partition in partitions:
       
        partitions_parts_list = cur_partition

        #if no partition is selected will take total stats
        if type(cur_partition) is str:
            if cur_partition not in exp.masks['total_stats']:
                continue

            partitions_parts_list = [cur_partition]
            mask = exp.masks['total_stats'][cur_partition]
            mask_ref = ref_exp.masks['total_stats'][cur_partition]
            if 'total' not in unique_out:
                unique_out['total'] = {}
            unique = unique_out['total']
            if 'total' not in unique_ref_out:
                unique_ref_out['total'] = {}
            unique_ref = unique_ref_out['total']
            unique[cur_partition] = {}
            #unique = unique[name]
            unique_ref[cur_partition] = {}
            #unique_ref = unique_ref[name]

        else: 
            if partitions_parts_list[-1] not in exp.masks['total_stats']:
                continue

            #calculated current partition masks        
            mask = pd.Series(True, range(exp.comp_data.shape[0]))
            mask_ref = pd.Series(True, range(ref_exp.comp_data.shape[0]))
            for n in partitions_parts_list[:-1]:
                for seg in exp.masks.keys():
                    if 'possible partitions' in exp.masks[seg] and n in exp.masks[seg]['possible partitions']:
                        cur_mask = exp.masks[seg]['masks'][exp.masks[seg]['possible partitions'].index(n)]
                        cur_mask_ref = ref_exp.masks[seg]['masks'][ref_exp.masks[seg]['possible partitions'].index(n)]
                        break    
                mask = mask & cur_mask
                mask_ref = mask_ref & cur_mask_ref
            
            mask = mask & exp.masks['total_stats'][partitions_parts_list[-1]]
            mask_ref = mask_ref & ref_exp.masks['total_stats'][partitions_parts_list[-1]]

        cur_u = unique
        cur_u_ref = unique_ref
        
        for seg in partitions_parts_list[:-1]:
            if seg not in cur_u:
                cur_u[seg] = {}
            if seg not in cur_u_ref:
                cur_u_ref[seg] = {}

            cur_u=cur_u[seg]
            cur_u_ref=cur_u_ref[seg]

        unique_array=[]
        unique_array_ref=[]

        for val in mask.index[mask==True]:
            if val not in main_ref_dict or mask_ref[main_ref_dict[val]] == False:
                unique_array.append(exp.ID_storage['prediction'][val])

        for val in mask_ref.index[mask_ref==True]:
            if val not in ref_main_dict or mask[ref_main_dict[val]] == False:
                unique_array_ref.append(ref_exp.ID_storage['prediction'][val])

        
        cur_u[partitions_parts_list[-1]] = np.array(unique_array)
        cur_u_ref[partitions_parts_list[-1]] = np.array(unique_array_ref)

        unique_stats[cur_partition] = len(unique_array)
        unique_stats_ref[cur_partition] = len(unique_array_ref)


    return unique_out, unique_ref_out,unique_stats, unique_stats_ref

        



