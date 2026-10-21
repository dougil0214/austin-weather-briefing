# Austin Weather Briefing Automation

A Python project that retrieves Austin weather forecasts, generates clothing suggestions using a local AI model, and sends the completed briefing to my iPhone.

It runs twice daily on a Windows homelab PC through Windows Task Scheduler.

## How it works

1. Requests location information from the National Weather Service API.
2. Retrieves the first two available forecast periods.
3. Extracts conditions, temperatures, wind, and precipitation chances.
4. Sends separate daytime and nighttime prompts to Llama 3.2 through Ollama.
5. Saves the forecast and clothing suggestions to a text file.
6. Sends the completed briefing through Pushover.

The weather forecast comes from NWS. AI generates only the clothing suggestions.

## Tools

- Python
- Requests
- National Weather Service API
- Ollama with `llama3.2:1b`
- Pushover
- Windows Task Scheduler

## Project files

| File | Purpose |
|---|---|
| `weather_briefing.py` | Retrieves and formats the forecast |
| `generate_briefing.py` | Generates clothing advice, saves output, and sends notifications |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Excludes credentials, temporary files, and generated output |

## Setup

1. Install Python and Ollama.
2. Install the Python dependency:

   ```powershell
   py -m pip install -r requirements.txt
   ```

3. Download the local model:

   ```powershell
   ollama pull llama3.2:1b
   ```

4. Create a Pushover account, register your phone, and create an application.
5. Set these Windows user environment variables:

   - `PUSHOVER_APP_TOKEN`
   - `PUSHOVER_USER_KEY`

6. Open a new terminal after saving the environment variables.
7. Ensure Ollama is running, then run:

   ```powershell
   generate_briefing.py
   ```

Running this script sends a notification to the configured Pushover account.

## Output

The combined briefing is saved as `full_briefing.txt` beside `generate_briefing.py`.

The forecast module also creates `weather_briefing.txt` in the current working directory. Both files are overwritten on each run.

## Scheduling

Create a Windows Task Scheduler task that runs `generate_briefing.py` using the full Python executable path.

Set the project folder as “Start in” and add the desired daily triggers. The task must run under an account with access to the Pushover environment variables.

The homelab must be awake, connected to the internet, and running Ollama.

## Limitations

- AI clothing advice can be inconsistent or ignore instructions.
- Daily highs and nightly lows do not describe every hour.
- The script assumes the first two periods include one daytime and one nighttime forecast.
- Request failures stop execution; automatic retries are not implemented.
- Weather data and notification delivery require external services.

## What I learned

- HTTP GET and POST requests
- JSON, dictionaries, and lists
- Conditional logic and missing-value handling
- Prompt design and reviewing AI output
- File paths and environment variables
- Scheduling and troubleshooting Python scripts

