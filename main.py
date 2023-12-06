from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import time
import os
from dotenv import load_dotenv
from constant import SKILL_SET_LIST, SEARCH_FOR
import schedule
from pyshadow.main import Shadow

load_dotenv('.env')
API_LIGIN_PAGE = os.getenv('API_LIGIN_PAGE')
USER_NAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASSWORD')
ua = UserAgent()
user_agent = ua.random

c_options = webdriver.ChromeOptions()
c_options.add_experimental_option("detach", value=True)
c_options.add_argument(f"--user-agent={user_agent}")

# INITIALIZING DRIVER
driver = webdriver.Chrome(c_options)
driver.maximize_window()
driver.implicitly_wait(30)
action = ActionChains(driver)


def easy_apply(link):
    easy_apply_btn = None
    link.click()
    # SWITCHING TO NEW TAB
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    requiered_skil_block = driver.find_element(By.CSS_SELECTOR,
                                               '#__next > div > main > div.container.lg\:grid.lg\:grid-cols-12.lg\:gap-6 > div > article > div.job-overview_jobOverview__ZHVdb > div.job-overview_skills__yAx_K > section > div')
    required_skill = requiered_skil_block.find_elements(By.TAG_NAME, 'span')
    skill_array = []
    skill_match_count = 0
    for item in required_skill:
        if item.text.find("-") != -1:
            format_string = ''.join(item.text.lower().replace(" ", "").split("-"))
        else:
            format_string = ''.join(item.text.lower().split(" "))
        skill_array.append(format_string)
        # print(skill_array)
        if SKILL_SET_LIST.count(format_string):
            skill_match_count += 1
    time.sleep(8)
    try:
        easy_apply_btn = driver.execute_script(
            'return document.querySelector("#applyButton > apply-button-wc").shadowRoot.querySelector("apply-button")').find_element(
            By.CSS_SELECTOR, "apply-button > div > button").text
    except:
        easy_apply_btn = driver.execute_script(
            'return document.querySelector("#applyButton > apply-button-wc").shadowRoot.querySelector("application-submitted")').find_element(
            By.CSS_SELECTOR, "application-submitted > div > p").text
    finally:
        if easy_apply_btn != "Easy Apply" or skill_match_count >= 5:
            driver.close()
            driver.switch_to.window(handles[0])
        else:
            easy_apply_btn = driver.find_element(By.XPATH, '//*[@id="applyButton"]/apply-button-wc')
            easy_apply_btn.click()
            action.send_keys(Keys.PAGE_UP).perform()
            time.sleep(1)
            next_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/span/div/main/div[4]/button[2]')
            next_button.click()
            action.send_keys(Keys.PAGE_UP).perform()
            apply_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/span/div/main/div[3]/button[2]')
            apply_button.click()
            driver.close()
            driver.switch_to.window(handles[0])


def working_on_jobs_links():
    all_selected_job_links = driver.find_elements(By.CSS_SELECTOR, ".search-card")
    for i in range(len(all_selected_job_links) - 1):
        link_element = driver.find_elements(By.CSS_SELECTOR, ".search-card")[i].find_element(By.TAG_NAME, "a")
        easy_apply(link_element)
        continue


# ACCESSING LOGIN IN  DICE THROUGH SELENIUM
def accessing_web_page():
    driver.get(API_LIGIN_PAGE)
    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "password")
    submit_btn = driver.find_element(By.CSS_SELECTOR, ".form-group div button")
    wait = WebDriverWait(driver, timeout=10)
    wait.until(lambda d: submit_btn.is_displayed())
    email_input.send_keys(USER_NAME)
    password_input.send_keys(PASSWORD)
    submit_btn.click()
    time.sleep(7)
    cross_link = driver.find_element(By.CLASS_NAME, 'fe-popup-cross')
    cross_link.click()
    search_input = driver.find_element(By.ID, "typeaheadInput")
    action.move_to_element(search_input).perform()
    search_input_wait = WebDriverWait(driver, timeout=10)
    search_input_wait.until(lambda d: search_input.is_displayed())
    search_input.send_keys(SEARCH_FOR)
    # time.sleep(1)
    search_button = driver.find_element(By.XPATH, '//*[@id="submitSearch-button"]')
    search_button.click()
    time.sleep(2)
    posted_date_today = driver.find_element(By.XPATH,
                                            '//*[@id="facets"]/dhi-accordion[2]/div[2]/div/js-single-select-filter/div/div/button[2]')
    posted_date_today.click()
    employment_type_contract = driver.find_element(By.XPATH,
                                                   '//*[@id="facets"]/dhi-accordion[3]/div[2]/div/js-multi-select-filter/div/ul/li[3]/span/button')
    employment_type_contract.click()
    working_on_jobs_links()


accessing_web_page()
# selecting_criteria_wait = WebDriverWait(driver, timeout=2)
# selecting_criteria_wait.until(lambda d: employment_type_contract.is_displayed())
# schedule.every(10).seconds()
# //*[@id="applyButton"]/apply-button-wc//apply-button/div/button #applyButton > apply-button-wc
# shadow_root_script = "return arguments[0].shadowRoot"application-submitted application-submitted > div
# document.querySelector("#applyButton > apply-button-wc").shadowRoot.querySelector("application-submitted > div > p")
# easy_apply_btn = driver.find_element(By.XPATH, '//*[@id="applyButton"]/apply-button-wc')
# shadow_root_btn = driver.execute_script('return document.querySelector("#applyButton > apply-button-wc").shadowRoot.querySelector("application-submitted")')
# submitted_text_ele = driver.find_element(By.XPATH, '//*[@id="applyButton"]/apply-button-wc').shadow_root.find_elements(By.CLASS_NAME, "app-text")
# print(submitted_text_ele)
# submit_date = submitted_text_ele.find_element(By.CLASS_NAME, "app-date").text
# print(submitted_text_ele, submit_date)
# print(skill_match_count, skill_array, easy_apply_btn)
# wait = WebDriverWait(driver, 20)
# print(shadow_root_btn.find_element(By.CSS_SELECTOR, "application-submitted > div > p").text)
# print(skill_match_count)
# driver.implicitly_wait(7000)document.querySelector("#applyButton > apply-button-wc").shadowRoot.querySelector("apply-button")
# time.sleep(1)
# GOING THROUGH SEARCH JOB PAGE
# REMOVING POPUP BOX
# wait_popup = WebDriverWait(driver, timeout=8)
# wait_popup.until(lambda d: cross_link.is_displayed())
# driver.implicitly_wait(3000)
# required_skill = driver.find_elements(By.XPATH, '//*[contains(@id, "skillChip:")]')
# for item in required_skill:
#     print(item.text)
# driver.implicitly_wait(3000)
# CHECKING FOR REQUIRED SKILLS
# driver.implicitly_wait(3000)
# required_skill = driver.find_elements(By.XPATH, '//*[contains(@id, "skillChip:")]')
# for item in skills_list:
#     print(item.text)
# //*[@id="__next"]/div/main/div[3]/div/article/div[2]/div[2]/section/div
