from pytube import YouTube
import os
from moviepy.editor import AudioFileClip
import json
from youtubesearchpython import SearchVideos

def download_audio(url, output_path):
    # Download the video
    video = YouTube(url)

    # Check if the video is age-restricted
    if video.age_restricted:
        print("Skipping age-restricted video")
        return
    stream = video.streams.filter(only_audio=True).first()
    output_file = stream.download(output_path=output_path)

    # Convert the file to mp3
    clip = AudioFileClip(output_file)
    clip.write_audiofile(output_file.replace(".mp4", ".mp3"),bitrate="320k")

    # Remove the original file
    os.remove(output_file)

def search_youtube(song):
    search = SearchVideos(song, offset = 1, mode = "json", max_results = 1)
    results = search.result()
    results_dict = json.loads(results)
    if results_dict['search_result']:
        first_result = results_dict['search_result'][0]
        url = first_result['link']
        return url
    else:
        return "No results found."

# Use the function
#download_audio("https://www.youtube.com/watch?v=fJ9rUzIMcZQ", "/path/to/output/directory")
