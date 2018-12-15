from bs4 import BeautifulSoup

from credentials import SERVER_URL
from logger import get_logger
import re

logger = get_logger(__name__)


def check_adventure(session=None, parser=None):
    """If any of adventures available then go, else do nothing."""
    
    if is_enough_health(parser) and is_adventure_available(parser):
        go_to_adventure(session)
        logger.info('Going to adventure')


def go_to_adventure(session):
    hero_page = session.get(SERVER_URL + 'hero.php?t=3').text
    hero_page_parser = BeautifulSoup(hero_page, 'html.parser')
    #Tutaj można dodać aby tylko wyzwania o niskim lub normalnym ryzyku były podejmowane
    """
    all_row = hero_page_parser.find_all('tr')
    for row in all_row:
        if( (row.find('img',{'alt' : 'Normalny'})) and ( row.find('a', {'class': 'gotoAdventure'})) ):
            link_to_adventure = row.find('a', {'class': 'gotoAdventure'})['href']
            break
    """
    link_to_adventure = hero_page_parser.find('a', {'class': 'gotoAdventure'})['href']

    confirmation_page = session.get(SERVER_URL + link_to_adventure).text
    confirmation_page_parser = BeautifulSoup(confirmation_page, 'html.parser')
    confirmation_form_inputs = confirmation_page_parser.find_all('input')
    # Tutaj można dodać postawienie nowego budynku 'Miejsce zbiórki'
    # lub trzeba wybudować go manualnie (samemu)
    # w przeciwnym razie nie zostaną wykonane wyzwania

    if confirmation_form_inputs:
        data = {tag['name']: tag['value'] for tag in confirmation_form_inputs}
        session.post(SERVER_URL + 'start_adventure.php', data=data)
    else:
        logger.info('Wyzawanie jest już w trakcie realizacji lub nie ma miejsca zbiórki')

def is_adventure_available(parser):

    adventure_button = parser.find('button', {'class': 'adventureWhite'})
    adventure_count_tag = adventure_button.find('div', {'class': 'speechBubbleContent'})

    hero_is_available = is_hero_available(parser)

    if adventure_count_tag and hero_is_available:
        return True

    return False


def is_hero_available(parser):
    hero_is_not_available = parser.find('img', {'alt': 'on the way'})
    hero_is_available = not bool(hero_is_not_available)

    return hero_is_available

def is_enough_health(parser):
    health = parser.find('div',{'class' : 'heroHealthBarBox alive'}).get('title')
    health = int(re.findall(r'\d+', health)[0])
    if health > 25:
        return True
    else:
        return False

