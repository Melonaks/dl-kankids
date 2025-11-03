from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By



def get_episode_manifest_url(episodes):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    for e in episodes:

        url = e.get('url')
        driver.get(url)

        div = driver.find_element(By.CSS_SELECTOR, 'div[data-dash-url]')
        dash_value = div.get_attribute("data-dash-url")
        raw_url = f"https:{dash_value}"
        e['manifest_url'] = raw_url
        print(f"{e['episode']} manifest collected - {raw_url}")

    driver.quit()
    return episodes