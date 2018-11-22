import telegram
from telegram.ext import Updater, CommandHandler
import logging
import signal, sys
import convertkit
import _thread
import pytube
import os
from pytube.exceptions import RegexMatchError as LinkNotFound

"""
You have to paste your API Token here:
"""

token = "INSERT YOUR TOKEN HERE"

bot = telegram.Bot(token)
updater = Updater(token)
dispatcher = updater.dispatcher

#def startServer(a, b):
#  httpd.runWebServer()

def setup():
  print("Starting YTDL_Bot...")
  start_handler = CommandHandler('start', start)
  download_handler = CommandHandler("download", download)
  help_handler = CommandHandler("help", help)
  about_handler = CommandHandler("about", about)
  dispatcher.add_handler(start_handler)
  dispatcher.add_handler(download_handler)
  dispatcher.add_handler(help_handler)
  dispatcher.add_handler(about_handler)
  updater.start_polling()
#  _thread.start_new_thread(startServer, (None, None))

def messageParse(message):
  new = str(message).split(" ")
  new.pop(0)
  return new

#setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(bot, update):
  welcome = open("./strings/welcomestring.txt", "r")
  bot.send_message(chat_id=update.message.chat_id, text=welcome.read())

def help(bot, update):
  msg = open("./strings/help.txt", 'r')
  bot.send_message(chat_id=update.message.chat_id, text=msg.read())

def about(bot, update):
  msg = open("./strings/about.txt", "r")
  bot.send_message(chat_id=update.message.chat_id, text=msg.read())

def download(bot, update):
  _thread.start_new_thread(_download, (bot, update))

def _download(bot, update):
  #parse the message
  links = messageParse(update.message.text)
  bot.send_message(chat_id=update.message.chat_id, text="Gotchu. If possible, you'll get the file asap.")
  for i in links:
    try:
      media = convertkit.download(i)
    except LinkNotFound:
      print("Link is not a YouTube Link, abort")
      bot.send_message(chat_id=update.message.chat_id, text="Oops," + i + " is not an YouTube Link :(")
    else:
      print ("Done")
      bot.send_audio(chat_id=update.message.chat_id, audio=open(media, 'rb',))

def stopBot(a, b):
  updater.stop()
  print ("SIGINT caught")
  sys.exit(0)

#signal.signal(signal.SIGINT, stopBot)
setup()
