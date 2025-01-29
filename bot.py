import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import yt_dlp
from io import BytesIO

# Bot Token
TOKEN = '7200682052:AAEqqGkBhoQJ4_l4ukQbzSM-4AssyPRLFIA'  # Replace with your bot token
TELEGRAM_UPLOAD_LIMIT_MB = 50
TELEGRAM_UPLOAD_LIMIT_BYTES = TELEGRAM_UPLOAD_LIMIT_MB * 1024 * 1024

def download_video(url):
    """Download video and return file path."""
    try:
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': 'video.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        return None

def send_video(update, context):
    """Handles user messages containing video URLs."""
    url = update.message.text
    update.message.reply_text("Downloading video, please wait...")
    
    file_path = download_video(url)
    if file_path and os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        if file_size > TELEGRAM_UPLOAD_LIMIT_BYTES:
            update.message.reply_text("Video is too large to send via Telegram.")
        else:
            with open(file_path, 'rb') as video_file:
                update.message.reply_video(video=telegram.InputFile(video_file), caption="Here is your video!")
        os.remove(file_path)
    else:
        update.message.reply_text("Failed to download video.")

def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, send_video))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
