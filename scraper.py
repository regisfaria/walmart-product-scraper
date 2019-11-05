from selectorlib import Extractor
import requests 
import json 
import argparse
from bs4 import BeautifulSoup
import webbrowser

argparser = argparse.ArgumentParser()
argparser.add_argument('url')

e = Extractor.from_yaml_file('selector.yml')

user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
headers = {'User-Agent': user_agent}


args = argparser.parse_args()
request = requests.get(args.url, headers=headers)
if request:
    # Pass the HTML of the page and create 
    data = e.extract(request.text)
    
    #   In Walmart's webpage we have a problem at crawling the picture from the product
    # so as a workaround, I've scraped the html that contains the link to the picture
    # and now I'll find the link inside the html scraped using bs4
    
    # scraping product imgs
    product_picture = ''

    html = data['product_main_image']
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.findAll('img')
    for image in images:
        product_picture = 'https:' + image['src']

    # formating the price to show
    current_price = ''
    for e in data['current_price']:
        current_price += e
    
    old_price = ''
    for e in data['original_price']:
        old_price += e
    if len(old_price) == 0:
        old_price = current_price
    
    # Print the data scraped
    print('------- Web page scraped -------')
    print('Name:', data['product_title'])
    print('\nCurrent price:', current_price)
    print('\nOriginal price:', old_price)
    print('\nDescription:', data['product_description'])
    print('\nThe product picture will be opened soon...')
    webbrowser.open_new(product_picture)