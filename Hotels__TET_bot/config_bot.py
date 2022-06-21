import os

from dotenv import load_dotenv

load_dotenv()
headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': os.getenv('RAPIDAPI_KEY')
    }

BOT_TOKEN = os.getenv('BOT_TOKEN')