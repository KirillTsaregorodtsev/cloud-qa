import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from src.config.enums import RegionID

load_dotenv()

def get_project_root() -> Path:
    current_dir = Path(__file__).resolve().parent
    while current_dir != current_dir.parent:
        if (current_dir / "pytest.ini").exists() or (current_dir / "requirements.txt").exists():
            return current_dir
        current_dir = current_dir.parent
    raise FileNotFoundError("Could not find project root")

#=============================INIT SETTINGS FOR TESTS=======================================
JIRA_TASK_ID = "GCLOUD2-18858"
FLAVOR = "bm1-hf-medium"
REGION_ID = RegionID.ANX_2
PROJECT_ID = 309102
OFFSET = 0
NUMBER_OF_SERVERS = 1
SSH_KEY_NAME = "qa-chk-bare"
SSH_KEY_PATH = os.getenv("KEY_PAIR_PATH", str(Path.home() / "Downloads/qa-chk-bare"))

#=============================INIT SETTINGS FOR PROJECT=======================================
PROJECT_ROOT = get_project_root()
MAX_WORKERS = os.getenv("MAX_WORKERS", 5)
LOG_FILE = "logs/app.log"
REPORT_FILE = os.path.join(PROJECT_ROOT, "reports", f"{JIRA_TASK_ID}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
DB_FILE = "data/report.db"
DB_INIT_SQL = "sql/init_db.sql"
TMP_PATH = PROJECT_ROOT / "tmp"
PROD_API_KEY = os.getenv("PROD_API_KEY")
BASE_URL = "https://api.gcore.com"
CLIENT_ID = os.getenv("CLIENT_ID", 130485)
