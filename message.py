import os

from asyncio import sleep
from datetime import datetime
from time import time

from bs4 import BeautifulSoup

from authorization import logged_in_session
from logger import info_logger_for_future_events



class Messages(object):
    """Creates an order for troops and send them to concrete point with timing."""

    def __init__(self, message_url=None):
        self.message_url = message_url
        self.messages_page_parser = None
        self.session = logged_in_session()

    def send_messages(self):
        messages_page = self.session.get(self.message_url).text
        self.messages_page_parser = BeautifulSoup(messages_page,'html.parser') 
        post_data={}
        post_data.update({'an':'piecia'})
        post_data.update({'be' : 'temat'})
        post_data.update({'message' : 'to z pythona'})
        self.session.post(self.message_url,data=post_data)
        print('Wyslano')
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
