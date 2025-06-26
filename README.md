### Manual for the tool
#### Installation
```
git clone https://github.com/sebsuenkler/seo-effekt-2
```

Virtual environment (optional):
```
python3 -m venv venv
source seoeffekt_edu/bin/activate
```

Installation of the packages:
```
pip install -r requirements.txt
```

#### Available Scrapers:
- Google_de: Scraper to collect search results from the German version Google
- Bing_de: Scraper to collect search results from the German verson of Bing
- Google_de_Top10: Scraper to collect the top-10 search results from the German version Google
- Bing_de_Top10: Scraper to collect the top-10 search results from the German verson of Bing

#### Setup
- RUN /install/python setup.db.py : To create the database for the tool
- RUN /install/ setup_scrapers.py : To install the necessary libraries and chromedriver to run the scrapers

#### Usage
- Create a csv file (e.g. queries.csv) with search queries (one per row)
- RUN python insert_study.py : to create a new study (type yes to scrape results and select which search engines you want to include)
- RUN python start.py or RUN nohup python start.py & : to run a BackgroundScheduler starting the threads to scrape and classify results; check the tool.log for progress
- RUN python check_status.py : to see if the tool is done
- RUN python export_results.py : export classified search results from the database
- RUN python stop.py : you can stop the tool at any point and restrat it with python start.py

### SEO-Effekt 2: Multiperspektivische Betrachtung des Einflusses der Suchmaschinenoptimie-rung auf die Qualität von Suchergebnissen und das Verhalten der NutzerInnen

The overarching goal of the project is to describe and explain the role of search engine optimization (SEO) from the perspective of the involved actor networks by analyzing search results/search result pages (SERPs) for optimized content, as well as by conducting quantitative and qualitative surveys of search engine users, search engine optimizers, and content providers. Building on the results of the first project phase (project number 417552432), the following sub-goals are pursued: (1) Expansion and refinement of the automatic analysis of search results (inclusion of additional factors, improved weightings, machine learning), (2) Conducting large empirical studies to measure the influence of SEO on topics relevant to opinion formation, (3) Broadening the understanding of SEO to include the perspectives of non-commercial content providers and search engine operators.

In the second project phase, we will further refine the original focus on informative content by concentrating on four areas of content relevant to opinion formation: health, environment, consumer protection, and politics. For these socially relevant areas, we will create extensive search clusters with thematically relevant search queries and search frequencies, and in empirical studies, we will investigate the impact of SEO in these areas. With the now further developed software, large-scale empirical studies will be conducted that realistically represent search queries and search frequencies. The refined automatic analysis of search results allows for a more precise measurement of the influence of search engine optimization and thus to quantify its impact.

As in the first project phase, the project is characterized by its combination of methods from computer science, information science, and social sciences. Through the triangulation of the results from technical and social science analyses, we anticipate deeper insights. These will contribute to theory development; by incorporating the influence of external interests on search results, a new information-seeking model can be developed that depicts realistic behavior of the actors (especially users and search engine operators). In terms of practical application, the results will be relevant, among other things, to issues of consumer protection.

Funding period: 04/01/2022 to 03/31/2025

Funded by: German Research Foundation (DFG – Deutsche Forschungsgemeinschaft), grant number 417552432.

