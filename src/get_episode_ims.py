import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

def get_episode_manifest_url(episodes):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    driver = webdriver.Chrome(options=options)

    for e in episodes:

        url = e.get('url')
        driver.get(url)
        print(f"Opening {url}")

        # Clicking Play button/area in order to trigger Manifest.ims request

        for action in ["rgpl-action-area", "rgpl-btn-play"]:
            element = WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, action))
            )
            element.click()

        # Getting DASH request URL
        logs = driver.get_log("performance")
        for log_entry in logs:
            message = json.loads(log_entry.get('message', '{}')).get('message')
            if message.get('method') in 'Network.requestWillBeSent':
                params = message.get('params', {})
                request = params.get('request', {})
                url = request.get('url')

                if 'Manifest.ism' in url:
                    e['manifest_url'] = url
        print(f"{e['episode']} manifest collected")

    driver.quit()
    return episodes