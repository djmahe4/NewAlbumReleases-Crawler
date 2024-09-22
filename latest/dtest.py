from spotdl import Spotdl
import os
from datetime import datetime, timezone

spotdl = Spotdl(client_id='16a580bdff3b4b6f822804fb6372712c', client_secret='7b7b8f6350bb452a880cf2a2adab3187')
today = datetime.now(timezone.utc).date()
year=int(str(today)[:4])
print(year)
exit(0)
songs = spotdl.search([
    'Bryce Dessner Lullaby for Jacques et Brune'])
file_name = "Lullaby for Jacques et Brune.mp3"
file_path = os.path.join("24 AUG 24", file_name)
#with open(file_path, "wb") as file:
    #file.write("This is the content of the new file.")
    #("Success")
#spotdl.downloader.settings.update({"save_file":file_path})
result = songs[0].url
song, fpath = spotdl.download(songs[0])
print(fpath)
os.rename(fpath, os.path.join("24 AUG 24", fpath))