import os
from pytube import YouTube
from datetime import datetime
# import subprocess
from subprocess import Popen, PIPE, STDOUT
from mp3_tagger import MP3File, VERSION_2, VERSION_1, VERSION_BOTH
from log2file import log as main_log

sample_link = 'https://www.youtube.com/watch?v=JGtz7jdgBqs'

stamp = None
def cleanup(file):
  os.remove(file)

def writeTags(name, out):
  #print name
  main_log(name)
  path = os.getcwd() + "/" + out
  #print path
  main_log(path)
  mp3 = MP3File(path)

  new = str(os.path.basename(str(name).split(".")[0]))
  main_log(new)
  mp3.song = new
  mp3.artist = "Converted by ytdl telegram bot"
  mp3.save()

def convert(a, b):
  #timestamp (might use this for converted mp3 file)
  #print path
  timestamp = str(datetime.now()).replace(" ", "_")
  #print os.path.basename(b.name)

  if not os.path.isdir("./logs/" + os.path.basename(b.name)):
    os.makedirs("./logs/" + os.path.basename(b.name))

  out = "out/" + timestamp + ".mp3"
  logpath = "logs/" + os.path.basename(b.name) + "/" +  timestamp
  global stamp
  stamp = out
  #downloaded file name
  #path = str(b).split("'")[1]
  path = b.name
  #print "Converting..."

  main_log("[b]: " + b.name)
  main_log("[path]: " + path)
  main_log("[out]: " + out)


  cmd = ["ffmpeg",
	"-y",
	"-i",
	path,
	"-f",
	"mp3",
	"-ab",
	"320000",
	"-vn",
	out]
  log = open(logpath, 'w')
  p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
  log.write(str(p.stdout.read()))
  log.close()
  writeTags(path, out)
  cleanup(path)

def download(link):
  print('Querying: ' + link)
  youtube = YouTube(link)
  youtube.register_on_complete_callback(convert)
  yt = youtube.streams.first().download()
  return stamp
