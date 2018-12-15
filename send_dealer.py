import os,re

from asyncio import sleep
from datetime import datetime
import time


from bs4 import BeautifulSoup

from authorization import logged_in_session
from logger import info_logger_for_future_events

from credentials import SERVER_URL
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
}
class Dealer(object):
    """Creates an order for troops and send them to concrete point with timing."""

    def __init__(self, dealer_url = None, coords = None):
        self.dealer_url = dealer_url
        self.coords = dict(coords)
        self.session = logged_in_session()
        
    def send_dealer(self):
        """The main function"""
        
        dealer_page = self.session.get(self.dealer_url).text
        self.dealer_parser = BeautifulSoup(dealer_page, 'html.parser')
        check_dealer = self.dealer_parser.find(class_='spacer')
        if(check_dealer):
            time_to_wait=self.dealer_parser.find('span', {'class' : 'timer'}).get('value')
            print(' Musisz poczekać:' ,time_to_wait)
            time.sleep(int(time_to_wait) + 15)
        # 1 zapytanie ------------------------------------------------------------------------
        # Wyszukanie tokena
        ajax_token = self.dealer_parser.find_all('script')
        for ajax in ajax_token:
            if ajax.contents:
                if 'Travian.thematicallyRetakingSeized' in ajax.contents[0]:
                    ajax_token = str(ajax.contents[0])
                    break
        # tutaj należy zrobić wyrażenie regularne 
        ajax_token = ajax_token.split(" ")[-5].replace(";","").replace("\n","").replace("'","")

        # Dodanie wszystkich danych do metody post
        hidden_inputs_tags = self.dealer_parser.find_all('input', {'type': 'hidden'})
        post_data= {}
        id_t = {tag['name']: tag['value'] for tag in hidden_inputs_tags}
        post_data.update(id_t)
        post_data.update({'cmd' : 'prepareMarketplace'})
        post_data.update({'r1' : '1', 'r2' : '1', 'r3' : '1', 'r4' :'1'})
        post_data.update(self.coords)
        post_data['dname'] = ''
        post_data['x2'] = '1'
        post_data['ajaxToken'] = ajax_token     

        
        confirmation = self.session.post(SERVER_URL + 'ajax.php?cmd=prepareMarketplace' , data=post_data ).text
        # 2 zapytanie -----------------------------------------------------------
        post_data = {}
        confirmation_parser = BeautifulSoup(confirmation, 'html.parser')
        hidden_inputs_tags = confirmation_parser.find_all('input')
        hidden_tags = {tag['name'].replace("\\","").replace("\"",""): tag['value'].replace("\\","").replace("\"","") for tag in hidden_inputs_tags}
        
        post_data.update(hidden_tags)
        post_data.update({'cmd' : 'prepareMarketplace'})
        post_data.update({'r1' : '1', 'r2' : '1', 'r3' : '1', 'r4' :'1'})
        post_data['ajaxToken'] = ajax_token  

        confirmation = self.session.post(SERVER_URL + 'ajax.php?cmd=prepareMarketplace' , data=post_data ).text
        confirmation_parser = BeautifulSoup(confirmation, 'html.parser')
        # error = self.dealer_parser.find('div', {'id' : 'prepareError'})
        # 3 zapytanie ----------------------------------------------------------------
        post_data = {}
        post_data.update({'cmd' : 'reloadMarketplace'})
        post_data.update({'ajaxToken' : ajax_token})

        zoba = self.session.post(SERVER_URL + 'ajax.php?cmd=reloadMarketplace', data=post_data).text
        zoba = BeautifulSoup(zoba,'html.parser')


        
    # def send_troops(self):
    #     """The main function"""
        
    #     barrack_page = self.session.get(self.barrack_url).text
    #     barrack_parser = BeautifulSoup(barrack_page, 'html.parser')

    #     hidden_inputs_tags = barrack_parser.find_all('input', {'type': 'hidden'})

    #     post_data = {tag['name']: tag['value'] for tag in hidden_inputs_tags}
    #     post_data.update(TROOPS)
    #     post_data.update(self.what_troops_available())
    #     post_data.update(self.coords)
    #     post_data.update(self.type)
    #     post_data['dname'] = ''
    #     post_data['s1'] = 'ok'
        
        

    #     confirmation = self.session.post(self.barrack_url, data=post_data).text

    #     confirmation_parser = BeautifulSoup(confirmation, 'html.parser')
    #     self.parse_time_of_next_raid(confirmation_parser)

    #     hidden_inputs_tags = confirmation_parser.find_all('input', {'type': 'hidden'})
    #     post_data = {tag['name']: tag['value'] for tag in hidden_inputs_tags}
    #     post_data['s1'] = 'ok'

    #     print(post_data)
    #     import time
    #     time.sleep(10)

    #     self.session.post(self.barrack_url, data=post_data)

    # def parse_troops_amount(self):
    #     """Parse amount of troops and save of to property"""
    #     overview_page_link = self.barrack_url.replace('tt=2', 'tt=1')
    #     overview_page = self.session.get(overview_page_link).text
    #     overview_page_parser = BeautifulSoup(overview_page, 'html.parser')

    #     # Get tags with amount of units.
    #     unit_name_tags = overview_page_parser.find_all('img', class_='unit')
    #     unit_amount_tags = overview_page_parser.find_all('td', class_='unit')

    #     # 11 poniewaz tyle jednostek ma kazady rodzaj np. galowie
    #     len_name = len(unit_name_tags) - 11
    #     for i in range(len_name):
    #         del unit_name_tags[0]
    #         del unit_amount_tags[0]

    #     # Create dictionary with troops information
    #     troops_amount = {name['alt']: amount.text for name, amount in zip(unit_name_tags, unit_amount_tags)}
    #     # wybierz tylko ostatnich 11 - Oddziały w tej osadzie i jej oazach
    #     # Mogą być jeszcze oddziały przychodzące ale one nie są twoje
    
    #     self.troops = troops_amount

    # def parse_time_of_next_raid(self, confirmation_parser):
    #     """Compute time to next raid. Takes parser of confirmation page"""
    #     timer_element = confirmation_parser.find('div', class_='at').contents[1]

    #     arrival_time_in_seconds = int(timer_element['value'])
    #     arrival_time = datetime.fromtimestamp(arrival_time_in_seconds) - datetime.now()

    #     seconds_to_come_back = arrival_time.total_seconds() * 2
    #     come_back_time = time() + seconds_to_come_back

    #     self.time_of_next_raid = come_back_time

    # def save_next_raid_time(self):
    #     """Save coords and time for next raid in file."""
    #     with open("raids.txt", "rt") as file_input:
    #         with open("new_raids.txt", "wt") as file_output:

    #             for line in file_input:
    #                 if str(self.coords) in line:
    #                     file_output.write(str(self.coords) + ';' + str(self.time_of_next_raid) + '\n')
    #                 else:
    #                     file_output.write(line)
    #     #dodany usunięcie pliku
    #     os.remove("raids.txt")
    #     os.rename('new_raids.txt', "raids.txt")

    # def what_troops_available(self):
    #     """Determine what type of troops will be sent based on their availability. Return type and amount"""
    #     if int(self.troops['Tropiciel']) >= 20:
    #         return {'t1':'100','t3': '20'}
