import feedparser
import sys
import csv
from bs4 import BeautifulSoup
import urllib2


def get_contact_link(guid, link):
    print link
    html_page = urllib2.urlopen(link, timeout=10)
    soup = BeautifulSoup(html_page)
    for link in soup.findAll('a'):
        title = link.text.lower()
        href = link.get('href').lower()
        if (("contact" in title and "us" in title) or ("contact" in href and "us" in href)):
            print title
            return link.get('href')
        if  ("contact.htm" in href):
            print title
            return link.get('href')
    return None

def save_home_text(guid, link):
    print link
    guid_name = replace_special_char(guid)
    path = "meta/home_raw/" + guid_name + ".text"
    print path
    request = urllib2.urlopen(link, timeout=10)
    with open(path, 'wb') as f:
        try:
            f.write(request.read())
        except:
            print("error")

    html_page = urllib2.urlopen(link, timeout=10)
    
    soup = BeautifulSoup(html_page)
    text = soup.get_text()
    text = text.encode('utf-8').strip()

    path = "meta/home_text/" + guid_name + ".text"
    text_file = open(path, 'wb')
    text_file.write(text)
    text_file.close()


def get_link(page):
    path = "meta/link/" + str(page) + ".csv"
    with open(path, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['title', 'link', 'guid', 'category',
                     'description', 'published', 'contact_link'])

        f = open("meta/rss/" + str(page) + ".csv", 'rb')
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            url = row[1]
            guid = row[2]
            contact_link = None
            try:
                contact_link = get_contact_link(guid, url)
            except:
                print "Unexpected contact error:", sys.exc_info()[0]
            
            
            try:
                if contact_link is None:
                    save_home_text(guid, url)
            except:
                print "Unexpected home error:", sys.exc_info()[0]

            print "\n contact_link : ", contact_link
            row.append(contact_link)
            wr.writerow(row)
            

            

others=[723]
# states = ["AN","AP","AR","AS","BR","CH","CG","DN","DD","DL","GA","GJ","HR","HP","JK","JH","KA","KL","LD","MP","MH","MN","ML","MZ","NL","OR","PY","PB","RJ","SK","TN","TG","TR","UK","UP","WB"]
states = ["MN","ML","MZ","NL","OR","PY","PB","RJ","SK","TN","TG","TR","UK","UP","WB"]
categs = ["IN","JUD"]
pages = []
# for page in range( 35, 100):
#     pages.append(str(page))
# for page in others:
#     pages.append(str(page))
for page in states:
    pages.append(str(page))
for page in categs:
    pages.append(str(page))
for page in pages:
    try:
        print page
        get_link(page)
    except:
        print "Unexpected error:", sys.exc_info()[0]
