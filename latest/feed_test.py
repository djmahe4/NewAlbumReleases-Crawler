#import feedparser
import asyncio
from spotdl import Spotdl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re
from datetime import datetime,timezone
import os

from feed_test2 import new_feed_input,page_view,page_view2
from defn import search_youtube, download_audio, song_details
from my_telegram import format_and_print_artist_info
spotdl = Spotdl(client_id='16a580bdff3b4b6f822804fb6372712c', client_secret='7b7b8f6350bb452a880cf2a2adab3187')
check={}
async def process_track(aname, y, match,directory,track_url,dance,tgram):
    if match >= 34 or dance>=34:
        query = f"{aname} {y}"
        #print(query)
        vidurl = search_youtube(query)
        print(vidurl)
        if vidurl != None: #"No results found."
            fpath=download_audio(str(vidurl), fr'{directory}')
            file = open(f'{directory}/songs.txt', 'a')
            try:
                file.write(f"{y} url: {vidurl}, Energy: {match}, Stats: {track_url}\n")
                print(f"{y} Success, Energy={match}")
                tgram[2]=vidurl
                #fpath = fpath.split("\\")[-1]
                format_and_print_artist_info(fpath,*tgram)
            except UnicodeEncodeError:
                file.write(f"Name Error; url: {vidurl}, Energy: {match}, Stats: {track_url}\n")
            file.close()

        else:
            print("Video not found :(")
    else:
        print(f"{y} Failed test, Energy={match}, Dancebility={dance}")

def process_spot_track(aname, y, match,directory,track_url,dance,tgram):
    if match >= 37 or dance>=37:
        query = f"{aname} {y}"
        #print(query)
        songs = spotdl.search([
            query])
        vidurl = songs[0].url
        print(vidurl)
        if vidurl != None: #"No results found."
            song, fpath = spotdl.download(songs[0])
            try:
                os.rename(fpath, os.path.join(directory, fpath))
            except (FileExistsError,TypeError):
                print("File exists..Or some error")
                return
            file = open(f'{directory}/songs.txt', 'a')
            try:
                file.write(f"{y} url: {vidurl}, Energy: {match}, Stats: {track_url}\n")
                print(f"{y} Success, Energy={match}")
                tgram[2]=vidurl
                #fpath = fpath.split("\\")[-1]
                format_and_print_artist_info(fpath,*tgram)
            except UnicodeEncodeError:
                file.write(f"Name Error; url: {vidurl}, Energy: {match}, Stats: {track_url}\n")
            file.close()

        else:
            print("Video not found :(")
    else:
        print(f"{y} Failed test, Energy={match}, Dancebility={dance}")

