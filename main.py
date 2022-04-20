from telegram import Update, InputMediaAudio
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
import spotify
import os
import glob

from pathlib import Path

WELCOME = '''Hi
This is Spotify Downloader!
You can use the command.
/album
/artist
/single
/help
'''
SINGLE_MESSAGE = '''send name and name of artist like this:
Name song
or for better search use this:
Name song - Name artist
'''

ALBUM_MESSAGE = '''send name and name of artist like this: 
Name album
or for better search use this:
Name album - Name artist
'''

sort = {}
telegram_token = '5130499370:AAEymk_-luU_awA5EhfQvkDue7CluiiLVrU'

def text_finder(txt):
    a = txt.find("https://open.spotify.com")
    print(txt)
    print(a)
    txt = txt[a:]
    return txt

def downloader(update, context, link, type):
    if type == 'AL':
        ITEMS = spotify.album(link)
    else:
        ITEMS = []
    print(ITEMS)
    MESSAGE = ""
    COUNT = 0
    for song in ITEMS:
        # if type == 'PL':
        #     song = song['track']
        COUNT += 1
        MESSAGE += f"{COUNT}. {song['name']}\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=MESSAGE)
    TRACKS = []
    for song in ITEMS:
        # if type == 'PL':
        #     song = song['track']
        TRACKS.append(song['name'])
        download_album(update, context, song['href'])
    send_album(update,context,TRACKS)


def send_album(update,context,TRACKS):
    audios = []
    counter = 1
    for track in TRACKS:
        if counter == 10:
            context.bot.send_media_group(chat_id=update.effective_chat.id, media=audios)
            audios.clear()
        try:
            audios.append(InputMediaAudio(open(f'./album/{track}.mp3','rb')))
        except:
            pass
        counter = counter + 1

    #
    # files = glob.glob('./album/')
    # for f in files:
    #     os.remove(f)





def download_album(update,context, link):
    song = spotify.Song(link=link)
    song.YTLink()
    try:
        song.YTDownload(type='AL')
    except:
        pass


def download_song(update, context, link):
    song = spotify.Song(link=link)
    song.YTLink()
    try:
        song.YTDownload(type='S')
        caption = f'Track: {song.trackName}\nAlbum: {song.album}\nArtist: {song.artist}'
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(f'./singles/{song.trackName}.mp3', 'rb'),
                               caption=caption, title=song.trackName)
        # delete song after downloading from disk
        os.remove(f'./singles/{song.trackName}.mp3')
    except:

        context.bot.send_sticker(chat_id=update.effective_chat.id,
                                 sticker='CAACAgQAAxkBAAIFSWBF_m3GHUtZJxQzobvD_iWxYVClAAJuAgACh4hSOhXuVi2-7-xQHgQ')
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'404\n"{song.trackName}" Not Found')






def start(update: Update, context: CallbackContext):
    context.bot.send_sticker(chat_id=update.effective_chat.id,
                             sticker='CAACAgIAAxkBAAEESR9iQEBGU3XhqeNxElehxQk3-y57pAACMAADV-_qHro_3HxAn3cTIwQ')
    context.bot.send_message(chat_id=update.effective_chat.id, text=WELCOME)

def single(update: Update, context: CallbackContext):
    context.bot.send_sticker(chat_id=update.effective_chat.id,
                             sticker='CAACAgIAAxkBAAEESRtiQD8GEjXrD6qQE-qYl47vCLZV9AACIwADV-_qHsBFO7KbfFG7IwQ')
    context.bot.send_message(chat_id=update.effective_chat.id, text=SINGLE_MESSAGE)
    sort[update.effective_chat.id] = 'single'

def album(update: Update, context: CallbackContext):
    # download_album(update, context)
    sort[update.effective_chat.id] = 'album'




def download(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = update.message.text
    msglink = text_finder(msg)

    if chat_id in sort:
        if sort[chat_id] == 'single':
            download_song(update, context, spotify.searchsingle(msg))
        elif sort[chat_id] == 'album':
            downloader(update, context, spotify.searchalbum(msg), 'AL')
        del sort[chat_id]
    else:
        context.bot.send_sticker(chat_id=update.effective_chat.id,
                                 sticker='CAACAgQAAxkBAAIBFGBLNcpfFcTLxnn5lR20ZbE2EJbrAAJRAQACEqdqA2XZDc7OSUrIHgQ')
        context.bot.send_message(chat_id=update.effective_chat.id, text='send me a link or use the commands!')


def run():
    updater = Updater(token=telegram_token, use_context=True)
    updater.start_polling()
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    single_handler = CommandHandler('single', single)
    album_handler = CommandHandler('album', album)


    download1_handler = MessageHandler(Filters.text & (~Filters.command), download)


    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(single_handler)
    dispatcher.add_handler(album_handler)
    dispatcher.add_handler(download1_handler)


    print('[TELEGRAM BOT] Listening...')


if __name__ == '__main__':
    run()