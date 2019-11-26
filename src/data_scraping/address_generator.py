"""
This function will be used to return an array of addresses that can be used to use Zillows API
"""
from src.data_scraping import get_headers
from bs4 import BeautifulSoup
import zillow
import requests



def getAddressesBasedOnUrl(url):
    """
    :param url: URL With Search Results
    :return: Array of Addresses that can be used to submit a request to zillow
    """
    zillow_page = requests.get(url, headers=get_headers())
    soup = BeautifulSoup(zillow_page.content, 'html.parser')
    # Clean Version of the html
    soup.prettify()
    listing_price_html = soup.find_all('h3', class_='list-card-addr')
    address_array = []
    for index, val in enumerate(listing_price_html):
        address_array.append(listing_price_html[index].get_text())
    return address_array

x = getAddressesBasedOnUrl("https://www.zillow.com/hoboken-nj/2-_beds/?searchQueryState={%22pagination%22:{},%22mapBounds%22:{%22west%22:-74.0749952737774,%22east%22:-73.98955472622265,%22south%22:40.723554921538465,%22north%22:40.76916170651425},%22regionSelection%22:[{%22regionId%22:25146,%22regionType%22:6}],%22isMapVisible%22:true,%22mapZoom%22:14,%22filterState%22:{%22sortSelection%22:{%22value%22:%22baths%22},%22beds%22:{%22min%22:2},%22price%22:{%22max%22:700000},%22monthlyPayment%22:{%22max%22:2562}},%22isListVisible%22:true}")