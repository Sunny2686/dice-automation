import time
import os
from dotenv import load_dotenv
from folder.constant import SKILL_SET_LIST, SEARCH_FOR, LOGIN_PAGE, USER_NAME, PASSWORD
from folder.dice import Dice

load_dotenv('.env')
API_LOGIN_PAGE = os.getenv('LOGIN_PAGE') or LOGIN_PAGE
USER_N = os.getenv('USER_NAME') or USER_NAME
PASS_WORD = os.getenv('PASSWORD') or PASSWORD

try:
    with Dice() as d:
        d.land_first_page(API_LOGIN_PAGE)
        # ENTER USER ID AND PASSWORD
        d.login(USER_N, PASS_WORD)
        time.sleep(7)
        # ENTER SKILL TO SEARCH
        d.search_skill(SEARCH_FOR)
        # PASS SKILL SET LIST LIKE IN CONSTANT FILE
        d.loop_through_job_links(SKILL_SET_LIST)
# Handling exception in dice
except Exception as e:
    print("Their is some problem working with command line interface")
    print("what should I print.")


