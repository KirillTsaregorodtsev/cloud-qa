# Cloud QA Team utils

## Installation

### 1. Clone the project

```bash
git clone https://gitlab-ed7.cloud.gc.onl/cloudapi/qa/team-qa.git
cd team-qa
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
```
### 2. Run the script
```bash
python scripts/run_service.py
```

## Output
The script will generate a CSV report in the _src/report_ directory.