Contacts: [SearchStudies](https://searchstudies.org)

Research data: [OSF](https://osf.io/jyv9r/)

Original rule-based-SEO-Classifier from SEO-Effekt 1: [https://github.com/sebsuenkler/seoeffekt_edu](https://github.com/sebsuenkler/seoeffekt_edu)

# SEO Score Classifier Documentation

## Overview
The SEO Score Classifier is a system designed to evaluate websites based on their search engine optimization (SEO) implementation. It analyzes various aspects of web pages and provides a comprehensive score indicating the level of SEO optimization.

## Scoring Categories and Weights
The classifier divides SEO factors into four main categories, each contributing differently to the final score:

1. Technical SEO (35% weight)
   - Focuses on technical implementation aspects
   - Highest weight due to fundamental importance in search engine crawling and indexing

2. Content Quality (30% weight)
   - Evaluates content structure and optimization
   - Second-highest weight reflecting content's crucial role in SEO

3. User Experience (20% weight)
   - Measures factors affecting user interaction
   - Moderate weight acknowledging growing importance of UX in SEO

4. Meta Elements (15% weight)
   - Assesses basic SEO meta tags and elements
   - Lower weight as these are fundamental but not sufficient alone

## Indicators and Data Collection

### 1. Technical SEO Indicators

#### HTTPS Implementation (20 points)
- **Collection Method**: URL scheme analysis
- **Scoring**: Binary (20 points if present, -20 if absent)
- **Rationale**: Security is crucial for modern SEO and user trust

#### Robots.txt (20 points)
- **Collection Method**: Server root file check
- **Scoring**: Binary (20 points if present, -20 if absent)
- **Rationale**: Essential for search engine crawl control

#### Sitemap (20 points)
- **Collection Method**: XML sitemap detection
- **Scoring**: Binary (20 points if present)
- **Rationale**: Aids search engine content discovery

#### Canonical Tags (20 points)
- **Collection Method**: HTML head tag analysis
- **Scoring**: Binary (20 points if present)
- **Rationale**: Prevents duplicate content issues

#### Structured Data (20 points)
- **Collection Method**: Detection of JSON-LD or Schema.org markup
- **Scoring**: Binary (20 points if present)
- **Rationale**: Enhances search result presentation

### 2. Content Quality Indicators

#### Content Length (30% of category)
- **Collection Method**: Text extraction and word count
- **Scoring**:
  - 100 points: ≥1500 words
  - 80 points: ≥1000 words
  - 60 points: ≥500 words
  - 40 points: ≥300 words
  - Below 300: Proportional scoring
- **Rationale**: Longer, comprehensive content typically ranks better

#### Heading Structure (20% of category)
- **Collection Method**: HTML heading tag analysis
- **Scoring**:
  - 40 points: Single H1 present
  - 30 points: H2/H3 tags present
  - 30 points: H4/H5/H6 tags present
- **Rationale**: Proper content hierarchy improves readability and SEO

#### Link Quality (20% of category)
- **Collection Method**: Anchor tag analysis
- **Scoring**:
  - 50 points: Optimal internal/external ratio (60-80% internal)
  - 30 points: Acceptable ratio (40-90% internal)
  - 50 points: ≥10 total links
  - 25 points: ≥5 total links
- **Rationale**: Balanced link structure improves site authority

#### Keyword Optimization (30% of category)
- **Collection Method**: Content analysis against target keywords
- **Scoring**:
  - 25 points each for:
    * Keyword in URL
    * Keyword in title
    * Keyword in meta description
    * Keyword in headers
- **Rationale**: Strategic keyword placement aids relevancy signals

### 3. User Experience Indicators

#### Loading Speed (40% of UX score)
- **Collection Method**: Page load time measurement
- **Scoring**:
  - 40 points: <2 seconds
  - 30 points: 2-3 seconds
  - 20 points: 3-4 seconds
- **Rationale**: Speed directly impacts user experience and rankings

#### Mobile Responsiveness (20% of UX score)
- **Collection Method**: Viewport meta tag detection
- **Scoring**: Binary (20 points if present)
- **Rationale**: Mobile optimization is crucial for modern SEO

#### Navigation Structure (20% of UX score)
- **Collection Method**: Navigation element analysis
- **Scoring**:
  - 40 points: Navigation menu present
  - 30 points: Footer present
  - 30 points: Forms present
- **Rationale**: Good navigation improves user engagement

#### SSL Security (20% of UX score)
- **Collection Method**: HTTPS verification
- **Scoring**: Binary (20 points if present)
- **Rationale**: Security affects user trust and rankings

### 4. Meta Elements Indicators

#### Title Tag (30% of meta score)
- **Collection Method**: HTML title tag analysis
- **Scoring**:
  - 100 points: 50-60 characters
  - 80 points: 40-70 characters
  - 60 points: 30-80 characters
  - 40 points: Other lengths
  - -30 points: Generic titles
- **Rationale**: Optimal title length improves CTR and rankings

#### Meta Description (30% of meta score)
- **Collection Method**: Meta description tag analysis
- **Scoring**:
  - 100 points: 150-160 characters
  - 80 points: 130-170 characters
  - 60 points: 110-190 characters
  - 40 points: Other lengths
  - -30 points: Generic descriptions
- **Rationale**: Well-crafted descriptions improve CTR

#### Social Tags (40% of meta score)
- **Collection Method**: Open Graph and Twitter card detection
- **Scoring**:
  - 50 points: Open Graph tags present
  - 50 points: Twitter cards present
- **Rationale**: Social optimization improves content sharing

## Bonus Points and Adjustments

### Analytics Tools (+5 points)
- **Collection Method**: Analytics script detection
- **Rationale**: Indicates active site monitoring and optimization

### SEO Tool Detection (Perfect Score)
- **Collection Method**: SEO plugin/tool detection
- **Scoring**: Automatic 100 points
- **Rationale**: Indicates active SEO management

### Tool-specific Bonuses
- Technical SEO:
  * Caching tools: +10 points
  * Micro tools: +5 points
- Content Quality:
  * Content tools: +10 points
  * Social tools: +5 points
- User Experience:
  * Micro tools: +5 points

## Classification Thresholds

The final score determines the SEO optimization classification:

- Most Probably Optimized: ≥75 points
- Probably Optimized: ≥45 points
- Probably Not Optimized: ≥20 points
- Most Probably Not Optimized: <20 points

## Implementation Details

The classifier uses BeautifulSoup and lxml for HTML parsing, making the analysis robust against different HTML structures. The system processes each indicator independently, allowing for granular scoring and detailed feedback.

Error handling ensures that individual indicator failures don't prevent overall scoring, making the system resilient to parsing edge cases.
