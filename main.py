import feedparser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import youtube_dl
from youtubesearchpython import SearchVideos
import json
from test import download_audio,search_youtube
from datetime import datetime

# Setup webdriver
now = datetime.now()
import os

# Specify the name of the directory to be created
directory = str(now.strftime("%d %b %y"))
if not os.path.exists(directory):
    os.mkdir(directory)

s=Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--blink-settings=imagesEnabled=false")  # Disable images
driver = webdriver.Chrome(service=s, options=options)

# Get the RSS feed data
rss_url ="https://newalbumreleases.net/feed/"
feed = feedparser.parse(rss_url)
entries=feed['entries']
a=entries[0]['links'][0]['href']

driver.get(a)

html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

details=[]
songs=[]
paragraphs = soup.find_all('p')
det=str(paragraphs[1])
details.append(det.split("<b>"))
tracks=str(paragraphs[2]).split("\n")
dets=details[0]
nodets=list(dets[1].split("<br>"))[0]
new=[]
valli=nodets.split('\n')
aname=valli[0][:-5]
print(aname)
#print(aname)

tracks.pop(0)
newtracks=[]
for i in tracks:
    #break
    newtracks.append(i[:-5])
x=newtracks[-1].split('"')[0]
url=f"{x}"
print(newtracks)

for i in newtracks[:-3]:
    x = i[5:]
    y = x.split("(")[0]
    string=y.split(" ")
    print(y)
    link=""
    for i in string:
        link=link+i+"+"
    driver.get(f"https://musicstax.com/search?q={aname}+{link}")
    #driver.implicitly_wait(10)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    site = str(soup.find(class_='song-image search-image'))
    #print(site)
    if site=="None":
        print("not found")
        continue
    match = site.split('"')[5]
    newlink="https://musicstax.com" + match
    print(newlink)
    driver.get(newlink)

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    site = soup.find_all(class_='song-bar-statistic-number')
    dance=str(site[2])
    splited=dance.split("%")[0]
    siter=int(splited.split("\n")[1])
    match = siter
    if match>80:
        print(f"Success, Energy={match}")
        query=f"{aname} - {i}"
        print(query)
        file=open(f'{directory}/songs.txt', 'w')
        file.write(f"{query} link: {a}\n")
        file.close()
        vidurl=search_youtube(query)
        print(vidurl)
        if vidurl!="No results found.":
            download_audio(str(vidurl),f'{directory}\{query}')
        else:
            print("Video not found :(")
    else:
        print(f"Failed test, Energy={match}")

driver.quit()
