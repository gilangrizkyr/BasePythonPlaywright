import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configuration settings untuk Playwright"""
    
    # Browser Settings
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    BROWSER_TYPE = os.getenv("BROWSER_TYPE", "chromium").lower()
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))
    
    # URL Settings
    BASE_URL = os.getenv("BASE_URL", "https://example.com")
    
    # Screenshot Settings
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    SCREENSHOTS_PATH = os.getenv("SCREENSHOTS_PATH", "./reports/screenshots")
    
    # Video Settings
    RECORD_VIDEO = os.getenv("RECORD_VIDEO", "false").lower() == "true"
    VIDEOS_PATH = os.getenv("VIDEOS_PATH", "./reports/videos")
    
    # Create directories if they don't exist
    @staticmethod
    def create_directories():
        os.makedirs(Settings.SCREENSHOTS_PATH, exist_ok=True)
        os.makedirs(Settings.VIDEOS_PATH, exist_ok=True)

settings = Settings()
