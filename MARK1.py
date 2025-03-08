import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import requests
from newsapi import NewsApiClient
import pycountry
import time
import sched
import pandas as pd
import random
import wolframalpha
import pyautogui
import ctypes

netflix_df = pd.read_csv("Location dataset",encoding='latin1')


reminders = {}
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
scheduler = sched.scheduler(time.time, time.sleep)
wolfram_app_id = 'XHRLEV-KHW7GP7LUG'
client = wolframalpha.Client(wolfram_app_id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Sir")

    elif 12 <= hour < 18:
        speak("Good Afternoon Sir")

    else:
        speak("Good Evening Sir")
   
    speak("I am Jarvis.")
    

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        if "cut" in query:
            return "cut"

    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def get_news(category, country):
    newsapi = NewsApiClient(api_key='YOUR API_KEY HERE')
    countries = {country.name: country.alpha_2 for country in pycountry.countries}
    country_code = countries.get(country.title(), 'Unknown code')
    top_headlines = newsapi.get_top_headlines(category=category.lower(), language='en', country=country_code.lower())
    headlines = top_headlines['articles']
    if headlines:
        for article in headlines:
            print(article['title'])
            speak(article['title'])
    else:
        print(f"No articles found for {country} in the {category} category.")

def open_video():
    speak("Sure, what video would you like me to open?")
    video_name = takeCommand().lower()
    speak(f"Searching for {video_name} video on YouTube...")
    search_query = '+'.join(video_name.split())
    search_url = f"https://www.youtube.com/results?search_query={search_query}"
    webbrowser.open(search_url)

def get_weather(city_name):
    api_key = 'YOUR API_KEY HERE'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    if data['cod'] == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        return f"The weather in {city_name} is {weather_description}. Temperature: {temperature}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s."
    else:
        return "Sorry, I couldn't retrieve the weather information."
import requests

def get_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    joke_data = response.json()
    if "setup" in joke_data and "punchline" in joke_data:
        setup = joke_data["setup"]
        punchline = joke_data["punchline"]
        return f"{setup} ... {punchline}"
    else:
        return "Sorry, I couldn't fetch a joke at the moment."


def get_movie_info(movie_title):

    movie_title = movie_title.lower()

    movie_data = netflix_df[netflix_df['title'].str.lower() == movie_title]
    
    if not movie_data.empty:
  
        title = movie_data.iloc[0]['title']
        director = movie_data.iloc[0]['director']
        cast = movie_data.iloc[0]['cast']
        rating = movie_data.iloc[0]['rating']
        description = movie_data.iloc[0]['description']

        response = f"Title: {title}\nDirector: {director}\nCast: {cast}\nRating: {rating}\nDescription: {description}"
    else:
        response = "Sorry, the movie you requested was not found."
    
    return response





def set_alarm(alarm_time):
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            speak("Alarm! It's time to wake up!")
            break
        time.sleep(30)
def reminder_task(reminder_text, reminder_time):
   
    current_time = time.time()

    delay = reminder_time - current_time

    scheduler.enter(delay, 1, speak, kwargs={'audio': reminder_text})

def schedule_reminder(reminder_text, year, month, day, hour, minute):
   
    reminder_time = datetime.datetime(year, month, day, hour, minute).timestamp()

    reminder_task(reminder_text, reminder_time)


def get_exchange_rate(base_currency, target_currency):
    api_key = 'YOUR API_KEY HERE'
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency.upper()}/{target_currency.upper()}'

    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()

        if data['result'] == 'success':
            conversion_rate = data['conversion_rate']
            return f"The exchange rate from {base_currency.upper()} to {target_currency.upper()} is {conversion_rate}."
        else:
            print("Error:", data.get('error', 'Unknown error'))
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
def get_motivational_quote():
    url = "https://type.fit/api/quotes"
    response = requests.get(url)
    quotes = response.json()
    random_quote = random.choice(quotes)
    quote_text = random_quote.get("text", "Keep pushing forward!")
    quote_author = random_quote.get("author", "Unknown")
    return f"Here's a motivational quote: {quote_text} - {quote_author}"
def get_random_fact():
    url = "http://numbersapi.com/random/trivia"
    try:
        response = requests.get(url)
        fact = response.text
        return fact
    except requests.exceptions.RequestException as e:
        print(f"Error fetching random fact: {e}")
        return None
def get_trivia_question():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    try:
        response = requests.get(url)
        data = response.json()
        if data['response_code'] == 0:
            question_data = data['results'][0]
            question = question_data['question']
            correct_answer = question_data['correct_answer']
            incorrect_answers = question_data['incorrect_answers']
            all_answers = incorrect_answers + [correct_answer]
            random.shuffle(all_answers)
            return question, correct_answer, all_answers
        else:
            return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trivia question: {e}")
        return None, None, None
