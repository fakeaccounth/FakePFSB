#(©)CodeXBotz

import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler


load_dotenv()

#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", " 6403720726:AAH2s38VIkj9TWcxA2ZNlRmnz-G2CSot4MA")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "23229610"))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "8fc13674e50502c5a9e6b809cac40212")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001999588896"))

LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002433740523"))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "1349045607"))

#Port
PORT = os.environ.get("PORT", "2728")

#Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://MONGONOOB:MONGONOOB@cluster0.7mj8fw2.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "MONGONOOB")


#force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1001913326364"))
JOIN_REQS_DB = os.environ.get("JOIN_REQS_DB", DB_URI)
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "0"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "80"))

#start message
START_PIC = os.environ.get("START_PIC", "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgZeTBvIzSK30yb3Q3zfD5TeRJzcNm17OfXQHJguruvu8Pqhxi6asqxUGqkmvPdNuRtQu33IPAP0YMQ69zAe4GsrBP1jDBDbByglbHXzPbbZfKGuVFiTWC2aeXFbRtNs-bT-0Y3q4DiMOE7_gPPB0f8X1hq8_u7FsM-JL7qzAbLEHjc4bdgnjjVu1T0c5On/w945-h600-p-k-no-nu/Frame%20475.png")
START_MSG = os.environ.get("START_MESSAGE", "Hello {first}\n\n<b>Radhe Radhe 🙏.</b>")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "1349045607").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

# Auto delete time in seconds.
AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "604800"))
AUTO_DELETE_MSG = os.environ.get("AUTO_DELETE_MSG", "<b>File will be automatically deleted in 7 Days. Please Watch It, Before Deleted.</b>")
AUTO_DEL_SUCCESS_MSG = os.environ.get("AUTO_DEL_SUCCESS_MSG", "<b>Your 📂 Deleted Successfully ✅</b>")


WEBSITE_URL_MODE = os.environ.get('WEBSITE_URL_MODE', False) # Set True or False

# If Website Url Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
WEBSITE_URL = os.environ.get("WEBSITE_URL", "") 

# Turn this feature on or off using True or False put value inside  ""
# TRUE for yes FALSE if no 
USE_SHORTLINK = True if os.environ.get('USE_SHORTLINK', "TRUE") == "TRUE" else False 
# only shareus service known rightnow rest you can test on your own
SHORTLINK_API_URL = os.environ.get("SHORTLINK_API_URL", "gplinks.com")
SHORTLINK_API_KEY = os.environ.get("SHORTLINK_API_KEY", "")

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", "True") == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "<b>❌ Don't Send Me Messages 👉 @Noob_Studio_Chat</b>"

ADMINS.append(OWNER_ID)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
