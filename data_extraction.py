import requests
import time
import os
from dotenv import load_dotenv

#load_dotenv(dotenv_path="environmentvariables.env") for local 
load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
NEWSIOAPI_KEY = os.getenv("NEWSIOAPI_KEY")
GNEWSAPI_KEY = os.getenv("GNEWSAPI_KEY")

def get_top_headlines_from_news_api(verbose=False):
    """
    Fetch top headlines from multiple news outlets using the NewsAPI.
    
    Args:
        api_key (str): Your NewsAPI key (optional, defaults to ENV variable).
        verbose (bool): If True, prints debug information.
    
    Returns:
        list: List of [title, description, content] for all retrieved articles.
    """

    list_of_sources  = ['cnn', 'new-york-magazine', 'reuters', 'the-washington-post', 'the-washington-times', 'associated-press', 'abc-news-au', 'australian-financial-review', 'google-news-au', 'news-com-au', 'aftenposten', 'nrk', 'ansa', 'il-sole-24-ore', 'football-italia', 'google-news-it', 'la-repubblica', 'argaam', 'google-news-sa', 'sabq', 'the-express-tribune', 'dawn', 'jang', 'the-news-international', 'brecorder', 'bbc-news', 'independent', 'wired-de', 'wirtschafts-woche', 'blasting-news-br', 'globo', 'google-news-br', 'info-money', 'cbc-news', 'financial-post', 'google-news-ca', 'the-globe-and-mail', 'el-mundo', 'google-news-ar', 'infobae', 'la-gaceta', 'la-nacion', 'google-news-fr', 'le-monde', 'les-echos', 'liberation', 'google-news-in', 'the-hindu', 'the-times-of-india', 'the-jerusalem-post', 'ynet', 'lenta', 'rbc', 'rt', 'tass', 'vedomosti', 'kommersant', 'the-moscow-times', 'goteborgs-posten', 'svenska-dagbladet', 'news24', 'eNCA', 'SABC News', 'Daily Maverick', 'The Mail & Guardian', 'Eyewitness News', 'RTE', 'RTL Nieuws', 'techcrunch-cn', 'xinhua-net']

    url = "https://newsapi.org/v2/top-headlines"
    concatenated = []

    with requests.Session() as session:
        for outlet in list_of_sources:
            params = {
                "sources": outlet,
                "apiKey": NEWSAPI_KEY
            }

            response = session.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])

                results = [
                    [
                        article.get("title", ""),
                        article.get("description", ""),
                    ]
                    for article in articles
                ]
                concatenated.extend(results)

                if verbose:
                    print(f"{outlet}: {len(results)} articles retrieved.")

            else:
                if verbose:
                    print("Error:", response.status_code, response.text)
            
            time.sleep(3)

    return concatenated


def get_headlines_from_newsio(reqs_per_min=15):

    """
    Fetch top headlines from multiple news outlets using the newsio.
    
    Args:
        reqs_per_min (int): Numerical value for how many proportions of requests to make

    Returns:
        list: List of [title, description, content] for all retrieved articles.
    """

    BASE_URL = "https://newsdata.io/api/1/latest"

    country_list = [
    'us', 'gb', 'ca', 'au', 'in', 'sg', 'za', 'ie',
    'fr', 'de', 'it', 'es', 'br', 'jp', 'ru', 'cn',
    'ae', 'sa', 'ng', 'ke', 'mx', 'ar']

    delay = 60.0 / reqs_per_min  # seconds between requests
    concatenated = []
    session = requests.Session()  # reuse TCP connection

    for country_code in country_list:
        params = {
            "apikey": NEWSIOAPI_KEY,
            "country": country_code,
            "language": "en",
            "category": "top"
        }

        try:
            response = session.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.HTTPError as e:
            # If the API returns 429 it means "too many requests"
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                wait = int(retry_after) if retry_after and retry_after.isdigit() else delay * 2
                print(f"Rate limited. Sleeping for {wait} seconds.")
                time.sleep(wait)
                # optionally retry once after sleeping
                try:
                    response = session.get(BASE_URL, params=params, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                except Exception as e2:
                    print(f"Retry failed for {country_code}: {e2}")
                    continue
            else:
                print(f"Request failed for {country_code}: {e}")
                continue
        except Exception as e:
            print(f"Request failed for {country_code}: {e}")
            continue

        articles = data.get("results", [])
        print(f"[{country_code}] Found {len(articles)} top headlines")

        for article in articles:
            if article.get("category") == "sports":
                continue
            concatenated.append({
                "title": article.get("title", "No title"),
                "description": article.get("description", "No description")
            })

        time.sleep(delay)

    return concatenated


def fetch_gnews_articles():

    """
    Fetch top headlines from multiple countries using the gnews.

    Returns:
        list: List of [title, description, content] for all retrieved articles.
    """

    country_codes = [
        'au',  # Australia
        'br',  # Brazil
        'ca',  # Canada
        'cn',  # China
        'eg',  # Egypt
        'fr',  # France
        'de',  # Germany
        'gr',  # Greece
        'hk',  # Hong Kong
        'in',  # India
        'ie',  # Ireland
        'it',  # Italy
        'jp',  # Japan
        'nl',  # Netherlands
        'no',  # Norway
        'pk',  # Pakistan
        'pe',  # Peru
        'ph',  # Philippines
        'pt',  # Portugal
        'ro',  # Romania
        'ru',  # Russian Federation
        'sg',  # Singapore
        'se',  # Sweden
        'ch',  # Switzerland
        'tw',  # Taiwan
        'ua',  # Ukraine
        'gb',  # United Kingdom
        'us'   # United States
    ]

    url = "https://gnews.io/api/v4/top-headlines"

    concat = []
    for country in country_codes:
        params = {
            "apikey": GNEWSAPI_KEY,
            "categories": "-sports",
            "country": country,
            "lang": "en"
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            for article in data.get("articles"):
                concat.append({
                    "title": article.get("title"),
                    "description": article.get("description")
                })
            print(f"{country} articles are extracted")
        except Exception as e:
            print(f" Failed for {country}: {e}")

        time.sleep(4)

    return concat
