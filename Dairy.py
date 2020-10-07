#program to new basic information about the day
#Date, time to go bed, sleep time, meeting with ...,... ok , no problem i think that everything maigth be added
#updates: aug 23 2020 - threading with audio 5 sec recording, upgrade with random_phrase and random_word.
from datetime import date
import os.path
import random
import calendar
import time
import requests
import pyaudio
import wave

import codecs
from googletrans import Translator
import threading

if os.path.isfile("./D.txt")==False:
    f = open("./D.txt", "w")
    f.close()
q = 'y'
add = True#123
f = open("D.txt")
date_str = str(date.today())
date ="Date : "+ str(date.today())

#getRandomPhrase method
def getRandomPhrase():
    random.seed(int(calendar.timegm(time.gmtime())))
    lines = []
    num = 0
    with codecs.open('remark_tri-tovarishcha.txt','r',encoding='utf-8') as f:
        for line in f:
            if line.strip():
                lines.append(line)
                num += 1

    num_tot = num
    num = random.randint(0,num)
    return str(num) + '/' + str(num_tot) + ' : ' + lines[num]
#/

#audio rec
def audio_rec(date_str):
    filename = "rec" + date_str  + ".wav"
    chunk = 1024
    FORMAT = pyaudio.paInt16
    channels = 1
    sample_rate = 44100
    record_seconds = 5
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    frames = []
    #print("Recording...")
    for i in range(int(44100 / chunk * record_seconds)):
        data = stream.read(chunk)
        # if you want to hear your voice while recording
        #stream.write(data)
        frames.append(data)
    #print("Finished recording.")
    # stop and close stream
    stream.stop_stream()
    stream.close()
    # terminate pyaudio object
    p.terminate()
    # save audio file
    counter_f = 1
    #check on dir
    if os.path.isdir('rec') == False:
        os.system('mkdir rec')
    filename = 'rec/'+ filename
    while os.path.isfile(filename): #extension missed up there
        filename = "rec/rec" + date_str + '(' + str(counter_f) + ')' + '.wav'
        counter_f += 1
    # open the file in 'write bytes' mode
    counter_f -= 1
    wf = wave.open(filename, "wb")
    # set the channels
    wf.setnchannels(channels)
    # set the sample format
    wf.setsampwidth(p.get_sample_size(FORMAT))
    # set the sample rate
    wf.setframerate(sample_rate)
    # write the frames as bytes
    wf.writeframes(b"".join(frames))
    # close the file
    wf.close()

#add thread for recording here
#/audio rec
for i in f:
    #print("cycle")
    i = i.rstrip()
    if i.startswith("Date : "):
        ii = date
        if(i == ii):
            add = False
        else:
            add = True
if add == False:
    q = input("The record for today is already in the Dairy, would u like to add one more?[enter 'y' if yes]")
    if q == "y":
        add = True
    else:
        print("exit")
        exit()
f.close()
filled_correctly = False
def get_random_word():
    try:
        url = 'https://randomword.com/'
        response = requests.get(url)
        text = response.text.split('\n')
        w = ''
        d = ''
        for i in text:
            if '"random_word"' in i:
                w = i[26:-6].strip()
            if '"random_word_definition"' in i:
                d = i[37:-6].strip()
                break
        return w,d
    except e:
        print("Error\n",e)
def getInput(type="str", message = "input information"):
    got = False
    while got != True:
        try:
            if type == "str":
                inp = input(message)
                got = True
            elif type == "int":
                inp = int(input(message))
                got = True
        except ValueError as e:
            print("ValueError " + str(e)+ "\nStart over again")
        except e:
            print(str(e))
    return inp
def get_wow_phase(s):
    o = "O"
    if(s>6):
        for i in range(s-6):
            o+="H"
    return o
#let's get all the data from the web before the program runs main loop
random_phrase = getRandomPhrase()
random_word = get_random_word()
translator = Translator()
#/
#main loop
def main_loop(f_c,f,random_phrase,random_word,translator):
    while f_c == False:
        try:
            if add == True:
                print(date)
                gobedtime = getInput(message = "So, when did u go to the bed today? ")
                if len(gobedtime) < 1:
                    print("valueError")
                    raise ValueError
                slptime = getInput(type='int', message="How many hours of sleep u had today?[int number] ")
                if(int(slptime)> 7):
                    print(get_wow_phase(int(slptime)) + " well! Have a good day)")
                else: 
                    print("OH my dear friend, u have to sleep more, u know!")
                workdone = getInput(message = "Any work u have done? ")
                tomorrowplan = getInput(message = "Any plans for tomorrow? ")
                f = open("D.txt", "a")
                f.write(date+"\n" +"Go bed time : " +gobedtime+ "\n" + "Sleep time : "+ str(slptime)+ "\n" + "Work done : " + workdone + "\n" + "Plans for tomorrow : " + tomorrowplan + "\n")
                f_c = True
                #print(date, gobedtime, slptime,workdone,tomorrowplan)
        except ValueError as e :
                print("Oh no,no,no. Plz input correct values\nStart over again\n")
                print(str(e))
                f_c = False
        except Exception as e:
                print(str(e))
                f_c = False
        finally:
                print(random_phrase+'And random word for today:\n-' + random_word[0] + '\n--' +  random_word[1] + '\n--' + translator.translate(random_word[1], dest='ru').text)
                print("Have a good life)")
                f.close()
                '''delete = input("If u want to delete original file of ur dairy enter '+' ")
                if delete == "+":
                    f = open("./D.txt", "w")
                    f.close()
                '''
                input()
#/
#main loop call
a = threading.Thread(target=main_loop, args=(filled_correctly,f,random_phrase,random_word,translator,))
b = threading.Thread(target=audio_rec, args=(date_str,), daemon=True)
a.start()
b.start()
b.join()
#/main loop threading ends
time.sleep( 10 )
