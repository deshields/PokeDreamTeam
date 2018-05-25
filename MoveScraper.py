from urllib.request import Request, urlopen
import csv
from bs4 import BeautifulSoup

sleep_page = "statuses/Sleep.html"#"https://bulbapedia.bulbagarden.net/wiki/Sleep_(status_condition)#Moves"
sleep = open(sleep_page)
sleep_soup = BeautifulSoup(sleep, 'html5lib')
#print(sleep_soup)
sleep_table = sleep_soup.find_all("table", class_="sortable")[0]
#print(sleep_table)
str = sleep_table.find_all("tr")[1:]

for tr in str:
    tds = tr.find_all('td')
    print("Move: %s Type: %s Category: %s" % \
        (tds[0].text, tds[1].text, tds[2].text))
