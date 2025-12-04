import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import wikipedia
import time
import requests
import json
import google.generativeai as genai
from newsapi import NewsApiClient

# Gemini API Setup
genai.configure(api_key="gemini_api")  # <-- Replace this!
model = genai.GenerativeModel('models/gemini-2.0-flash')

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Oops, something went wrong with Gemini."

# Initialize TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

def speak(audio):
    print("Zyra:", audio)
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("Hi, I'm Zyra. How can I help you?")

def takeCommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except Exception:
        speak("Say that again please...")
        return "None"
    return query.lower()

def search_web(query):
    speak("Searching the web...")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def get_weather(city_name):
    api_key = 'deb91b8f90b414c9e81bf84889fbe9f7'  # <-- Replace this!
    if api_key == 'YOUR_API_KEY':
        speak("Weather API key missing. Please add it.")
        return
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        speak(f"The temperature in {city_name} is {main['temp']}\u00b0C with {weather['description']}.")
    else:
        speak("City not found.")

from newsapi import NewsApiClient

def get_news():
    api_key = '42652197cda347f6adfaff52aa646589'  # your working key
    newsapi = NewsApiClient(api_key=api_key)

    try:
        headlines = newsapi.get_top_headlines(language='en')


        articles = headlines.get("articles", [])
        if not articles:
            print("No news articles found.")
            return

        print("Top News Headlines:")
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article.get('title')}")
            # speak(article.get('title'))  # optional voice integration

    except Exception as e:
        print(f"Error fetching news: {e}")



def set_alarm(alarm_time):
    speak(f"Setting alarm for {alarm_time}.")
    while datetime.datetime.now().strftime("%H:%M") != alarm_time:
        time.sleep(5)
    speak("Wake up! It's time!")

reminders = []

def add_reminder(task, time_str):
    reminders.append((task, time_str))
    speak(f"Reminder set for {task} at {time_str}")

def check_reminders():
    now = datetime.datetime.now().strftime("%H:%M")
    for task, time_str in reminders:
        if time_str == now:
            speak(f"Reminder: {task}")
            reminders.remove((task, time_str))

# Main loop
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        if "weather" in query:
            speak("Which city?")
            city = takeCommand()
            get_weather(city)

        elif "news" in query:
            get_news()

        elif "search" in query:
            search_web(query.replace("search", "").strip())

        elif "alarm" in query:
            speak("At what time should I set the alarm? (HH:MM format)")
            alarm_time = takeCommand()
            set_alarm(alarm_time)

        elif "remind me to" in query:
            try:
                task = query.split("remind me to")[1].split(" at ")[0].strip()
                time_str = query.split(" at ")[1].strip()
                add_reminder(task, time_str)
            except IndexError:
                speak("Please say it like 'remind me to take medicine at 5:30'.")

        elif "who is" in query or "what is" in query or "tell me about" in query:
            speak("Let me check that for you...")
            result = ask_gemini(query)
            speak(result.split(".")[0])

        elif "tell me a joke" in query:
            joke = ask_gemini("Tell me a short funny joke.")
            speak(joke.split(".")[0])

        elif "motivate me" in query or "inspire me" in query:
            quote = ask_gemini("Give me a motivational quote.")
            speak(quote.split(".")[0])

        elif "define" in query:
            word = query.replace("define", "").strip()
            definition = ask_gemini(f"Define the word: {word}")
            speak(definition.split(".")[0])

        elif query == "cut":
            speak("Exiting... Goodbye!")
            break

        check_reminders()