def fetch_topic_information(subject, topic):
    try:
        search_query = f"{subject} {topic}"
        res = client.query(search_query)
        answer = next(res.results).text
        return answer
    except Exception as e:
        return "Sorry, I couldn't retrieve the information at the moment."


def fetch_topic_information(subject, topic):
    try:
        result = wikipedia.summary(f"{subject} {topic}", sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return "There are multiple results for your query. Please be more specific."
    except wikipedia.exceptions.PageError:
        return "No results found for your query."

def learning_mode():
    speak("Welcome to learning mode. Please tell me the subject.")
    subject = takeCommand().lower()
    if subject == "none":
        speak("Sorry, I didn't get that. Please try again.")
        return

    speak(f"You chose {subject}. Now, please tell me the topic you want to learn about.")
    topic = takeCommand().lower()
    if topic == "none":
        speak("Sorry, I didn't get that. Please try again.")
        return

    speak(f"Searching for information about {topic} in {subject}.")
    information = fetch_topic_information(subject, topic)
    print(information)
    speak(information)
def calculate(expression):
    try:
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return "Sorry, I couldn't calculate that."

def handle_calculator_command():
    speak("Please tell me the calculation you would like to perform.")
    expression = takeCommand()
    expression = expression.replace('x', '*').replace('X', '*')
    
    if expression:
        result = calculate(expression)
        print(result)
        speak(result)
    else:
        speak("I didn't catch that. Please try again.")
import requests

def get_word_definition(word):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            definitions = data[0]['meanings']
            definition_str = f"Word: {word}\n"
            for meaning in definitions:
                part_of_speech = meaning['partOfSpeech']
                definition_str += f"Part of Speech: {part_of_speech}\n"
                for definition in meaning['definitions']:
                    definition_str += f"Definition: {definition['definition']}\n"
                    if 'example' in definition:
                        definition_str += f"Example: {definition['example']}\n"
                    definition_str += '\n'
            return definition_str
        else:
            return "Sorry, no definitions found for that word."
    else:
        return "Sorry, I couldn't find the definition for that word."

def handle_dictionary_command():
    speak("Please tell me the word you want to look up.")
    word = takeCommand().lower()
    if word != "none":
        result = get_word_definition(word)
        print(result)
        speak(result)
    else:
        speak("I didn't catch that. Please try again.")


def take_snapshot():
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save('screenshot.png')  
        return screenshot
    
    except Exception as e:
        print(f"Error while taking screenshot: {e}")
        return None
def handle_command(command):
    if "take snapshot" in command:
        speak("Taking snapshot...")
        snapshot = take_snapshot()
        if snapshot:
            speak("Snapshot taken successfully.")
        else:
            speak("Sorry, there was an error taking the snapshot.")
    elif "other_command" in command:
        # Handle other commands
        pass
    else:
        speak("Command not recognized. Please try again.")
def sleep_computer():
    speak("Putting the computer to sleep.")
    ctypes.windll.powrprof.SetSuspendState(0, 1, 0)

def shutdown_computer():
    speak("Shutting down the computer.")
    os.system("shutdown /s /f /t 0")

def handle_system_command(command):
    if 'sleep' in command:
        sleep_computer()
    elif 'shutdown' in command:
        shutdown_computer()
    else:
        speak("Sorry, I didn't understand the command.")







if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        if query == "cut":
            speak("Exiting...")
            break
        elif 'sleep' in query:
           handle_system_command('sleep')
        elif 'shutdown' in query:
           handle_system_command('shutdown')
        elif 'open' in query:
           handle_system_command(f'open {query.split("open", 1)[1].strip()}')

        elif "calculate" in query or "calculator" in query:
            handle_calculator_command()
        elif "define" in query or "dictionary" in query:
            handle_dictionary_command()
        # elif "snap shot" in query or "snapshot" in query:
        #     handle_command()

        if "movie" in query or "TV show" in query:
            speak("Sure, which movie or TV show are you interested in?")
            title_query = takeCommand()
            title = title_query.replace("movie", "").replace("TV show", "").strip()
            movie_info = get_movie_info(title)
            print(movie_info)
            speak(movie_info)
        elif "ask me a trivia question" in query or "ask me a question" in query:
            question, correct_answer, all_answers = get_trivia_question()
            if question:
                speak("Here's a trivia question for you:")
                speak(question)
                print(question)
                for i, answer in enumerate(all_answers):
                    speak(f"Option {i + 1}: {answer}")
                    print(f"Option {i + 1}: {answer}")
                speak("Please say the number of your answer.")
                
                user_answer = takeCommand().lower()
                try:
                    user_answer_index = int(user_answer.split()[-1]) - 1
                    if all_answers[user_answer_index] == correct_answer:
                        speak("That's correct! Well done.")
                    else:
                        speak(f"Sorry, the correct answer was {correct_answer}.")
                except (ValueError, IndexError):
                    speak("I didn't understand your answer. Please try again.")
            else:
                speak("Sorry, I couldn't fetch a trivia question at the moment.")



        if "how are you" in query:
            speak("I'm fine sir, how can i help you ?")
        elif "tell me a fact" in query or "interesting fact" in query:
            fact = get_random_fact()
            if fact:
                speak("Here's an interesting fact for you:")
                speak(fact)
                print(fact)
            else:
                speak("Sorry, I couldn't fetch a random fact at the moment.")



        elif "who are you" in query:
            speak("Sir I am Jarvis personal assistant ")

        elif "open youtube" in query:
            speak("Opening youtube Boss")
            print("Opening YouTube.......")
            webbrowser.open("https://www.youtube.com/")
        elif "learning mode" in query:
            learning_mode()

        elif "open video" in query:
            open_video()

        elif 'news' in query:
            speak("Sure, which category of news are you interested in?")
            category = takeCommand().lower()
            speak("And from which country?")
            country = takeCommand().lower()
            get_news(category, country)
        elif "motivate me" in query:
            quote = get_motivational_quote()
            print(quote)
            speak(quote)

        elif "tell me a joke" in query:
            joke = get_joke()
            print(joke)
            speak(joke)
        if "set alarm" in query:
            speak("At what time would you like to set the alarm?")
            alarm_time = input("Enter the time (in HH:MM format): ")
            speak(f"Alarm set for {alarm_time}")
            set_alarm(alarm_time)


        elif "open spotify" in query:
            speak("Opening Spotify , enjoy your music Boss....")
            print("Opening Spotify.......")
            webbrowser.open("https://open.spotify.com/")
        elif("wikipedia" in query) or ("information" in query) or ("details" in query):
            speak('According to wikipedia')
            query = query.replace("wikipedia", "")
            results =  wikipedia.summary(query, sentences = 3)
            print(results)
            speak(results)
            speak("Would you like to read more about this topic?")
        elif "exchange rate" in query:
            speak("Please specify the base currency.")
            base_currency = takeCommand().upper()
            speak("Please specify the target currency.")
            target_currency = takeCommand().upper()
            exchange_rate = get_exchange_rate(base_currency, target_currency)

            if exchange_rate:
                speak(exchange_rate)
                print(exchange_rate)
            else:
                speak("Failed to retrieve the exchange rate.")
                print("Failed to retrieve the exchange rate.")
            
        user_response = takeCommand().lower()
        
        if 'yes' in user_response:
            page_url = wikipedia.page(query).url
            speak("Sure! Here is the Wikipedia page for further information:")
            print("Wikipedia page:", page_url)
            webbrowser.open(page_url)

        elif 'reminder' in query:
            speak("What would you like to be reminded of?")
            reminder_text = takeCommand()
            speak("When would you like to be reminded? Please specify the time.")
            speak("For example, you can say 'Remind me at 3:30 PM'.")
            reminder_time = takeCommand()
            try:
                reminder_time = datetime.datetime.strptime(reminder_time, '%I:%M %p')
            except ValueError:
                speak("Invalid time format. Please try again.")
                continue
            schedule_reminder(reminder_text, datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, reminder_time.hour, reminder_time.minute)
        
        elif "open chat gpt" in query:
            speak("Opening Chat G P T Boss..")
            print("Opening Chat GPT.......")
            webbrowser.open("https://chat.openai.com/")
        

        elif "open google" in query:
            speak("Opening Google Boss..")
            print("Opening Google.......")
            webbrowser.open('https://www.google.co.in/')
        elif ("weather" in query) or ("temperature" in query):
            speak("Sure, which city's weather would you like to know?")
            city_name = takeCommand().lower()
            print("the weather in requested locality is:",city_name)
            weather_info = get_weather(city_name)
            print(weather_info)
            speak(weather_info)
            speak("Have a good day sir")
            


        elif "coding videos" in query:
            speak("Suggesting you some programming youtube channels, Boss.....")
            print("Suggested videos for you, boss.......")
            webbrowser.open("https://www.youtube.com/@CodeWithHarry")
            webbrowser.open("https://www.youtube.com/@ApnaCollegeOfficial")
            webbrowser.open("https://www.youtube.com/@edurekaIN")
            webbrowser.open("https://www.youtube.com/@JennyslecturesCSIT")
            webbrowser.open("https://www.youtube.com/@LukeBarousse")

        elif "play music" in query:
            music_file = "C:/Users/Aryan/Music/SawanoHiroyuki_nZk_XAI_-_DARK_ARIA_LV2_(Hydr0.org).mp3"
            os.startfile(music_file)

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
       

        elif ("goodbye" in query) or ("get lost" in query) or ("bye" in query) or ("shut down" in query):
            speak("Thanks for using me boss, have a good day")
            exit()