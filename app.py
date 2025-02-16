from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = '72c95f9b04b7726c6cc2115087b3f86f'  # Replace with your actual API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        if not city:
            return render_template('index.html', message="Please enter a valid city name.")

        complete_url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
        response = requests.get(complete_url)
        data = response.json()

        if data.get('cod') != 200:
            message = data.get('message', "City not found or API issue!")
            return render_template('index.html', message=message)

        weather = data.get('main', {})
        temperature = weather.get('temp', "N/A")
        humidity = weather.get('humidity', "N/A")
        wind_speed = data.get('wind', {}).get('speed', "N/A")
        description = data.get('weather', [{}])[0].get('description', "N/A")

        # Simple farming advice
        advice = "Weather is favorable for farming today."
        if temperature != "N/A" and temperature > 30:
            advice = "High temperatures detected, consider irrigating your crops."
        elif humidity != "N/A" and humidity > 80:
            advice = "High humidity, watch out for fungal diseases."

        return render_template('index.html', city=city, temperature=temperature,
                               humidity=humidity, wind_speed=wind_speed, description=description, advice=advice)

    # Ensure a valid response is always returned
    return render_template('index.html', message=None)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render’s assigned port
    app.run(host="0.0.0.0", port=port)
 


       
