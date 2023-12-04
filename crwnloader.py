import asyncio
import aiohttp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from aiohttp.client import ClientSession
import re
from aiohttp.connector import TCPConnector
from datetime import datetime
import os
from test import search_youtube, download_audio

# Function to process each track
async def process_track(aname, y, match,directory,a):
    if match >= 80:
        print(f"{y} Success, Energy={match}")
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
        print(f"{y} Failed test, Energy={match}")

async def main():
    now = datetime.now()
    directory = str(now.strftime("%d %b %y"))
    if not os.path.exists(directory):
        os.mkdir(directory)
    # Get user input for the URL
    a = input("Enter url:")

    s = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")  # Disable images
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(a)
    driver.set_page_load_timeout(10)

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
    #new = []
    valli = nodets.split('\n')
    aname = valli[0][:-5]
    print(aname)

    tracks.pop(0)
    newtracks = []
    for i in tracks:
        newtracks.append(i[:-5])
    newtracks=newtracks[:-3]
    print(newtracks)
    tasks = []
    hotdict={}
    for track in newtracks:
        ntrack=track[5:]
        # Create a search query for each track
        #search_query = aname + '+' + track
        afeed = aname.split(" ")
        custom=""
        for af in afeed:
            custom = custom + af + "+"
        link = ""
        string = ntrack.split(" ")
        for i in string:
            link = link + i + "+"
        link = re.sub(r"[^\w']", "+", link)
        custom = re.sub(r"[^\w']", "+", custom)
        print(ntrack)
        # Extract song URL from search results
        for _ in range(5):  # Retry up to 5 times
            try:
                print(f"https://musicstax.com/search?q={custom}+{link}")
                driver.get(f"https://musicstax.com/search?q={custom}+{link}")
                break  # If successful, break the loop
            except TimeoutException:
                print("Loading took too much time! Retrying...")
        driver.implicitly_wait(3)
        html_content1 = driver.page_source
        soup1 = BeautifulSoup(html_content1, 'html.parser')
        track_element = str(soup1.find(class_='song-image search-image'))
        if track_element == "None":
            print("not found")
            continue
        else:
            match = track_element.split('"')[5]
            track_url = "https://musicstax.com" + match
            print(track_url)
            for _ in range(5):  # Retry up to 5 times
                try:
                    driver.get(track_url)
                    break  # If successful, break the loop
                except TimeoutException:
                    print("Loading took too much time! Retrying...")
        driver.implicitly_wait(2)
        html_content2 = driver.page_source
        soup2 = BeautifulSoup(html_content2, 'html.parser')
        site = soup2.find_all(class_='song-bar-statistic-number')
        dance = str(site[2])
        splited = dance.split("%")[0]
        siter = int(splited.split("\n")[1])
        match = siter
        print("Energy is:",match)
        if match< 80:
            continue
        hotdict.update({ntrack:match})
        tasks.append(asyncio.create_task(process_track(aname, ntrack, match,directory,a)))
    print(hotdict)

    # Run all tasks concurrently and wait for completion
    await asyncio.gather(*tasks)
    driver.quit()

asyncio.run(main())
