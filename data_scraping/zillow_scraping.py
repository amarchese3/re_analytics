"""
This File is used to scrape data from Zillow
"""

import zillow
#
# with open("./bin/config/zillow_key.conf", 'r') as f:
#     key = f.readline().replace("\n", "")

key = "X1-ZWz17j2ro8zpqj_8e096"

print(key)

address = "3400 Pacific Ave., Marina Del Rey, CA"
postal_code = "90292"


api = zillow.ValuationApi()
# data = api.GetSearchResults(key, address, postal_code)

zpid="2100641621"
detail_data = api.GetZEstimate(key, zpid)


print(detail_data.get_dict())


zpid="2100641621"
detail_data = api.GetComps(key, zpid)

print("detail_data", detail_data['comps'])

for i in detail_data['comps']:
    print("Value",i.get_dict())