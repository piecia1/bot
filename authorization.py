import requests
import sys
from bs4 import BeautifulSoup
import time
from credentials import LOGIN_PASSWORD, LOGIN_USERNAME, HEADERS, VILLAGE_URL

from logger import get_logger
logger = get_logger(__name__)

def logged_in_session():
    session = requests.Session()
    session.headers = HEADERS
    html = session.get(VILLAGE_URL).text
    resp_parser = BeautifulSoup(html, 'html.parser')
    """
    #Dodane w przypadku prac na serwerze
    if(resp_parser.find('h1').contents[0] == 'Prace konserwacyjne'):
        logger.info('Prace konserwacyjne')
        time.sleep(1000)
        logged_in_session()
        #sys.exit()
    """
    try:
        login_value = resp_parser.find('input', {'name': 'login'})['value']
    except TypeError:
        logger.info('Prace konserwacyjne')
        time.sleep(10000)
        logged_in_session()
    else:
        data = {
            'name': LOGIN_USERNAME,
            'password': LOGIN_PASSWORD,
            's1': 'Login',
            'w': '1600:900',
            'login': login_value
        }

        session.post(VILLAGE_URL, data=data)

    return session
