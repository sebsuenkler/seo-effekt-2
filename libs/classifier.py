import base64
from datetime import date

today = date.today()

from urllib.parse import urlsplit
from urllib.parse import urlparse
import socket

from lxml import html
from bs4 import BeautifulSoup
import fnmatch


import requests
import os
import inspect
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
from datetime import datetime
from lxml import html
import json

import datetime

current_path = os.path.abspath(__file__)
script_path = os.path.dirname(current_path)
project_path = os.path.dirname(script_path)

if project_path not in sys.path:
    sys.path.insert(0, project_path) 

from libs.sources import *
from libs.log import *
from libs.db import *
from libs.indicators import *

# Import everything from the indicators module

class SEOScorer:
    """Handles SEO scoring logic"""
    def __init__(self):
        # Category weights (total = 100)
        self.category_weights = {
            'technical_seo': 35,
            'content_quality': 30,
            'user_experience': 20,
            'meta_elements': 15
        }
        
        self.classification_thresholds = {
            'most_probably_optimized': 75,
            'probably_optimized': 45,
            'probably_not_optimized': 20,
            'most_probably_not_optimized': 0
        }
        
        self.analytics_score_boost = 5
        
        # Tool weights for bonuses
        self.tool_weights = {
            'technical_seo': {
                'caching_tools': 10,
                'micro_tools': 5
            },
            'content_quality': {
                'content_tools': 10,
                'social_tools': 5
            },
            'user_experience': {
                'micro_tools': 5
            }
        }


    def get_classification(self, score):
        """Determine SEO optimization classification based on score"""
        if score >= self.classification_thresholds['most_probably_optimized']:
            return 'most_probably_optimized'
        elif score >= self.classification_thresholds['probably_optimized']:
            return 'probably_optimized'
        elif score >= self.classification_thresholds['probably_not_optimized']:
            return 'probably_not_optimized'
        else:
            return 'most_probably_not_optimized'

    def calculate_score(self, indicators):
        """Calculate overall SEO score based on indicators"""
        if not indicators:
            return {'total_score': 0}

        # Check if it's not an HTML document
        if not indicators.get('is_html', True):  # Default to True for backward compatibility
            return {
                'total_score': 0,
                'status': 'excluded',
                'reason': indicators.get('reason', 'Non-HTML document excluded from SEO scoring'),
                'content_type': indicators.get('content_type', 'unknown')
            }

        # If SEO plugins are detected, return perfect score
        if indicators.get('tools_seo', []):
            perfect_scores = {cat: 100 for cat in self.category_weights}
            self._last_category_scores = perfect_scores
            return {
                'total_score': 100,
                'category_scores': perfect_scores,
                'classification': 'most_probably_optimized',
                'explanation': self._generate_explanation(indicators)
            }

        # Calculate category scores
        category_scores = {}
        
        # Technical SEO (35%)
        technical_score = self._calculate_technical_score(indicators)
        
        # Content Quality (30%)
        content_score = self._calculate_content_score(indicators)
        
        # User Experience (20%)
        ux_score = self._calculate_user_experience_score(indicators)
        
        # Meta Elements (15%)
        meta_score = self._calculate_meta_score(indicators)
        
        category_scores = {
            'technical_seo': technical_score,
            'content_quality': content_score,
            'user_experience': ux_score,
            'meta_elements': meta_score
        }
        
        # Calculate weighted total
        total_score = sum(score * (self.category_weights[cat] / 100) 
                        for cat, score in category_scores.items())
        
        # Add analytics boost if present
        if indicators.get('tools_analytics', []):
            total_score = min(100, total_score + self.analytics_score_boost)
            
        final_score = round(total_score, 2)
        
        # Store category scores for detailed explanation
        self._last_category_scores = category_scores
        
        return {
            'total_score': final_score,
            'category_scores': category_scores,
            'classification': self.get_classification(final_score),
            'explanation': self._generate_explanation(indicators)
        }

    def _calculate_technical_score(self, indicators):
        """Calculate technical SEO score"""
        score = 0
        
        # Core technical indicators
        if indicators.get('https', False):
            score += 20
        else:
            score -= 20
        if indicators.get('robots_txt', False):
            score += 20
        else:
            score -= 20
        if indicators.get('sitemap', False):
            score += 20
        if indicators.get('canonical', False):
            score += 20
        if 'application/ld+json' in str(indicators) or 'schema.org' in str(indicators):
            score += 20
            
        # Tool bonuses
        if indicators.get('tools_caching', []):
            score += self.tool_weights['technical_seo']['caching_tools']
        if indicators.get('tools_micro', []):
            score += self.tool_weights['technical_seo']['micro_tools']
            
        return min(100, max(0, score)) 

    def _calculate_content_score(self, indicators):
        """Calculate content quality score with meta element consideration"""
        score = 0
        
        # Content indicators (each weighted equally)
        score += indicators.get('content_length_score', 0) * 0.3
        score += indicators.get('heading_structure_score', 0) * 0.2
        score += indicators.get('link_quality_score', 0) * 0.2
        score += indicators.get('keyword_optimization_score', 0) * 0.3
        
        # Image optimization bonus
        score += indicators.get('image_optimization_score', 0) * 0.2
        
        # Penalize if basic meta elements are missing
        if indicators.get('title_score', 0) == 0 or indicators.get('description_score', 0) == 0:
            score = max(0, score - 20)  # Additional content penalty for missing basic meta
        
        # Tool bonuses
        if indicators.get('tools_content', []):
            score += self.tool_weights['content_quality']['content_tools']
        if indicators.get('tools_social', []):
            score += self.tool_weights['content_quality']['social_tools']
                
        return min(100, max(0, score))
    def _calculate_user_experience_score(self, indicators):
        """Calculate user experience score"""
        score = 0
        
        # Loading speed (40% of UX score)
        loading_time = indicators.get('loading_time', -1)
        if 0 < loading_time < 2:
            score += 40
        elif 2 <= loading_time < 3:
            score += 30
        elif 3 <= loading_time < 4:
            score += 20
            
        # Mobile friendliness (20% of UX score)
        if indicators.get('viewport', False):
            score += 20
            
        # Navigation (20% of UX score)
        score += (indicators.get('navigation_score', 0) * 0.2)
        
        # SSL security (20% of UX score)
        if indicators.get('https', False):
            score += 20
            
        # Tool bonus
        if indicators.get('tools_micro', []):
            score += self.tool_weights['user_experience']['micro_tools']
            
        return min(100, max(0, score)) 

    def _calculate_meta_score(self, indicators):
        """Calculate meta elements score with penalties for missing elements"""
        score = 0
        penalties = 0
        
        # Title tag (30%)
        title_score = indicators.get('title_score', 0)
        if title_score == 0:  # Missing title
            penalties += 30
        else:
            score += title_score * 0.3
        
        # Meta description (30%)
        desc_score = indicators.get('description_score', 0)
        if desc_score == 0:  # Missing description
            penalties += 30
        else:
            score += desc_score * 0.3
        
        # Social tags (40%)
        social_score = indicators.get('social_tags_score', 0)
        if social_score == 0:  # No social tags
            penalties += 20
        else:
            score += social_score * 0.4
        
        # Additional meta elements
        if not indicators.get('viewport', False):
            penalties += 10
        else:
            score += 10
            
        if not indicators.get('h1', False):
            penalties += 10
        else:
            score += 10

        # Apply penalties and ensure score doesn't go below 0
        final_score = max(0, score - penalties)
        return min(100, final_score)

    def _generate_explanation(self, indicators):
        """Generate detailed human-readable explanation of the score"""
        # Check if it's not HTML
        if not indicators.get('is_html', True):
            return indicators.get('reason', 'Non-HTML document excluded from SEO scoring')

        explanations = []
        
        # Tools and plugins detection
        if indicators.get('tools_analytics', []):
            explanations.append(f"Analytics tools detected (+{self.analytics_score_boost} points)")
        
        if indicators.get('tools_seo', []):
            explanations.append("SEO tools detected (major positive factor)")
            
        social_tools = indicators.get('tools_social', [])
        if social_tools:
            explanations.append(f"Social media tools detected: {len(social_tools)} (+{min(len(social_tools) * 2, 3)} points)")
            
        # Technical details
        loading_time = indicators.get('loading_time', -1)
        if loading_time > 0:
            explanations.append(f"Page loading time: {loading_time:.1f}s")
        
        # Category score breakdowns
        if hasattr(self, '_last_category_scores'):
            explanations.append("\nScore breakdown by category:")
            
            # Technical SEO
            tech_score = self._last_category_scores['technical_seo']
            tech_weight = self.category_weights['technical_seo']
            tech_contribution = round(tech_score * (tech_weight / 100), 2)
            explanations.append(f"- Technical SEO: {tech_score:.1f}/100 (weight: {tech_weight}%, contributes {tech_contribution} points)")
            
            # Content Quality
            content_score = self._last_category_scores['content_quality']
            content_weight = self.category_weights['content_quality']
            content_contribution = round(content_score * (content_weight / 100), 2)
            explanations.append(f"- Content Quality: {content_score:.1f}/100 (weight: {content_weight}%, contributes {content_contribution} points)")
            
            # User Experience
            ux_score = self._last_category_scores['user_experience']
            ux_weight = self.category_weights['user_experience']
            ux_contribution = round(ux_score * (ux_weight / 100), 2)
            explanations.append(f"- User Experience: {ux_score:.1f}/100 (weight: {ux_weight}%, contributes {ux_contribution} points)")
            
            # Meta Elements
            meta_score = self._last_category_scores['meta_elements']
            meta_weight = self.category_weights['meta_elements']
            meta_contribution = round(meta_score * (meta_weight / 100), 2)
            explanations.append(f"- Meta Elements: {meta_score:.1f}/100 (weight: {meta_weight}%, contributes {meta_contribution} points)")
            
            # Calculate total
            total_base = sum([tech_contribution, content_contribution, ux_contribution, meta_contribution])
            explanations.append(f"\nBase score: {total_base:.2f}")
            
            # Analytics boost explanation if applicable
            if indicators.get('tools_analytics', []):
                explanations.append(f"Analytics boost: +{self.analytics_score_boost}")
                explanations.append(f"Final score: {min(100, total_base + self.analytics_score_boost):.2f}")
                
        return ". ".join(explanations)

