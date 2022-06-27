#!/usr/bin/env python
# Modified frmo https://github.com/Q42/SimpleOAIHarvester/blob/master/harvest.py
import requests, os, sys
from xml.dom import minidom

if len(sys.argv) < 2: raise Exception('API key required')
resumeFile = sys.argv[2] if len(sys.argv) >= 3 else None
apikey = sys.argv[1]
if len(sys.argv) == 3:
    save_folder = sys.argv[3]
else:
    save_folder = ""

url = "http://www.rijksmuseum.nl/api/oai/%s/?verb=listrecords&metadataPrefix=oai_dc" % apikey
url2 = "http://www.rijksmuseum.nl/api/oai/%s/?verb=listrecords&resumptiontoken=" % apikey
count = 0 # keep track of number of records harvested
token = ""

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def harvest(url):
    print("downloading: " + url)
    data = requests.get(url).text

    dom = minidom.parseString(data)

    # check for error
    error = dom.getElementsByTagName('error')
    if len(error) > 0:
        errType = error[0].getAttribute('code')
        desc = getText(error[0].childNodes)
        raise Exception(errType + ": " +desc)

    save(data)

    countRecords = len(dom.getElementsByTagName('record'))

    nodelist = dom.getElementsByTagName('resumptionToken')
    if len(nodelist) == 0: return None, countRecords
    strToken = getText(nodelist[0].childNodes)

    return strToken, countRecords

def save(data):

    filename = os.path.join(".", save_folder, str(count) + '.xml')
    print('saving: ' + filename)
    with open(filename, 'w') as f:
        for s in data:
            f.write(s)

def file_name(fn):
    if "/" and "\\" not in fn:
        return os.path.join(".", save_folder, str(count) + '.xml')
    else:
        return os.path.join(save_folder, str(count) + '.xml')


def resume(filename):
    with open(filename, 'r') as f:
        data = f.read()
         # cache the data because this file-like object is not seekable
        cached  = ""
        for s in data:
            cached += s

        dom = minidom.parseString(cached)

        countRecords = len(dom.getElementsByTagName('record'))

        nodelist = dom.getElementsByTagName('resumptionToken')
        if len(nodelist) == 0: return None, countRecords
        strToken = getText(nodelist[0].childNodes)

        return strToken, countRecords

try:
    if resumeFile:
        token, countRecords = resume(resumeFile)
        count += int(resumeFile.split('.')[0]) + countRecords
    else:
        token, countRecords = harvest(url)
        count += countRecords

    while token:
        token, countRecords = harvest(url2 + token)
        count += countRecords

except:
    print("\n!!!")
    print("Unexpected error")
    print("To resume run this script with the last succesfully harvested file as second paramater:")
    print("python harvest.py <API KEY> <LAST HARVESTED FILE>")
    print("!!!\n")
    raise
