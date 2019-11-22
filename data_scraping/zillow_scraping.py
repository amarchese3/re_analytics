"""
This File is used to scrape data from Zillow
"""
from bs4 import BeautifulSoup
import zillow
import requests

class ZillowScraper:
    def __init__(self, api_key):

        self.api_key = api_key
        self.zillow_api = zillow.ValuationApi()

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
        postal_code = "07030"
        for index, val in enumerate(address_array):
            try:
                zillow_response = self.zillow_api.GetSearchResults(key, val, postal_code)
                zillow_listing_url = self.get_address_link_from_ZillowGetSearchResultsAPI(zillow_response)
                listing_price = self.get_listing_price_from_zillow_url(zillow_listing_url)
                zestimate = self.get_zestimate_from_ZillowGetSearchResultsAPI(zillow_response)
                home_dict[val] = listing_price - zestimate
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


key = "X1-ZWz17j2ro8zpqj_8e096"

x = ZillowScraper(api_key=key)

search_url = "https://www.zillow.com/hoboken-nj/2-_beds/?searchQueryState={%22pagination%22:{},%22mapBounds%22:{%22west%22:-74.0749952737774,%22east%22:-73.98955472622265,%22south%22:40.723554921538465,%22north%22:40.76916170651425},%22regionSelection%22:[{%22regionId%22:25146,%22regionType%22:6}],%22isMapVisible%22:true,%22mapZoom%22:14,%22filterState%22:{%22sortSelection%22:{%22value%22:%22baths%22},%22beds%22:{%22min%22:2},%22price%22:{%22max%22:700000},%22monthlyPayment%22:{%22max%22:2562}},%22isListVisible%22:true}"

address_array = x.get_addresses_from_url(url=search_url)

listing_dict = x.compare_zestimate_to_listing_price(address_array)