def analyze_content_length(soup):
    """Analyze content length and return score"""
    text = soup.get_text()
    words = len(text.split())
    
    if words >= 1500:
        return 100
    elif words >= 1000:
        return 80
    elif words >= 500:
        return 60
    elif words >= 300:
        return 40
    else:
        return max(0, (words / 300) * 40)

def analyze_heading_structure(soup):
    """Analyze heading structure and return score"""
    score = 0
    if len(soup.find_all('h1')) == 1:
        score += 40
    if soup.find_all(['h2', 'h3']):
        score += 30
    if soup.find_all(['h4', 'h5', 'h6']):
        score += 30
    return score

def analyze_link_quality(internal_links, external_links):
    """Analyze link quality and structure"""
        
    score = 0
    total_links = internal_links + external_links
    
    # Score based on internal/external link ratio
    if internal_links + external_links > 0:
        ratio = internal_links / (internal_links + external_links)
        if 0.6 <= ratio <= 0.8:
            score += 50
        elif 0.4 <= ratio <= 0.9:
            score += 30
        
    # Score based on total number of links
    if total_links >= 10:
        score += 50
    elif total_links >= 5:
        score += 25
        
    return score

def analyze_images(soup):
    """Calculate percentage of images with alt text"""
    images = soup.find_all('img')
    if not images:
        return 0
    images_with_alt = len([img for img in images if img.get('alt')])
    return round((images_with_alt / len(images)) * 100)

