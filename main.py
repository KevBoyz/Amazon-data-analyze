import bs4
import pandas as pd
from time import sleep
import requests as r
from selenium.webdriver import Chrome
from selenium.webdriver.common import by
# from selenium.webdriver import Firefox


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
    df = pd.DataFrame(values, columns=['Product Names', 'Prices'])
    print(df)


def start(link):
    site = r.get(link)
    if site.ok:
        ...
    else:
        if site.status_code == 404:
            print('Not found 404')
        else:
            bad_status(link, Chrome())


start('https://www.amazon.com/s?k=touchscreen+laptop&crid=2JTPVF06XM1R1&sprefix=touc%2Caps%2C354&ref=nb_sb_ss_ts-doa-p_4_4')
