from pytube import YouTube
import os
from moviepy.editor import AudioFileClip
import json
from youtubesearchpython import SearchVideos
import pytube.exceptions

def download_audio(url, output_path):
    # Download the video
    video = YouTube(url)
    # Check if the video duration is greater than 7 minutes (420 seconds)
    if video.length > 420:
        print("Skipping long video")
        return
    # Check if the video is age-restricted
    if video.age_restricted:
        print("Skipping age-restricted video")
        return
    stream = video.streams.filter(only_audio=True).order_by('abr').desc()
    output_file = stream.first().download(output_path=output_path)

    # Check the file extension
    file_extension = os.path.splitext(output_file)[1]
    audio_file = output_file.replace(file_extension, ".mp3")

    # Convert the file to mp3
    clip = AudioFileClip(output_file)
    clip.write_audiofile(audio_file, bitrate="320k")

    # Remove the original file
    os.remove(output_file)

def search_youtube(song):
    try:
        search = SearchVideos(song, offset=1, mode="json", max_results=1)
        results = search.result()
        results_dict = json.loads(results)
        if results_dict['search_result']:
            first_result = results_dict['search_result'][0]
            url = first_result['link']
            return url
    except (pytube.exceptions.RegexMatchError, TypeError):
        print("An error occurred while searching for the video.")

# Use the function
#download_audio("https://www.youtube.com/watch?v=fJ9rUzIMcZQ", "/03 Dec 23")
