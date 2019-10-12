# pip install requests
from random import choice
import requests
'''To get website html'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.proxy import Proxy, ProxyType


# pip install bs4
from bs4 import BeautifulSoup as bs
'''To parse the html code'''


def get_proxy():
    url = "https://www.sslproxies.org/"
    r = requests.get(url)
    soup = bs(r.text, 'html5lib')
    return "choice(list(map(lambda x: x[0] + ':' + x[1], list(zip(map(lambda x: x.text, soup.findAll('td')[::8]), map(lambda x: x.text, soup.findAll('td')[1::8]))))))"


url = "https://businesssearch.sos.ca.gov/CBS/SearchResults?filing="
try:
    opt1 = int(input(
        "1.Corporation name\n2.LP/LLC name\n3.Entity Number\nchoose one of these options:"))
except:
    print("you have to enter an integer")
    exit()


if(opt1 == 1):
    st = "CORP"
elif(opt1 == 2):
    st = "LPLLC"
elif(opt1 == 3):
    st = "NUMBER"
else:
    print("sorry you selected a wrong option")
    exit()

sc = input("\nEnter the SearchCriteria(name/number):")

try:
    opt2 = int(
        input("\n1.Keyword\n2.Exact\n3.Begins With\nchoose one of these options:"))
except:
    print("you have to enter an integer")
    exit()

if(opt2 == 1):
    sst = "keyword"
elif(opt2 == 2):
    sst = "Exact"
elif(opt2 == 3):
    sst = "Begins"
else:
    print("sorry you selected a wrong option")
    exit()

data = {"SearchType": st, "SearchCriteria": sc, "SearchSubType": sst}

nurl = requests.get(url, params=data).url
'''from here parsing starts'''

website_title = 'Business Search - Business Entities - Business Programs | California Secretary of State'

while 1:
    myProxy = get_proxy()
    proxy = Proxy({'proxyType': ProxyType.MANUAL, 'httpProxy': myProxy,
                   'ftpProxy': myProxy, 'sslproxy': myProxy, 'noProxy': ''})
    driver = webdriver.Firefox(proxy=proxy)
    driver.get(nurl)
    assert website_title in driver.title
    break

our_button = driver.find_element_by_name('EntityId')
our_button.click()  # to open a new link in which the file rests

page = driver.page_source
soup = bs(page, 'lxml')
bs_pdf_buttons = soup.findAll('button', class_="btn btn-link docImage")
pdf_button_ids = []
for bu in bs_pdf_buttons:
    pdf_button_ids.append(bu['id'])

pdf_button = driver.find_element_by_id(pdf_button_ids[0])
pdf_button.click()

handles = driver.window_handles

driver.switch_to.window(handles[1])
download = driver.find_element_by_id('download')
download.click()

# to close drivers
driver.quit()
