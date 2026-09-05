from dotenv import load_dotenv
import os

# Retrieve the base file path on which .env file is stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# User load_dotenv which is a python module to load environment file which is .env
load_dotenv(os.path.join(BASE_DIR, ".env"))