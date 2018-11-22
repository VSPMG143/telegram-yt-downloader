#import os
import datetime

def log(msg, tag=datetime.datetime.now().isoformat()):
  with open("./logs/main.log", "a") as l:
    l.write(tag + ": " + msg + "\n")
    print(msg)
    l.close()
