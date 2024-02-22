import os
from pathlib import Path
import re
from experiment_engine.file_storage_handler import parallel_get_files_on_local_storage, StoreType
from app_config.dataframe_tokens import DataFrameTokens


def export_list(images_list, exp_main, exp_ref, output_dir, cell_name, states, is_unique, show_ref_report):
   
    main_data = exp_main.comp_data
    ref_data = exp_ref.comp_data if exp_ref else None
    data = main_data if not show_ref_report else ref_data
    files_to_download = {}
    files_dest = [] 
    
    output_dir = os.path.join(output_dir, 'downloaded_images')
        
    unique = '_unique' if is_unique else ''
    segment_string = re.sub('[^A-Za-z0-9]+', '_', f'{cell_name}_{states}{unique}')
    
    for video in list(images_list.keys()):
        for key, event in images_list[video].items():
            dst_folder = os.path.join(output_dir, segment_string, os.path.basename(os.path.dirname((video))))
            if len(event['frames']):
                Path(dst_folder).mkdir(parents=True, exist_ok=True)
            for frame in event['frames']:
                current_sample = data.loc[frame[1]]
                image_paths = exp_main.get_sample_images_paths(current_sample, False)
                for key,value in image_paths.items():
                    files_to_download[value]=key
                    name_suffix = ''
                    if key == StoreType.Annotations:
                        name_suffix = 'input'
                    elif key == StoreType.Data:
                        name_suffix = 'GT'
                    elif key == StoreType.Predictions:
                        name_suffix = 'prediction'
                    files_dest.append(os.path.join(dst_folder,f'frame-{current_sample[DataFrameTokens.LABELS_GROUP_KEY]}_{name_suffix}.png'))
            parallel_get_files_on_local_storage(files_to_download, files_dest)            
                
    return output_dir 