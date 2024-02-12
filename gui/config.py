from os import environ
from dotenv import load_dotenv

load_dotenv()

SO_PATH = environ.get("SO_PATH", "")
NN_DUMP_PATH = environ.get("NN_DUMP_PATH", "")
GS_PATH = environ.get("GS_PATH", "")
