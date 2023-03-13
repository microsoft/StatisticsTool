import json



def loading_json(path):
    with open(path) as json_file:
        return json.load(json_file)

def empty_when_negative_x(row):
    return True if row['x'] == -1 else False

def save_json(saving_file_dir, object_to_save):
    with open(saving_file_dir, 'w', encoding='utf-8') as f:
        json.dump(object_to_save, f, ensure_ascii=False, indent=4)

