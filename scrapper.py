import os
import shutil
from math import ceil

import json
from urllib.request import Request
from urllib.request import urlopen, urlretrieve
from urllib.request import HTTPError, URLError
from bs4 import BeautifulSoup as bs
import sqlite3
import smtplib, ssl

from offer import Offer

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "otodomscraper0000@gmail.com"  # Enter your address
receiver_email = "rafalk1703@gmail.com"  # Enter receiver address

offersPerPage = 24  # offers on page. 24 - standard. 48, 72

db = sqlite3.connect("data.db")


# cursor.execute('''CREATE TABLE offers
#                (url text, name text, address text, price text)''')


# return parsed html file
def download_page(url):
    try:
        request = Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 ' +
                          '(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        sauce = urlopen(request).read()
        soup = bs(sauce.decode('utf-8', 'ignore'), 'lxml')
    except HTTPError:
        soup = None
    return soup


# return amount of ofers in specific category
def get_offers_amount(url):
    html = download_page(url)
    offers_amount = html.find('div', class_='e1ia8j2v7').find('span', class_='css-klxieh').text if html else '0'
    return int(''.join(offers_amount.split()))


# return list of offers on page
def get_offers(url):
    html = download_page(url)
    div_container = html.find('div', class_='css-1sxg93g e76enq86').find_all('div', {'data-cy': 'search.listing'})[1]
    offers_urls = []
    for article in div_container.find_all('li', class_='css-p74l73 es62z2j19'):
        offers_urls.append(article.find('a', class_='css-b2mfz3 es62z2j16').get('href'))
    return offers_urls

def send_email(offer):
    context = ssl.create_default_context()
    message = """\
    Subject: nowe mieszkanie\n\n
    Nowe mieszkanie: {}
    
    Adres: {}
    Cena: {}
    Nazwa: {} """.format(offer.url, offer.address, offer.price, offer.name).encode('utf-8', errors='ignore')

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, "ksoo dwkz qkla rmig")
        server.sendmail(sender_email, receiver_email, message)
    print(offer.url)
    print(offer.name)
    print(offer.price)
    print(offer.address)


def parse_offer(url):
    html = download_page(url)
    data = html.find('div', class_='css-1sxg93g e1t9fvcw3')

    title = data.find('h1', class_='css-11kn46p eu6swcv20').string
    price = data.find('strong', class_='css-8qi9av eu6swcv19').string
    location = data.find('div', class_='css-1k12nzr eu6swcv15').find('a', class_='e1nbpvi60 css-1kforri e1enecw71').getText()

    rows = cursor.execute("SELECT * FROM offers WHERE url=?", (url,)).fetchall()

    if rows.__len__() == 0:
        cursor.execute('INSERT INTO offers VALUES(?, ?, ?, ?)', (url, title, location, price))
        db.commit()
        send_email(Offer(url, title, location, price))




# generate page url
def get_page_url(url, page_number):
    return url if page_number == 1 else f'{url}&page={page_number}'


# create project data dir for scrapper results
def create_dir(path):
    if not os.path.exists(path): os.mkdir(path)


def get_path(dir_):
    return f'{dataPath}\{dir_}'


# combine all data from a specific category into one file
def to_one_file(dir_):
    path = get_path(dir_)
    for (dirpath, dirnames, filenames) in os.walk(path):
        data = []

        for filename in filenames:
            with open(f'{path}\{filename}', encoding="utf8") as json_file:
                data += json.load(json_file)

        with open(f'{dataPath}\{dir_}.json', 'w', encoding="utf8") as outfile:
            json.dump(data, outfile, indent=1)

        shutil.rmtree(path)


def get_pages_amount(url):
    return ceil(get_offers_amount(url) / offersPerPage)


if __name__ == "__main__":
    cursor = db.cursor()
    # main()
    offers_url = "https://www.otodom.pl/pl/oferty/wynajem/mieszkanie/krakow?distanceRadius=0&page=1&limit=72&market=ALL&ownerTypeSingleSelect=ALL&locations=%5Bcities_6-38%5D&priceMin=1700&priceMax=2800&viewType=listing"
    # url = "https://www.otodom.pl/pl/oferty/wynajem/mieszkanie/krakow?distanceRadius=0&page=1&limit=24&market=ALL&ownerTypeSingleSelect=ALL&locations=%5Bcities_6-38%5D&viewType=listing"
    # print(get_offers_amount(url))
    # print(get_offers(url))


    urls = get_offers(offers_url)
    for url in urls:

        # url = '/pl/oferta/wynajme-lokal-mieszkalny-z-jednym-pokojem-krakow-ID4i1Co'

        offer_url = f'https://www.otodom.pl{url}'

        parse_offer(offer_url)

    db.close()

