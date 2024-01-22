from typing import List
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from fake_useragent import UserAgent
from selenium.webdriver.remote.webelement import WebElement

load_dotenv('../.env')
ua = UserAgent()
user_agent = ua.random
c_options = webdriver.ChromeOptions()
c_options.add_experimental_option("detach", value=True)
# c_options.add_experimental_option("excludeSwitches", ['enable-logging'])
c_options.add_argument(f"--user-agent={user_agent}")


class Dice(webdriver.Chrome):
    def __init__(self):
        super().__init__(c_options)
        self.email = ''
        self.password = ''
        self.implicitly_wait(15)
        self.maximize_window()
        self.action = ActionChains(self)

    def land_first_page(self, login_page):
        self.get(login_page)

    def login(self, email: str, password: str):
        submit_btn = self.find_element(By.CSS_SELECTOR, ".form-group div button")
        WebDriverWait(self, timeout=20).until(lambda d: submit_btn.is_displayed())
        self.email = self.find_element(By.ID, "email")
        self.password = self.find_element(By.ID, "password")
        self.email.clear()
        self.password.clear()
        self.email.send_keys(email)
        self.password.send_keys(password)
        submit_btn.click()

    def search_skill(self, searched_skill: str):
        try:
            cross_link = self.find_element(By.CLASS_NAME, 'fe-popup-cross')
            cross_link.click()
        except:
            print("No popup found")
        finally:
            search_input = self.find_element(By.ID, "typeaheadInput")
            search_input.clear()
            self.action.move_to_element(search_input).perform()
            WebDriverWait(self, timeout=10).until(lambda d: search_input.is_displayed())
            search_input.send_keys(searched_skill)
            WebDriverWait(self, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="submitSearch-button"]'))
            ).click()
            time.sleep(2)
            posted_date_today = self.find_element(By.XPATH,
                                                  '//*[@id="facets"]/dhi-accordion[2]/div[2]/div/js-single-select-filter/div/div/button[2]')
            posted_date_today.click()
            employment_type_contract = self.find_element(By.XPATH,
                                                         '//*[@id="facets"]/dhi-accordion[3]/div[2]/div/js-multi-select-filter/div/ul/li[3]/span/button')
            employment_type_contract.click()
            # self.loop_through_job_links()

    #
    def loop_through_job_links(self, skill_set: List[str]):
        all_selected_job_links = self.find_elements(By.CSS_SELECTOR, ".search-card")
        for i in range(len(all_selected_job_links) - 1):
            link_element = self.find_elements(By.CSS_SELECTOR, ".search-card")[i].find_element(By.TAG_NAME, "a")
            self.__easy_apply(link_element, skill_set)
            continue

    def __easy_apply(self, link: WebElement, skill_list: List[str]):
        easy_apply_btn = None
        link.click()
        # SWITCHING TO NEW TAB
        handles = self.window_handles
        self.switch_to.window(handles[1])
        required_skil_block = self.find_element(By.CSS_SELECTOR,
                                                '#__next > div > main > div.container.lg\:grid.lg\:grid-cols-12.lg'
                                                '\:gap-6 > div > article > div.job-overview_jobOverview__ZHVdb > '
                                                'div.job-overview_skills__yAx_K > section > div')
        required_skill = required_skil_block.find_elements(By.TAG_NAME, 'span')
        skill_array = []
        skill_match_count = 0
        for item in required_skill:
            if item.text.find("-") != -1:
                format_string = ''.join(item.text.strip().lower().replace(" ", "").split("-"))
            else:
                format_string = ''.join(item.text.strip().lower().split(" "))
            skill_array.append(format_string)
            if skill_list.count(format_string):
                skill_match_count += 1
        time.sleep(6)
        try:
            easy_apply_btn = self.execute_script(
                'return document.querySelector("#applyButton > apply-button-wc").shadowRoot.querySelector('
                '"apply-button")').find_element(
                By.CSS_SELECTOR, "apply-button > div > button").text
        except:
            easy_apply_btn = self.execute_script(
                'return document.querySelector("#applyButton > apply-button-wc").shadowRoot.querySelector('
                '"application-submitted")').find_element(
                By.CSS_SELECTOR, "application-submitted > div > p").text
        finally:
            if easy_apply_btn != "Easy Apply" or skill_match_count <= 3:
                self.close()
                self.switch_to.window(handles[0])
            else:
                easy_apply_btn = self.find_element(By.XPATH, '//*[@id="applyButton"]/apply-button-wc')
                easy_apply_btn.click()
                WebDriverWait(self, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/span/div/main/div[4]/button[2]'))
                ).click()
                WebDriverWait(self, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/span/div/main/div[3]/button[2]'))
                ).click()
                self.close()
                self.switch_to.window(handles[0])
