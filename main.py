import bs4
import pandas as pd
from time import sleep
import requests as r
from selenium.webdriver import Chrome
from selenium.webdriver.common import by
from os import getlogin


def bad_status(link, browser):  # Request error case, use selenium
    values = []
    browser.get(link)
    sleep(2)
    divs = browser.find_elements(by.By.CSS_SELECTOR, '[class="a-section"]')
    for c in range(len(divs)):
        code = bs4.BeautifulSoup(divs[c].get_attribute('outerHTML'), 'html.parser')
        title = code.find('span', 'a-size-medium a-color-base a-text-normal')
        price = code.find('span', 'a-price-whole')
        try:
            values.append([title.text, str(price.text).replace('.', '')])
        except:
            pass
    if values:
        df = pd.DataFrame(values, columns=['Product Names', 'Prices'])
        print(f'\n{df}')
    else:
        print('Error: Can\'t locate html elements on this page')
        print('Try a link like this: https://www.amazon.com/s?k=pc')


def start(link):
    try:
        site = r.get(link)
        if site.status_code == 404:
            print('Not found 404')
        else:
            bad_status(link, Chrome())
    except Exception as e:
        print(e)


while True:
    am_link = str(input('Amazon Search: ')).strip().lower()
    if am_link.find('www.amazon.com') == -1:
        print('\nError: Invalid Url, needs point to to amazon.com')
        print('Try a link like this: https://www.amazon.com/s?k=pc\n')
    else:
        break
start(am_link)
input(f'\n/{getlogin()}> [Press ENTER to exit] ~ ')
