
from gcore import Gcore

from src.config.settings import PROJECT_ID, REGION_ID, PROD_API_KEY, BASE_URL

API_KEY = PROD_API_KEY
if not API_KEY:
    raise EnvironmentError("PROD_API_KEY not found in environment or .env file")

client = Gcore(api_key=API_KEY,
               base_url=BASE_URL,
               cloud_project_id=PROJECT_ID,
               cloud_region_id=REGION_ID)

__all__ = ["client"]