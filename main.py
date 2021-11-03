import bs4
import pandas as pd
from time import sleep
import requests as r
from selenium.webdriver import Chrome
from selenium.webdriver.common import by
from os import getlogin
from pyautogui import press


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
            values.append([title.text, str(price.text).replace('.', '')])
        except:
            pass
    if values:
        df = pd.DataFrame(values, columns=['Product Names', 'Prices'])
        print(f'\n{df}\n')
    else:
        print('Error: Can\'t locate html elements on this page')
        print('Check if the page looks like this: https://www.amazon.com/s?k=pc')
        print('This script don\'t work for some Amazon pages, try search for another thing\n')


def start(search):
    try:
        amazon = r.get('https://www.amazon.com')
        if amazon.status_code == 404:
            print('Not found 404\n')
        else:
            amazon_scrap(search, Chrome())
    except Exception as e:
        print(e)


while True:
    search = str(input('Search for: ')).strip().lower()
    if search.find('www.amazon.com') != -1 or search.find('https://www.') != -1:
        print('\nError: This input don\'t accept URL\'s')
        print('Do a search like: \"pc\" or \"cpu\"\n')
    else:
        if search == '--exit':
            break
        else:
            start(search)
input(f'\n/{getlogin()}> [Press ENTER to exit] ~ ')
