import requests
import csv
import urllib

from datetime import datetime
from bs4 import BeautifulSoup


PROTOCOL_AND_DOMAIN_NAME = 'https://www.bizben.com'
URL = '{}/business-for-sale/new-business-for-sale.php?lastSort=&limit=900&offset=0&orderby=topDate+DESC'.format(PROTOCOL_AND_DOMAIN_NAME)

def web_scrape():
    response = requests.get(URL)
    show_html = BeautifulSoup(response.content, 'html.parser')
    information_container = show_html.find_all('div', class_='rsltsItemNar')

    all_information = []
    for div in information_container:

        avalaible = div.find('a', class_='medstrblueU')['href']
        complete_available = PROTOCOL_AND_DOMAIN_NAME + avalaible[2:]

        info_between_tags_one = div.find('div', class_='srFrstRow').find_all('b')

        for tag in info_between_tags_one:
            if tag.text == 'Status: ':
                status = tag.next_sibling
            elif tag.text == 'Posting #: ':
                posting = int(tag.next_sibling) 
            else:
                refreshed = tag.next_sibling

        info_between_tags_two = div.find_all('div', class_='srItmRow')

        i = True
        for div in info_between_tags_two[0:2]:
            for tag in div.find_all('b'):
                if tag.text == 'Contact: ':
                    contact = tag.next_sibling
                elif tag.text == 'Phone: ':
                    if i:
                        phone = tag.next_sibling
                        i = False
                    else:
                        phone_2 = tag.next_sibling
                        i = True
                elif tag.text == 'Price: ':
                    try:
                        price = tag.next_sibling[1:]
                        print(price)
                    except ValueError:
                        price = tag.next_sibling
                elif tag.text == 'Adj Net: ':
                    adj_net = tag.next_sibling
                else:
                    down = tag.next_sibling

        information_object = {
            "Available": complete_available, 
            "Status": status, 
            "Refreshed": refreshed, 
            "Posting": posting, 
            'Contact': contact, 
            'Phone 1': phone, 
            'Phone 2': phone_2, 
            'Adj Net': adj_net, 
            'Price': price, 
            'Down': down
            }
        
        all_information.append(information_object)
        

    with open('format.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        csv_rows = []
        for row in reader:
            date = datetime.strptime(row['Refreshed'], '%m/%d/%Y')
            csv_rows.append(row)

    with open('format.csv', 'w') as csvfile:
        fieldnames = ['Available','Refreshed','Price','Down','Adj Net','Contact','Phone 1', 'Phone 2', 'Posting', 'Status']
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        writer.writerows(all_information)

    with open('format.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
        
if __name__ == '__main__':
    web_scrape()

