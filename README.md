# Cloud QA Team utils
This repository contains various utilities and scripts for the Cloud QA team, including tools for managing cloud resources, 
generating reports, and automating tasks.
### Table of covering  

| Test    | Description                  |
|---------|------------------------------|
| CPU     | check CPU's family           |
| RAM     | Shows RAM capacity           |
| DISK    | Shows lsblk output           |
| CONSOLE | Check the VNC Console access |
| PING    | check the ping to google.com |

## Installation

### 1. Clone the project

```bash
git https://github.com/KirillTsaregorodtsev/cloud-qa.git
cd cloud-qa
```

### 2. Create a virtual environment

#### For Windows:
```bash
py -m pip install --user virtualenv
py -m venv env
.\env\Scripts\activate
```

#### For Mac:
```bash
python3 -m pip install --user virtualenv
python3 -m venv .venv
source .venv/bin/activate
```
### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Environment Variables
```bash
touch .env
echo "PROD_API_KEY=<YOUR_API_KEY>" >> .env
```

## How to Use

### 1. Set up the required environment variables in _src/config/settings.py_ before executing the script.
example:
```pyhon
JIRA_TASK_ID = "GCLOUD2-1234"
FLAVOR = "bm0-infrastructure-small"
REGION_ID = RegionID.ED_16
PROJECT_ID = 309102
default_key_path = Path.home() / "Downloads" / "qa-ssh-key"
SSH_KEY_PATH = os.getenv("KEY_PAIR_PATH", str(default_key_path))
```
### 2. Run the script
```bash
python scripts/run_service.py
```

## Output
The script will generate a CSV report in the _reports_ directory.