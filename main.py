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
import matplotlib.pyplot as plt


def amazon_scrap(search, browser, pagesToTun=1):
    global div_class, title_class, price_class
    browser.get('https://www.amazon.com')  # Opening the site on a browser
    browser.implicitly_wait(30)  # Max time to wait the load
    browser.find_element(by.By.ID, 'twotabsearchtextbox').send_keys(search)  # Find and use the search bar
    press('enter')  # send the keys
    values = []  # 30-72 items
    sleep(3)
    for p in range(0, pagesToTun):  # 6 search pages = 120-300 elements
        sleep(2)
        divs = browser.find_elements(by.By.CSS_SELECTOR, '[class="sg-col-inner"]')  # Find all items
        for c in range(len(divs)):  # Get data of the item
            code = bs4.BeautifulSoup(divs[c].get_attribute('outerHTML'), 'html.parser')
            title = code.find('span', 'a-text-normal')
            price = code.find('span', 'a-price-whole')
            try:
                values.append([title.text, int(str(price.text).replace('.', ''))])
            except Exception as e:
                pass
        ul = browser.find_element(by.By.CLASS_NAME, 'a-pagination')
        ul.find_element(by.By.CLASS_NAME, 'a-last').click()  # Go to next search page
    if values:  # All done, return the DataFrame resumed
        df = pd.DataFrame(values, columns=['Product Names', 'Prices'])
        return [ceil(df["Prices"].mean()), len(values), ceil(df["Prices"].sum())]
    else:  # ^ Prices media - items processed - total value of all items ^
        print('\nError: Can\'t locate html elements on this page')
        print('Check if the page looks like this: https://www.amazon.com/s?k=outfit')
        print('This script don\'t work for some Amazon pages, try search for hardware or common things, like chairs\n')


def shopee_scrap(search, browser):
    browser.get('https://shopee.com')
    browser.implicitly_wait(30)
    try:
        browser.find_element(by.By.CLASS_NAME, 'shopee-popup__close-btn').click()  # Close the popup, if you find it
    except:
        pass
    browser.find_element(by.By.CLASS_NAME, 'shopee-searchbar-input__input').send_keys(search)  # Get and use to search
    press('enter')  # Send the keys
    sleep(4)  # Load time, this will be wbd wait in future like others sleep()
    for c in range(0, 6):  # Run the page to render and load all items (55-60)
        for p in range(0, 17):  # Press the down_arrow 17 times, do this 6 times
            press('down')  # If the user interact with the browser this will probably break
    divs = browser.find_elements(by.By.CSS_SELECTOR, '[class="col-xs-2-4 shopee-search-item-result__item"]')  # Get them
    values = []
    for c in range(len(divs)):  # Extract the information about the product
        code = bs4.BeautifulSoup(divs[c].get_attribute('outerHTML'), 'html.parser')
        title = code.find('div', '_10Wbs- _5SSWfi UjjMrh')
        price = code.find('span', '_1d9_77')
        try:
            values.append([title.text.strip(), int(str(price.text).replace('R$', ''))])  # Sometimes, return Attribute e
        except:  # Some .text values in titles are like "text". In this case, the text need to be picked manually
            try:  # Other error can occurred with price if he are bigger than 999.00 he receive 2+ points 1.000.00
                title = str(title).replace('<div class="_10Wbs- _5SSWfi UjjMrh">', '').replace('</div>', '')
                price = str(price).replace('<span class="_1d9_77">', '').replace('</span>', '').replace('\"',
                                                                                                        '').replace(',',
                                                                                                                    '.')
                try:
                    values.append([title.strip(), float(price)])  # Prices can return errors
                except:  # This code fix the None value at price variable
                    if price.count('.') >= 2:  # 1.000.00
                        while price.count('.') >= 2:
                            price = price[:-3]  # Remove .00
                    values.append([title.strip(), int(price.replace('.', '').replace('R$', ''))])
            except Exception as e:  # If unexpected error occurred
                print(e)
    if values:  # All done, return the info
        df = pd.DataFrame(values, columns=['Product Names', 'Prices'])
        return [ceil(df["Prices"].mean()), len(values), ceil(df["Prices"].sum())]
    else:
        print('\nError: Can\'t locate html elements on this page (shopee.com)')


