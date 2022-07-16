import os

# DATABASE
DB_HOST = os.getenv('DB_HOST') or 'localhost'
DB_PORT = os.getenv('DB_PORT') or '3306'
DB_USER = os.getenv('DB_USER') or 'root'
DB_PASSWORD = os.getenv('DB_PASSWORD') or 'ZAQ!2wsx'
DB_NAME = os.getenv('DB_NAME') or 'financial_summary'
# NORDIGEN
NORDIGEN_ID = os.getenv('NORDIGEN_ID') or ''
NORDIGEN_SECRET = os.getenv('NORDIGEN_SECRET') or ''
# SCHEDULER
FETCH_INTERVAL_IN_SECONDS = int(os.getenv('FETCH_INTERVAL_IN_SECONDS')) or 10