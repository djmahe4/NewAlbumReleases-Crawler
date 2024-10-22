import datetime
import os
import re
import difflib
import json
import pickle
import time,datetime

from fuzzywuzzy import process

def get_tweet(folder_name, artist, song):
    with open(f"{folder_name}.txt", "r", encoding='utf-8') as f:
        lines = f.readlines()

    tweet = ""
    urls = []

    for index, line in enumerate(lines):
        if line.strip() == f"Song: {song}":
            if index + 1 < len(lines) and lines[index + 1].strip() == f"Artist: {artist}":
                tweet += line + "\n"
                tweet += lines[index + 1] + "\n"
                # Continue to add subsequent lines until a URL is found or the end of the file is reached
                for subsequent_line in lines[index + 2:]:
                    if "https" in subsequent_line:
                        url_pattern = r'https?://[^\s]+'
                        urls = re.findall(url_pattern, subsequent_line)
                        if urls:
                            print(urls[0])
                            break
                    tweet += subsequent_line
                break

    return tweet.strip(), urls[0] if urls else None

def get_song_details(folder_name):
    song_dict = {}
    song_files = [f for f in os.listdir(folder_name) if f.endswith('.mp3')]
    with open(os.path.join(folder_name, 'telegram.txt'), 'r', encoding='utf-8') as file:
        content = file.readlines()
        for i in content:
            data=json.loads(i)
            data=dict(data)
            print(data)
            #song_dict={}
            #if data['file'][:-4] in song_files:#.mp3 is written twice
                #song_dict[data['file'][:-4]] = {'song_name': [data['file']],
                                        #"desc": f' Artist: {data["Artist"]}\n\n Album: {data["Album"]}\n\n Link: {data["Link"]}\n\n Released: {data["Released"]}\n\n Style: {data["Style"]}'.encode(
                                            #"ascii", "ignore").decode()}
            if data['file'][:-4] in song_files:#.mp3 is written twice
                song_dict[data['file'][:-4]] = {'song_name': [data['file']],
                                        "desc": f' Artist: {data["Artist"]}\n\n Album: <a href="{data["Link"]}">{data["Album"]}</a>\n\n Released: {data["Released"]}\n\n Style: {data["Style"]}'.encode(
                                            "ascii", "ignore").decode()}
            #songs.append(song_dict)
                #get_tweet(folder_name, data["Artist"], data['file'][:-6])
    #print(song_dict)
    return song_dict


if __name__=="__main__":
    folder_name = '14 SEP 24'  # Replace with your actual folder name
    song_dict = get_song_details(folder_name)
    for song_file, song_details in song_dict.items():
        print(f'{song_file}: {song_details}\n')
    print(len(song_dict))
    #print(get_tweet(folder_name,"Bad Moves","Eviction Party"))
    #print(datetime.datetime.date(datetime.datetime.today()))

