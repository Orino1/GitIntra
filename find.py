import os
import subprocess

def get_root():
    home_dir = os.path.expanduser("~")
    return home_dir

def finder(search_path, dir_name):
    for root, dirs, files in os.walk(search_path):
        if dir_name in dirs:
            dir = os.path.join(root, dir_name)
            return dir
        else:
            pass
    return None
def clone_repo(root_path, shh_key):
    command_prefix = 'git clone '
    command = command_prefix + shh_key
    #changing the currect working dir/this shit is better than c holly molly
    os.chdir(root_path)
    #running a child procces here/remember shell=True used to run the command an a shell env
    subprocess.run(command, shell=True)
#excute cd command :

def execute_cd(cd_path):
    script_name = 'cd_script'
    #this fking funtion dosnt just accept the name as a path
    script_path = os.path.join(os.getcwd(), script_name)
    #changing the secend line of script
    file = open(script_name, 'r')
    lines = file.readlines()
    file.close()

    lines[1] = f"cd {cd_path}\n"
    #overwrite the whole file
    file = open(script_name, 'w')
    file.writelines(lines)
    file.close

    #to do: changing the dir ...


#to-do: case: more than one file in the description
def creat(root,repo_name, directory, final_list):
    full_path = os.path.join(root, repo_name, directory)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    for i in range(len(final_list)):
        files_path = os.path.join(full_path, final_list[i])
        files_path = files_path.replace(',', '')
        files_path = files_path.strip()
        if not os.path.exists(files_path):
            file = open(files_path, "w")
            if final_list[i].endswith(".py"):
                subprocess.call(["chmod", "+x", files_path])
                file.write("#!/usr/bin/python3\n")
            elif '.' not in files_path:
                file.write("#!/bin/bash\n")
                subprocess.call(["chmod", "+x", files_path])
            file.close()
        