from dotenv import load_dotenv
from pathlib import Path
import os

folderID = "42b75e35-a029-4f73-aade-4b301c3a6be6"
ENV_PATH = "packages/utils/.env"
BASE_URL = "https://pw01shs6btnap01.bdx.com/BarTender/"
PRINT_URL = "https://pw01shs6btnap01.bdx.com/BarTender/Print/{}/".format(folderID)
EXECUTABLE_PATH = Path("./libs/drivers/chromedriver.exe")
INPUT_DIR = Path("./input")
LOG_DIR = Path("./logs") 

if Path('packages/utils/.env').exists():
    load_dotenv(ENV_PATH)
    
USERNAME = os.getenv("MC-USERNAME")
PASSWORD = os.getenv("MC-PASSWORD")
DB_USER = os.getenv("USER")
DB_PASSWORD = os.getenv("PASSWORD")
DB_SERVER = os.getenv("SERVER")