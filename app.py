from flask import Flask, render_template, request
import requests
import random
from dotenv import load_dotenv
import os

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
app = Flask(__name__)

# Function to get response from OpenAI API via RapidAPI
def get_oracle_answer(question):
    url = "https://free-chatgpt-api.p.rapidapi.com/chat-completion-one"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "free-chatgpt-api.p.rapidapi.com"
    }
    querystring = {"prompt": question}  # Using question as the prompt

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        try:
            answer = response.json().get("response", "I foresee only darkness...")  # Extracting expected field
            return answer
        except:
            return "Mysterious forces prevent me from answering!"
    else:
        return "I am unable to foresee the answer right now. Try again later!"

# Function to return a funny incorrect answer
def get_funny_answer():
    funny_answers = [
        "Absolutely not!",
        "42, obviously.",
        "Ask again after you buy me a coffee.",
        "Only if the moon is in retrograde.",
        "The Oracle is on a break. Try again in 500 years.",
        "Sure, but only if pigs fly tomorrow."
    ]
    return random.choice(funny_answers)

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    question = None
    if request.method == "POST":
        question = request.form.get("question")
        if question:
            answer = get_oracle_answer(question)  # Now using API for real answers
    return render_template("index.html", question=question, answer=answer)

if __name__ == '__main__':
    app.run(debug=True)
