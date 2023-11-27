import feedparser
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


# Get the RSS feed data
#rss_url = "https://newalbumreleases.net/feed/"
rss_url ="https://newalbumreleases.net/category/pop/feed/"
#rss_url = "https://newalbumreleases.net/category/indie/feed/"
#rss_url ="https://newalbumreleases.net/category/electronic/feed/"
feed = feedparser.parse(rss_url)
#   print(feed)
entries=feed['entries']
a=entries[0]['links'][0]['href']
#response=requests.get(url=f"{a}")
#print(response.json())
# Check if the request was successful (status code 200)
driver = webdriver.Chrome()  # You need to have the ChromeDriver executable in your PATH

driver.get(a)
# Wait for some time to allow dynamic content to load
driver.implicitly_wait(5)  # Adjust the time based on your needs
# Now you can get the page source
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')
#print(soup)
details=[]
songs=[]
paragraphs = soup.find_all('p')
det=str(paragraphs[1])
details.append(det.split("<b>"))
tracks=str(paragraphs[2]).split("\n")
dets=details[0]
nodets=dets
new=[]
#print(details)
#print(tracks)
for i in dets:
    nodets.pop(dets.index((i)))
    #print(i)
    x=i.split("\n")
    new.append(x)
aname=new[1][0][:-5]
print(aname)
tracks.pop(0)
newtracks=[]
for i in tracks:
    newtracks.append(i[:-5])
print(newtracks)
x=newtracks[-1].split('"')[0]
url=f"{x}"
for i in newtracks[:-3]:
    x = i[5:]
    y = x.split("(")[0]
    string=y.split(" ")
    print(string)
    link=""
    for i in string:
        link=link+i+"+"
    driver = webdriver.Chrome()
    driver.get(f"https://musicstax.com/search?q={aname}+{link}")
    driver.implicitly_wait(10)
    button = driver.find_element(By.CSS_SELECTOR, 'a[data-cy="song-image"].song-image.search-image')
    # Scroll into view
    driver.execute_script("arguments[0].click();", button)
    driver.implicitly_wait(15)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    #print(soup)
    site = soup.find_all(class_='song-bar-statistic-number')
    dance=str(site[2])
    splited=dance.split("%")[0]
    siter=int(splited.split("\n")[1])
    #print(siter)
    match = siter
    if match>80:
        print(f"Success, Energy={match}")
        query=f"{aname} - {i}"
        with open('songs.txt', 'w') as file:
            file.write(f"{query} link: {a}\n")
        #break

    else:
        print(f"Failed test, Energy={match}")
    #break
# Proceed with extracting data using BeautifulSoup
# ...
driver.quit()
