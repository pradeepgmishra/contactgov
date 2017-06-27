import sys
import re
import csv
from bs4 import BeautifulSoup
import urllib2
# import urllib


def replace_special_char(guid):
    return re.sub('[^a-zA-Z0-9 \n\.]', '', guid)


def save_contact_text(guid, link):
    print link
    guid_name = replace_special_char(guid)
    path = "meta/raw/" + guid_name + ".text"
    print path
    request = urllib2.urlopen(link, timeout=50)
    with open(path, 'wb') as f:
        try:
            f.write(request.read())
        except:
            print("error")

    html_page = urllib2.urlopen(link, timeout=50)
    
    soup = BeautifulSoup(html_page)
    text = soup.get_text()
    text = text.encode('utf-8').strip()

    path = "meta/text/" + guid_name + ".text"
    text_file = open(path, 'wb')
    text_file.write(text)
    text_file.close()


def get_link(page):
    f = open("meta/link/" + str(page) + ".csv", 'rb')
    reader = csv.reader(f)
    reader.next()
    for row in reader:
        try:
            guid = row[2]
            contact_link = row[1] + "/" + row[6]
            save_contact_text(guid, contact_link)
        except:
            print "Unexpected error:", sys.exc_info()[0]


others=[723]
states = ["AN","AP","AR","AS","BR","CH","CG","DN","DD","DL","GA","GJ","HR","HP","JK","JH","KA","KL","LD","MP","MH","MN","ML","MZ","NL","OR","PY","PB","RJ","SK","TN","TG","TR","UK","UP","WB"]
categs = ["IN","JUD"]
pages = []
# for page in range( 2, 100):
for page in range( 46, 100):
    pages.append(str(page))
for page in others:
    pages.append(str(page))
for page in states:
    pages.append(str(page))
for page in categs:
    pages.append(str(page))
pages.append(str(1))
for page in pages:
    try:
        print "Page -> "+page
        get_link(page)
    except:
        print "Unexpected error:", sys.exc_info()[0]
