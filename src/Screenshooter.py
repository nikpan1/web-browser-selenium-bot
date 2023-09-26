from datetime import datetime
import os
import selenium
from selenium.webdriver.remote.webdriver import WebDriver
from CoreSettings import *

def make_screenshot(driver: WebDriver, directory: str = SCREENSHOTS_DIR) -> str:
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        screenshot_path = os.path.join(directory, filename)

        driver.save_screenshot(screenshot_path)
        return screenshot_path
    except Exception as e:
        # Handle any exceptions that might occur during the screenshot process
        print(f"Error capturing screenshot: {e}")
        return ""


