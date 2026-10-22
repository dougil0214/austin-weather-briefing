import requests
import emoji



# This API endpoint describes a location using latitude and longitude.
# These coordinates represent a point in Austin.
# Its response includes a link to the forecast for that location.
url = "https://api.weather.gov/points/30.2672,-97.7431"

# Headers are extra information sent along with a request.
# "User-Agent" identifies our application to the weather service.
# "AustinWeatherBriefing/1.0" is a name
headers = {
    "User-Agent": "AustinWeatherBriefing/1.0"
}

# Send a GET request: ask the API to return information.
# Store its response in a variable called response.
# The response includes a status code, headers, and the returned data.
response = requests.get(url, headers=headers, timeout=20)
response.raise_for_status()

# 200 means success, 400 means bad request, and 404 means not found.
# print(response.status_code)

# The API sends its data as JSON.
# .json() converts that JSON into Python objects.
# For this response, the outermost object is a dictionary.
data = response.json()

# .keys() shows the dictionary's top-level key names.
# print(data.keys())

# Access the "properties" dictionary, then its "forecast" value.
# That value is a URL pointing to the actual forecast.
# print(data["properties"]["forecast"])

# Save that forecast URL to request it next.
forecast_url = data["properties"]["forecast"]


# Retrieve the actual forecast.

# Make a second request, this time to the forecast URL.
# Use the same headers to identify the application.
forecast_response = requests.get(forecast_url, headers=headers, timeout=20)
forecast_response.raise_for_status()

# Convert this second response's JSON into a Python dictionary.
forecast_data = forecast_response.json()

# Inside "properties", "periods" contains a list of forecast periods.
# Each item is a dictionary describing a period like Today or Tonight.
periods = forecast_data["properties"]["periods"]

# An inspection print that shows the first period's dictionary:
# print(periods[0])
# print(periods[1])


# Select the first period and describe its temperature.

# Lists start at index 0, so this selects the first forecast period.
first_period = periods[0]
second_period = periods[1]

# "isDaytime" is True or False.
# Choose the temperature label based on that value.
if first_period["isDaytime"]:
    temp_label = "high"
else:
    temp_label = "low"

if second_period["isDaytime"]:
    second_temp_label = "high"
else:
    second_temp_label = "low"

# In case there's no value for precepitiaiton 

first_precipitation = first_period['probabilityOfPrecipitation']['value']
second_precipitation = second_period['probabilityOfPrecipitation']['value']

if first_precipitation is None:
    first_precipitation_text = "Unavailable"
else:
    first_precipitation_text = f"{first_precipitation}%"

if second_precipitation is None:
    second_precipitation_text = "Unavailable"
else:
    second_precipitation_text = f"{second_precipitation}%"

# Emojis for added effects
if first_period['shortForecast']:
    if "rain" in first_period['shortForecast'].lower():
        day_emoji = emoji.emojize(":umbrella:")
    elif "sunny" in first_period['shortForecast'].lower():
        day_emoji = emoji.emojize(":sun_with_face:")
    elif "clear" in first_period['shortForecast'].lower():
        day_emoji = emoji.emojize(":moon:")
    elif "hot" in first_period['shortForecast'].lower():
        day_emoji = emoji.emojize(":thermometer:")
    elif "cold" in first_period['shortForecast'].lower():
        day_emoji = emoji.emojize(":cold_face:")
    elif "thunderstorm" in first_period['shortForecast'].lower():
        day_emoji = emoji.emojize(":cloud_with_lightning_and_rain:")
    elif "windy" in first_period['shortForecast'].lower():
        day_emoji = emoji.emojize(":cyclone:")
    else:
        day_emoji = ""
else:
    day_emoji = ""

if second_period['shortForecast']:
    if "rain" in second_period['shortForecast'].lower():
        night_emoji = emoji.emojize(":umbrella:")
    elif "sunny" in second_period['shortForecast'].lower():
        night_emoji = emoji.emojize(":sun_with_face:")
    elif "clear" in second_period['shortForecast'].lower():
        night_emoji = emoji.emojize(":crescent_moon:")
    elif "hot" in second_period['shortForecast'].lower():
        night_emoji = emoji.emojize(":thermometer:")
    elif "cold" in second_period['shortForecast'].lower():
        night_emoji = emoji.emojize(":cold_face:")
    elif "thunderstorm" in second_period['shortForecast'].lower():
        night_emoji = emoji.emojize(":cloud_with_lightning_and_rain:")
    elif "windy" in second_period['shortForecast'].lower():
        night_emoji = emoji.emojize(":cyclone:")
    else:
        night_emoji = ""
else:
    night_emoji = ""

# Bring the forecast all together 

briefing = (
    f"{day_emoji} {first_period['name']}'s forecast is "
    f"{first_period['shortForecast'].lower()} with a {temp_label} of "
    f"{first_period['temperature']} {first_period['temperatureUnit']}. "
    f"Winds {first_period['windSpeed']} "
    f"from the {first_period['windDirection']}. "
    f"Chance of precipitation is {first_precipitation_text}. \n\n"
    # Night time forecast
    f"{night_emoji} {second_period['name']}'s forecast is "
    f"{second_period['shortForecast'].lower()} with a {second_temp_label} of "
    f"{second_period['temperature']} {second_period['temperatureUnit']}. "
    f"Winds {second_period['windSpeed']} "
    f"from the {second_period['windDirection']}. "
    f"Chance of precipitation is {second_precipitation_text}. \n"
)


if __name__ == "__main__":
    print(briefing)
#Save into txt
with open("weather_briefing.txt", "w", encoding="utf-8") as file:
    file.write(briefing)