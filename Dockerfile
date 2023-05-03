FROM python:3.10.11-slim-buster

RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose the port that the Flask app will run on
EXPOSE 5000

# Set the environment variable for Flask to run in production mode
ENV FLASK_ENV=production

# Riot API Key
ENV RIOT_KEY=***************************

RUN chmod +x game_api.py
CMD ["python3", "./game_api.py"]