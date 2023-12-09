from flask import Flask, request, send_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

app = Flask(__name__)

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode

# Set up the WebDriver with the specified viewport size
driver = webdriver.Chrome(options=chrome_options)

# Specify the path where you want to save the screenshot
save_path = "/images"
# Global variable to keep track of the screenshot count
screenshot_count = 0

@app.route('/')
def capture_and_download():
    global screenshot_count

    # Get parameters from the URL
    url = request.args.get('url', "https://transgol.com/oddsservice/match.asp?no_third_party_tracking=true")
    width = int(request.args.get('width', 600))
    height = int(request.args.get('height', 600))
    
    # Get filename parameter from the URL
    filename = request.args.get('filename', f'screenshot_{screenshot_count}.png')

    # Navigate to the specified URL
    driver.get(url)
    driver.set_window_size(width, height)

    # Increment the screenshot count
    screenshot_count += 1
    full_path = os.path.join(save_path, filename)
    # Capture screenshot and save it with the specified filename
    driver.save_screenshot(full_path)

    return send_file(full_path, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



