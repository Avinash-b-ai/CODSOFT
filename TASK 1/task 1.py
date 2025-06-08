import tkinter as tk
from tkinter import scrolledtext
import re
import datetime
import random
import sqlite3

# SQLite setup
conn = sqlite3.connect('chatbot_memory.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        birth_year INTEGER
    )
''')
conn.commit()

def get_stored_name():
    cursor.execute("SELECT name FROM user_data ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    return row[0] if row else "Friend"

def save_name(name):
    cursor.execute("INSERT INTO user_data (name) VALUES (?)", (name,))
    conn.commit()

def save_birth_year(year):
    cursor.execute("UPDATE user_data SET birth_year = ? WHERE id = (SELECT MAX(id) FROM user_data)", (year,))
    conn.commit()

def get_age():
    cursor.execute("SELECT birth_year FROM user_data ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    if row and row[0]:
        return datetime.datetime.now().year - int(row[0])
    return None

user_name = get_stored_name()

# GUI App
root = tk.Tk()
root.title("Smart ChatBot - CodSoft AI Task 1")
root.geometry("500x550")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', font=('Arial', 12))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(root, font=('Arial', 14))
entry.pack(padx=10, pady=10, fill=tk.X)

def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return
    display_message(f"{user_name}: {user_input}")
    entry.delete(0, tk.END)
    respond(user_input)

def display_message(message):
    chat_area.config(state='normal')
    chat_area.insert(tk.END, message + "\n")
    chat_area.yview(tk.END)
    chat_area.config(state='disabled')

def respond(user_input):
    global user_name
    lower_input = user_input.lower()

    if lower_input in ['bye', 'exit', 'quit']:
        display_message("Chatbot: Bye! Take care.")
        root.quit()

    elif re.search(r'\bhi\b|\bhello\b|\bhey\b', lower_input):
        display_message("Chatbot: Hello there!")

    elif "your name" in lower_input:
        display_message("Chatbot: I'm your chatbot. What's your name?")

    elif re.search(r"my name is (.*)", lower_input):
        user_name = re.search(r"my name is (.*)", lower_input).group(1).capitalize()
        save_name(user_name)
        display_message(f"Chatbot: Nice to meet you, {user_name}!")

    elif "how are you" in lower_input:
        display_message("Chatbot: I'm doing well. How about you?")

    elif "date" in lower_input:
        today = datetime.date.today()
        display_message(f"Chatbot: Today's date is {today.strftime('%A, %B %d, %Y')}")

    elif "time" in lower_input:
        now = datetime.datetime.now()
        display_message(f"Chatbot: Current time is {now.strftime('%I:%M %p')}")

    elif "joke" in lower_input:
        jokes = [
            "Why don't programmers like nature? It has too many bugs.",
            "Why do Java developers wear glasses? Because they don't C#.",
            "What do you call a fake noodle? An impasta."
        ]
        display_message("Chatbot: " + random.choice(jokes))

    elif "thank" in lower_input:
        display_message("Chatbot: You're welcome!")

    elif "help" in lower_input:
        display_message("Chatbot: I can talk, tell jokes, show date/time, solve math, and remember your name.")

    elif re.search(r'\d+ [\+\-\*/] \d+', lower_input):
        try:
            result = eval(lower_input)
            display_message(f"Chatbot: The result is {result}")
        except:
            display_message("Chatbot: Sorry, something went wrong with the calculation.")

    elif "weather" in lower_input:
        display_message("Chatbot: I can't fetch real weather data, but I hope it's a great day!")

    elif "quote" in lower_input:
        quotes = [
            "Believe in yourself and all that you are.",
            "Success is not final, failure is not fatal.",
            "The best way to get started is to quit talking and begin doing."
        ]
        display_message("Chatbot: " + random.choice(quotes))

    elif "age" in lower_input:
        age = get_age()
        if age:
            display_message(f"Chatbot: You are around {age} years old.")
        else:
            display_message("Chatbot: I don't know your age. Type like: 'I was born in 2000'.")

    elif "i was born in" in lower_input:
        match = re.search(r"i was born in (\d{4})", lower_input)
        if match:
            yob = int(match.group(1))
            save_birth_year(yob)
            display_message(f"Chatbot: Got it! You're around {datetime.datetime.now().year - yob} years old.")
        else:
            display_message("Chatbot: Please tell your birth year like 'I was born in 2000'.")

    elif "i am sad" in lower_input or "feeling sad" in lower_input:
        display_message("Chatbot: I'm here for you. Things will get better. 💖")

    elif "compliment" in lower_input:
        compliments = ["You're doing great!", "You are very intelligent!", "You have a wonderful personality."]
        display_message("Chatbot: " + random.choice(compliments))

    elif "i am bored" in lower_input:
        suggestions = ["Read a book 📚", "Try learning a new skill 🧠", "Watch a movie 🎬"]
        display_message("Chatbot: Try this - " + random.choice(suggestions))

    elif "i love you" in lower_input:
        display_message("Chatbot: Thank you. I appreciate that. ❤️")

    elif "convert" in lower_input and "celsius" in lower_input:
        display_message("Chatbot: Enter like '100 c to f'")

    elif "convert" in lower_input and "fahrenheit" in lower_input:
        display_message("Chatbot: Enter like '212 f to c'")

    elif re.match(r'\d+ c to f', lower_input):
        c = int(re.match(r'(\d+)', lower_input).group())
        f = (c * 9/5) + 32
        display_message(f"Chatbot: That's {f:.1f}°F")

    elif re.match(r'\d+ f to c', lower_input):
        f = int(re.match(r'(\d+)', lower_input).group())
        c = (f - 32) * 5/9
        display_message(f"Chatbot: That's {c:.1f}°C")

    elif "fact" in lower_input:
        facts = [
            "Octopuses have three hearts.",
            "Bananas are berries, but strawberries are not.",
            "Honey never spoils."
        ]
        display_message("Chatbot: " + random.choice(facts))

    else:
        display_message("Chatbot: I didn't understand that. Could you rephrase?")

# Bind enter key to send
entry.bind("<Return>", lambda event: send_message())

send_btn = tk.Button(root, text="Send", command=send_message)
send_btn.pack(pady=5)

root.mainloop()

conn.close()
