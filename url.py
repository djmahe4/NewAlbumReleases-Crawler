from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from test import download_audio, search_youtube
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import os
import re
# Function to process each track
def process_tracks(tracks):
    for i in tracks:
        # Your existing code for processing each track goes here
        print(i)
        x = i[5:]
        y = x
        string = y.split(" ")
        print(y)
        link = ""
        for i in string:
            link = link + i + "+"
        link = re.sub(r"[^\w']", "+", link)
        driver.get(f"https://musicstax.com/search?q={aname}+{link}")
        driver.implicitly_wait(3)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        site = str(soup.find(class_='song-image search-image'))
        # print(site)
        if site == "None":
            print("not found")
            continue
        match = site.split('"')[5]
        newlink = "https://musicstax.com" + match
        print(newlink)
        driver.get(newlink)
        driver.implicitly_wait(5)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        site = soup.find_all(class_='song-bar-statistic-number')
        dance = str(site[2])
        splited = dance.split("%")[0]
        siter = int(splited.split("\n")[1])
        match = siter
        if match >= 80:
            print(f"Success, Energy={match}")
            query = f"{aname} - {y}"
            print(query)
            vidurl = search_youtube(query)
            print(vidurl)
            file = open(f'{directory}/songs.txt', 'a')
            file.write(f"{query} link: {a} url: {vidurl}\n")
            file.close()
            if vidurl != "No results found.":
                download_audio(str(vidurl), fr'{directory}')
            else:
                print("Video not found :(")
        else:
            print(f"Failed test, Energy={match}")

# Function to split list into chunks
def split_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

# Setup webdriver
now = datetime.now()
directory = str(now.strftime("%d %b %y"))
if not os.path.exists(directory):
    os.mkdir(directory)

a = input("Enter url:")
s = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--headless")  # Disable images
driver = webdriver.Chrome(service=s, options=options)

driver.get(a)

html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

details = []
songs = []
paragraphs = soup.find_all('p')
det = str(paragraphs[1])
details.append(det.split("<b>"))
tracks = str(paragraphs[2]).split("\n")
dets = details[0]
nodets = list(dets[1].split("<br>"))[0]
new = []
valli = nodets.split('\n')
aname = valli[0][:-5]
print(aname)

tracks.pop(0)
newtracks = []
for i in tracks:
    newtracks.append(i[:-5])
x = newtracks[-1].split('"')[0]
url = f"{x}"
print(newtracks)

# Split the newtracks list into chunks of size 5
chunk_size = 5
track_chunks = list(split_list(newtracks[:-3], chunk_size))

# Create threads
with ThreadPoolExecutor() as executor:
    # Use map to assign each item in the list to a worker in the pool
    for i in track_chunks:
        executor.map(process_tracks, track_chunks)
    driver.quit()
