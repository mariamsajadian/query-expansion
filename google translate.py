"""Query over local metadata"""
""" Last up_data 11-1-2021, This program translate a set of keywords from English into Dutch. Then, it queries over metadata in ttl format
matches user keywords with the content in RDF file. Next, extract relevant links and identifier. The relevant links is for
checking relevant and irrelevant datasets. Besides, the output of identifiers are used for evaluation of google translate API
"""
from google_trans_new import google_translator
import rdflib
from fuzzywuzzy import fuzz
import re
import csv
import nltk
import time # computing the exact time it takes to finish running
from humanfriendly import format_timespan # computing the exact time it takes to finish running


path_output = "C:\\0000Pythoncodes\\API\\final\\output\\Trans\\"
Path_input = "C:\\0000Pythoncodes\\API\\final\\input\\"

######## translate questions into Dutch using google trans api
with open(Path_input + "KeywordsEnglish.txt") as English:
    name = English.read()

translator = google_translator()
translate_text = translator.translate(name,lang_tgt='nl')[0:-1]
print(" the output api:", translate_text)
key = translate_text.split('/n')
# key = nltk.word_tokenize(translate_text)
print(key)
g = rdflib.Graph()
##### parse in an RDF file = ahn3test-ttl.ttl
RDF = g.parse(Path_input + "metadata_pdok_all_removed.ttl", format="ttl")
##### Run a Query
lineList = []
for k in key:
    print(key)
    k = k.replace("-","")
    # print(k)
    qres = RDF.query(""" SELECT ?s ?k WHERE {
                                   ?s <https://schema.org/name>|<https://schema.org/about>|<https://schema.org/keywords>|<https://schema.org/description> ?k }""")

    #### start extracting  URIs and metadata content for keyword matched with correspond URI
    #### remove unwanted characters and strings
    for row in qres:
        strrow = (str(row)).replace("rdflib.term.URIRef", "")
        strrow = strrow.replace("(('", "")
        strrow = strrow.replace("')", "")
        strrow = strrow.replace("rdflib.term.Literal('", "")
        metadata = strrow.replace(")", "")
        # print(metadata)
        #### keyword matching and scoring the result of matched keywords
        Ratio = fuzz.partial_ratio(k.lower(), metadata.lower())
        # Ratio = fuzz.partial_token_sort_ratio(k, metadata)
        ##### extract URIs with 80% similarity by string pattern matching to allow special characters to be used without invoking their special meaning.
        if Ratio == 100:  ##80 for prural
            link_regex = re.compile("((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)")
            links = re.findall(link_regex, metadata)
            ##### filter out unwanted characters from URLs using index
            for word in links:
                word = str(word).split(",")[0]
                URIs = word.replace("('", "")
                ##### filter out unwanted URLs in description from URLs linked to metadata
                if len(URIs) > 50:
                    if (".pdf" in URIs):
                        pdf = URIs
                    elif ("kadaster.nl" in URIs):
                        kadaster = URIs
                    elif ("cbs.nl" in URIs):
                        cbs = URIs
                    else:
                        lineList.append(URIs)
                        mylist = sorted(list(dict.fromkeys(lineList)))

# result output
count = []
count1 = []

for uri in mylist[:50]:
    if len(uri) > 100:
        result_search1 = uri
        count1.append(result_search1)
        print(uri)
    else:
        result_search = "https://data.labs.kadaster.nl/pdok/metadata/browser?resource=" + uri
        print(result_search)
        count.append(result_search)
count1.extend(count)
number = (len(mylist))  # this is for check
number = str(number)
print("this is number of links:", number)

#### write a URI to a file a csv file
with open(path_output + name + "_" + k + number + ".csv", "w", newline='') as w:
    wr = csv.writer(w, quoting=csv.QUOTE_ALL)
    for word in mylist:
        wr.writerow([word])

# computing the exact time it takes to finish running
begin_time = time.time()
# Put your code here
end_time = time.time() - begin_time
print("Total execution time: ", format_timespan(end_time))

"""please check the numbers: this is number: and this is number of links:, they should be the same.. if the numbers were the same, you can delete one of them."""