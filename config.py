import os
import dotenv
dotenv.load_dotenv()

BOT_TOKEN=os.getenv('BOT_TOKEN')
START_IMAGE=os.getenv('START_IMAGE')
CHOOSING_MONTH_IMAGE=os.getenv('CHOOSING_MONTH_IMAGE')
CHOOSING_DAY_IMAGE=os.getenv('CHOOSING_DAY_IMAGE')
TRIAL_IMAGE=os.getenv('TRIAL_IMAGE')
HOST=os.getenv('HOST')
USER=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')
DB=os.getenv('DB')
PORT=os.getenv('PORT')