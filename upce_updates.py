import re

from bs4 import BeautifulSoup
import requests
from random import randint
import time
from telebot import TeleBot
from googletrans import Translator

HEADERS = {"YOUR": "HEADERS"}

# translator object
TRANSLATOR = Translator()
# bot object
BOT = TeleBot("BOT_API")


# return soup object of webpage by link
def get_soup(link):
    return BeautifulSoup(requests.get(link, headers=HEADERS).text, "html.parser")


# main function to send msgs
def send_updates():
    # get links of news
    news = get_links()
    while True:
        # for scraping once per hour
        time.sleep(3600)
        # get links of news one more time
        act_news = get_links()
        # check if there are new links of news
        if act_news != news:
            # get text for every news
            news_text = get_news([i for i in act_news if i not in news])
            for i in news_text:
                time.sleep(randint(1, 3))
                # send text of news
                BOT.send_message("CHAT_ID", i)
                time.sleep(randint(1, 3))
                # send translated text of news
                BOT.send_message(
                    "CHAT_ID",
                    TRANSLATOR.translate(i, src="cs", dest="ru").text,
                )

            news = act_news


def get_links():
    link = "https://www.upce.cz/novinky"
    links = get_soup(link).find_all(
        "div", {"class": "col-xs-12 col-sm-6 col-md-4 xs-mb-4 sm-mb-0"}
    )
    # reverse to chronological
    links.reverse()
    links = [i.find("a")["href"] for i in links]
    return links


def get_news(links):
    result = []
    for link in links:
        text = get_soup(link).find(id="block-system-main").text
        # replace multiply \n to one \n
        result.append(re.sub(r"\n+", "\n", text).strip() + 3 * "\n" + link)
    return result


if __name__ == '__main__':
    send_updates()
