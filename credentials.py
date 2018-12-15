import os

SERVER_URL = 'https://ts3.travian.pl/'
#LOGIN_USERNAME = 'piecia'
#LOGIN_PASSWORD = 'piecia1'
LOGIN_USERNAME = 'baitsporp'
LOGIN_PASSWORD = 'tsporp'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
}

VILLAGE_URL = SERVER_URL + 'dorf1.php'
TOWN_URL = SERVER_URL + 'dorf2.php'