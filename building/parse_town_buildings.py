import re

from bs4 import BeautifulSoup

from .builder2 import Builder
from credentials import SERVER_URL


class UpgradeBuilding(Builder):
    """Build the list of buildings"""
    def __init__(self, town_page_url, queue):
        super().__init__(town_page_url)
        self.queue = queue

    async def __call__(self, *args, **kwargs):
        """Build buildings until queue is not empty."""
        if self.queue:
            successfully_built = await super().__call__(*args, **kwargs)

            if successfully_built:
                del self.queue[0]

            await self.__call__()

    def parse_buildings(self):
        """Return all buildings and related links"""
        building_links={}
        for name in self.queue:
            all_div = self.parser_main_page.find_all('div',{'title' : re.compile(r'{}'.format(name))})
            for div in all_div:
                whole_link = div.get('onclick')
                link = re.findall(r'build\.php\?id=\d+', whole_link)[0]
                building_links[name] = link    
        """
        buildings_path=[]
        #all_div = self.parser_main_page.find_all('button',{'class' : 'buildingSlot a25 g0 aid25'})
        link_to_building_field = SERVER_URL + 'dorf2.php'
        building_field_page = self.session.get(link_to_building_field).text
        self.parser_location_to_build = BeautifulSoup(building_field_page, 'html.parser')
        all_div = self.parser_location_to_build.find_all('div',{'title' : re.compile(r'Główny budynek')})
        for div in all_div:
            print(div.get('onclick'))
        # all_div = self.parser_location_to_build.find_all('button',{'class' : 'green new'})
        # for button in all_div:
        #     print(button.get('onclick'))
        
        
        all_path = self.parser_main_page.find_all('path')
        for building in all_path:
            for cont in building.contents:
                if(cont.contents[0] == 'Plac budowy'):
                    if((building not in buildings_path)):
                        buildings_path.append(building)
        building_links = {}
        for building in buildings_path:      
            alt_attr = building.get('onclick')
            first_word = re.match(r'\d', alt_attr).group(0)
            print(first_word)
        import time
        time.sleep(10)
            #link = building.get('href')
            #building_links[first_word] = link
        
        building_links = {'2' : 'build.php?id=19'}
        """
        return building_links

    def set_parser_location_to_build(self):
        building_to_build = self.queue[0]
        building_sites = self.parse_buildings()
        # If given building was found then set parser, else KeyError.
        if building_to_build in building_sites:
            link_to_building_field = SERVER_URL + building_sites[building_to_build]
            building_field_page = self.session.get(link_to_building_field).text

            self.parser_location_to_build = BeautifulSoup(building_field_page, 'html.parser')

        else:
            raise KeyError(f'Incorrect input of building name {building_to_build}')
