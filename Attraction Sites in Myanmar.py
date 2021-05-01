import csv
import requests
from bs4 import BeautifulSoup

url = "https://www.tripadvisor.co.uk/Attractions-g294190-Activities-oa{}-Myanmar.html"

row_list = []
def remove(filter_col):
        rating = filter_col.split(' ')[1]
        rating = rating[-3:]
        return rating


for page in range(0,61):  # < from page 1 to 61
    print("Getting page {}..".format(page))
    soup = BeautifulSoup(requests.get(url.format(page * 30)).content, "html.parser")
    cards = soup.find_all('section',class_='_2TabEHya _3YhIe-Un')
    for card in cards:
        try: 
            name = card.find('div',class_='_1gpq3zsA _1zP41Z7X').text          
        except:
            name = ''
        try: 
            rating = str(card.find('svg',class_='zWXXYhVR'))
            rating = remove(filter_col=rating)
        except:
            rating = ""                
        try:
            review_count = card.find('span',class_='DrjyGw-P _26S7gyB4 _14_buatE _1dimhEoy').text
        except:
            review_count =""
        try:
            status = card.find('div',class_='DrjyGw-P _26S7gyB4 _3SccQt-T').text 
        except:
            status = ""    

        row_list.append([name,rating,status,review_count])
    
with open("top_sites.csv", "w",encoding="utf-8") as f_out:
    w = csv.writer(f_out,delimiter=',')
    w.writerows(row_list)
