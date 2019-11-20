"""
This File is used to scrape data from Zillow
"""
from bs4 import BeautifulSoup
import zillow
import requests
#
# with open("./bin/config/zillow_key.conf", 'r') as f:
#     key = f.readline().replace("\n", "")

key = "X1-ZWz17j2ro8zpqj_8e096"

def get_listing_price(address, postal_code):
    """

    :param address: Full Address of Listing
    :param postal_code: Zip Code of Listing
    :return: Listing Price of Listing
    """
    api = zillow.ValuationApi()
    detail_data = api.GetSearchResults(key, address, postal_code)
    address_dict = detail_data.get_dict()
    print(address_dict)
    address_link = address_dict['links']['home_details']
    zillow_page = requests.get(address_link, headers=get_headers())
    soup = BeautifulSoup(zillow_page.content, 'html.parser')
    listing_price_html = soup.find_all('span', class_='ds-value')
    # Getting listing price html, getting text, converting to readable python format 100,000 to 100000, making int
    listing_price = int(listing_price_html[0].get_text()[1:].replace(',', ''))
    return listing_price

def get_headers():
    """
    :return: Usable header to mimic a browser
    """
    # Creating headers.
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    return headers

address = "99 Garden St # 1, Hoboken, NJ"
postal_code = "07030"
listing_price = get_listing_price(address, postal_code)
print(listing_price)
