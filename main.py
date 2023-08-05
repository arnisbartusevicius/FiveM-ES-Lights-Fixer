import os
import re
import easygui
import random

def generate_id(existing_ids):
    while True:
        new_id = str(random.randint(14, 255))
        if new_id not in existing_ids:
            existing_ids.add(new_id)
            return new_id

def get_id(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    match = re.search(r'<id value="(\d+)" />', content)
    if match:
        return match.group(1)
    return None

def replace_id(file_path, old_id, new_id):
    with open(file_path, 'r') as file:
        content = file.read()
    content = content.replace(f'{old_id}', f'{new_id}')
    with open(file_path, 'w') as file:
        file.write(content)

def replace_duplicate_ids(folder_path):
    car_folders = []

    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            car_folder_path = os.path.join(root, dir)
            carcols_file_path = os.path.join(car_folder_path, 'carcols.meta')
            carvars_file_path = os.path.join(car_folder_path, 'carvariations.meta')
            
            if os.path.exists(carcols_file_path) and os.path.exists(carvars_file_path):
                car_folders.append(car_folder_path)

    existing_ids = set()

    for car_folder in car_folders:
        carcols_file_path = os.path.join(car_folder, 'carcols.meta')
        carvars_file_path = os.path.join(car_folder, 'carvariations.meta')

        old_id = get_id(carcols_file_path)
        if old_id:
            if old_id in existing_ids or int(old_id) > 255:
                new_id = generate_id(existing_ids)
                replace_id(carcols_file_path, old_id, new_id)
                replace_id(carvars_file_path, old_id, new_id)
            else:
                existing_ids.add(old_id)

dir_path = easygui.diropenbox(title="Select the directory containing your vehicles.")
if dir_path:
    replace_duplicate_ids(dir_path)

easygui.msgbox("The script has successfully fixed all broken ES lights.\n-Arnis", "Success")
