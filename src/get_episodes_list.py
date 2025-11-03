import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_episodes_list(series_url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    # Tweak to get page with all seasons on single page
    all_seasons_url = f"{series_url}?page=1&itemsToShow=9999"
    driver.get(all_seasons_url)

    seasons_html = driver.page_source

    soup = BeautifulSoup(seasons_html, "html.parser")

    # Find all divs that have the attribute 'data-season-id'
    season_divs = soup.find_all("div", attrs={"data-season-id": True})

    seasons_html_list = []

    for div in season_divs:
        title_tag = div.find("h2")
        season_name_raw = title_tag.get_text(strip=True) if title_tag else None
        season_html = str(div)

        seasons_html_list.append({
            "season_name_raw": season_name_raw,
            "season_html": season_html
        })

    return episodes_processor(seasons_html_list, series_url)


def episodes_processor(seasons_html_list, season_url):
    episodes = []

    for s in seasons_html_list:

        # Parse page for episodes list
        season_div = BeautifulSoup(s['season_html'], "html.parser")
        ul = season_div.find("ul") if season_div else None

        if ul:
            # Processing list of episodes
            for i, li in enumerate(ul.find_all("li"), start=1):
                a = li.find("a")
                if a and a.get("href"):
                    rel_url = a["href"]
                    episode_url = urljoin(season_url, rel_url)

                    # Removing Hebrew letters to get rid of RTL issues during parsing
                    hebrew_pattern = r'[\u0590-\u05FF]+'
                    url_without_hebrew = re.sub(hebrew_pattern, '', episode_url)
                    season_number = re.sub(r'\D', '', s['season_name_raw'])
                    if season_number == '': season_number = "0"
                    parsed_url = urlparse(url_without_hebrew)
                    striped_url = parsed_url.path.strip('/').split('/')

                    # Parsing series name and season
                    series_name = striped_url[-3]

                    episodes.append({
                        "episode": f"{series_name}.s{season_number}e{i}",
                        "url": episode_url
                    })

    return episodes
