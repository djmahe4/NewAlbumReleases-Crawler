#from pytube import YouTube #"""I guess i fixed it but not sure , currently using pytubefix"""
import csv

from pytubefix import YouTube
import os
from moviepy.editor import AudioFileClip
import json
from youtubesearchpython import SearchVideos
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
#import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np
import random
#import csv
#import pytube.exceptions as exep
import pytubefix.exceptions as exep
import re
#from twitter import *
from feed_test2 import page_view2
check={}
isFirst=True

def analyze_and_tweet_song(song_data1, song_data2, aname, sname, dir,date,image,genre,energy):
    global final_score,isFirst
    score = 0
    tweet_text = ""
    #diction={}
    try:
        if genre == "Hip Hop":  # and 'min' in song_data2["Key"]:
            if song_data1["Danceability"] < 70:
                print("No moves no hip-hop")
                return False
        if genre == "Country" or genre == "Indie Pop":  # and 'min' in song_data2["Key"]:
            if song_data1["'Acousticness'"] > 50:
                print("Highly acoustic!")
                return False
        if genre == "Indie Rock":  # and 'min' in song_data2["Key"]:
            if song_data1["Energy"] < 75 and song_data1["Positiveness"] < 65:
                print("No energy no indie")
                return False
        if "dance" in genre.lower():
            if song_data1["Danceability"] < 70 or (song_data2["tempo"]<120.0 and song_data1["Energy"] < 70):
                print("No dance moves")
                return False
        if (song_data1["Liveness"] >= 80 or song_data1["Instrumentalness"] >= 80) and song_data1["Danceability"] < 49:
            print("Track avoided due to high Liveness or Instrumentalness.")
            return False
    except KeyError:
        pass
    try:
        # Analyze song characteristics, awarding scores and composing tweet segments
        if 'Maj' in song_data2["Key"]: #and song_data1["Energy"] >= 70:
            score += 2
            tweet_text += "☀️ Uplifting key! (+2)"+ " " + song_data2["Key"] + "\n"
            if song_data1["Danceability"] >= 55:
                score += 2
                tweet_text += f"🤘 Danceable!  (+2)" + " " + str(song_data1["Danceability"]) + "%\n"  # Ready to groove!
                # diction.update({"Danceability":song_data1["Danceability"]})
            if song_data1["Energy"] >= 70:
                score += 2
                tweet_text += "⚡️ Energifying! (+2)" + " " + str(song_data1["Energy"]) + "%\n"  # High-energy vibes
                # diction.update({"Energy": song_data1["Energy"]})
            if song_data1["Positiveness"] >= 60:
                score += 2
                tweet_text += "😇 Motivational! (+2)" + " " + str(song_data1["Positiveness"]) + "%\n"  # Feel-good factor
                # diction.update({"Positiveness": song_data1["Positiveness"]})
            if float(song_data2["Tempo"][:-4]) >= 119.0:
                score += 2
                tweet_text += "️💨 Fast-paced! (+2)" + " " + song_data2["Tempo"] + "\n"  # Fast-paced beats
                # diction.update({"Tempo": song_data2["Tempo"]})
                # diction.update({"Key": song_data2["Key"]})
            if score < 10 and song_data1["Popularity"] >= 50:
                score += 2
                tweet_text += f"🌐 Popular Pick! (+2)" + " " + str(song_data1["Popularity"]) + "%\n"
            # ... (Add more analysis criteria as desired)

            # Calculate final score and format tweet, ensuring Twitter character limit
            final_score = score  # Scale to 10 points
            if (final_score <= 4 and song_data1["Energy"] < 80) and song_data1["Popularity"] < 49:
                print("Failed test.")
                return False
        elif 'min' in song_data2["Key"]:
            score = 0
            tweet_text = ""
            # Analyze song characteristics, awarding scores and composing tweet segments
            if song_data1["Danceability"] >= 50:
                score += 2
                tweet_text += f"🤘 Danceable!  (+2)" + " " + str(song_data1["Danceability"]) + "%\n"
            if song_data1["Energy"] >= 60:
                score += 2
                tweet_text += "⚡️ Energifying! (+2)" + " " + str(song_data1["Energy"]) + "%\n"
            if song_data1["Positiveness"] >= 50:
                score += 2
                tweet_text += "😇 Motivational! (+2)" + " " + str(song_data1["Positiveness"]) + "%\n"
            if float(song_data2["Tempo"][:-4]) >= 99.0:
                score += 2
                tweet_text += "️💨 Fast-paced! (+2)" + " " + song_data2["Tempo"] + "\n"
            if 'min' in song_data2["Key"]:
                score += 2
                tweet_text += "✨ Deep key! (+2)" + " " + song_data2["Key"] + "\n"
            if score < 10 and song_data1["Popularity"] >= 50:
                score += 2
                tweet_text += f"🌐 Popular Pick! (+2)" + " " + str(song_data1["Popularity"]) + "%\n"
        final_score = score  # Scale to 10 points
        if (final_score <= 4 and song_data1["Danceability"] < 69) and song_data1["Popularity"] < 49:
            print("Failed test.")
            return False
    except KeyError:
        return False
        # Calculate final score and format tweet, ensuring Twitter character limit

    #else:
        #return False
    if final_score<=4:
        tweet_text +="🔥 But its worth the vibe!!"
    # Create a dictionary
    song_dict = {
        "Song": sname,
        "Artist": aname,
        "Score": str(final_score) + "/10",
    }
    print("Score:",final_score)
        # Format the dictionary into a string
    dict_text = "\n".join([f"{k}: {v}" for k, v in song_dict.items()])
    atag="#"
    for i in list(aname.split(" ")):
        atag += i + "_"
    atag=atag[:-1]
    gtag = "#"
    for i in list(genre.split(" ")):
        gtag += i + "_"
    gtag = gtag[:-1]
    if gtag=="#R":
        gtag="#RnB"
    tweet_text = (
        dict_text
        + "\n\n"
        + tweet_text
        # dict_text
        + "\n"
        + atag
        + " "
        + gtag
        + " #music "
        + '#stats\n'
        + date
        + "\t"
        + image
        + '\n\n'
    )
    tweet_text = tweet_text.encode('utf-8').decode('utf-8')  # Encode and then decode the string
    #if len(tweet_text)>280:
        #tweet_text = tweet_text[:280]  # Truncate to Twitter character limit
    file=open(f"{dir}.txt",'a', encoding='utf-8')
    file.write(tweet_text)
    file.close()
    """new code
    with open("music_data.txt", "a") as f:
        new_dict = {"identifier": aname+sname,"genre":genre,"liked":0}
        new_dict.update(song_data1)
        #new_dict.update(song_data2)
        writer=csv.writer(f,delimiter="\t")
        if isFirst:
            writer.writerow(list(new_dict.keys()))
            isFirst=False
        writer.writerow(list(new_dict.values()))
    --"""
    return final_score
    # Post the tweet (replace placeholders with your Twitter API credentials)
    #try:
        #api = Twitter( auth=('1289071209607393281-OSGG0LcS4CWh8wzbnAuctYC5FXCuIF', 'gXX7d7g6eJMaDe6etnRYDe0CT3b6UhV2KAmqCssXUHmk7','NpoKoELqgd9TVfr7WmxoC2cHA','JeXNlHCct1Ved1IAYpBpWjNPBA6mCLyswKmNsyLaduYwkudxSP'))
        #status = api.PostUpdate(tweet_text)
        #print("Tweet posted successfully!")
    #except twitter.TwitterError as error:
        #print("Error posting tweet:", error)


