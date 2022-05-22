from telegram import InputMediaAudio, Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import MessageHandler, filters, ApplicationBuilder, CallbackContext, CallbackQueryHandler, CommandHandler
import logging
from config import *
import spotify
import os
import glob
from pytube import YouTube
import concurrent.futures



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

LINK_MESSAGE = '''
Send link to music from Youtube
'''

WELCOME = '''Hi
This is Spotify Downloader bot!
You can use the command /start
to check it out

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

menu_delete = None
menu_message = None
sort = {}


async def downloader(update, context, link, type):
    ITEMS = spotify.album(link)
    TRACKS = []
    hrefs = []
    for song in ITEMS:
        TRACKS.append(song['name'])
        hrefs.append(song['href'])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_album, hrefs)

    await send_album(update,context,TRACKS)


async def send_album(update, context, TRACKS):
    audios = []
    counter = 0
    for track in TRACKS:
        if counter == 10:
            await context.bot.send_media_group(chat_id=update.effective_chat.id, media=audios)
            counter = 0
            audios.clear()
        try:
            audios.append(InputMediaAudio(open(f'./album/{track}.mp3', 'rb')),)
        except:
            pass
        counter = counter + 1
    await context.bot.send_media_group(chat_id=update.effective_chat.id, media=audios)

    dir = os.getcwd() + '/album'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)


def download_album(link):
    song = spotify.Song(link=link)
    song.YTLink()
    try:
        song.YTDownload(type='AL')
    except:
        pass


async def download_song(update, context, link):
    song = spotify.Song(link=link)
    try:
        song.YTDownload(type='S')
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(f'./singles/{song.trackName}.mp3', 'rb'),
                            title=song.trackName)
        # delete song after downloading from disk
        os.remove(f'./singles/{song.trackName}.mp3')
    except:
        await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                 sticker='CAACAgQAAxkBAAIFSWBF_m3GHUtZJxQzobvD_iWxYVClAAJuAgACh4hSOhXuVi2-7-xQHgQ')
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'404\n"{song.trackName}" Not Found')


async def download_link(update, context, link):
    yt = YouTube(link)
    mp3_file = yt.streams.filter(only_audio=True).first()
    out_file = mp3_file.download('./singles')
    destination = './singles/'
    new_file = out_file.title()[:-4] + '.mp3'
    os.rename(out_file, new_file)

    try:
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(f'./singles/{yt.title}.mp3', 'rb'),
                            title=yt.title)
        # delete song after downloading from disk
    except:
        await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                 sticker='CAACAgQAAxkBAAIFSWBF_m3GHUtZJxQzobvD_iWxYVClAAJuAgACh4hSOhXuVi2-7-xQHgQ')
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'404\n Not Found')



async def help(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                   sticker='CAACAgIAAxkBAAEESR9iQEBGU3XhqeNxElehxQk3-y57pAACMAADV-_qHro_3HxAn3cTIwQ')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=WELCOME)







async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton(text="single",callback_data="/single"),
            InlineKeyboardButton(text="album",callback_data="/album"),
            InlineKeyboardButton(text="link", callback_data="/link")
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)


    global menu_delete
    menu_delete = await update.message.reply_text("Please choose:", reply_markup=reply_markup)

    await Bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id,self=context.bot)






async def button(update: Update, context: CallbackContext.DEFAULT_TYPE):
    query = update.callback_query
    query.answer
    global menu_message

    if query.data == '/single':
        menu_message = await context.bot.send_message(chat_id=update.effective_chat.id, text=SINGLE_MESSAGE)
        sort[update.effective_chat.id] = 'single'
    elif query.data == '/link':
        menu_message = await context.bot.send_message(chat_id=update.effective_chat.id, text=LINK_MESSAGE)
        sort[update.effective_chat.id] = 'link'
    elif query.data == '/album':
        menu_message = await context.bot.send_message(chat_id=update.effective_chat.id, text=ALBUM_MESSAGE)
        sort[update.effective_chat.id] = 'album'





async def help(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_sticker(chat_id=update.effective_chat.id,
                             sticker='CAACAgIAAxkBAAEESR9iQEBGU3XhqeNxElehxQk3-y57pAACMAADV-_qHro_3HxAn3cTIwQ')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=WELCOME)


async def download(update: Update, context: CallbackContext):

    await Bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id, self=context.bot)
    await Bot.delete_message(chat_id=update.effective_chat.id, message_id=menu_delete.message_id, self=context.bot)
    await Bot.delete_message(chat_id=update.effective_chat.id, message_id=menu_message.message_id, self=context.bot)

    chat_id = update.effective_chat.id
    msg = update.message.text

    if chat_id in sort:
        if sort[chat_id] == 'single':
            await download_song(update, context, spotify.searchsingle(msg))
        elif sort[chat_id] == 'album':
            await downloader(update, context, spotify.searchalbum(msg), 'AL')
        elif sort[chat_id] == 'link':
            await download_link(update, context, msg)
        del sort[chat_id]
    else:
        await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                 sticker='CAACAgQAAxkBAAIBFGBLNcpfFcTLxnn5lR20ZbE2EJbrAAJRAQACEqdqA2XZDc7OSUrIHgQ')
        await context.bot.send_message(chat_id=update.effective_chat.id, text='send me a link or use the commands!')






def run():

    application = ApplicationBuilder().token(telegram_token).build()

    start_handler = CommandHandler('start', start)
    button_handler = CallbackQueryHandler(button)
    download_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), download)


    application.add_handler(start_handler)
    application.add_handler(button_handler)
    application.add_handler(download_handler)

    application.run_polling(stop_signals=None)



if __name__ == '__main__':
    run()