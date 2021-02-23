import xml.etree.ElementTree as ET
import requests
# import OWSLib
url = 'https://geodata.nationaalgeoregister.nl/ahn3/wfs?request=GetCapabilities'
# url = 'https://www.nationaalgeoregister.nl/geonetwork/srv/api/records/c567c20d-5bb9-4c45-bbce-3692955b4fab/formatters/xml?approved=true'
AHN3 = requests.get(url)

# Reading the data from a string
tree = ET.fromstring(AHN3.text)
# print(tree)
for c in tree.findall('{http://www.opengis.net/ows/1.1}ServiceIdentification'):
    for keyword in c.iter('{http://www.opengis.net/ows/1.1}Keyword'):
        print(keyword.text)