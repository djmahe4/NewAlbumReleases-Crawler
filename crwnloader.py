import feedparser
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os
from test import search_youtube, download_audio
async def process_track(aname, y, match,directory,a,track_url):
    if match >= 75:
        print(f"{y} Success, Energy={match}")
        query = f"{aname} - {y}"
        print(query)
        vidurl = search_youtube(query)
        print(vidurl)
        file = open(f'{directory}/songs.txt', 'a')
        file.write(f"{query} link: {a} url: {vidurl}, Energy: {match}, Stats: {track_url}\n")
        file.close()
        if vidurl != "No results found.":
            download_audio(str(vidurl), fr'{directory}')
        else:
            print("Video not found :(")
    else:
        print(f"{y} Failed test, Energy={match}")

async def main():
    now = datetime.now()
    today=datetime.today().date()
    today=input("Enter date (yyyy-mm-dd):")
    #print(today)
    directory=now.strftime("%d %b %y").upper()
    directory = input("Enter date (dd me yy):")
    links=[]
    if not os.path.exists(directory):
        os.mkdir(directory)
    # Get user input for the URL
    rss_url = "https://newalbumreleases.net/feed/"
    feed=feedparser.parse(rss_url)
    for entry in feed["entries"]:
        #print(entry)
        # Parse the date of the entry
        entry_date = datetime.strptime(entry['published'], "%a, %d %b %Y %H:%M:%S %z").date()
        #print(type(entry_date))
        lastitem=entry['published']
        # Check if the entry date is today
        if str(entry_date) == str(today):
            # Add the entry link to the list
            links.append(entry['links'][0]['href'])
        else:
            continue
    print(f"Getting feeds from untill...{lastitem[:-6]}")
    print(f"Found {len(links)} number of link(s)")
    cont = input("Enter number:")
    links=links[::-1]
    for a in links:
        if cont != "":
            if links.index(a)<int(cont):
                continue
        print(a)
        if "essentials" in a:
            print("Essentials is a very long playlist..Skipping...")
            continue
        print(f"links remaining:{len(links) - links.index(a)}/{len(links)}")
        print(f"If fails enter :{links.index(a)}")
        s = Service(ChromeDriverManager().install())
        options = Options()
        options.add_argument("--headless")  # Disable images
        driver = webdriver.Chrome(service=s, options=options)
        driver.set_page_load_timeout(10)



        details = []
        songs = []


        for _ in range(3):  # Retry up to 3 times
            try:
                # Your main code here
                driver.get(a)
                html_content = driver.page_source
                soup = BeautifulSoup(html_content, 'html.parser')
                paragraphs = soup.find_all('p')
                det = str(paragraphs[1])
                # More of your code...

                break  # If successful, break the loop
            except (IndexError, TimeoutException):
                print("Retrying...")
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
            if i =="":
                continue
            newtracks.append(i[:-5])
        newtracks=newtracks[:-3]
        print(newtracks)
        tasks = []
        hotdict={}
        for track in newtracks[:-1]:
            if "instrumental" in track.lower():
                print("Instrumental version (N/A)")
                continue
            if re.search(r'\blive\b', track.lower()):
                print("Live version (N/A)")
                continue
            if "remastered" in track.lower():
                print("Remastered version (N/A)")
                continue
            if "extended" in track.lower():
                print("Extended version (N/A)")
                continue
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
            print(f'{track[:2]}) {ntrack}')
            # Extract song URL from search results
            for _ in range(5):  # Retry up to 5 times
                try:
                    #print(f"https://musicstax.com/search?q={custom}+{link}")
                    driver.get(f"https://musicstax.com/search?q={custom}+{link}")
                    driver.implicitly_wait(3)
                    html_content1 = driver.page_source
                    break  # If successful, break the loop
                except TimeoutException:
                    print(f"Searching Track...")

            soup1 = BeautifulSoup(html_content1, 'html.parser')
            track_element = str(soup1.find(class_='song-image search-image'))
            if track_element == "None":
                print("not found")
                continue
            else:
                match = track_element.split('"')[5]
                track_url = "https://musicstax.com" + match
                #print(track_url)
                for _ in range(5):  # Retry up to 5 times
                    try:
                        driver.get(track_url)
                        html_content2 = driver.page_source
                        driver.implicitly_wait(2)
                        soup2 = BeautifulSoup(html_content2, 'html.parser')
                        site = soup2.find_all(class_='song-bar-statistic-number')
                        dance = str(site[2])
                        break  # If successful, break the loop
                    except (TimeoutException,IndexError):
                        print("Loading track details...")
            splited = dance.split("%")[0]
            siter = int(splited.split("\n")[1])
            match = siter
            print("Energy is:",match)
            if match < 40:
                print("Negative")
                break
            elif match< 75 or match>= 90:
                continue
            hotdict.update({ntrack:match})
            tasks.append(asyncio.create_task(process_track(aname, ntrack, match,directory,a,track_url)))
        print(hotdict)

        # Run all tasks concurrently and wait for completion
        await asyncio.gather(*tasks)
        driver.quit()
asyncio.run(main())
