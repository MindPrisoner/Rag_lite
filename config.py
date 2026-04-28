import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

TOP_K = int(os.getenv("TOP_K", "3"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "180"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "40"))
KNOWLEDGE_DIR = os.getenv("KNOWLEDGE_DIR", "knowledge")

if not API_KEY:
    raise ValueError("缺少 API_KEY，请检查 .env")
if not BASE_URL:
    raise ValueError("缺少 BASE_URL，请检查 .env")
if not MODEL_NAME:
    raise ValueError("缺少 MODEL_NAME，请检查 .env")
