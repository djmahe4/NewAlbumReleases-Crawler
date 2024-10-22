import os
import logging
import json
from telegram import Update, ForceReply, Bot
from telegram.ext import filters
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import csv


def edit_record_by_identifier(file_path, identifier, new_liked_value=1):
    """
    Edits a specific record in a text file based on the identifier column, setting the 'liked' column to 1.

    Args:
        file_path: The path to the text file.
        identifier: The value of the identifier column to search for.
        new_liked_value: The new value for the 'liked' column (default is 1).
    """

    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        #reader =file.readlines()
        table_data = list(reader)
    #print(table_data)
    identifier_index = table_data[0].index('identifier')
    #print(table_data[0])
    liked_index = table_data[0].index('liked')

    for row in table_data[1:]:
        if row[identifier_index] == identifier:
            row[liked_index] = new_liked_value
            table_data[table_data.index(row)]=row
            #print(table_data[table_data.index(row)])
            #exit(0)
            break

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerows(table_data)
def format_and_print_artist_info(spath,artist, album, album_link, released, style,location="/text.txt",song="nill"):
  """
  Formats and prints artist information in the desired format,
  including bold text, hyperlinked album name, and suitability for Telegram and text file.

  Args:
      artist: String representing the artist name.
      album: String representing the album name.
      album_link: String representing the URL of the album.
      released: String representing the album release year.
      style: String representing the album style.
  """

  # Create bold text using ANSI escape sequences (compatible with some terminals)
  gtag = "#"
  for i in list(style.split(" ")):
      gtag += i + "_"
  gtag = gtag[:-1]
  if gtag == "#R":
      gtag = "#RnB"
  telegram_text={
      "file":f"{spath}.mp3",
      "Artist":artist,
      "Album":album,
      "Released": released,
      "Style": gtag,
      "Link":album_link
  }
  #text=text.encode('utf-8').decode('utf-8')
  # Print the formatted text
  #print(text)

  # Prepare text for Telegram and text file (remove escape sequences for wider compatibility)
  #telegram_text = text.replace(bold_start, "").replace(bold_end, "")
  #telegram_text = text.encode('utf-8').decode('utf-8')

  # Append the formatted text to the specified file
  #with open(f"{location}", "a") as f:
    #f.write(telegram_text + "\n")
  with open(f"{location}","a",encoding="utf-8") as f:
      #f.write("[")
      json.dump(telegram_text, f,ensure_ascii=False)
      #f.write("]")
      f.write("\n")

# Example usage
artist = "Les Frangines"
album = "Notes"
album_link = "https://example.com/album/notes"
released = "2021"
style = "#Pop"

#format_and_print_artist_info(artist, album, album_link, released, style)

def get_song_details(folder_name):
    song_dict = {}
    try:
        with open(os.path.join(folder_name, 'telegram.txt'), 'r', encoding='cp1252') as file:
            content = list(file.readlines())
    except UnicodeDecodeError:
        with open(os.path.join(folder_name, 'telegram.txt'), 'r', encoding='utf-8') as file:
            content = list(file.readlines())

    org = []
    for i in content:
        if i != [] and i != "\n":
            org.append(i)
    #print(org)
    songs = []
    tup = []
    for x in org:
        if x[:4] == "    ":
            song_name = x[4:-1]
            # print(song_name)
            tup.append(song_name)
        elif "Artist:" in x:
            artist = x.split(":")[-1][:-1]
            # print(artist)
            tup.append(artist)
        elif "Album:" in x:
            album = x.split(":")[1][:-9]
            link = x.split(":")[-1][2:]
            tup.append(album)
            tup.append(link)
        elif "Released:" in x:
            released = x.split(":")[-1][:-1]
            tup.append(released)
        elif "Style:" in x:
            style = x.split(":")[-1][:-1]
            tup.append(style)
            songs.append(tuple(tup))
            tup = []
    # print(artist)
    # return
    # songs = re.findall(r'\n\s+(.*?)\n\nArtist:(.*?)\n\nAlbum:(.*?)\s+(https://.*?)\n\nReleased:(.*?)\n\nStyle:(.*?)\n\n+', content, re.DOTALL)
    #print(songs)
    song_files = [f for f in os.listdir(folder_name) if f.endswith('.mp3')]
    got_ =[]
    songn=[]
    song_files = [f for f in os.listdir(folder_name) if f.endswith('.mp3')]
    got_ = []
    for song in songs:
        song_name, artist, album, link, released, style = map(str.strip, song)
        song_name = re.sub(r'[^\w\s]', '', song_name)
        song_file, score = process.extractOne(f"{artist} {song_name}", song_files)
        score = score - 20 if song_name not in song_file else score
        if score > 70 or any(s.lower() in song_file.lower() for s in [song_name, artist]):
            song_dict[song_file] = {'song_name': [song_name, score],
                                    "desc": f' Artist: {artist}\n\n Album: {album}\n\n Link: {link}\n\n Released: {released}\n\n Style: {style}'.encode(
                                        "ascii", "ignore").decode()}
            got_.append(song_file)
            #file_path = 'music_data.txt'
            #identifier_to_edit = artist+song_name

            #edit_record_by_identifier(file_path, identifier_to_edit)
        else:
            print(f"Not found: {song_name}:{score}:{song_file}")

    for x in song_files:
        if x not in got_:
            print(f"Not found: {x}")
    return song_dict
