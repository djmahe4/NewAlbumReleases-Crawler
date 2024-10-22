from typing import final
from telegram import Update
from telegram.constants import ParseMode
import telegram.error
#from telegram import constants
from telegram import ext
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes
from debug import get_song_details
import os
import time

TOKEN: final = ""#Token of your bot using botfather
BOT_USERNAME: final = ""#Username of your bot using botfather
WATERMARK: final ="@djmahe04"
folder_name = input("Enter folder:")
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global folder_name
    songs = get_song_details(folder_name)
    print(songs)
    print(f"Found {len(songs)} number of songs.")

    # Track the song that caused the error (initialize to None)
    errored_song = None

    for filename, song_info in songs.items():
        song_path = os.path.join(folder_name, filename)
        song_info = song_info["desc"]  # Assuming description is in "desc" key

        if os.path.exists(song_path):
            message = f"<b>{song_info}\n\n{WATERMARK}</b>"

            # Define maximum retry attempts
            max_retries = 3

            for attempt in range(max_retries):
                try:
                    await update.message.reply_audio(audio=open(song_path, 'rb'), caption=message, parse_mode=ParseMode.HTML)
                    break  # Exit the loop on successful send
                except Exception as e:
                    if attempt == max_retries - 1:
                        time.sleep(5)
                        print(f"Error sending {filename} after {max_retries} retries: {e}")
                        errored_song = filename
                    else:
                        print(f"Error sending {filename}. Retrying...")

    # Handle successful completion or error after all songs
    if errored_song is None:
        print("Process Complete.")
        await update.message.reply_text("COMPLETED SUCCESSFULLY!!")
    else:
        print(f"Error sending {errored_song}. Consider retrying manually.")
        await update.message.reply_text(f"Error sending {errored_song}. Please try again later.")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'{update}, caused error {context.error}')
    await update.message.reply_text(f"ERROR: {context.error}!!")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start_command))
    app.add_error_handler(error)
    print("Polling..")
    app.run_polling(poll_interval=20)
