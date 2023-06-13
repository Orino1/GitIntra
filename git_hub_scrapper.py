
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver):

    driver.set_page_load_timeout(5)

    container = driver.find_element_by_css_selector('div[data-target="loading-context.details"]')

    #getting all repos from the account
    time.sleep(2)
    repo_list = []
    repo_ul = container.find_element(By.CLASS_NAME, 'list-style-none')
    repo_li = repo_ul.find_elements(By.TAG_NAME, 'li')
    for li in repo_li:
        a_element = li.find_element(By.TAG_NAME, 'a')
        href = a_element.get_attribute('href')
        repo_list.append(href)
    

def get_shh_by_name_of_repo(shh_list, repo_name):
    for shh in shh_list:
        if repo_name in shh:
            return shh
def get_repos(driver):
    #change the string "username" with your github user name
    driver.get('https://github.com/username?tab=repositories')
    #getting list of repos:
    ul = driver.find_element(By.XPATH, '//*[@id="user-repositories-list"]/ul')
    lis = ul.find_elements(By.TAG_NAME, 'li')
    #extracting the list of repos:
    repo_list = []
    for li in lis:
        repo_http = li.find_element(By.TAG_NAME, 'a').get_attribute('href')
        repo_list.append(repo_http)
    shh_repo = []

    for repo in repo_list:
        new_string = repo.replace("https://", "git@")
        new_string = new_string.replace("/", ":", 1)
        shh_repo.append(new_string)
    return shh_repo

def creat_new_repo(driver, repo_name):
    #login
    driver.get('https://github.com/login')
    time.sleep(2)
    #add you github info
    github_email = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'login')))
    github_email.send_keys('test@gmail.com')
    github_pass = driver.find_element(By.NAME, 'password')
    github_pass.send_keys('test')
    time.sleep(2)

    github_login_btn = driver.find_element(By.XPATH, '//*[@id="login"]/div[4]/form/div/input[13]')
    github_login_btn.click()
    time.sleep(2)

    driver.get('https://github.com/new')
    new_repo_name = driver.find_element(By.XPATH, '//*[@id="react-aria-2"]')
    new_repo_name.send_keys(repo_name)
    time.sleep(2)
    confirm_btn = driver.find_element(By.CSS_SELECTOR, '.types__StyledButton-sc-ws60qy-0.iWYfoa')
    confirm_btn.click()
    time.sleep(2)
    # Getting new repo
    #remove_later_as temi slepp will prb work
    shh_value = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="empty-setup-clone-url"]')))
    return shh_value.get_attribute('value')

def repo_parser(repo_list):
    new_list = []
    for repo in repo_list:
        repo_name = repo.split('/')[-1]
        new_list.append(repo_name)
    return new_list
