import feedparser, csv, sys
from bs4 import BeautifulSoup

# http://goidirectory.nic.in/rss/new_additions_rss.php
# ministry - http://goidirectory.nic.in/rss/minstry_rss.php?categ_id=
# sates - http://goidirectory.nic.in/rss/state_rss.php?categ_id=
# http://goidirectory.nic.in/rss/orgn_category_rss.php?categ_id=JUD,IN
states = ["AN","AP","AR","AS","BR","CH","CG","DN","DD","DL","GA","GJ","HR","HP","JK","JH","KA","KL","LD","MP","MH","MN","ML","MZ","NL","OR","PY","PB","RJ","SK","TN","TG","TR","UK","UP","WB"]
categs = ["IN","JUD"]
# for page in range( 1, 1000 ):
for page in categs:
    try:
        rssPR = feedparser.parse("http://goidirectory.nic.in/rss/orgn_category_rss.php?categ_id="+str(page))
        # rssPR = feedparser.parse("http://goidirectory.nic.in/rss/new_additions_rss.php")
        rssDataList = []
        path = "meta/rss/"+str(page)+".csv"
        with open(path, 'wb') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(['title', 'link', 'guid', 'category', 'description', 'published'])
            for index, item in enumerate(rssPR.entries):
                url = item.link.encode('utf-8')
                wr.writerow([item.title.encode('utf-8'), url, item.guid.encode('utf-8'), item.category.encode('utf-8'), item.description.encode('utf-8'), item.published.encode('utf-8')])
    except:
        print "Unexpected error:", sys.exc_info()[0]
    
