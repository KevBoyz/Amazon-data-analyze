import bs4
import pandas as pd
from time import sleep
import requests as r
from selenium.webdriver import Chrome
from selenium.webdriver.common import by
from selenium.webdriver.common.keys import Keys
from os import getlogin
from pyautogui import press
from math import ceil


def amazon_scrap(search, browser):
    browser.get('https://www.amazon.com')
    browser.implicitly_wait(30)
    browser.find_element(by.By.ID, 'twotabsearchtextbox').send_keys(search)
    press('enter')
    sleep(5)
    divs = browser.find_elements(by.By.CSS_SELECTOR, '[class="a-section"]')
    values = []
    for c in range(len(divs)):
        code = bs4.BeautifulSoup(divs[c].get_attribute('outerHTML'), 'html.parser')
        title = code.find('span', 'a-size-medium a-color-base a-text-normal')
        price = code.find('span', 'a-price-whole')
        try:
            values.append([title.text, int(str(price.text).replace('.', ''))])
        except:
            pass
    if values:
        df = pd.DataFrame(values, columns=['Product Names', 'Prices'])
        print(f'\nAmazon total price: {ceil(df["Prices"].sum())} ({len(values)} items)')
    else:
        print('\nError: Can\'t locate html elements on this page')
        print('Check if the page looks like this: https://www.amazon.com/s?k=pc')
        print('This script don\'t work for some Amazon pages, try search for hardware\n')


def shopee_scrap(search, browser):
    browser.get('https://shopee.com')
    browser.implicitly_wait(30)
    try:
        browser.find_element(by.By.CLASS_NAME, 'shopee-popup__close-btn').click()
    except:
        pass
    browser.find_element(by.By.CLASS_NAME, 'shopee-searchbar-input__input').send_keys(search)
    press('enter')
    sleep(4)
    for c in range(0, 6):
        for p in range(0, 17):
            press('down')
    divs = browser.find_elements(by.By.CSS_SELECTOR, '[class="col-xs-2-4 shopee-search-item-result__item"]')
    values = []
    for c in range(len(divs)):
        code = bs4.BeautifulSoup(divs[c].get_attribute('outerHTML'), 'html.parser')
        title = code.find('div', '_10Wbs- _5SSWfi UjjMrh')
        price = code.find('span', '_1d9_77')
        try:
            values.append([title.text.strip(), int(str(price.text).replace('R$', ''))])
        except:
            try:
                title = str(title).replace('<div class="_10Wbs- _5SSWfi UjjMrh">', '').replace('</div>', '')
                price = str(price).replace('<span class="_1d9_77">', '').replace('</span>', '').replace('\"', '').replace(',', '.')
                try:
                    values.append([title.strip(), float(str(price.replace(',', '.')))])
                except:
                    if price.count('.') >= 2:  # 1.000.00
                        while price.count('.') >= 2:
                            price = price[:-3]  # Remove .00
                    values.append([title.strip(), int(price.replace('.', ''))])
            except Exception as e:
                print(e)
    if values:
        df = pd.DataFrame(values, columns=['Product Names', 'Prices'])
        print(f'\nShopee total price: {ceil(df["Prices"].sum())} ({len(values)} items)')
    else:
        print('\nError: Can\'t locate html elements on this page (shopee.com)')


def start(search):
    try:
        amazon = r.get('https://www.amazon.com')
        # shopee = r.get('https://www.submarino.com')
        if amazon.status_code == 404:
            print('Error: [https://www.amazon.com] Not found 404\n')
        else:
            amazon_scrap(search, Chrome())
            shopee_scrap(search, Chrome())
    except Exception as e:
        print(e)


while True:
    search = str(input('\nSearch for: ')).strip().lower()
    if search.find('www.amazon.com') != -1 or search.find('https://www.') != -1:
        print('\nError: This input don\'t accept URL\'s')
        print('Do a search like: \"pc\" or \"cpu\"\n')
    else:
        if search == '--exit':
            break
        else:
            start(search)
input(f'\n/{getlogin()}> [Press ENTER to exit] ~ ')