def download_audio(url, output_path):
    # Download the video
    try:
        video = YouTube(url)
    except exep.RegexMatchError:
        return
    # Check if the video duration is greater than 7 minutes (420 seconds)
    if video.length > 420:
        print("Skipping long video")
        return
    # Check if the video is age-restricted
    if video.age_restricted:
        print("Skipping age-restricted video")
        return
    try:
        stream = video.streams.filter(only_audio=True).order_by('abr').desc()
    except (exep.AgeRestrictedError, exep.LiveStreamError, AttributeError):
        print("Skipping age-restricted/error video")
        return
    output_file = stream.first().download(output_path=output_path)

    # Check the file extension
    file_extension = os.path.splitext(output_file)[1]
    audio_file = output_file.replace(file_extension, ".mp3")

    # Convert the file to mp3
    clip = AudioFileClip(output_file)
    clip.write_audiofile(audio_file, bitrate="256k")

    # Remove the original file
    os.remove(output_file)
    return os.path.split(audio_file)[1]

def search_youtube(song):
    try:
        # Define the maximum length of the song title
        max_length = 10

        # If the song title is too long
        if len(song) > max_length or ('(' or '&' in song):
            # Remove the bracketed values
            song = re.sub(r"\(", "", song)
            song = re.sub(r"\)", "", song)
            song = re.sub(r"&amp; ", "", song)
            #print(song)
        song = re.sub(r"[^\w\s()–.]", "", song)
        print(f"real search: {song}")
        search = SearchVideos(song, offset=1, mode="json", max_results=1)
        results = search.result()
        results_dict = json.loads(results)
        if results_dict['search_result']:
            first_result = results_dict['search_result'][0]
            url = first_result['link']
            return url
    except (exep.RegexMatchError, TypeError, exep.AgeRestrictedError):
        print("An error occurred while searching for the video.")
        return

# Use the function
#download_audio("https://www.youtube.com/watch?v=fJ9rUzIMcZQ", "/03 Dec 23")

def song_details(stats,facts,image,aname,sname,dir,genre,energy,cyear,date):
        try:
            x=analyze_and_tweet_song(stats, facts, aname, sname,dir,date,image,genre,energy)
            if x==False and energy<80:
                return False
            return x
            #break  # If successful, break the loop
        except TimeoutException:
                print("Retrying...")

#s = Service('D:\chromedriver-win64\chromedriver-win64\chromedriver.exe')
#options = Options()
#options.add_argument("--headless")  # Disable images
#driver = webdriver.Chrome(service=s, options=options)
#driver.set_page_load_timeout(20)
#song_details(driver,"https://musicstax.com/track/city-life-remastered-2023/7B6TewKSbCY9Fifb7F6sOc",aname="xyz",sname="xyz",dir="any",genre="simple",energy=80,date="12th July 2024",cyear=2023)