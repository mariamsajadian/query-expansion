import rdflib

# create a Graph
g = rdflib.Graph()

# parse in an RDF file
RDF = g.parse("ahn3test-ttl.ttl", format="ttl")

# Run a Query
qres = RDF.query(""" SELECT ?k WHERE {
                               ?s <https://schema.org/keywords> ?k }""")
keywords = []
for row in qres:
    strrow = (str(row)).replace("(rdflib.term.Literal('","")
    strrow = strrow.replace("'),)","")
    keywords.append(strrow)
# print(keywords)
keywords = list(dict.fromkeys(keywords))
print(keywords)
    # strrow = strrow.replace("')","")
    # strrow = strrow.replace("rdflib.term.Literal('","")
    # strrow = strrow.replace(")","")
    # print(strrow) #<class 'rdflib.query.ResultRow'>
# print("well done!")