def graph_output(search, data):
    dt_tb = pd.DataFrame(  # Load DataFrame to extract info
        data,
        columns=['Prices media', 'Items analyzed', 'Sum of all'],
        index=['Amazon', 'Shopee']
    )
    items_analyzed = dt_tb['Items analyzed'].values  # Values iterator    (random ascii that I make; inset/spaceship)
    prices_media = dt_tb['Prices media'].values  # Values iterator                     ##          \/-kh}---|k
    file = open('database.txt', 'a')  # Saving the data -- on a text file           --####  -       \/-eo}--|h
    file.write(f'{search}\n{prices_media[0]} {prices_media[1]}\n')  # #               #  ##          \/-vy}-|b
    file.close()  # Close                                                           --####  -         \/-bz}|y
    plt.pie(  # Relation of items processed for each site scraped                      ##              \/\/\|z
        [items_analyzed[0], items_analyzed[1]],  # Values
        labels=['Amazon', 'Shopee'],  # Labels
        autopct="%1.2f%%",  # Show the percentage
        colors=['orange', 'red'],  # Define the colors
    )  # Generating gui graphics - Amazon, Shopee, x?  (consider this on line +- 97)
    plt.title(f'Items processed for site - Search tab: \"{search}\"')
    plt.xlabel(f'Total of items captured: {dt_tb["Items analyzed"].values[0] + dt_tb["Items analyzed"].values[1]}')
    plt.ylabel(f' Amazon: {items_analyzed[0]}{" " * 30}\nShopee: {items_analyzed[1]}{" " * 30}').set_rotation(0)
    plt.show()
    plt.bar(  # Prices media graph (bars)
        ['Amazon', 'Shopee'],  # Legends, values
        [prices_media[0], prices_media[1]],
        color=['orange', 'red'])
    plt.title(f'Prices media - {search}')
    plt.xlabel('Scraped sites')
    plt.show()
    searches = []
    amazon_l = []
    shp_l = []
    file = open('database.txt', 'r')
    c = 0
    for line in file.readlines():
        c += 1
        if c % 2 != 0:  # Search
            searches.append(str(line)[:-1])  # Remove \n
        else:  # Prices
            line_iter = line.split()
            for i in range(len(line_iter)):
                line_iter[i] = int(line_iter[i])
                if i % 2 != 0:  # [1]
                    shp_l.append(line_iter[i])
                else:  # [0]
                    amazon_l.append(line_iter[i])
    file.close()
    plt.figure(facecolor='#cccccc')
    ax = plt.axes()
    ax.set_facecolor("#dddddd")
    plt.plot(searches, amazon_l, color='orange', marker='o')
    plt.plot(searches, shp_l, color='red', marker='o')
    plt.title(f'Prices media plot - Last search')
    plt.legend(['Amazon', 'Shopee'])
    plt.grid()
    plt.show()


def start(search):
    try:
        amazon = r.get('https://www.amazon.com')  # Probably return 503
        # shopee = r.get('https://www.submarino.com')  # Too much time to respond
        if amazon.status_code == 404:
            print('Error: [https://www.amazon.com] Not found 404\n')
        else:  # Automation initialization
            data = [
                amazon_scrap(search, Chrome(), 2),
                shopee_scrap(search, Chrome())
            ]
            graph_output(search, data)  # Show the results
    except Exception as e:
        print(e)


while True:  # Program interface
    search = str(input('\nSearch for: ')).strip()
    if search.find('www.amazon.com') != -1 or search.find('https://www.') != -1:  # Invalid values processing
        print('\nError: This input don\'t accept URL\'s')
        print('Do a search like: \"pc\" or \"cpu\"\n')
    else:
        if search == '--exit':
            break
        else:
            start(search)
input(f'\n/{getlogin()}> [Press ENTER to exit] ~ ')
