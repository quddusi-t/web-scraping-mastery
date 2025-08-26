#!/usr/bin/env python3
"""
🚀 HACKER NEWS PRODUCTION SCRAPER - DEBUGGED VERSION
Based on super debug findings - no more hide and seek!
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

def scrape_hacker_news():
    print("🚀 HACKER NEWS PRODUCTION SCRAPER")
    print("Based on your DevTools detective work!")
    print("=" * 50)
    
    url = "https://news.ycombinator.com"
    
    # Get the page
    try:
        print("🔍 Scraping Hacker News front page...")
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        print("=" * 50)
        print(f"✅ Status: {response.status_code}")
        print(f"📏 Page size: {len(response.text):,} characters")
        
    except requests.RequestException as e:
        print(f"❌ Failed to fetch page: {e}")
        return []
    
    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find story containers
    story_containers = soup.find_all('tr', class_='athing')
    print(f"🔍 Found {len(story_containers)} story containers")
    
    stories = []
    failed_extractions = 0
    
    # Extract stories with VERBOSE error reporting
    for i, container in enumerate(story_containers):
        try:
            print(f"\n🔄 Processing story #{i+1} (ID: {container.get('id', 'UNKNOWN')})")
            
            # Extract title and URL
            title_elem = container.select_one('td.title a')
            if not title_elem:
                print(f"  ❌ No title element found in container {i+1}")
                failed_extractions += 1
                continue
                
            title = title_elem.get_text(strip=True)
            url = title_elem.get('href', '')
            
            if not title:
                print(f"  ❌ Empty title in container {i+1}")
                failed_extractions += 1
                continue
            
            print(f"  ✅ Title: {title[:50]}{'...' if len(title) > 50 else ''}")
            print(f"  ✅ URL: {url[:50]}{'...' if len(url) > 50 else ''}")
            
            # Find metadata row
            metadata_row = container.find_next_sibling('tr')
            score = 0
            author = "Unknown"
            comments = 0
            
            if metadata_row:
                print(f"  ✅ Found metadata row")
                
                # Extract score - BE FORGIVING
                try:
                    score_elem = metadata_row.select_one('.score')
                    if score_elem:
                        score_text = score_elem.get_text()
                        score_match = re.search(r'(\d+)', score_text)
                        if score_match:
                            score = int(score_match.group(1))
                            print(f"  ✅ Score: {score}")
                        else:
                            print(f"  ⚠️  Score element found but no number: '{score_text}'")
                    else:
                        print(f"  ⚠️  No score element found")
                except Exception as e:
                    print(f"  ⚠️  Score extraction error: {e}")
                
                # Extract author - BE FORGIVING  
                try:
                    author_elem = metadata_row.select_one('.hnuser')
                    if author_elem:
                        author = author_elem.get_text(strip=True)
                        print(f"  ✅ Author: {author}")
                    else:
                        print(f"  ⚠️  No author found")
                except Exception as e:
                    print(f"  ⚠️  Author extraction error: {e}")
                
                # Extract comments - BE FORGIVING
                try:
                    comment_links = metadata_row.select('a[href*="item"]')
                    if comment_links:
                        for link in comment_links:
                            link_text = link.get_text().lower()
                            if 'comment' in link_text:
                                comment_match = re.search(r'(\d+)', link.get_text())
                                if comment_match:
                                    comments = int(comment_match.group(1))
                                    print(f"  ✅ Comments: {comments}")
                                    break
                        else:
                            print(f"  ⚠️  Comment links found but no comment count")
                    else:
                        print(f"  ⚠️  No comment links found")
                except Exception as e:
                    print(f"  ⚠️  Comments extraction error: {e}")
                    
            else:
                print(f"  ⚠️  No metadata row found")
            
            # Create story object - ALWAYS INCLUDE if we have title
            story = {
                'rank': i + 1,
                'title': title,
                'url': url,
                'score': score,
                'author': author,
                'comments': comments,
                'scraped_at': datetime.now().isoformat()
            }
            
            stories.append(story)
            print(f"  🎯 Story #{i+1}: SUCCESSFULLY ADDED!")
            
        except Exception as e:
            print(f"  💥 CRITICAL ERROR in story #{i+1}: {e}")
            print(f"  🔍 Container HTML preview: {str(container)[:100]}...")
            failed_extractions += 1
            continue
    
    print("=" * 50)
    print(f"🎯 Successfully extracted {len(stories)} stories!")
    if failed_extractions > 0:
        print(f"⚠️  Failed extractions: {failed_extractions}")
    
    if len(stories) == 0:
        print("❌ No stories extracted. Check the selectors or site structure.")
        return []
    
    # Save results
    try:
        filename = f"hacker_news_stories_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stories, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(stories)} stories to: {filename}")
        
        # Also show first few stories
        print("\n📊 FIRST 3 STORIES PREVIEW:")
        print("-" * 30)
        for i, story in enumerate(stories[:3]):
            print(f"\n{i+1}. {story['title']}")
            print(f"   🔗 {story['url']}")
            print(f"   ⭐ {story['score']} points | 👤 {story['author']} | 💬 {story['comments']} comments")
            
    except Exception as e:
        print(f"❌ Error saving file: {e}")
    
    return stories

if __name__ == "__main__":
    stories = scrape_hacker_news()
    print(f"\n🏆 FINAL RESULT: {len(stories)} stories successfully scraped!")
    if len(stories) > 0:
        print("🎉 Victory! Your DevTools detective work paid off!")