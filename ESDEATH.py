import os
import pyttsx3 #pip install pyttsx3
import datetime
import pyperclip
import wikipedia # pip install wikipedia
import webbrowser
import speech_recognition as sr #pip install speechRecognition
from random import choice
from RUNS.os_operaters import open_calculator, open_camera, open_cmd, open_notepad
from RUNS.es_operators import find_my_ip, get_trending_movies


#Defining browser

chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
webbrowser.get('chrome')

#Defining some important vars

USER = 'DORTROX'
BOT = 'ESDEATH'
GreetingPro = ['How can i help you today?', 'How can i assist you?']
summ = 0
from openings import opening_text

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

    speak(timing + ' ' +USER)

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
        if not 'how are you' in query or 'who are you' in query or 'who created you' in query:
            speak(choice(opening_text))
    except Exception as e:
        # print(e)
        print('Sorry, I could not understand. Could you please say that again?')
        speak('Sorry, I could not understand. Could you please say that again?')
        return "None"
    return query

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower() # 

        #logic for executing tasks based on query
        if "how are you" in query:
            speak("I'm fine sir, Glad you asked me.")

        elif "who are you" in query:
            speak("I am esdeath, a personal assistant")
        
        elif "who created you" in query:
            speak("I was created by Dortrox, for educational and for his personal uses.")
        
        elif "esdeath" in query:
            speak("At your service sir")

        elif 'wikipedia' in query:
            speak('Searching Wikipedia...please wait')
            query = query.replace("wikipedia", "")
            results =  wikipedia.summary(query, sentences = 2)
            speak("wikipedia says")
            print(results)
            speak(results)

        elif 'open notepad' in query:
            open_notepad()
            
        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
            print(f'Your IP Address is {ip_address}')

        elif "trending movies" in query:
            speak(f"Some of the trending movies are: {get_trending_movies()}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(*get_trending_movies(), sep='\n')
        
        elif'open youtube' in query:
            webbrowser.get('chrome').open("youtube.com")

        elif 'open google' in query:
            webbrowser.get('chrome').open('https://www.google.co.in/')

        elif 'open stack overflow' in query:
            webbrowser.get('chrome').open('https://stackoverflow.com/')


        elif 'play music'in query:
            music_dir = "E:\Music"
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\Baali\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'turn off' in query:
            speak("Thanks you for using esdeath Sir")
            exit()
        elif 'shutdown laptop' in query:
            speak("Hope you have a good day sir")
            speak("Shutting down your laptop")
            os.system("shutdown /s /t 1")
        elif 'close edge' in query: #DONT JUDGE MOMENT
            speak("Closing edge")
            os.system("taskkill /f /im msedge.exe")
        elif 'save file' in query:
            x = query.split("as")
            x = x[1]
            speak('Saving file as' + x)
            with open('C:/Users/dortr/OneDrive/Desktop/Python/'+ x +'.txt', 'w') as f:
                text = pyperclip.paste()
                f.write(text)
        elif 'sum of' in query:
            x = query[7:]
            x = x.split('and ')
            print(x)
            for i in x:
                i = int(i)
                summ += i
            print(summ)
            speak('It\'s ' + summ)
