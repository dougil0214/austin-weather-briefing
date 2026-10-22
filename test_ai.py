import requests
import weather_briefing
from pathlib import Path
import os

# Identify which of the two periods is daytime.
if weather_briefing.first_period["isDaytime"]:
    day = weather_briefing.first_period
    night = weather_briefing.second_period
else:
    night = weather_briefing.first_period
    day = weather_briefing.second_period

#same for precipitaion 
day_precipitation = day["probabilityOfPrecipitation"]["value"]
night_precipitation = night["probabilityOfPrecipitation"]["value"]

if day_precipitation is None:
    day_precipitation_text = "Unavailable"
else:
    day_precipitation_text = f"{day_precipitation}%"

if night_precipitation is None:
    night_precipitation_text = "Unavailable"
else:
    night_precipitation_text = f"{night_precipitation}%"


# AI Prompt
prompt_day = (
   "Recommend practical men's clothing for casual daytime wear. "
    "Answer in one sentence describing clothing only. "
    "Do not describe the weather or suggest colors or styles. "
    "Recommend extra layers only if the forecast supports them.\n"
    f"Conditions: {day['shortForecast']}. "
    f"Daytime high: {day['temperature']} {day['temperatureUnit']}. "
    f"Wind: {day['windSpeed']}. "
    f"Rain chance: {day_precipitation_text}. "
    f"Forecast period: {day['name']}. "
)
prompt_night=(
    "Recommend practical men's clothing for casual night wear. "
    "Answer in one sentence describing clothing only. "
    "Do not describe the weather or suggest colors or styles. "
    "Recommend extra layers only if the forecast supports them.\n"
    f"Conditions: {night['shortForecast']}. "
    f"Nighttime low: {night['temperature']} {night['temperatureUnit']}. "
    f"Wind: {night['windSpeed']}. "
    f"Rain chance: {night_precipitation_text}. "
    f"Forecast period: {night['name']}. "
)

# A dictionary describing which model to use and what to ask.
day_payload = {
    "model": "llama3.2:1b",
    "prompt": prompt_day,
    "stream": False
}
night_payload = {
    "model": "llama3.2:1b",
    "prompt": prompt_night,
    "stream": False
}

# POST sends our prompt to Ollama.
day_response = requests.post(
    "http://localhost:11434/api/generate",
    json=day_payload,
    timeout=180
)
day_response.raise_for_status()

night_response = requests.post(
    "http://localhost:11434/api/generate",
    json=night_payload,
    timeout=180
)
night_response.raise_for_status()


day_data = day_response.json()
night_data = night_response.json()

# Print only the generated answer.
clothing_suggestion_day = day_data["response"]
clothing_suggestion_night = night_data["response"]

# Full briefing including weather and clothing suggestions.
full_briefing = (
    f"{weather_briefing.briefing}\n"
    f"{day['name']}: {clothing_suggestion_day}\n"
    f"{night['name']}: {clothing_suggestion_night}"
)
if __name__ == "__main__":
    print(full_briefing)

#Save to txt
output_path = Path(__file__).resolve().parent / "full_briefing.txt"
with output_path.open("w", encoding="utf-8") as file:
    file.write(full_briefing)

# Send to app code
app_token = os.environ["PUSHOVER_APP_TOKEN"]
user_key = os.environ["PUSHOVER_USER_KEY"]

# Notification package
payload = {
    "token": app_token,
    "user": user_key,
    "message": full_briefing
}

# Sends to Pushover app
response = requests.post("https://api.pushover.net/1/messages.json", data=payload, timeout=30)
print(response.text)
response.raise_for_status()
print("Notification sent.")

print(response.json())