import os, pyttsx3, datetime, pyperclip, webbrowser, json, re
from os import system, name
from googlesearch import search
import speech_recognition as sr
from random import choice
from RUNS.os_operators import *
from RUNS.es_operators import *
from RUNS.math import *

#Defining Config
Obj = open('config.json')
data = json.load(Obj)
Browser = data['Browser']
Owner = data['Owner']
stack_path = data['stack_path']
music_path = data['music_path']

#Defining browser
edge_path = Browser
webbrowser.register('browcli', None,webbrowser.BackgroundBrowser(edge_path))
webbrowser.get('browcli')


#Defining some important vars
GreetingPro = ['How can i help you today?', 'How can i assist you?']

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice', voices[0].id)



def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():

    timing = 'Nill'; 
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        timing = 'Good Morning'

    elif hour>=12 and hour<18:
        timing = 'Good Afternoon'
    else:
        timing = 'Good Evening'

    speak(f"{timing} {Owner}")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

# it converts the audio input into string
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')
        print(f"User said: {query}\n")
    except Exception as e:
        # print(e)
        print('Sorry, I could not understand. Could you please say that again?')
        return "None"
    return query

if __name__ == "__main__":
    wishMe()
    while True:
        print("""
   ▄████████    ▄████████ ████████▄     ▄████████    ▄████████     ███        ▄█    █▄    
  ███    ███   ███    ███ ███   ▀███   ███    ███   ███    ███ ▀█████████▄   ███    ███   
  ███    █▀    ███    █▀  ███    ███   ███    █▀    ███    ███    ▀███▀▀██   ███    ███   
 ▄███▄▄▄       ███        ███    ███  ▄███▄▄▄       ███    ███     ███   ▀  ▄███▄▄▄▄███▄▄ 
▀▀███▀▀▀     ▀███████████ ███    ███ ▀▀███▀▀▀     ▀███████████     ███     ▀▀███▀▀▀▀███▀  
  ███    █▄           ███ ███    ███   ███    █▄    ███    ███     ███       ███    ███   
  ███    ███    ▄█    ███ ███   ▄███   ███    ███   ███    ███     ███       ███    ███   
  ██████████  ▄████████▀  ████████▀    ██████████   ███    █▀     ▄████▀     ███    █▀    
                            Dev : D O R T R O 乂\n\n                                                                        
        """)
        query = takeCommand().lower() # 

        # Client Interaction

        if "how are you" in query:
            speak("I'm fine sir, Glad you asked me.")

        elif "who are you" in query:
            speak("I am esdeath, a personal assistant")
        
        elif "who created you" in query:
            speak("I was created by Dortrox, for educational and for his personal uses.")
        
        elif "esdeath" in query:
            speak("At your service sir")

        # Search Results

        elif 'wikipedia' in query:
            x = query.split('wikipedia')
            print(x[1])
            if x[1] == " " or x[1] == "" or re.search(".*[a-zA-Z].*", x[1]):
                sentencess = 10
            else:
                sentencess = int(x[1])
            speak('Searching Wikipedia...please wait')
            results = wikipediaa(query, sentencess)
            speak(results)
            
        # Will work on it later got bored
        # elif 'search' in query:
        #     text = pyperclip.paste()
        #     for j in search(text,num=10, stop=10, pause=2):
        #         print(j)

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
            print(f'Your IP Address is {ip_address}')

        elif "trending movies" in query:
            speak(f"Some of the trending movies are: {get_trending_movies()}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(*get_trending_movies(), sep='\n')
        
        elif'open youtube' in query:
            webbrowser.get('browcli').open("youtube.com")

        elif 'open google' in query:
            webbrowser.get('browcli').open('https://www.google.co.in/')

        elif 'open stack overflow' in query:
            webbrowser.get('browcli').open('https://stackoverflow.com/')

        # Applications and system interactions

        elif 'open notepad' in query:
            open_notepad()
            
        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'open code' in query:
            codePath = "C:\\Users\\DORTROX\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'turn off' in query:
            speak("Thanks you for using esdeath Sir")
            exit()

        elif 'shutdown laptop' in query:
            speak("Hope you have a good day sir")
            speak("Shutting down your laptop")
            os.system("shutdown /s /t 1")

        elif 'close edge' in query:
            speak("Closing edge")
            os.system("taskkill /f /im msedge.exe")

        elif 'save file' in query:
            x = query.split("as")
            x = x[1]
            speak('Saving file as' + x)
            with open(f'{stack_path}{x}.txt', 'w+') as f:
                text = pyperclip.paste()
                f.write(text)

        # Entertainment

        elif 'play music'in query:
            x = query.split('play music ')
            music_dir = music_path
            songs = os.listdir(music_dir)
            print(songs)
            i = 0
            for song in songs:
                if x[1] in song.lower():
                    os.startfile(os.path.join(music_dir, song))
                    i = 1
                    break
                else:
                    pass
            if i == 0:
                speak("No song found")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

#Math functions (BASICS)

        elif 'add' in query:
            add = addition(query)
            speak(f'It\'s {add}')
            print(f'It\'s {add}')

        elif 'subtract' in query:
            subs = subtract(query)
            speak(f'It\'s {subs}')
            print(f'It\'s {subs}')

        elif 'divide' in query:
            div = subtract(query)
            speak(f'It\'s {div}')
            print(f'It\'s {div}')

        elif 'multiply' in query:
            mul = multiply(query)
            speak(f'It\'s {mul}')
            print(f'It\'s {mul}')
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')