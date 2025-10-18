import langid
from dotenv import load_dotenv

load_dotenv(dotenv_path="environmentvariables.env")

def filter_english_articles_and_duplicate(articles):
    """
    Filters a list of article dictionaries, keeping only English ones and non-duplicates.

    Args:
        articles (list of dict): Each dict should have 'title' and optionally 'description'.

    Returns:
        list of dict: Same structure as input, but only English-language and unique by title.
    """
    seen_titles = set()
    filtered = []

    for article in articles:
        title = (article.get("title") or "").strip()
        description = (article.get("description") or "").strip()

        # Skip if title already seen or text is too short
        if not title or title in seen_titles:
            continue

        combined_text = f"{title} {description}"
        if len(combined_text) < 20:
            continue

        lang, _ = langid.classify(combined_text)
        if lang == "en":
            seen_titles.add(title)
            filtered.append(article)

    return filtered

def consolidate_dataframe(newsapi_list, newsio_list, gnews_list):
    """
    Consolidates lists of articles from various sources (APIs) into a single master list.

    Args:
        newsapi_list (list): List of articles fetched from NewsAPI.
        newsio_list (list): List of articles fetched from Newsdata.io or similar.
        gnews_list (list): List of articles fetched from a Google News source.

    Returns:
        list: A single, consolidated list containing all articles from the input lists.
    """

    full_articles_database = []

    for articles_descriptions in [newsapi_list,newsio_list,gnews_list]:
        for specific_articles in articles_descriptions:
            full_articles_database.append(specific_articles)
    return full_articles_database

