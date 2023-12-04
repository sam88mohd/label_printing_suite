from dotenv import load_dotenv
from pathlib import Path
import os

ENV_PATH = "packages/utils/.env"
BASE_URL = "https://pw01shs6btnap01.bdx.com/BarTender/Print/7f4b2eb0-2b17-4b9e-bda5-ebd99f8eb02d/Malaysia/"
SEVEN_URL_PATH = BASE_URL + "Strip Pack/Pouch/Variable Labels/"
P7215_PHASE2_URL_PATH = BASE_URL + "Strip Pack/Project 7215/Phase - 2/DC-7215-Pouch Variable/"
P7215_PHASE1_URL_PATH = BASE_URL + "Strip Pack/Project 7215/Phase - 1/DC-7215-Pouch Variable/"
TEN_URL_PATH = BASE_URL + "Strip Pack/Pouch/Variable Labels/Bell-Mark 10 Lane/"
P7128_URL_PATH = BASE_URL + "Strip Pack/Pouch/Project 7182/7182-Single Lane/"
EXECUTABLE_PATH = Path("./libs/drivers/msedgedriver.exe")
INPUT_DIR = Path("./input")
LOG_DIR = Path("./logs") 

if Path('packages/utils/.env').exists():
    load_dotenv(ENV_PATH)
    
USERNAME = os.getenv("MC-USERNAME")
PASSWORD = os.getenv("MC-PASSWORD")
DB_USER = os.getenv("USER")
DB_PASSWORD = os.getenv("PASSWORD")
DB_SERVER = os.getenv("SERVER")