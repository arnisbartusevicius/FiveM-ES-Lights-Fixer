import os
import re
import easygui
import random

def generate_id():
    while True:
        new_id = str(random.randint(1000000, 9999999))
        if not any(abs(int(new_id[i]) - int(new_id[i+1])) == 1 for i in range(len(new_id)-1)):
            return new_id

def replace_id(file_path, old_id, new_id):
    with open(file_path, 'r') as file:
        content = file.read()
    content = content.replace(old_id, new_id)
    matches = re.findall(r'\b' + old_id + r'\b', content)
    for match in matches: 
        content = content.replace(match, new_id)
    with open(file_path, 'w') as file:
        file.write(content)

def replace_id_in_folders(folder_paths):
    for folder_path in folder_paths:
        file_list = os.listdir(folder_path)
        file_list = [f for f in file_list if f.endswith('meta')]
        with open(os.path.join(folder_path, file_list[0]), 'r') as file:
            content = file.read()
            old_id = re.search(r'\b\d{6,7}\b', content).group(0)
        new_id = generate_id()
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            replace_id(file_path, old_id=old_id, new_id=new_id)

dir_path = easygui.diropenbox(title="Select the directory containing your vehicles.")
if dir_path:
    folder_paths = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))]
    choices = [os.path.basename(f) for f in folder_paths]
    selected_folders = easygui.multchoicebox("Choose folders that contain broken vehicles", "Select Broken Vehicles", choices=choices)
    if selected_folders:
        selected_paths = [folder_paths[i] for i in range(len(folder_paths)) if choices[i] in selected_folders]
        replace_id_in_folders(selected_paths)
        
easygui.msgbox("The broken lights have been fixed. If they are still broken, use this script again on the files with broken lights.\n-Arnis", "Success")
