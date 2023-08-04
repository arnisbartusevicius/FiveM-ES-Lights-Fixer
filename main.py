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

def replace_id_in_files(folder_path):
    file_list = os.listdir(folder_path)
    file_list = [f for f in file_list if f.endswith('meta')]
    with open(os.path.join(folder_path, file_list[0]), 'r') as file:
        content = file.read()
        old_id = re.search(r'\b\d{6,7}\b', content).group(0)
    new_id = generate_id()
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        replace_id(file_path, old_id=old_id, new_id=new_id)
    easygui.msgbox("Lights have successfully been fixed. If they are still broken, run this script again and select the broken vehicle folder.", "Success")
folder_path = easygui.diropenbox("Choose a folder that contains the meta files")
replace_id_in_files(folder_path)