def analyze_navigation(soup):
    """Analyze navigation structure"""
    score = 0
    if soup.find(['nav', 'menu']):
        score += 40
    if soup.find('footer'):
        score += 30
    if soup.find('form'):
        score += 30
    return score

def analyze_title(soup):
    """Analyze title tag with stricter scoring"""
    title = soup.find('title')
    if not title:
        return 0, None
        
    title_text = title.text.strip()
    if not title_text:  # Empty title tag
        return 0, None
        
    length = len(title_text)
    score = 0
    
    if 50 <= length <= 60:
        score = 100
    elif 40 <= length <= 70:
        score = 80
    elif 30 <= length <= 80:
        score = 60
    else:
        score = 40
        
    # Additional check for common SEO issues
    if title_text.lower() in ['untitled', 'home', 'page']:
        score = max(0, score - 30)  # Penalty for generic titles
        
    return score, title_text

def analyze_description(soup):
    """Analyze meta description with stricter scoring"""
    desc = soup.find('meta', {'name': 'description'})
    if not desc:
        return 0, None
        
    content = desc.get('content', '')
    if not content.strip():  # Empty description
        return 0, None
        
    length = len(content)
    score = 0
    
    if 150 <= length <= 160:
        score = 100
    elif 130 <= length <= 170:
        score = 80
    elif 110 <= length <= 190:
        score = 60
    else:
        score = 40
        
    # Additional check for common SEO issues
    if content.lower() in ['description', 'website description']:
        score = max(0, score - 30)  # Penalty for generic descriptions
        
    return score, content

def check_social_tags(soup):
    """Check for social media meta tags"""
    score = 0
    og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
    twitter_tags = soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')})
    
    if og_tags:
        score += 50
    if twitter_tags:
        score += 50
        
    return score, {
        'og_tags': [tag.get('property', '') for tag in og_tags],
        'twitter_tags': [tag.get('name', '') for tag in twitter_tags]
    }

