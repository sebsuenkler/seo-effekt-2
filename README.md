# SEO-Effekt 2: SEO Analysis and Scoring Tool

[![Project Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) <!-- Optional: Add more relevant badges -->

This repository contains the software developed for the "SEO-Effekt 2" research project. The tool allows for scraping search engine results, analyzing web pages for SEO characteristics, and classifying their optimization level based on a detailed scoring model.

**Part of the DFG-funded research project "SEO-Effekt 2: Multiperspektivische Betrachtung des Einflusses der Suchmaschinenoptimierung auf die Qualität von Suchergebnissen und das Verhalten der NutzerInnen."** (Grant No. 417552432)

---

## Table of Contents

1.  [Overview](#overview-of-the-tool)
2.  [Features](#features)
3.  [Prerequisites](#prerequisites)
4.  [Installation & Setup](#installation--setup)
5.  [Usage Workflow](#usage-workflow)
6.  [SEO Score Classifier Methodology](#seo-score-classifier-methodology)
    *   [Scoring Categories and Weights](#scoring-categories-and-weights)
    *   [Indicators and Data Collection](#indicators-and-data-collection)
    *   [Bonus Points and Adjustments](#bonus-points-and-adjustments)
    *   [Classification Thresholds](#classification-thresholds)
    *   [Implementation Details](#implementation-details)
7.  [About the SEO-Effekt 2 Research Project](#about-the-seo-effekt-2-research-project)
8.  [Funding & Links](#funding--links)

---

## Overview of the Tool

This tool is designed to:
*   Collect search results from Google and Bing for a given set of queries.
*   Analyze the retrieved web pages against a comprehensive set of SEO indicators.
*   Calculate an SEO score and classify the optimization level of each page.
*   Store and export the collected data and analysis results.

It facilitates empirical research on the impact of SEO on search result quality and user behavior.

---

## Features

*   **Automated SERP Scraping:**
    *   `Google_de`: Scrapes search results from Google (German version).
    *   `Bing_de`: Scrapes search results from Bing (German version).
    *   `Google_de_Top10`: Scrapes the top 10 search results from Google (German version).
    *   `Bing_de_Top10`: Scrapes the top 10 search results from Bing (German version).
*   **Comprehensive SEO Analysis:** Evaluates technical SEO, content quality, user experience, and meta elements.
*   **Study Management:** Allows creation and management of distinct data collection studies.
*   **Background Processing:** Supports running scraping and classification tasks in the background.
*   **Data Export:** Enables exporting of classified search results.
*   **SQLite Database:** Stores all collected queries, results, and analyses.

---

## Prerequisites

*   Python 3 (ensure it's added to your PATH)
*   Git

---

## Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/sebsuenkler/seo-effekt-2.git
    cd seo-effekt-2
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows (Git Bash or similar):
        ```bash
        python -m venv venv
        source venv/Scripts/activate
        ```
    *   On Windows (Command Prompt):
        ```bash
        python -m venv venv
        venv\Scripts\activate.bat
        ```

3.  **Install Required Packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initial Tool Setup:**
    *   **Create the SQLite Database:**
        ```bash
        python install/setup_db.py
        ```
    *   **Install Scraper Dependencies (incl. Chromedriver):**
        ```bash
        python install/setup_scrapers.py
        ```
        *(This script will attempt to download the appropriate Chromedriver. Ensure you have Google Chrome installed.)*

---

## Usage Workflow

1.  **Prepare Search Queries:**
    Create a CSV file (e.g., `queries.csv`) with one search query per row. Example:
    ```csv
    how to bake a cake
    best python ide
    latest tech news
    ```

2.  **Create a New Study and Initiate Scraping:**
    This script will prompt you to name the study, confirm if you want to start scraping, and select the search engines to use.
    ```bash
    python insert_study.py
    ```
    *(Follow the on-screen prompts. When asked, type `yes` to scrape results and select the desired search engines.)*

3.  **Start the Scraping and Classification Process:**
    This runs a background scheduler that manages the scraping and classification threads.
    *   To run in the foreground (output to console):
        ```bash
        python start.py
        ```
    *   To run in the background (on Linux/macOS, output logged to `tool.log`):
        ```bash
        nohup python start.py &
        ```
    Check `tool.log` for progress updates.

4.  **Check the Status:**
    See if the scraping and classification tasks are complete for the active study.
    ```bash
    python check_status.py
    ```

5.  **Export Results:**
    Once the tool is done, export the classified search results from the database.
    ```bash
    python export_results.py
    ```
    *(This will typically create a CSV or Excel file with the results.)*

6.  **Stop the Tool (If Running in Background):**
    You can stop the background process at any point.
    ```bash
    python stop.py
    ```
    You can restart it later with `python start.py`, and it should resume based on the database state.

---

## SEO Score Classifier Methodology

The SEO Score Classifier is a system designed to evaluate websites based on their search engine optimization (SEO) implementation. It analyzes various aspects of web pages and provides a comprehensive score indicating the level of SEO optimization.

### Scoring Categories and Weights

The classifier divides SEO factors into four main categories, each contributing differently to the final score:

1.  **Technical SEO (35% weight)**
    *   Focuses on technical implementation aspects.
    *   Highest weight due to fundamental importance in search engine crawling and indexing.
2.  **Content Quality (30% weight)**
    *   Evaluates content structure and optimization.
    *   Second-highest weight reflecting content's crucial role in SEO.
3.  **User Experience (20% weight)**
    *   Measures factors affecting user interaction.
    *   Moderate weight acknowledging growing importance of UX in SEO.
4.  **Meta Elements (15% weight)**
    *   Assesses basic SEO meta tags and elements.
    *   Lower weight as these are fundamental but not sufficient alone.

### Indicators and Data Collection

*(This section details the specific metrics used. For brevity in this overview, only main indicators are listed. Refer to the source code or more detailed project documentation for exhaustive scoring logic.)*

#### 1. Technical SEO Indicators
*   **HTTPS Implementation (20 points):** URL scheme analysis. Binary (20 if present, -20 if absent).
*   **Robots.txt (20 points):** Server root file check. Binary (20 if present, -20 if absent).
*   **Sitemap (20 points):** XML sitemap detection. Binary (20 if present).
*   **Canonical Tags (20 points):** HTML head tag analysis. Binary (20 if present).
*   **Structured Data (20 points):** Detection of JSON-LD or Schema.org. Binary (20 if present).

#### 2. Content Quality Indicators
*   **Content Length (30% of category):** Word count. Scores based on thresholds (e.g., ≥1500 words = 100 pts).
*   **Heading Structure (20% of category):** H1, H2/H3, H4-H6 presence and structure.
*   **Link Quality (20% of category):** Internal/external link ratio and total link count.
*   **Keyword Optimization (30% of category):** Keyword presence in URL, title, meta description, headers.

#### 3. User Experience Indicators
*   **Loading Speed (40% of UX score):** Page load time. Scores based on speed (e.g., <2s = 40 pts).
*   **Mobile Responsiveness (20% of UX score):** Viewport meta tag detection. Binary (20 if present).
*   **Navigation Structure (20% of UX score):** Presence of navigation menus, footers, forms.
*   **SSL Security (20% of UX score):** HTTPS verification (overlaps with Technical, reinforces UX impact). Binary (20 if present).

#### 4. Meta Elements Indicators
*   **Title Tag (30% of meta score):** Optimal length (50-60 chars = 100 pts), penalties for generic titles.
*   **Meta Description (30% of meta score):** Optimal length (150-160 chars = 100 pts), penalties for generic descriptions.
*   **Social Tags (40% of meta score):** Open Graph and Twitter card detection. (50 pts each if present).

### Bonus Points and Adjustments

*   **Analytics Tools:** +5 points (e.g., Google Analytics detected).
*   **SEO Tool Detection:** Automatic 100 points (e.g., Yoast SEO, Rank Math detected).
*   **Tool-specific Bonuses:**
    *   Technical SEO: Caching tools (+10), Micro tools (+5).
    *   Content Quality: Content tools (+10), Social tools (+5).
    *   User Experience: Micro tools (+5).

### Classification Thresholds

The final score determines the SEO optimization classification:

*   **Most Probably Optimized:** ≥75 points
*   **Probably Optimized:** ≥45 points
*   **Probably Not Optimized:** ≥20 points
*   **Most Probably Not Optimized:** <20 points

### Implementation Details

The classifier uses BeautifulSoup and lxml for HTML parsing, making the analysis robust against different HTML structures. The system processes each indicator independently, allowing for granular scoring and detailed feedback. Error handling ensures that individual indicator failures don't prevent overall scoring, making the system resilient to parsing edge cases.

---

## About the SEO-Effekt 2 Research Project

**Title:** SEO-Effekt 2: Multiperspektivische Betrachtung des Einflusses der Suchmaschinenoptimierung auf die Qualität von Suchergebnissen und das Verhalten der NutzerInnen
*(English: SEO-Effect 2: A Multi-Perspective View on the Influence of Search Engine Optimization on the Quality of Search Results and User Behavior)*

The overarching goal of the project is to describe and explain the role of search engine optimization (SEO) from the perspective of the involved actor networks by analyzing search results/search result pages (SERPs) for optimized content, as well as by conducting quantitative and qualitative surveys of search engine users, search engine optimizers, and content providers. Building on the results of the first project phase (project number 417552432), the following sub-goals are pursued:
(1) Expansion and refinement of the automatic analysis of search results (inclusion of additional factors, improved weightings, machine learning).
(2) Conducting large empirical studies to measure the influence of SEO on topics relevant to opinion formation.
(3) Broadening the understanding of SEO to include the perspectives of non-commercial content providers and search engine operators.

In the second project phase, we will further refine the original focus on informative content by concentrating on four areas of content relevant to opinion formation: health, environment, consumer protection, and politics. For these socially relevant areas, we will create extensive search clusters with thematically relevant search queries and search frequencies, and in empirical studies, we will investigate the impact of SEO in these areas. With the now further developed software, large-scale empirical studies will be conducted that realistically represent search queries and search frequencies. The refined automatic analysis of search results allows for a more precise measurement of the influence of search engine optimization and thus to quantify its impact.

As in the first project phase, the project is characterized by its combination of methods from computer science, information science, and social sciences. Through the triangulation of the results from technical and social science analyses, we anticipate deeper insights. These will contribute to theory development; by incorporating the influence of external interests on search results, a new information-seeking model can be developed that depicts realistic behavior of the actors (especially users and search engine operators). In terms of practical application, the results will be relevant, among other things, to issues of consumer protection.

---

## Funding & Links

*   **Funding Period:** 04/01/2022 to 03/31/2025
*   **Funded by:** German Research Foundation (DFG – Deutsche Forschungsgemeinschaft), grant number 417552432.
*   **Project Contact & Information:** [SearchStudies.org](https://searchstudies.org)
*   **Research Data (OSF):** [osf.io/jyv9r/](https://osf.io/jyv9r/)
*   **Original Rule-Based SEO Classifier (SEO-Effekt 1):** [github.com/sebsuenkler/seoeffekt_edu](https://github.com/sebsuenkler/seoeffekt_edu)

---
<!-- Optional: Add a License section if you have one -->
<!--
## License
This project is licensed under the [MIT License](LICENSE.md) - see the LICENSE.md file for details.
-->