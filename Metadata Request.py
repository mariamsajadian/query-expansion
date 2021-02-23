""" old version and this is for test api and a setting for Restful api
"""

# Find metadata for each keyword and answers can be more than one answer
# This can be useful for evaluation
# Keyword should be in Dutch
from SPARQLWrapper import SPARQLWrapper, JSON
# from rdflib import Graph

sparql = SPARQLWrapper('https://api.labs.kadaster.nl/datasets/pdok/metadata/services/metadata/sparql')
# natuur, Gebouwen
Input_Keyword = "'industrie'"
# you can search by: keywords, about, dateIssued, name
SearchBy = "keywords"
sparql.setQuery("""
PREFIX sdo: <https://schema.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT * WHERE {  ?sub sdo:""" + SearchBy + Input_Keyword + """. } """)

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    a = result
    # print(a)
    # print(type(a))
    listOfDictionary = (a['sub'])
    # print (listOfDictionary)
    # print(type(listOfDictionary))
    URI = (listOfDictionary['value'])
    metadata = "https://data.labs.kadaster.nl/pdok/metadata/browser?resource=" + URI
    # print (URI)
    print(Input_Keyword)
    print(metadata)

print('-------------------------------------------')
print("well done! now open the answer in a browser")
print('Next step to make everything automatic: read excel file in python and replace keywords in obj(query) and find new URIs')

