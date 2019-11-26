"""
This File is used to scrape data from Zillow
"""
from bs4 import BeautifulSoup
import zillow
import requests
import pandas as pd
import json
from src.utils import get_project_root
import datetime

root = get_project_root()

class ZillowScraper:
    def __init__(self, api_key, root_folder):

        self.api_key = api_key
        self.zillow_api = zillow.ValuationApi()
        self.root_folder = root_folder

    def get_addresses_from_url(self, url):
        """
        :param url: URL With Search Results
        :return: Array of Addresses that can be used to submit a request to zillow
        """
        zillow_page = requests.get(url, headers=self.get_headers())
        soup = BeautifulSoup(zillow_page.content, 'html.parser')
        # Clean Version of the html
        soup.prettify()
        listing_price_html = soup.find_all('h3', class_='list-card-addr')
        address_array = []
        for index, val in enumerate(listing_price_html):
            address_array.append(listing_price_html[index].get_text())
        return address_array


    def compare_zestimate_to_listing_price(self, address_array):

        home_dict = {}
        postal_code = address_array[0][-5:]
        count = 0
        for index, val in enumerate(address_array):
            try:
                zillow_response = self.zillow_api.GetDeepSearchResults(key, val, postal_code)
                self.zillow_response = zillow_response
                zillow_response_dict = zillow_response.get_dict()
                self.zillow_response_dict = zillow_response_dict
                zillow_listing_url = self.get_address_link_from_ZillowGetSearchResultsAPI(zillow_response)
                listing_price = self.get_listing_price_from_zillow_url(zillow_listing_url)
                zestimate = self.get_zestimate_from_ZillowGetSearchResultsAPI(zillow_response)
                home_dict[count] = zillow_response_dict
                home_dict[count]['listing_price'] = listing_price
                home_dict[count]['zestimate_listing_price_difference'] = zestimate - listing_price
                # Count is used instead of the index because there are occasionally errors which throw an exception
                count += 1
                print(len(home_dict))
            except Exception as e:
                print(e)
                pass

        return home_dict


    def get_listing_price_from_zillow_url(self, url):
        zillow_page = requests.get(url, headers=self.get_headers())
        soup = BeautifulSoup(zillow_page.content, 'html.parser')
        listing_price_html = soup.find_all('span', class_='ds-value')
        # Getting listing price html, getting text, converting to readable python format 100,000 to 100000, making int
        listing_price = int(listing_price_html[0].get_text()[1:].replace(',', ''))
        return listing_price

    def get_address_link_from_ZillowGetSearchResultsAPI(self, zillow_response):
        response_dict = zillow_response.get_dict()
        zillow_listing_url = response_dict['links']['home_details']
        return zillow_listing_url

    def get_zestimate_from_ZillowGetSearchResultsAPI(self, zillow_response):
        response_dict = zillow_response.get_dict()
        zestimate = response_dict['zestimate']['amount']
        return zestimate


    def get_headers(self):
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

    def save_dict(self, city, building_type, dict):
        today = datetime.datetime.now().strftime("%Y%m%d")
        with open(f'{self.root_folder}\\\data\{city}\\{building_type}_{today}.json', 'w') as fp:
            json.dump(dict, fp)


key = "X1-ZWz17j2ro8zpqj_8e096"

x = ZillowScraper(api_key=key, root_folder = root)

#  Notice pagination, not all results are in this same response, add
# search_url = "https://www.zillow.com/hoboken-nj/2-_beds/?searchQueryState={%22pagination%22:{'currentPage':2},%22mapBounds%22:{%22west%22:-74.0749952737774,%22east%22:-73.98955472622265,%22south%22:40.723554921538465,%22north%22:40.76916170651425},%22regionSelection%22:[{%22regionId%22:25146,%22regionType%22:6}],%22isMapVisible%22:true,%22mapZoom%22:14,%22filterState%22:{%22sortSelection%22:{%22value%22:%22baths%22},%22beds%22:{%22min%22:2},%22price%22:{%22max%22:700000},%22monthlyPayment%22:{%22max%22:2562}},%22isListVisible%22:true}"
# search_url_hoboken_2_bad = "https://www.zillow.com/hoboken-nj/2-_beds/?searchQueryState={%22pagination%22:{},%22mapBounds%22:{%22west%22:-74.11771554755478,%22east%22:-73.94683445244527,%22south%22:40.700739801409206,%22north%22:40.79195336949885},%22mapZoom%22:13,%22regionSelection%22:[{%22regionId%22:25146,%22regionType%22:6}],%22isMapVisible%22:true,%22filterState%22:{%22sortSelection%22:{%22value%22:%22baths%22},%22beds%22:{%22min%22:2},%22price%22:{%22max%22:700000},%22monthlyPayment%22:{%22max%22:2562}},%22isListVisible%22:true}"
#
# address_array = x.get_addresses_from_url(url=search_url_hoboken_2_bad)
# listing_dict = x.compare_zestimate_to_listing_price(address_array)
# x.save_dict("hoboken", "2_bed", listing_dict)


search_url_hoboken_2_bad = "https://www.zillow.com/jersey-city-nj/2-_beds/?searchQueryState={%22pagination%22:{},%22usersSearchTerm%22:%22Jersey%20City,%20NJ%22,%22mapBounds%22:{%22west%22:-74.23961109510947,%22east%22:-73.89784890489045,%22south%22:40.62394735499965,%22north%22:40.8064597496185},%22regionSelection%22:[{%22regionId%22:25320,%22regionType%22:6}],%22isMapVisible%22:true,%22mapZoom%22:12,%22filterState%22:{%22price%22:{%22min%22:0,%22max%22:700000},%22monthlyPayment%22:{%22min%22:0,%22max%22:2562},%22beds%22:{%22min%22:2},%22sortSelection%22:{%22value%22:%22baths%22}},%22isListVisible%22:true}"
address_array_jc = x.get_addresses_from_url(url=search_url_hoboken_2_bad)
listing_dict_jc = x.compare_zestimate_to_listing_price(address_array_jc)
x.save_dict("jersey_city", "2_bed_plus", listing_dict_jc)


df =pd.DataFrame.from_dict(listing_dict_jc, orient='columns')