import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

GITLAB_ACCESS_TOKEN = os.getenv("GITLAB_ACCESS_TOKEN")
KEADMIN_AUTH_SID = os.getenv("KEADMIN_AUTH_SID")
YOUTRACK_AUTHORIZATION = os.getenv("YOUTRACK_AUTHORIZATION")
