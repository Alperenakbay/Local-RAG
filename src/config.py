#import os
#from dotenv import load_dotenv

#load_dotenv()

#FOUNDRY_URL = os.getenv("FOUNDRY_URL")
#FOUNDRY_API_KEY = os.getenv("FOUNDRY_API_KEY")
#CHAT_MODEL = os.getenv("CHAT_MODEL")

import os
from dotenv import load_dotenv

load_dotenv(override=True)

FOUNDRY_URL = os.getenv("FOUNDRY_URL")
FOUNDRY_API_KEY = os.getenv("FOUNDRY_API_KEY")
CHAT_MODEL = os.getenv("CHAT_MODEL")

