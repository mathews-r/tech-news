from bs4 import BeautifulSoup
import requests
import time
from tech_news import database


headers = {"User-Agent": "Fake user-agent"}
base_url = "https://blog.betrybe.com/"


# Requisito 1
def fetch(url: str):
    try:
        response = requests.get(url, headers=headers)
        time.sleep(1)
        response.raise_for_status()

    except (requests.HTTPError, requests.ReadTimeout):
        return None

    return response.text


# Requisito 2
def scrape_updates(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    news_list = []
    for news in soup.find_all("a", class_="cs-overlay-link"):
        news_list.append(news.get("href"))
    return news_list


# Requisito 3
def scrape_next_page_link(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    next_page = soup.find("a", class_="next page-numbers")

    if next_page is None:
        return None

    return next_page.get("href")


# Requisito 4
def scrape_news(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    url = soup.find("link", rel="canonical").get("href")
    title = soup.find("h1", class_="entry-title").text.strip()
    timestamp = soup.find("li", class_="meta-date").text
    writer = soup.find("a", class_="url fn n").text
    reading_time = soup.find("li", class_="meta-reading-time").text[:2]
    summary = soup.find_all("p")[0].text.strip()
    category = soup.find("span", class_="label").text

    dict_news = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": int(reading_time),
        "summary": summary,
        "category": category,
    }
    return dict_news


# Requisito 5
def get_tech_news(amount):
    response = fetch(base_url)

    get_all_links = scrape_updates(response)

    list_news = []
    for link in get_all_links:
        news = fetch(link)
        list_news.append(scrape_news(news))

    data = list_news.count(amount)
    print(data)
    # database.create_news(data)

    return data


get_tech_news(5)
