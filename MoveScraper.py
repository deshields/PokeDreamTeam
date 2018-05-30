from urllib.request import Request, urlopen
import csv
from bs4 import BeautifulSoup
import pandas as pd

all_page = "statuses/All Moves.html"
all = open(all_page)
all_soup = BeautifulSoup(all, 'html5lib')
all_table = all_soup.find_all("table", class_="sortable")[0]
atr = all_table.find_all("tr")[1:] #atr is a List
#print(atr[1])

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
freeze_table = freeze_soup.find_all("table", class_="sortable")[0]
ftr = freeze_table.find_all("tr")[1:]

poison_page = "statuses/Poison.html"
poison = open(poison_page)
poison_soup = BeautifulSoup(poison, 'html5lib')
poison_table = poison_soup.find_all("table", class_="sortable")[0]
potr = poison_table.find_all("tr")[1:]
bad_poison_table = poison_soup.find_all("table", class_="sortable")[1]
bptr = bad_poison_table.find_all("tr")[1:]

# TODO: add the other effects before the write statement


# with open("status_causing_moves.csv", 'w') as init:
#     hdrs = ["Name", "No.", "Type", "Category", "Power", "PP", "Accuracy", "Effect", "Notes"] # Effect => ["Freeze", 6.67]
#     writer = csv.DictWriter(init, fieldnames=hdrs)
#     writer.writeheader()
#
#     # Scan all moves first
    # for tr in atr:
# tds = atr[1].find_all('td') # this works


for tr in range(1, len(atr)):   # now
    tds = atr[tr].find_all('td') # this
    print("Result: ", tds[4].text) # does
#         dict = {"Name": tds[1].text, "No.": tds[0].text, "Type": tds[2].text, "Category":tds[3].text, "Power": tds[6].text, "PP": tds[5].text, "Accuracy":tds[7].text, "Effect": [] }
#         writer.writerow(dict)
#
#     #TODO: check for status-inducing moves and update accordingly
#
# df = pd.read_csv("status_causing_moves.csv", index_col=0)
#
# for t1, t2, t3, t4, t5, t6 in izip(str, btr, ptr, ftr, potr, bptr):
#     tds1, tds2, tds3, tds4, tds5, tds6 = t1.find_all('td'), t2.find_all('td'), t3.find_all('td'), t4.find_all('td'), t5.find_all('td'), t6.find_all('td')
#     df.loc[tds1[0].text]["Effect"] = ["SLEEP", float(tds1[3].text.strip('%'))/100]
#     df.loc[tds2[0].text]["Effect"] = ["BURNED", float(tds2[3].text.strip('%'))/100]
#     df.loc[tds3[0].text]["Effect"] = ["PARALYZED", float(tds3[3].text.strip('%'))/100]
#     df.loc[tds4[0].text]["Effect"] = ["FROZEN", float(tds4[3].text.strip('%'))/100]
#     df.loc[tds5[0].text]["Effect"] = ["POISONED", float(tds5[3].text.strip('%'))/100]
#     df.loc[tds6[0].text]["Effect"] = ["BADLY POISONED", float(tds6[3].text.strip('%'))/100]


        #
        #
        # print("Move: %s Type: %s Category: %s" % \
        #     (tds[0].text, tds[1].text, tds[2].text))
