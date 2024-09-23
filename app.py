from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import requests
import config

app = Flask(__name__)

# Mocked data for simplicity
tasks = []
animals = []
conversation_history = []
client = OpenAI(api_key=config.OPENAI_API_KEY)

# Route for the main dashboard
@app.route("/")
def index():
    return render_template("index.html")

# Route for weather forecast
@app.route("/weather")
def get_weather():
    weather_data = requests.get(f"http://api.weatherapi.com/v1/current.json?key={config.WEATHER_API_KEY}&q=YourLocation")
    return jsonify(weather_data.json())

# Route for fertilizer suggestion (Static)
@app.route("/fertilizer", methods=["POST"])
def suggest_fertilizer():
    field_data = request.json
    # Process the field_data and suggest fertilizer
    suggested_fertilizer = "NPK 20-20-20"
    return jsonify({"suggested_fertilizer": suggested_fertilizer})

# Route for animal tracking status
@app.route("/animal_tracking")
def animal_tracking():
    animal_status = {
        "status": "All animals healthy"
    }
    return jsonify(animal_status)

# Route to log tasks
@app.route("/log_task", methods=["POST"])
def log_task():
    task_description = request.form.get("task")
    tasks.append(task_description)
    return '', 204

# Route to handle chat for fertilizer recommendations using OpenAI
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')

    model_engine = "gpt-3.5-turbo"

    conversation_history.append({"role": "user", "content": userText})
    response = client.chat.completions.create(
        model=model_engine,
        messages=conversation_history
    )
    # Append AI response to conversation history
    ai_response = response.choices[0].message.content

    conversation_history.append({"role": "assistant", "content": ai_response})

    return ai_response

# Route to add animals
@app.route("/add_animal", methods=["POST"])
def add_animal():
    animal = request.json
    animals.append(animal)
    return jsonify({"status": "success", "animal": animal}), 200

# Route to get list of animals
@app.route("/get_animals", methods=["GET"])
def get_animals():
    return jsonify(animals)

if __name__ == "__main__":
    app.run(debug=True)
