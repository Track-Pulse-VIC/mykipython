from dotenv import load_dotenv
from src.mykipython import *
import os

# env reading:
load_dotenv()

print('Reading password...')
myki_username = os.getenv("MYKI_USERNAME")
myki_password = os.getenv("MYKI_PASSWORD")

if not myki_username or not myki_password:
    print("Error: Please set MYKI_USERNAME and MYKI_PASSWORD in an .env file.")
    exit()


print(getMykiInfo(myki_username, myki_password))

