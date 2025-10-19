<div align="center">

# 📰 World Headlines Tracker for Stock Picks

### *AI-Powered News Intelligence Pipeline for Market Insights*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

*Automatically collect, classify, and visualize daily trending news from global sources using machine learning to identify market-moving themes.*

[Features](#-features) • [Quick Start](#-quick-start) • [How It Works](#-how-it-works) • [Demo](#-example-output)

---

</div>

## 🎯 Overview

Wake up every morning to an **AI-curated digest** of the world's top news stories, automatically organized by theme. This pipeline harnesses the power of machine learning and natural language processing to help you spot emerging trends and potential market opportunities before they become obvious.

### What Makes This Special?

- 🤖 **AI-Powered Clustering** - Machine learning groups similar stories automatically
- 🏷️ **Smart Labeling** - Gemini AI generates human-readable category names
- 📊 **Interactive Dashboard** - Beautiful HTML visualization of news trends
- 📧 **Email Delivery** - Daily digest sent straight to your inbox
- 🌍 **Multi-Source Aggregation** - Combines NewsData.io, NewsAPI, and GNews
- ⚡ **Fully Automated** - Set it and forget it

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔍 Intelligent News Extraction
- Pulls from multiple premium news APIs
- Captures headlines, summaries, and metadata
- Covers global sources and regions
- Real-time trending story detection

</td>
<td width="50%">

### 🧠 Advanced ML Processing
- K-Means clustering for topic discovery
- Semantic similarity analysis
- Automatic deduplication
- Theme identification and ranking

</td>
</tr>
<tr>
<td width="50%">

### 📱 Beautiful Visualization
- Interactive HTML dashboard
- Mobile-responsive design
- Category-based organization
- One-click article access

</td>
<td width="50%">

### 🚀 Automation Ready
- Email integration included
- Scheduled execution support
- Cloud deployment compatible
- GitHub Actions ready

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DAILY NEWS PIPELINE                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   📥 Data Extraction          │
              │   • NewsData.io               │
              │   • NewsAPI                   │
              │   • GNews                     │
              └───────────────┬───────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   🧹 Data Formatting          │
              │   • Cleaning                  │
              │   • Deduplication             │
              │   • Consolidation             │
              └───────────────┬───────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   🤖 ML Clustering            │
              │   • K-Means Algorithm         │
              │   • Gemini AI Labeling        │
              │   • Theme Extraction          │
              └───────────────┬───────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   📊 HTML Generation          │
              │   • Interactive Dashboard     │
              │   • Category Organization     │
              │   • Mobile Responsive         │
              └───────────────┬───────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   📧 Email Delivery           │
              │   • Automated Sending         │
              │   • HTML Formatting           │
              └───────────────────────────────┘
```

---

## 📂 Repository Structure

```
news-intelligence-pipeline/
│
├── 📥 data_extraction/
│   ├── newsio_extraction.py      # NewsData.io API integration
│   ├── newsapi_extraction.py     # NewsAPI integration
│   ├── gnews_extraction.py       # GNews API integration
│   └── __init__.py
│
├── 🧹 data_formatting/
│   ├── dataframe_cleaning.py     # Data cleaning utilities
│   ├── dataframe_consolidation.py # Merge & deduplicate
│   └── __init__.py
│
├── 🤖 clustering/
│   ├── kmeans_clustering.py      # ML clustering algorithm
│   ├── gemini_labeling.py        # AI category labeling
│   └── __init__.py
│
├── 📊 interaction/
│   ├── html_generation.py        # Dashboard creation
│   ├── email_sender.py           # Email automation
│   └── __init__.py
│
├── 🚀 main_script.py             # Pipeline orchestrator
├── 🔐 environmentvariables.env   # Configuration template
├── 📋 requirements.txt           # Python dependencies
└── 📖 README.md                  # You are here
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- API keys from news providers (free tiers available)
- Gmail account for email delivery

### Installation

```bash
# 1️⃣ Clone the repository
git clone https://github.com/yourusername/news-intelligence-pipeline.git
cd news-intelligence-pipeline

# 2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\Scripts\activate    # Windows

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Configure environment variables
cp environmentvariables.env .env
# Edit .env with your API keys
```

### Configuration

Create a `.env` file with your credentials:

```env
# News API Keys
NEWSDATA_API_KEY=your_newsdata_api_key_here
NEWSAPI_KEY=your_newsapi_key_here
GNEWS_API_KEY=your_gnews_api_key_here

# AI Service
GEMINI_API_KEY=your_gemini_api_key_here

# Email Configuration
EMAIL_USER=your_email@gmail.com
EMAIL_APP_PASSWORD=your_gmail_app_password
```

### Run the Pipeline

```bash
python main_script.py
```

That's it! Check your email for the daily digest. 📬

---

## 🔧 How It Works

### Step 1: Data Extraction 📥

The pipeline queries multiple news APIs simultaneously, collecting the latest headlines and article summaries. Each source is processed independently and formatted into a standardized structure.

### Step 2: Data Formatting 🧹

Raw data undergoes cleaning, normalization, and deduplication. Articles are merged into a unified dataset with consistent fields for downstream processing.

### Step 3: ML Clustering 🤖

K-Means algorithm groups semantically similar headlines together. The optimal number of clusters is determined automatically based on the day's news volume and diversity.

### Step 4: AI Labeling 🏷️

Google Gemini analyzes each cluster and generates descriptive category names that capture the essence of the grouped stories, making the output immediately understandable.

### Step 5: Visualization & Delivery 📊

An interactive HTML dashboard is generated showing:
- **Top 5 most-covered themes** of the day
- Headlines organized by category
- Source attribution and timestamps
- Direct links to original articles

The dashboard is automatically emailed to you in a mobile-friendly format.

---

## 📊 Example Output

<div align="center">

### Sample Daily Digest Categories

| 🏆 Rank | Category | Headlines | Coverage |
|---------|----------|-----------|----------|
| 1 | 🏛️ Global Politics | 47 | ████████░░ 82% |
| 2 | 💹 Market Updates | 31 | ██████░░░░ 61% |
| 3 | 🌍 Climate Action | 28 | █████░░░░░ 54% |
| 4 | 💻 Tech Innovation | 19 | ████░░░░░░ 38% |
| 5 | ⚽ Sports Highlights | 15 | ███░░░░░░░ 29% |

*Actual output includes interactive HTML with expandable sections and styled components*

</div>

---

## 🎨 Customization

### Adjusting Number of Categories

Edit `clustering/kmeans_clustering.py`:

```python
n_clusters = 5  # Change to your preferred number
```

### Filtering by Region

Modify the API calls in `data_extraction/`:

```python
params = {
    'country': 'us,uk,ca',  # Add your target countries
    'language': 'en'
}
```

### Scheduling Automation

Use cron (Linux/Mac):

```bash
# Run daily at 7 AM
0 7 * * * /path/to/venv/bin/python /path/to/main_script.py
```

Or Task Scheduler (Windows) for automated daily execution.

---

## 🔮 Future Enhancements

- [ ] **Sentiment Analysis** - Add emotion detection for each cluster
- [ ] **Stock Ticker Matching** - Automatically identify mentioned companies
- [ ] **Historical Trending** - Track topic evolution over time
- [ ] **Multi-language Support** - Process news in multiple languages
- [ ] **Custom Alerts** - Get notified about specific keywords
- [ ] **GitHub Actions Integration** - Fully cloud-based automation
- [ ] **REST API** - Expose pipeline as a service
- [ ] **Slack/Discord Integration** - Alternative delivery methods

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**[Your Name]**

Data Scientist | AI Enthusiast | Market Intelligence Specialist

*Passionate about applying artificial intelligence to information aggregation, financial analysis, and automation.*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/yourprofile)
[![Twitter](https://img.shields.io/badge/Twitter-Follow-1DA1F2)](https://twitter.com/yourhandle)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-success)](https://yourwebsite.com)

---

<div align="center">

### ⭐ Star this repo if you find it useful!

*Built with ❤️ using Python, Machine Learning, and AI*

</div>
