from telegram import Update, InputMediaAudio
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
import spotify
import os
import glob
from pytube import YouTube
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


def downloader(update, context, link, type):
    ITEMS = spotify.album(link)
    MESSAGE = ""
    # COUNT = 0
    # for song in ITEMS:
    #     # if type == 'PL':
    #     #     song = song['track']
    #     COUNT += 1
    #     MESSAGE += f"{COUNT}. {song['name']}\n"
    # context.bot.send_message(chat_id=update.effective_chat.id, text=MESSAGE)
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
            counter = 0
        try:
            audios.append(InputMediaAudio(open(f'./album/{track}.mp3','rb')))
        except:
            pass
        counter = counter + 1

    dir = os.getcwd() + '/album'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)
   

def download_album(update,context, link):
    song = spotify.Song(link=link)
    song.YTLink()
    try:
        song.YTDownload(type='AL')
    except:
        pass


def download_song(update, context, link):
    song = spotify.Song(link=link)
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


def download_link(update,context,link):
    yt = YouTube(link)
    mp3_file = yt.streams.filter(only_audio=True).first()
    out_file = mp3_file.download('./singles')
    destination = './singles/'

    new_file = os.getcwd() + destination + yt.title + '.mp3'
    os.rename(out_file, new_file)

    try:
        caption = f'Track: {yt.title}'
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(f'./singles/{yt.title}.mp3', 'rb'),
                               caption=caption, title=yt.title)
        # delete song after downloading from disk
        os.remove(f'./singles/{yt.title}.mp3')
    except:
        context.bot.send_sticker(chat_id=update.effective_chat.id,
                                 sticker='CAACAgQAAxkBAAIFSWBF_m3GHUtZJxQzobvD_iWxYVClAAJuAgACh4hSOhXuVi2-7-xQHgQ')
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'404\n Not Found')





def start(update: Update, context: CallbackContext):
    context.bot.send_sticker(chat_id=update.effective_chat.id,
                             sticker='CAACAgIAAxkBAAEESR9iQEBGU3XhqeNxElehxQk3-y57pAACMAADV-_qHro_3HxAn3cTIwQ')
    context.bot.send_message(chat_id=update.effective_chat.id, text=WELCOME)
def single(update: Update, context: CallbackContext):
    sort[update.effective_chat.id] = 'single'
def album(update: Update, context: CallbackContext):
    sort[update.effective_chat.id] = 'album'
def link(update: Update, context: CallbackContext):
    sort[update.effective_chat.id] = 'link'



def download(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = update.message.text

    if chat_id in sort:
        if sort[chat_id] == 'single':
            download_song(update, context, spotify.searchsingle(msg))
        elif sort[chat_id] == 'album':
            downloader(update, context, spotify.searchalbum(msg), 'AL')
        elif sort[chat_id] == 'link':
            download_link(update, context, msg)
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
    link_handler = CommandHandler('link', link)
    album_handler = CommandHandler('album', album)
    download_handler = MessageHandler(Filters.text & (~Filters.command), download)


    dispatcher.add_handler(link_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(single_handler)
    dispatcher.add_handler(album_handler)
    dispatcher.add_handler(download_handler)


    print('[TELEGRAM BOT] Listening...')


if __name__ == '__main__':
    run()