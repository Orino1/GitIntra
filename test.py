#!/usr/local/bin/python3

import os
import sys
import find
import time
import git_hub_scrapper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://intranet.alxswe.com/')
#add your intra info
email = driver.find_element(By.XPATH, '//*[@id="user_email"]')
email.send_keys('test@gmail.com')
passw = driver.find_element(By.XPATH, '//*[@id="user_password"]')
passw.send_keys('test')
button = driver.find_element(By.XPATH, '//*[@id="new_user"]/div[4]/input')
button.click()
#getting a list of project
get_div = driver.find_element(By.XPATH, '/html/body/main/article/div[2]/div/div[1]/div[2]')
list_of_project = get_div.find_element(By.CLASS_NAME, 'list-group')
li_elements = list_of_project.find_elements(By.TAG_NAME, 'li')
if not li_elements:
    print("Oh, how absolutely thrilling! No projects available.")
    sys.exit()
for index, li_element in enumerate(li_elements):
    a_element = li_element.find_element(By.TAG_NAME, 'a')
    print(f"{index + 1}: {a_element.text}")
#selecting a project
index = input("Select a project: ")
if not index.isdigit():
    print("Not a number" )
    sys.exit()
index = int(index)
#open the page of the project
selected_project = li_elements[index - 1].find_element(By.TAG_NAME, 'a')
selected_project_value = selected_project.text
selected_project.click()
#the actual project page task-num-0
project_group = driver.find_element(By.CSS_SELECTOR, '.project.row')
tasks = project_group.find_elements(By.XPATH, '//div[@data-position and starts-with(@id, "task-num-")]')
if not tasks:
    print(f"{selected_project_value} >>> Halt! The coding powers demand a quiz. Answer wisely or prepare for an epic dance-off with mischievous bugs!")
    sys.exit()
#new trick learned :)
repo_name = False
#create a list of lines that contain files names + repo + dir
final_list = []
for task in tasks:
    task_footer = task.find_element(By.CLASS_NAME, 'list-group-item')
    lines_list = task_footer.text.split('\n')
    #retriving a list of name of file/files only
    last_line = lines_list[-1]
    file_names = last_line.split(" ")
    file_names = file_names[1:]
    final_list.extend(file_names)
    #retriving name of repo + dir/creating the repo if user choose to
    if not repo_name:
        repo_name = lines_list[1].split(":")[1].strip()
        directory = lines_list[2].split(":")[1].strip()
#checking if user have the repo locally
root = find.get_root()
repo_path = find.finder(root, repo_name)
full_path = ''
if repo_path is None:
    #cheking github for the repo
    shh_repo_list = git_hub_scrapper.get_repos(driver)
    repo_list = git_hub_scrapper.repo_parser(shh_repo_list)
    shh_key = ''
    #repo exist in git hub
    if repo_name in repo_list:
        
        choice = input(f"Repo exists on GitHub. Would you like to clone your repo into '{root}'? (y/n): ")
        if choice.upper() == 'Y':
            shh_key = git_hub_scrapper.get_shh_by_name_of_repo(shh_repo_list, repo_name)
            find.clone_repo(root, shh_key)
            find.creat(root,repo_name, directory, final_list)
            full_path = os.path.join(root, repo_name, directory)
            print(f"Repo {repo_name} was cloned successfully.")
            print(f"Unleash your coding powers with this mystical command:\ncd {full_path}")
        else:
            pass
    #repo dosnt exist in git hub
    else:
        choice = input(f"Repo not found on GitHub. Would you like to create '{repo_name}' repo on GitHub? (y/n): ")
        if choice.upper() == 'Y':
            shh_key = git_hub_scrapper.creat_new_repo(driver, repo_name)
            find.clone_repo(root, shh_key)
            find.creat(root,repo_name, directory, final_list)
            full_path = os.path.join(root, repo_name, directory)
            print(f"Repo {repo_name} was created and cloned successfully.")
            print(f"Unleash your coding powers with this mystical command:\ncd {full_path}")
        else:
            pass
    # Directory doesn't exist + user slected N, create full path
    if shh_key == '':
        full_path = os.path.join(root, repo_name, directory)
        find.creat(root,repo_name, directory, final_list)
        print(f"The project directory '{directory}' has been successfully created, along with any nesesery files.")
        print(f"Unleash your coding powers with this mystical command:\ncd {full_path}")
else:
    choice = input(f"The repo '{repo_name}' already exists locally. Create the project directory inside? (y/n): ")
    if choice.upper() == 'Y':
        full_path = os.path.join(root, repo_name, directory)
        find.creat(root,repo_name, directory, final_list)
        print(f"The project directory '{directory}' has been successfully created, along with any nesesery files.")
        print(f"Unleash your coding powers with this mystical command:\ncd {full_path}")