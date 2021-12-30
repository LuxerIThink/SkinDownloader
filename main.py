# This is a sample Python script.

# All imported libraries

from mojang import MojangAPI
import requests
import os
from PIL import Image
from io import BytesIO
import numpy as np
import sys
import time
from queue import Queue
import threading
from itertools import islice

# Default options.txt location

def optionsLoc():
    return os.getcwd() + '\options.txt'

# Default skin folder location

def defSkinsLoc():
    return os.getcwd() + '\Skins'

# Default nicknames txt file location

def defNicknamesLoc():
    return os.getcwd() + '\\nicknames.txt'

# Default prefix location

def defPrefix():
    return 'True'

# Generate options file with default options

def genOptions(arg=[defSkinsLoc(), defNicknamesLoc(), defPrefix()]):
    with open(optionsLoc(), 'w+') as f:
        f.write('PathForSkins: ' + arg[0] + '\n' + 'PathForNicknames: ' + arg[1] + '\n' + 'AddPrefix: ' + arg[2])
    exit()
    pass

# Generate example file for nicknames and names

def genExampleNickNameFile(loc):
    with open(loc, "w+") as f:
        f.write('Notch'+'\n'+'jeb_ Jeb')

# Function return true if argument can be converted to bool

def str2bool(arg):
    if arg.lower() in ("yes", "true", "t", "1", "no", "false", "f", "0"): return True
    else: return False

# Load options if exist from options.txt and check them
# create list for user options
# read user options and copy them to list
# if there are not all option generate new options file
# create variable to decide of update options file
# if first option is not directory return to default directory
# if second options is not file check is it directory
# if is not directory return to default directory
# else create file with name created by user or default
# if third variable is not bool return to default value
# if the script has not been closed, return user options

def LoadOptions():
    if not os.path.exists(optionsLoc()): genOptions()
    else:
        out = []
        with open(optionsLoc(), 'r') as f:
            for line in f.read().splitlines(): out.append(line.split(' ',1)[1])
        if not len(out)==3: genOptions()
        change = False
        if not os.path.isdir(out[0]):
            out[0] = defSkinsLoc()
            change = True
        if not os.path.isfile(out[1]):
            if not os.path.isdir(out[1]):
                if os.path.isdir(os.path.dirname(out[1])):
                    genExampleNickNameFile(out[1])
                else:
                    out[1] = defNicknamesLoc()
                    change = True
            else:
                out[1] = out[1] + '\\nicknames.txt'
                if not os.path.isfile(out[1]):
                    genExampleNickNameFile(out[1])
                change = True
        else:
            if os.path.getsize(out[1]) == 0:
                genExampleNickNameFile(out[1])
        if not str2bool(out[2]):
            out[2] = defPrefix()
            change = True
        if change == True: genOptions(out)
        return out
    pass

# All elements locations to convert skin from 64x32 to 64x64
# first 6 lines - leg cooridnates, nex 6 lines - arm cooridnates
# [topTexture]
# [bottomTexture]
# [rightTexture -> leftTexture]
# [frontTexture]
# [leftTexture -> rightTexture]
# [backTexture]
# every 4 value packet contains:
# [xLocUpLeftCorner, yLocUpLeftCorner, xLocDownRightCorner, yLocDownRightCorner]
# values of image pixels start from 0

# Old texture coordinates (giver)

def getOldTxtCoord():
    return np.array([[ 4, 16,  8, 20],
                     [ 8, 16, 12, 20],
                     [ 0, 20,  4, 32],
                     [ 4, 20,  8, 32],
                     [ 8, 20, 12, 32],
                     [12, 20, 16, 32],
                     [44, 16, 48, 20],
                     [48, 16, 52, 20],
                     [40, 20, 44, 32],
                     [44, 20, 48, 32],
                     [48, 20, 52, 32],
                     [52, 20, 56, 32]])

# New texture coordinates (recipient)

def getNewTxtCoord():
    return np.array([[20, 48, 24, 52],
                     [24, 48, 28, 52],
                     [24, 52, 28, 64],
                     [20, 52, 24, 64],
                     [16, 52, 20, 64],
                     [28, 52, 32, 64],
                     [36, 48, 40, 52],
                     [40, 48, 44, 52],
                     [40, 52, 44, 64],
                     [36, 52, 40, 64],
                     [32, 52, 36, 64],
                     [44, 52, 48, 64]])

# Paste from giver to receiver cropped and flip horizontaly texture of element

def changeTxt(rTxt, lTxt, rLoc, lLoc):
    return rTxt.paste(lTxt.crop(rLoc).transpose(Image.FLIP_LEFT_RIGHT), lLoc)

# Convert skin from 64x32 to 64x64 (1.7- -> 1.8+)
# create new texture file
# paste old texture to new texure
# create variables for giver and recipient textures coordinates
# perform operations on textures

def OldToNew(oldSkin):
    newSkin = Image.new("RGBA", (64, 64))
    newSkin.paste(oldSkin, (0, 0, 64, 32))
    oldTxtCoord = getOldTxtCoord()
    newTxtCoord = getNewTxtCoord()
    for j in range(len(oldTxtCoord)): changeTxt(newSkin, oldSkin, tuple(oldTxtCoord[j]), tuple(newTxtCoord[j]))
    return newSkin

# Return prefix if prefix option is True

def addPrefix(prefixOption, skinType):
    if prefixOption == True:
        if (skinType == 'classic'): return '_S'
        elif (skinType == 'slim'): return '_A'
    else: return ''

# Download skin from Mojang server
# get minecraft player uuid
# if not exist pass
# get player profile
# download player skin
# if old type skin convert to new
# save skin to indicated location

def downloadSkin(loc, prefix, *nickandname):
    if len(nickandname) == 2: nickname, filename = nickandname
    else: nickname = filename = ' '.join(nickandname)
    uuid = MojangAPI.get_uuid(nickname)
    if not uuid: return
    profile = MojangAPI.get_profile(uuid)
    outSkin = Image.open(BytesIO(requests.get(profile.skin_url).content))
    if (outSkin.size[1] == 32): outSkin = OldToNew(outSkin)
    outSkin.save(loc + '/' + filename + addPrefix(prefix, profile.skin_model) + '.png')
    return

# Main branch of this script
# load options from options.txt and check them
# read lines from player names file
# create queeue
# put skin location dir, prefix option and skin name + eventually user name of player to packet for thread
# create threads
# put packet of threads and run skin dowloand function per thread
# turn off threads

def mainFunction():
    loc = LoadOptions()
    with open(loc[1], 'r') as f: lines = f.read().splitlines()
    packets = Queue()
    for i in lines:
        if not i == '': packets.put([loc[0]] + [loc[2]] + i.split())
    threads = []
    while not packets.empty(): thread = threading.Thread(target=downloadSkin, args=(packets.get())).start()
    for t in threads: t.join()

# Main

if __name__ == '__main__':
    start = time.time()
    mainFunction()
    end = time.time()
    print(end - start)
