class EnhancedArticleClusterer:
    def __init__(self, n_clusters='auto', method='kmeans', use_categories=False, 
                 category_weight=2):
        """
        Initialize the enhanced article clusterer.
        
        Args:
            n_clusters: Number of clusters (int) or 'auto' for automatic detection
            method: 'kmeans', 'dbscan', or 'hierarchical'
            use_categories: Whether to use LLM categories in clustering
            category_weight: How many times to repeat categories for emphasis (default: 2)
        """
        self.n_clusters = n_clusters
        self.method = method
        self.use_categories = use_categories
        self.category_weight = category_weight
        self.vectorizer = None
        self.clusters = {}
        self.category_stats = {}
        
    def preprocess_text(self, text):
        """Clean and preprocess text for better clustering."""
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = ' '.join(text.split())
        return text
    
    def combine_all_text(self, article):
        """Combine title, description, and categories into one text string."""
        title = article[0]
        description = article[1]
        categories = article[2]
        
        # Handle categories as text
        if isinstance(categories, str):
            category_text = categories
        elif isinstance(categories, list):
            category_text = ' '.join(categories)
        else:
            category_text = ''
        
        # Weight title more heavily, include categories multiple times for emphasis
        combined = f"{title} {title} {description} {category_text} {category_text}"
        return self.preprocess_text(combined)
    
    def combine_title_description(self, article):
        """Combine title and description with title weighted more heavily (for text-only mode)."""
        title = article.get('title', '')
        description = article.get('description', '')
        combined = f"{title} {title} {description}"
        return self.preprocess_text(combined)
    
    def determine_optimal_clusters(self, vectors, max_clusters=10):
        """Use elbow method to determine optimal number of clusters."""
        n_samples = len(vectors)
        max_k = min(max_clusters, n_samples // 2)
        
        if max_k < 2:
            return 2
            
        inertias = []
        k_range = range(2, max_k + 1)
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(vectors)
            inertias.append(kmeans.inertia_)
        
        if len(inertias) < 2:
            return 2
            
        # Calculate rate of change to find elbow
        rates = [inertias[i-1] - inertias[i] for i in range(1, len(inertias))]
        optimal_k = rates.index(max(rates)) + 3
        
        return min(optimal_k, max_k)
    
    def cluster_articles(self, articles):
        """
        Cluster articles based on text content and LLM categories.
        
        Args:
            articles: List of dictionaries with 'title', 'description', and optionally 'categories' keys
            
        Returns:
            Dictionary with cluster labels as keys and lists of titles as values
        """
        if not articles:
            return {}
        
        # Combine all text (title, description, and categories)
        if self.use_categories:
            combined_texts = [self.combine_all_text(article) for article in articles]
        else:
            combined_texts = [self.combine_title_description(article) for article in articles]
        
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.8
        )
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(combined_texts)
        except ValueError:
            # Handle case where all documents are identical or empty
            return {"Cluster 1": [article['title'] for article in articles]}
        
        # Determine number of clusters
        if self.n_clusters == 'auto':
            n_clusters = self.determine_optimal_clusters(tfidf_matrix.toarray())
        else:
            n_clusters = min(self.n_clusters, len(articles))
        
        # Apply clustering algorithm
        if self.method == 'kmeans':
            clusterer = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = clusterer.fit_predict(tfidf_matrix)
        elif self.method == 'dbscan':
            clusterer = DBSCAN(eps=0.5, min_samples=2, metric='cosine')
            cluster_labels = clusterer.fit_predict(tfidf_matrix.toarray())
        else:
            raise ValueError("Method must be 'kmeans' or 'dbscan'")
        
        # Group articles by cluster
        clusters = defaultdict(list)
        for i, label in enumerate(cluster_labels):
            if label == -1:  # DBSCAN noise points
                clusters["Miscellaneous"].append(articles[i]['title'])
            else:
                clusters[f"Cluster {label + 1}"].append(articles[i]['title'])
        
        # Sort by cluster size
        self.clusters = dict(sorted(clusters.items(), 
                                  key=lambda x: len(x[1]), 
                                  reverse=True))
        
        # Generate cluster statistics
        self._generate_cluster_stats(articles, cluster_labels)
        
        return self.clusters
    
    def _generate_cluster_stats(self, articles, cluster_labels):
        """Generate statistics about categories in each cluster."""
        self.category_stats = {}
        
        for i, label in enumerate(cluster_labels):
            if label == -1:
                cluster_name = "Miscellaneous"
            else:
                cluster_name = f"Cluster {label + 1}"
            
            if cluster_name not in self.category_stats:
                self.category_stats[cluster_name] = Counter()
            
            # Count categories in this cluster
            categories = articles[i].get('categories', [])
            if isinstance(categories, str):
                categories = [categories]
            
            for category in categories:
                self.category_stats[cluster_name][category] += 1
    
    def get_cluster_categories(self, cluster_name, top_n=3):
        """Get the most common LLM categories in a cluster."""
        if cluster_name not in self.category_stats:
            return []
        
        return [cat for cat, count in self.category_stats[cluster_name].most_common(top_n)]
    
    def cluster_articles_by_category_only(self, articles):
        """Alternative method: Cluster purely based on LLM categories."""
        if not any('categories' in article for article in articles):
            print("No categories found in articles!")
            return {}
        
        # Group articles by exact category matches
        category_groups = defaultdict(list)
        
        for article in articles:
            categories = article.get('categories', [])
            if isinstance(categories, str):
                categories = [categories]
            
            # Create a key from sorted categories
            category_key = tuple(sorted(categories)) if categories else ('Uncategorized',)
            category_groups[category_key].append(article['title'])
        
        # Convert to readable format
        readable_clusters = {}
        for i, (category_tuple, titles) in enumerate(category_groups.items()):
            if category_tuple == ('Uncategorized',):
                cluster_name = "Uncategorized"
            else:
                cluster_name = f"Category: {', '.join(category_tuple)}"
            readable_clusters[cluster_name] = titles
        
        return dict(sorted(readable_clusters.items(), 
                          key=lambda x: len(x[1]), 
                          reverse=True))
    
    def print_clusters_with_categories(self):
        """Print clusters with their dominant categories."""
        if not self.clusters:
            print("No clusters found. Run cluster_articles() first.")
            return
        
        print(f"\nFound {len(self.clusters)} clusters:")
        print("=" * 60)
        
        for cluster_name, titles in self.clusters.items():
            top_categories = self.get_cluster_categories(cluster_name)
            category_str = f" (Categories: {', '.join(top_categories)})" if top_categories else ""
            
            print(f"\n{cluster_name} ({len(titles)} articles){category_str}:")
            print("-" * 40)
            for i, title in enumerate(titles, 1):
                print(f"{i}. {title}")
    
    def print_clusters(self):
        """Standard cluster printing without category info."""
        if not self.clusters:
            print("No clusters found. Run cluster_articles() first.")
            return
        
        print(f"\nFound {len(self.clusters)} clusters:")
        print("=" * 50)
        
        for cluster_name, titles in self.clusters.items():
            print(f"\n{cluster_name} ({len(titles)} articles):")
            print("-" * 30)
            for i, title in enumerate(titles, 1):
                print(f"{i}. {title}")



