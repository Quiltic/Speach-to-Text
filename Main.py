import pyaudio, os, wave, winsound, numpy
import speech_recognition as sr
import pyautogui, time, keyboard

slow = 0
screenWidth, screenHeight = pyautogui.size()

Programing = False
Key = False
RECORD_SECONDS = 5
Minimum = 500
tally = 0
mute = -1
while True:
    try:
        os.remove('useme.wav')
    except:
        pass

    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    #RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "useme.wav"
     
    audio = pyaudio.PyAudio()
     
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    print ("Waiting...")
    frames = []

    dirp = 0
    data = stream.read(CHUNK)
    while max(numpy.fromstring(data, dtype=numpy.int16)) < Minimum:
        data = stream.read(CHUNK)

    frames.append(data)
    if mute < 0:
        winsound.Beep(1000,100)
    print ("recording...")
    
    while dirp < 50:
        data = stream.read(CHUNK)
        if max(numpy.fromstring(data, dtype=numpy.int16)) > Minimum:
            mnb = max(numpy.fromstring(data, dtype=numpy.int16))
            print(mnb)
            dirp = 0
        else:
            dirp += 1
        frames.append(data)

    print ("finished recording")
    if mute < 0:
        winsound.Beep(500,100)

    
     
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
     
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

     
    AUDIO_FILE = ("useme.wav")
     
    r = sr.Recognizer()
     
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)

    
    On = False
    try:
        d = r.recognize_google(audio)
        print("The audio file contains: " + d)
        On = True
        tally = 0

     
    except sr.UnknownValueError:
        On = False
        print("Speech Recognition could not understand audio")
        tally += 1
        if tally > 5:
            d = 'ask'
            On = True
     
    except sr.RequestError as e:
        On = False
        print("Could not request results from Speech Recognition service; {0}".format(e))
        break

    #Working stuff
    if On:
        x , y = pyautogui.position()

        #Mouse Tools
        if d == 'click':
            pyautogui.click(x,y,button = 'left')
        elif d == 'right click':
            pyautogui.click(x,y,button = 'right')
            
        elif d[:13] == "move Mouse to":
            d = d.replace('and','')
            d = d.replace(',','')
            d = d.replace('by','')
            d = [int(d[13:17]),int(d[17:])]
            print(d)
            pyautogui.moveTo(d[0], d[1], duration=.1)
        elif d[:10] == "move Mouse":
            d = d.replace('and','')
            d = d.replace(',','')
            d = d.replace('by','')
            d = [int(d[10:14]),int(d[14:])]
            print(d)
            pyautogui.moveRel(d[0], d[1], duration=.1)
        elif d[:11] == "who's Mouse":
            d = d.replace('and','')
            d = d.replace(',','')
            d = d.replace('by','')
            d = [int(d[11:15]),int(d[15:])]
            print(d)
            pyautogui.moveRel(d[0], d[1], duration=.1)
            
        elif d[:11] == "scroll down" in d:
            pyautogui.scroll(-int(d[11:])*5)
        elif d[:6] == "scroll" in d:
            pyautogui.scroll(int(d[6:])*5)
        

            
            #Key Tools
        elif (d == "copy") or (d == 'coffee'):
            pyautogui.keyDown('ctrl')
            pyautogui.press('c')
            pyautogui.keyUp('ctrl')
        elif d == "cut":
            pyautogui.keyDown('ctrl')
            pyautogui.press('x')
            pyautogui.keyUp('ctrl')
        elif (d == "paste") or (d == "haste") or (d == "taste"):
            pyautogui.keyDown('ctrl')
            pyautogui.press('v')
            pyautogui.keyUp('ctrl')
        elif (d == "undo") or (d == "fondue"):
            pyautogui.keyDown('ctrl')
            pyautogui.press('z')
            pyautogui.keyUp('ctrl')
        elif d == "redo":
            pyautogui.keyDown('ctrl')
            pyautogui.keyDown('shift')
            pyautogui.press('z')
            pyautogui.keyUp('shift')
            pyautogui.keyUp('ctrl')
        elif d == "save":
            pyautogui.keyDown('ctrl')
            pyautogui.press('s')
            pyautogui.keyUp('ctrl')
        elif d == "run":
            pyautogui.keyDown('ctrl')
            pyautogui.press('s')
            pyautogui.keyUp('ctrl')
            pyautogui.press('f5')
        elif (d == "return") or (d == "turn"):
            pyautogui.press('enter')
        elif d == "tab":
            pyautogui.press('tab')
        elif d[:6] == "delete":
            while "delete" in d:
                pyautogui.press('backspace')
                d = d.replace('delete','')
        elif d == "quit":
            quit()
        elif d == "ask":
            input('Hit enter to continue.')
        elif d == "mute":
            mute = mute*-1
        elif d == "game":
            print('On')
            on = False
            while True:
                try:
                    
                    #used try so that if user pressed other than the given key error
                    #will not be shown
                    if (keyboard.read_key() == 'shift'):#keyboard.is_pressed('shift'):
                        #if key 'shift' is pressed
                        on = True
                        print('You Pressed A Key!')
                        pyautogui.keyDown('alt')
                        pyautogui.keyDown('w')
                    elif (keyboard.read_key() == 'q'):
                        pyautogui.keyUp('alt')
                        pyautogui.keyUp('w')
                        break
                    elif (keyboard.read_key() != 'shift'):
                        if on == True:
                            pyautogui.keyUp('alt')
                            if (keyboard.read_key() != 'w'):
                                pyautogui.keyUp('w')
                            on = False
                    
                    else:
                        pass
                except:
                    #if user pressed other than the given key the loop will break
                    pyautogui.keyUp('alt')
                    pyautogui.keyUp('w')
            print('Off')



            #Typing
        elif d == "keyboard":
            if Key:
                print("Keybord Off.")
                Key = False
            else:
                print("Keybord On.")
                Key = True
        elif Key:
            d = d #' '+d
            pyautogui.typewrite(d, interval = 0.05)
            #Key = Key*-1
            if Programing:
                Programing = False
        
            
        elif d[:4] == "type" in d:
            pyautogui.typewrite(d[4:], interval=0.1)

        elif d == "programming":
            if Programing:
                print("Programming Off.")
                Programing = False
            else:
                print("Programming On.")
                Programing = True
            
        elif Programing:
            commands = [['length','len(',')'],['range', 'range(',')'],['for','for ',':'],['print','print(',')'],['if','if ',':'],['else if','elif ',':'],['else','else',':']]
            for a in commands:
                if a[0] in d:
                    d = d[:d.index(a[0])]+a[1]+d[d.index(a[0])+len(a[0])+1:]+a[2]
                    print(d)
                    print(a[0])

            info = [[' times ','*'],[' divided by ','/'],[' plus ','+'],[' minus ','-'],[' end cube bracket ',']'],[' cube bracket ','['],[' end round bracket ',')'],[' and round bracket ',')'],[' round bracket ','('],['true','True'],['false','False'],[' equals ','='],[' dots',':']]
            for a in info:
                d = d.replace(a[0],a[1])
            pyautogui.typewrite(d)
            if Key:
                Key = False
        
            #Utility
        elif "sleep" in d:
            d = d.replace('sleep','')
            d = d.replace(' ','')
            print('Sleeping...')
            time.sleep(int(d))
        elif "record " in d:
            d = d.replace('record','')
            d = d.replace(' ','')
            print('Recording time set to: '+d)
            RECORD_SECONDS =  int(d)
        elif "minimum " in d:
            d = d.replace('minimum','')
            d = d.replace(' ','')
            print('Recording minimum set to: '+d)
            Minimum =  int(d)

            #Other tools
        elif "Google " in d:
            d = d.replace('Google','')
            #d = d.replace(' ','')
            print('Googleing: '+d)
            os.startfile('https://www.google.com/webhp')
            time.sleep(2)
            pyautogui.typewrite(d, interval=0.1)
            pyautogui.press('enter')
        elif 'help' in d:
            print('Command list: Copy,Cut,Paste,Undo,Redo,Save,Run,Return,Tab,Delete,Quit,Ask,Mute,Game,Keyboard,Type,Programing,Sleep,Record,Minimum,Google,and Help.')
            


            

        winsound.Beep(200,100)
