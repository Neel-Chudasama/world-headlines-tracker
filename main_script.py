from data_extraction import get_headlines_from_newsio, get_top_headlines_from_news_api, fetch_gnews_articles
from data_formatting import filter_english_articles_and_duplicate, consolidate_dataframe
from clustering import EnhancedArticleClusterer, determine_category_for_cluster, make_categorisations
from interaction import HeadlineViewer, generate_html_report, send_email

import os
from dotenv import load_dotenv
#load_dotenv(dotenv_path="environmentvariables.env") # for local 
load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
NEWSIOAPI_KEY = os.getenv("NEWSIOAPI_KEY")
GNEWSAPI_KEY = os.getenv("GNEWSAPI_KEY")
GOOGLE_API = os.getenv("GOOGLE_API")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


#headline extraction
concat_headlines_news_api = get_top_headlines_from_news_api(verbose = True)
newsio_headlines = get_headlines_from_newsio()
concat_gnews_articles = fetch_gnews_articles()

#data cleaning 
articles_news_api_cleaned = filter_english_articles_and_duplicate(concat_headlines_news_api)
articles_newsio_cleaned = filter_english_articles_and_duplicate(newsio_headlines)
articles_gnews_cleaned = filter_english_articles_and_duplicate(concat_gnews_articles)

#consolidate dataframes
full_articles_database = consolidate_dataframe(
    articles_news_api_cleaned,
    articles_newsio_cleaned,
    articles_gnews_cleaned
)

#clustering of data headlines
clusterer = EnhancedArticleClusterer(n_clusters='auto', method='kmeans', 
                                       category_weight=3)
clusters = clusterer.cluster_articles(full_articles_database)
clusterer.print_clusters_with_categories()

#determine categories for clusters
final_filtered_data = make_categorisations(full_articles_database)

#interactions for email
html = generate_html_report(final_filtered_data)
send_email(html, EMAIL_USER)