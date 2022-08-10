#!/usr/bin/env python
# Modified frmo https://github.com/Q42/SimpleOAIHarvester/blob/master/harvest.py
import requests, os, sys
import argparse
from xml.dom import minidom
from tqdm import tqdm
import winsound
import glob
from send_mail import send_mail

if len(sys.argv) < 2: raise Exception('API key required')
resumeFile = sys.argv[3] if len(sys.argv) >= 4 else None
apikey = sys.argv[1]
if len(sys.argv) >= 3:
    save_folder = sys.argv[2]
else:
    save_folder = ""

url = "http://www.rijksmuseum.nl/api/oai/%s/?verb=listrecords&metadataPrefix=lido" % apikey
url2 = "http://www.rijksmuseum.nl/api/oai/%s/?verb=listrecords&resumptiontoken=" % apikey
count = 0 # keep track of number of records harvested
token = ""

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def url_get(url, s=None):
    x = 0
    while x < 10:
        print(x)
        try:
            if s:
                r = s.get(url)
            else:
                r = requests.get(url)
            x = 11
        except KeyboardInterrupt:
            print("Ctrl-c detected, exiting")
            import sys; sys.exit()
            raise KeyboardInterrupt
        except Exception as e:
            x+=1
            raise(e)
            continue

        if r.status_code == 200:
            x = 10
    return r

def harvest(url, s=None):
    print("downloading: " + url)
    if s:
        data = url_get(url, s).text
    else:
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
    filename = file_name(save_folder)
    print('saving: ' + filename)
    with open(filename, 'w', encoding="utf-8") as f:
        for s in data:
            f.write(s)

def file_name(fn):
    if "/" and "\\" not in fn:
        return os.path.join(".", save_folder, str(count) + '.xml')
    else:
        return os.path.join(save_folder, str(count) + '.xml')


def resume(filename):
    with open(filename, 'r', encoding="utf-8") as f:
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
    s = requests.Session()
    # s = None
    if resumeFile:
        token, countRecords = resume(os.path.join(save_folder, resumeFile))
        count += int(resumeFile.split('.')[0]) + countRecords
    else:
        token, countRecords = harvest(url, s)
        count += countRecords

    with tqdm(total=33000) as pbar:
        while token:
            token, countRecords = harvest(url2 + token, s)
            count += countRecords
            pbar.update(1)

except:
    # requests.post("https://notify.run/c/BlqCBFeCJhxKLcEprOMg", data={"Crashed once"})
    send_mail("crashed once", " ")
    list_of_files = glob.glob('F:\\museum-collections\\rijks\\1\\*')
    resumeFile = max(list_of_files, key=os.path.getctime)
    resumeFile = resumeFile.split("\\")[-1]
    print(resumeFile)
    try:
        s = requests.Session()
        # s = None
        if resumeFile:
            token, countRecords = resume(os.path.join(save_folder, resumeFile))
            count += int(resumeFile.split('.')[0]) + countRecords
        else:
            token, countRecords = harvest(url, s)
            count += countRecords

        with tqdm(total=33000) as pbar:
            while token:
                token, countRecords = harvest(url2 + token, s)
                count += countRecords
                pbar.update(1)

    except:
        # requests.post("https://notify.run/c/BlqCBFeCJhxKLcEprOMg", data={"Hard crash, restart ASAP"})
        send_mail("hard crash, restart ASAP", " ")
        print("\n!!!")
        print("Unexpected error")
        print("To resume run this script with the last succesfully harvested file as second paramater:")
        print("python harvest.py <API KEY> <LAST HARVESTED FILE>")
        print("!!!\n")
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        raise
