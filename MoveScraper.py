from urllib.request import Request, urlopen
import csv
from bs4 import BeautifulSoup

all_page = "statuses/All Moves.html"
all = open(all_page)
all_soup = BeautifulSoup(all, 'html5lib')
all_table = all_soup.find_all("table", class_="sortable")[0]
atr = all_table.find_all("tr")[1:]

sleep_page = "statuses/Sleep.html"
sleep = open(sleep_page)
sleep_soup = BeautifulSoup(sleep, 'html5lib')
#print(sleep_soup)
sleep_table = sleep_soup.find_all("table", class_="sortable")[0]
#print(sleep_table)
str = sleep_table.find_all("tr")[1:]

burn_page = "statuses/Burn.html"
burn = open(burn_page)
burn_soup = BeautifulSoup(burn, 'html5lib')
burn_table = burn_soup.find_all("table", class_="sortable")[0]
btr = burn_table.find_all("tr")[1:]

para_page = "statuses/Paralysis.html"
para = open(para_page)
para_soup = BeautifulSoup(para, 'html5lib')
para_table = para_soup.find_all("table", class_="sortable")[0]
ptr = para_table.find_all("tr")[1:]

freeze_page = "statuses/Freeze.html"
freeze = open(freeze_page)
freeze_soup = BeautifulSoup(freeze, 'html5lib')
freeze_table = free_soup.find_all("table", class_="sortable")[0]
ftr = freeze_table.find_all("tr")[1:]

poison_page = "statuses/Poison.html"
poison = open(poison_page)
poison_soup = BeautifulSoup(poison, 'html5lib')
poison_table = poison_soup.find_all("table", class_="sortable")[0]
ptr = poison_table.find_all("tr")[1:]
bad_poison_table = poison_soup.find_all("table", class_="sortable")[1]
bptr = bad_poison_table.find_all("tr")[1:]

# TODO: add the other effects before the write statement


with open("status_causing_moves.csv", 'w') as init:
    hdrs = ["Move", "No.", "Type", "Category", "Power", "PP", "Accuracy", "Effect", "Notes"] # Effect => ["Freeze", 6.67]
    writer = csv.DictWriter(csvfile, fieldnames=hdrs)
    writer.writeheader()

    # Scan all moves first
    for tr in atr:
        tds = tr.find_all('td')
        dict = {"Move": tds[1], "No.": tds[0], "Type": tds[2], "Category":tds[3], "Power":tds[6], "PP":tds[5], "Accuracy":tds[7] }
        writer.writerow(dict)



        print("Move: %s Type: %s Category: %s" % \
            (tds[0].text, tds[1].text, tds[2].text))
