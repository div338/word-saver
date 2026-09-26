import os

from dotenv import load_dotenv

load_dotenv()

TOMTOM_API_KEY = os.environ["TOMTOM_API_KEY"]

# Navsari and Mumbai coordinates (lat, lon)
ORIGIN = (20.9467, 72.9520)
DESTINATION = (19.0760, 72.8777)

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "travel.db")
