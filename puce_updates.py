import re

from bs4 import BeautifulSoup
import requests
from random import randint
from time import sleep
from telebot import TeleBot
from googletrans import Translator


# translator object
translator = Translator()
# bot object
BOT = TeleBot("BOT_API")
news_link = []


# return soup object of webpage by link
def get_soup(link):
    return BeautifulSoup(requests.get(link).text, features="lxml")


# main function to send msgs
def send_updates():
    # get links of news
    news = get_links()
    while True:
        sleep(randint(15000, 17000))
        # get links of news one more time
        act_news = get_links()
        # check if there are new links of news
        if act_news != news:
            # get text for every news
            news_text = get_news([i for i in act_news if i not in news])
            for i in news_text:
                sleep(randint(1, 3))
                # send text of news
                BOT.send_message("-1001501024008", i)
                sleep(randint(1, 3))
                # send translated text of news 
                BOT.send_message('-1001501024008', translator.translate(i, src='cs', dest='ru').text)
            
            news = act_news


def get_links():
    link = 'https://www.upce.cz/novinky'
    links = get_soup(link). \
        find_all("div", {"class": "col-xs-12 col-sm-6 col-md-4 xs-mb-4 sm-mb-0"})
    # reverse to chronological
    links.reverse()
    links = [i.find('a')['href'] for i in links]
    return links


def get_news(links):
    result = []
    for link in links:
        text = get_soup(link).find(id='block-system-main').text
        # replace multiply \n to one \n
        result.append(re.sub(r'\n+', '\n', text).strip())
    return result


send_updates()