def determine_category_for_cluster(headline, description, google_api):
    """
    Feeds a cluster of headlines into Gemini to determine and name the category.

    Args:
        cluster_name (str): The name of the cluster.
        headlines_list (list): A list of nested lists, where each inner list
                               contains a headline and a description.
        
    Returns:
        dict: A dictionary containing the cluster name, the determined category,
              and a summary.
    """

    genai.configure(api_key=google_api)

    # Initialize the Gemini Pro model
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    # 🌟 NEW CODE: Combine headline and description for each story.
    # We'll create a new list of strings, where each string is a story.
    combined_stories = [
        f"Headline: {headline}\nDescription: {description}" 
    ]

    # Combine all these new story strings into a single string for the prompt
    headlines_text = "\n\n".join(combined_stories)
    
    # Craft the prompt to perform the task
    prompt = f"""
    Analyze the following news headlines and descriptions. They are different categories of news.
    Your task is to:
    1.  Determine the most fitting and specific news category name for this headline and description.
    2.  Provide a short, one-sentence summary of the main topic.
    3.  Provide a category name for the headline and description. For example, oil finance, sustainable energy etc.
    
    Return the result in a JSON object with two keys: "category_name" and "summary".

    Here is the list of headlines and descriptions from ":
    
    {headlines_text}
    """

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        
        # Clean up any markdown or extra text the model might generate
        if raw_text.startswith("```json"):
            raw_text = raw_text.strip("```json").strip("```")

        result = json.loads(raw_text)
        
        return {
            "determined_category": result.get("category_name", "Unknown"),
            "summary": result.get("summary", "No summary provided.")
        }
        
    except Exception as e:
        print(f"An error occurred for cluster {headline}: {e}")
        return {
            "error": str(e)
        }
    
def make_categorisations(full_articles_database):
    final_enhanced_outputs = []
    for i in full_articles_database:
        result = determine_category_for_cluster(i['title'],i['description'])
        
        if "error" in result:
            print(f"Failed to process {i['title']}: {result['error']}")
        else:
            print(f"\n--- Analysis for {i['title']} ---")
            print(f"Determined Category: {result['determined_category']}")
            print(f"Summary: {result['summary']}")
            final_enhanced_outputs.append([result['determined_category'],i['title'],i['description']])

        time.sleep(3)
    
    final_filtered_data = [item for item in final_enhanced_outputs if 'sport' or 'lottery' or 'music'  not in item[0].lower()]

    return final_filtered_data

