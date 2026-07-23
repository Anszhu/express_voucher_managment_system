import os
from dotenv import load_dotenv

load_dotenv()

EXPRESS_API_URL = os.getenv("EXPRESS_API_URL", "http://localhost:4000/api/v1")
APP_NAME = "Voucher Admin Dashboard"
APP_ICON = "📊"