def analyze_keyword_usage(soup, url, query):
    """Analyze keyword usage in content"""
    if not query:
        return analyze_general_content_optimization(soup)
    return analyze_specific_keyword(soup, url, query)

def analyze_general_content_optimization(soup):
    """Analyze general content optimization without specific keyword"""
    score = 0
    reasons = []
    
    # Check title optimization
    title = soup.find('title')
    if title and 20 <= len(title.text.strip()) <= 70:
        score += 25
        reasons.append('Optimized title length')
        
    # Check meta description
    meta_desc = soup.find('meta', {'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        content = meta_desc.get('content')
        if 120 <= len(content) <= 160:
            score += 25
            reasons.append('Optimized description length')
            
    # Check heading structure
    headings = soup.find_all(['h1', 'h2', 'h3'])
    if headings:
        if len(soup.find_all('h1')) == 1:
            score += 25
            reasons.append('Proper H1 usage')
        if len(headings) >= 3:
            score += 25
            reasons.append('Good heading structure')
            
    return score, reasons

def analyze_specific_keyword(soup, url, query):
    """Analyze keyword-specific optimization"""
    score = 0
    reasons = []
    query = query.lower()
    
    # URL contains keyword
    if query in url.lower():
        score += 25
        reasons.append('Keyword in URL')
        
    # Title contains keyword
    title = soup.find('title')
    if title and query in title.text.lower():
        score += 25
        reasons.append('Keyword in title')
        
    # Meta description contains keyword
    meta_desc = soup.find('meta', {'name': 'description'})
    if meta_desc and query in meta_desc.get('content', '').lower():
        score += 25
        reasons.append('Keyword in description')
        
    # Headers contain keyword
    headers = soup.find_all(['h1', 'h2', 'h3'])
    if any(query in h.text.lower() for h in headers):
        score += 25
        reasons.append('Keyword in headers')
        
    return score, reasons


def classify_result(code, url, main, query, result_id, scorer):

    print(url)
    
    def check_progress_classification():
        connection = connect_to_db()
        cursor = connection.cursor()
        dup = False
        data = cursor.execute("SELECT result_id FROM EVALUATION WHERE result_id = ? LIMIT 1",(result_id,))
        connection.commit()
        for row in data:
            dup = row
        close_connection_to_db(connection)
        if not dup:
            return True
        else:
            return False


    def check_classification_dup(result_id):
        connection = connect_to_db()
        cursor = connection.cursor()
        dup = False
        data = cursor.execute("SELECT result_id FROM CLASSIFICATION WHERE result_id = ?",(result_id,))
        connection.commit()
        for row in data:
            dup = row
        close_connection_to_db(connection)
        if not dup:
            return True
        else:
            return False

    def check_insert_result_dup(module):
        connection = connect_to_db()
        cursor = connection.cursor()
        dup = False
        data = cursor.execute("SELECT result_id FROM EVALUATION WHERE result_id = ? AND module = ?",(result_id, module,))
        connection.commit()
        for row in data:
            dup = row
        close_connection_to_db(connection)
        if not dup:
            return True
        else:
            return False

    def insert_results(module, insert_result):
        connection = connect_to_db()
        cursor = connection.cursor()
        sql = 'INSERT INTO EVALUATION(result_id, module, value, date) values(?,?,?,?)'
        data = (result_id, module, insert_result, today)
        cursor.execute(sql, data)
        connection.commit()
        close_connection_to_db(connection)

    if check_progress_classification():

        if source !="error":


            # Parse content
            soup = BeautifulSoup(code, 'lxml')

            print(f"Beginne die Klassifizierung von: {url}")
            
            # Collect all indicators
            indicators = {}
            
            # Content Analysis
            indicators['content_length_score'] = analyze_content_length(soup)
            indicators['heading_structure_score'] = analyze_heading_structure(soup)
            
            # Link Analysis

            hyperlinks = identify_hyperlinks(get_hyperlinks(code, main), main)
            indicators['internal_links'] = hyperlinks["internal"]
            indicators['external_links'] = hyperlinks["external"]

            link_score = analyze_link_quality(hyperlinks["internal"], hyperlinks["external"])
            indicators['link_quality_score'] = link_score 
            
            # Image Analysis
            indicators['image_optimization_score'] = analyze_images(soup)
            
            # Navigation Analysis
            indicators['navigation_score'] = analyze_navigation(soup)
            
            # Title Analysis
            title_score, title_text = analyze_title(soup)
            indicators['title_score'] = title_score
            indicators['title_text'] = title_text if title_text else ''
            
            # Description Analysis
            desc_score, desc_text = analyze_description(soup)
            indicators['description_score'] = desc_score
            indicators['description_text'] = desc_text if desc_text else ''
            
            # Social Tags Analysis
            social_score, social_tags = check_social_tags(soup)
            indicators['social_tags_score'] = social_score
            indicators['social_tags'] = social_tags
            
            # Keyword Analysis
            if query:
                keyword_score, keyword_reasons = analyze_keyword_usage(soup, url, query)
                indicators['keyword_optimization_score'] = keyword_score
                indicators['keyword_optimization_reasons'] = keyword_reasons
            
            # Original indicators from seo_rule_based.py
            plugins = identify_plugins(code)
            indicators.update({
                'tools_analytics': plugins['tools analytics'],
                'tools_seo': plugins['tools seo'],
                'tools_caching': plugins['tools caching'],
                'tools_social': plugins['tools social'],
                'tools_ads': plugins['tools ads']
            })
            
            # Technical indicators
            indicators['robots_txt'] = identify_robots_txt(main)
            indicators['loading_time'] = calculate_loading_time(url)
            
            # Parse URL and links
            parsed_url = urlparse(url)
            indicators['https'] = parsed_url.scheme == 'https'
            

            
            # Additional technical indicators
            indicators.update({
                'url_length': identify_url_length(url),
                'micros': identify_micros(code),
                'sitemap': identify_sitemap(code),
                'og': identify_og(code),
                'viewport': identify_viewport(code),
                'wordpress': identify_wordpress(code),
                'canonical': identify_canonical(code),
                'nofollow': identify_nofollow(code),
                'h1': identify_h1(code)
            })

            score_results = scorer.calculate_score(indicators)

            indicators['technical_score'] = f"{score_results['category_scores']['technical_seo']}"
            indicators['content_score'] = f"{score_results['category_scores']['content_quality']}"
            indicators['ux_score'] = f"{score_results['category_scores']['user_experience']}"
            indicators['meta_score'] = f"{score_results['category_scores']['meta_elements']}"

            classification_score = f"{score_results['total_score']}"
            
            classification_result = scorer.get_classification(score_results['total_score'])
            
            print(f"Klassifizierung von {url} abgeschlossen.")
            print(f"SEO-Score: {classification_score}")
            print(f"SEO-Ergebnis: {classification_result}")

            for key, value in indicators.items():

                if type(value) != list and type(value) is not dict:
                    module = key
                    insert_result = str(value)

                    if check_insert_result_dup(module):
                        insert_results(module, insert_result)
                else:
                    if (type(value) is list):
                        module = key
                        insert_result = ", ".join(value)

                        if check_insert_result_dup(module):
                            insert_results(module, insert_result)

                    if (type(value) is dict):
                        for k, v in value.items():
                            module = k
                            insert_result = v
                            if (type(v) is list):
                                insert_result = ", ".join(v)
                            else:
                                insert_result = str(v)

                            if check_insert_result_dup(module):
                                insert_results(module, insert_result)

        if source == "error":
            classification_result = "error"
            classification_value = "error"

        if check_classification_dup(result_id):
            connection = connect_to_db()
            cursor = connection.cursor()
            sql = 'INSERT INTO classification(result_id, classification, value, date) values(?,?,?,?)'
            data = (result_id, classification_result, classification_score, today)
            cursor.execute(sql, data)
            connection.commit()
            close_connection_to_db(connection)

if __name__ == "__main__":
    scorer = SEOScorer()
    connection = connect_to_db()
    cursor = connection.cursor()
    source_results = cursor.execute("SELECT source, url, main_url, query, source.result_id  FROM source, search_result, query WHERE source.result_id = search_result.id AND search_result.query_id = query.id AND progress = 1 AND source.result_id = search_result.id AND source.result_id NOT IN (SELECT classification.result_id FROM classification) AND source.source IS NOT NULL ORDER BY RANDOM() LIMIT 5")
    connection.commit()

    for s in source_results:
        source = s[0]
        if source != "error":
            try:
                source = decode_source(s[0])
            except:
                source = "error"

        url = s[1]
        main_url = s[2]
        query = s[3]
        result_id = s[4]

        timestamp = datetime.datetime.now()
        timestamp = timestamp.strftime("%d-%m-%Y, %H:%M:%S")

        write_to_log(timestamp, "Classify "+str(url))

        classify_result(source, url, main_url, query, result_id, scorer)
    
    close_connection_to_db(connection)
