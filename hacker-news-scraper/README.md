# Hacker News Scraper

A robust Python scraper for extracting stories from Hacker News front page with detailed error handling and verbose logging.

## Features

- **Comprehensive Data Extraction**: Captures title, URL, score, author, comments, and rank
- **Robust Error Handling**: Graceful handling of missing data and parsing errors
- **Detailed Logging**: Verbose output for debugging and monitoring
- **JSON Output**: Clean structured data export with timestamps
- **Production Ready**: Handles edge cases and malformed data

## Demo Output

The scraper extracts data like this sample:
```json
{
  "rank": 1,
  "title": "Happy 0b100000th Birthday, Debian",
  "url": "https://lists.debian.org/debian-devel-announce/2025/08/msg00006.html",
  "score": 48,
  "author": "pabs3",
  "comments": 5,
  "scraped_at": "2025-08-22T04:44:26.698506"
}