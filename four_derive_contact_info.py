import sys
import re
import csv
from bs4 import BeautifulSoup
import urllib2
import json


def is_phone(phone_nuber):
    pattern = re.compile("^[\dA-Z]{3}-[\dA-Z]{3}-[\dA-Z]{4}$", re.IGNORECASE)
    return pattern.match(phone_nuber) is not None


def is_email(text):
    regexp = re.compile(
        r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$', re.IGNORECASE)
    email = regexp.findall(text)
    if email:
        return True
    return False


def replace_special_char(guid):
    return re.sub('[^a-zA-Z0-9 \n\.]', '', guid)


def get_text_blocks(text):
print "IMPLEMENT IT"
sys.exit()

def get_excel_contacts(raw):
    # algo 1.  check if <table> present. if yes, find each row, check if row contains address and return it
    # algo 2. later. check if <div> and <br> based rows present
    # algo 1 -
    contact_cards = []
    soup = BeautifulSoup(raw)
    for tr in soup.findAll('tr'):
        contact_card = {}
        is_contact = False
        col_name_seq = ""
        for column in tr.get('td'):
            col_name_seq = col_name_seq + "_col_"
            col_name = col_name_seq
            if is_email(column) or is_phone(column):
                is_contact = true
            if is_email(column):
                col_name = "email"
            if is_phone(column):
                col_name = "phone"
            contact_card[col_name] = column.text

        if is_contact:
            contact_cards.append(contact_card)

        return contact_cards


def get_contact_text_blocks(raw, text):
    contact_cards = []
    # find_excel_blocks_in_text with atleast 1 column containing email or phone
    excel_contacts = get_excel_contacts(raw)
    for contact_card in excel_contacts:
        contact_cards.append(contact_card)
    text_blocks = get_text_blocks(text)
    for text_block in text_blocks:
        contact_card = contact_from_text(text_block)
        contact_cards.append(contact_card)

    return contact_cards


def get_link(page):
    f = open("meta/link/" + str(page) + ".csv", 'rb')
    reader = csv.reader(f)
    reader.next()
    for row in reader:
        try:
            guid = row[2]
            guid_name = replace_special_char(guid)
            path = "meta/text/" + guid_name + ".text"
            text_file = open(path)
            text = text_file.read()
            text_file.close()

            path = "meta/raw/" + guid_name + ".text"
            raw_file = open(path)
            raw = raw_file.read()
            raw_file.close()
            contact_cards = get_contact_text_blocks(raw, text)
            contacts = {}
            contacts["contacts"] = contact_cards

            path = "meta/contact/" + guid_name + ".json"
            with open(path, 'wb') as outfile:
                json.dump(contacts, outfile,
                      default=lambda o: o.__dict__, indent=4)

        except:
            print "Unexpected error:", sys.exc_info()[0]


for page in range(1, 2):
    try:
        get_link(page)
    except:
        print "Unexpected error:", sys.exc_info()[0]