def main():
    global ntrack, syear
    now = datetime.now()
    #n=0
    today=input("Enter date (yyyy-mm-dd):")
    if today=="":
        today = datetime.now(timezone.utc).date()
    year=int(str(today)[:4])
    #else:
    #year = int(today[:4])
    print("YEAR",year)
    directory = input("Enter date (dd me yy):")
    if directory=="":
        directory = now.strftime("%d %b %y").upper()
    links=[]
    if not os.path.exists(directory):
        os.mkdir(directory)
    print(directory)
    # Get user input for the URL
    rss_url = "https://newalbumreleases.net/feed/"
    # Initialize lastitem
    #lastitem = None
    links, lastitem = new_feed_input(today)
    print(f"Getting feeds from until...{lastitem[:-6]}")
    print(f"Found {len(links)} number of link(s)")
    for nlink in links:
        print(f"{len(links)-links.index(nlink)-1}:{nlink}")
    cont = input("Enter number:")
    links=links[::-1]

    for a in links:
        if cont != "":
            if links.index(a)<int(cont):
                continue
        print(a)
        if "soundtrack" in a:
            print("Soundtracks are always plain and boring..Skipping...")
            continue
        print(f"links remaining:{len(links) - links.index(a)}/{len(links)}")
        print(f"If fails enter :{links.index(a)}")

        #s = Service(ChromeDriverManager().install())
        #s = Service('D:\chromedriver-win64\chromedriver-win64\chromedriver.exe')
        #options = Options()
        #options.add_argument("--disk-cache-dir=/cache")
        #options.add_experimental_option("prefs", {"profile.manged_default_content_settings.images": 2})
        # options.add_argument("--headless")  # Disable images
        #driver = webdriver.Chrome(service=s, options=options)
        #driver.set_page_load_timeout(20)
        details = []
        songs = []


        for _ in range(3):  # Retry up to 3 times
        #while True:
            try:
                # Your main code here
                #driver.get(a)
                #html_content = driver.page_source
                #soup = BeautifulSoup(html_content, 'html.parser')
                soup=page_view(a)
                paragraphs = soup.find_all('p')
                det = str(paragraphs[1])
                # More of your code...

                break  # If successful, break the loop
            except (IndexError, TimeoutException):
                print("Retrying...")
        else:
            continue
        details.append(det.split("<b>"))
        tracks = str(paragraphs[2]).split("\n")

        dets = details[0]
        nodets = list(dets[1].split("<br>"))[0]
        #new = []
        valli = nodets.split('\n')
        aname = valli[0][:-5]
        genre = re.search(r'Style: (\w+ \w+|\w+)', det)
        album_name = re.search(r'Album: (.*)', det)
        if genre:
            genre = genre.group(1)
        if album_name:
            album_name = album_name.group(1)[3:-5]
        print(aname)
        print("Genre:", genre)
        print("Album:", album_name)
        cont=False
        skip_genres = ["Soundtrack", "Reggae", "Jazz", "Hard Rock", "Blues Rock", "Art Pop","World Music", "Hip Hop",
                       "Pop Punk","Power Pop","Americana","Pop Rock"]
        #, "Country"
        skip_keywords = ["core", "metal"]

        for i in skip_genres:
            if i == genre:
                print(f"Skipping {genre} tracks...")
                cont=True
        if cont==True:
            continue

        for keyword in skip_keywords:
            if keyword.lower() in genre.lower():
                print(f"Skipping {keyword} tracks...")
                cont=True
        if cont==True:
            continue

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
        ss=0
        negatives=0
        #number=len(newtracks)-1
        sn=0

        for track in newtracks[:-1]:
            if negatives>3:
                print("Lot of negatives..Skipping...")
                break
            if "instrumental" in track.lower():
                print(f"Instrumental version; {track} (N/A)")
                #negatives+=1
                continue
            if re.search(r'\blive\b', track.lower()):
                print(f"Live version; {track} (N/A)")
                #negatives += 1
                continue
            if "remaster" in track.lower():
                print(f"Remastered version; {track} (N/A)")
                #negatives += 1
                continue
            if "extended" in track.lower():
                print(f"Extended version; {track} (N/A)")
                #negatives += 1
                continue
            if re.search(r'\bdemo\b', track.lower()):
                print("Why listen to demos?...")
                #negatives += 1
                continue
            ntrack=track[5:]
            # Create a search query for each track
            #search_query = aname + '+' + track
            afeed = aname.split(" ")
            custom=""
            for af in afeed:
                custom = custom + af + "+"
            link = ""
            if "&amp;" in ntrack:
                ntrack = ntrack.replace("&amp;", "and")
            string = ntrack.split(" ")
            for i in string:
                link = link + i + "+"
            if "," in link:
                link = link.replace(",", "")
            link = re.sub(r"[^\w']", "+", link)
            custom = re.sub(r"[^\w']", "+", custom)
            if '+and+' in custom.lower():
                custom = re.sub(r'\+and\+', '+2C%+', custom, flags=re.IGNORECASE)
            print(f'{track[:2]}) {ntrack}')
            # Extract song URL from search results

            #for _ in range(5):  # Retry up to 5 times
            #while True:
                #try:
                    #print(f"https://musicstax.com/search?q={custom}+{link}")
                    #driver.get(f"https://musicstax.com/search?q={custom}+{link}")
                    #driver.implicitly_wait(15)
                    #html_content1 = driver.page_source
                    #break  # If successful, break the loop
                #except TimeoutException:
                    #print(f"Searching Track...")
            #else:
                #continue
            soup1 = page_view2(f"https://musicstax.com/search?q={custom}+{link}")
            track_element = str(soup1.find(class_='song-image search-image'))
            if track_element == "None":
                print("not found")
                continue
            else:
                match = track_element.split('"')[5]
                track_url = "https://musicstax.com" + match
                #print(track_url)
                for _ in range(7):  # Retry up to 7 times
                #while True:
                    try:
                        #driver.get(track_url)
                        #html_content2 = driver.page_source
                        #driver.implicitly_wait(5)
                        soup2=page_view2(track_url)
                        #soup2 = BeautifulSoup(html_content2, 'html.parser')
                        site = soup2.find_all(class_='song-bar-statistic-number')
                        #print(site)
                        dance = str(site[2])
                        energy= str(site[1])
                        release_date_value = None  # Initialize the variable
                        release_date_label = soup2.find_all(class_='song-meta-item-stat')

                        if release_date_label:
                            release_date_value = release_date_label[3]

                        date = release_date_value.text if release_date_value else "None"
                        try:
                            syear = int(date[-4:])
                        except ValueError:
                            print("Unknown year")
                            syear="None"
                        break  # If successful, break the loop
                    except (TimeoutException,IndexError):
                        print("Loading track details...")
                else:
                    print("Loop exceeded..track details not found")
                    continue
            splitr = energy.split("%")[0]
            splited = dance.split("%")[0]
            siterdan = int(splited.split("\n")[1])
            siter = int(splitr.split("\n")[1])
            print("Danceability is:",siterdan)
            print("Energy is :",siter)
            if siter < 10 or siterdan <= 20:
                print("Negative")
                negatives+=1
                continue
            if (siter< 35 or siter> 96) or siterdan<34:
                continue
            global check
            if track_url not in check:
                check.update({track_url: 0})
            if check[track_url] > 3:
                print("A lot of old songs skipping..")
                return False
            necc = True #TO SKIP THE SONG THAT TOO OLD
            for _ in range(5):  # Retry up to 3 times
                try:
                    # driver.get(url)
                    # html_content2 = driver.page_source
                    # soup = BeautifulSoup(html_content2, 'html.parser')
                    soup = soup2
                    stats = {}

                    # find all stat containers
                    for stat_container in soup.find_all('div', class_='song-fact-3-stat'):
                        # find the stat title
                        title = stat_container.find('div', class_='song-bar-stat-title-text').text.strip()
                        # find the stat value
                        value = stat_container.find('div', class_='song-bar-statistic-number').text.strip()
                        # add to the dictionary
                        stats[title] = int(value[:-1])

                    facts = {}

                    # find all fact containers
                    for fact_container in soup.find_all('div', class_='song-fact-container'):
                        # find the fact title
                        title = fact_container.find('div', class_='song-fact-container-title').text.strip()
                        # find the fact value
                        value = fact_container.find('div', class_='song-fact-container-stat').text.strip()
                        # add to the dictionary
                        facts[title[:-3]] = value
                    # release_date_value = None  # Initialize the variable
                    image = None
                    # Find the div with the specific class
                    div_tag = soup.find('div', {'class': 'song-details-right__image'})

                    # Find the img tag within the div
                    img_tag = div_tag.find('img') if div_tag else None

                    # Extract the src attribute which contains the image URL
                    image = img_tag['src'] if img_tag else 'None'
                    # release_date_label = soup.find('div', attrs={'data-cy': 'meta-Release+Date-label'})
                    # if release_date_label:
                    # release_date_value = release_date_label.find_next_sibling('div')

                    # date = release_date_value.text if release_date_value else "None"
                    try:
                        syear = int(date[-4:])
                        if year - syear > 10:
                            print(f"Released before {year - 10} is not downloaded")
                            print(f"Song released in {date}")
                            necc=False
                            indval = check[track_url]
                            check.update({track_url: indval + 1})
                            break
                    except ValueError:
                        print("Unknown year")
                    print(stats)
                    print(facts)
                    break
                except TimeoutException:
                    print("Retrying...")
            if necc==False:
                continue
            criteria=song_details(stats,facts,image,aname,ntrack,directory,genre,siter,year,date)
            if criteria== False:
                try:
                    ns=((ss/sn)*10)-2
                    if ns<0:
                        ns=0
                except ZeroDivisionError:
                    ns=0
                ss+=ns
                sn+=10
                ns=round(ns)
                print("xScore:",ns)
                continue
            if criteria!=None:
                ss += criteria
                sn+=10
            hotdict.update({ntrack:siter})
            loc = f'{directory}/telegram.txt'
            tgram=[aname, album_name, a, syear, genre, loc, ntrack]
            #tasks.append(asyncio.create_task(process_track(aname, ntrack, siter,directory,track_url,siterdan,tgram)))
            process_spot_track(aname, ntrack, siter, directory, track_url, siterdan, tgram)
        try:
            org_score=float((ss/sn)*10)
            org_score=round(org_score, 2)
            print(f"Album score: {(ss/sn)*10}/10")
        except ZeroDivisionError:
            print(f"Album score: 0")
            org_score=0
        print(hotdict)
        file = open(f'{directory}/songs.txt', 'a')
        try:
            file.write(f"\n\nAlbum: {album_name}, Artist: {aname}, Album Score: {round(org_score, 1)}, link: {a} \n\n")
        except UnicodeEncodeError:
            file.write(f"\n\nName Error; Album Score: {round(org_score, 1)}, link: {a} \n\n")
        file.close()
        # Run all tasks concurrently and wait for completion
        #await asyncio.gather(*tasks)
        #driver.quit()
main()