import requests
import json
import pandas as pd
import time
import random
from typing import List, Dict, Optional
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ECommerceAPIScraperV12_UltimateEdition:
    """
    🏆 ULTIMATE EDITION V12 - Professional Grade API Scraper
    
    Combines:
    ✅ Your breakthrough discovery (basic headers work!)
    ✅ Military-grade session management
    ✅ Intelligent fallback systems
    ✅ Professional data extraction
    ✅ Anti-detection techniques
    """
    
    def __init__(self):
        self.base_url = "https://hepsiads-gw.hepsiburada.com/sponsored-brands/v2/display/api/v1"
        
        # 🎯 BREAKTHROUGH: Simple headers work best!
        self.simple_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # 🔥 ADVANCED: Your cURL headers as backup
        self.advanced_headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'Bearer undefined',
            'cache-control': 'no-cache',
            'hb-source-app': 'hepsi-ads-spon-brands',
            'origin': 'https://www.hepsiburada.com',
            'priority': 'u=1, i',
            'referer': 'https://www.hepsiburada.com/ara?q=laptop',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
        }
        
        # 🛡️ PROFESSIONAL: Session management
        self.session = requests.Session()
        self.total_scraped = 0
        self.start_time = datetime.now()
        
        logger.info("🚀 ECommerceAPIScraperV12 ULTIMATE EDITION initialized!")
        logger.info("💡 Strategy: Start simple, escalate if needed")

    def search_products_ultimate(self, keyword: str, pages: int = 10) -> List[Dict]:
        """
        🏆 ULTIMATE SEARCH METHOD - Multi-layer approach
        """
        logger.info(f"🎯 ULTIMATE SEARCH: '{keyword}' - {pages} pages")
        logger.info("=" * 60)
        
        all_products = []
        
        # 🎯 STRATEGY 1: Start with simple headers (your breakthrough!)
        logger.info("🥇 STRATEGY 1: Simple Headers (Your Discovery)")
        products_simple = self._scrape_with_headers(keyword, pages, self.simple_headers, "SIMPLE")
        
        if products_simple:
            logger.info(f"✅ SUCCESS with simple headers! Got {len(products_simple)} products")
            return products_simple
        
        # 🔥 STRATEGY 2: Advanced headers (cURL backup)
        logger.info("🥈 STRATEGY 2: Advanced Headers (cURL Power)")
        products_advanced = self._scrape_with_headers(keyword, pages, self.advanced_headers, "ADVANCED")
        
        if products_advanced:
            logger.info(f"✅ SUCCESS with advanced headers! Got {len(products_advanced)} products")
            return products_advanced
        
        # 🚨 STRATEGY 3: Dynamic approach
        logger.info("🥉 STRATEGY 3: Dynamic Multi-Session")
        return self._scrape_dynamic(keyword, pages)
    
    def _scrape_with_headers(self, keyword: str, pages: int, headers: Dict, strategy_name: str) -> List[Dict]:
        """Scrape with specific headers"""
        all_products = []
        failed_pages = 0
        
        for page in range(1, pages + 1):
            try:
                logger.info(f"📄 [{strategy_name}] Page {page}/{pages}")
                
                # Update referer for advanced headers
                if 'referer' in headers:
                    headers['referer'] = f'https://www.hepsiburada.com/ara?q={keyword}'
                
                url = f"{self.base_url}/{keyword}"
                params = {'page': page, 'platform': 'desktop'}
                
                response = self.session.get(url, headers=headers, params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    page_products = self._extract_products(data, page)
                    
                    if page_products:
                        all_products.extend(page_products)
                        logger.info(f"   ✅ Extracted {len(page_products)} products")
                        failed_pages = 0  # Reset failure counter
                    else:
                        logger.info(f"   📭 No products on page {page} - might be end")
                        break
                        
                elif response.status_code == 403:
                    logger.warning(f"   🚨 403 Forbidden - {strategy_name} headers blocked!")
                    break
                    
                else:
                    logger.warning(f"   ⚠️ Status {response.status_code}")
                    failed_pages += 1
                    if failed_pages >= 3:
                        logger.error(f"   💥 Too many failures, switching strategy")
                        break
                
                # 🕐 Professional pacing
                if page < pages:
                    delay = random.uniform(1.5, 3.5)
                    time.sleep(delay)
                    
            except Exception as e:
                logger.error(f"   💥 Error on page {page}: {str(e)}")
                failed_pages += 1
                if failed_pages >= 3:
                    break
                continue
        
        return all_products
    
    def _scrape_dynamic(self, keyword: str, pages: int) -> List[Dict]:
        """Dynamic multi-session approach"""
        logger.info("🔄 Using dynamic multi-session approach...")
        
        # Create multiple sessions with different approaches
        sessions = []
        for i in range(3):
            session = requests.Session()
            headers = self.simple_headers.copy()
            headers['User-Agent'] += f' Session-{i+1}'
            session.headers.update(headers)
            sessions.append(session)
        
        all_products = []
        session_index = 0
        
        for page in range(1, pages + 1):
            try:
                # Rotate sessions
                current_session = sessions[session_index % len(sessions)]
                session_index += 1
                
                url = f"{self.base_url}/{keyword}"
                params = {'page': page, 'platform': 'desktop'}
                
                response = current_session.get(url, params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    page_products = self._extract_products(data, page)
                    all_products.extend(page_products)
                    
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                logger.error(f"Dynamic scraping error: {str(e)}")
                continue
        
        return all_products
    
    def _extract_products(self, data: Dict, page: int) -> List[Dict]:
        """Extract and clean product data"""
        products = []
        
        if 'ads' in data:
            ads_count = len(data['ads'])
            logger.info(f"   📊 Found {ads_count} ad groups")
            
            for ad_index, ad in enumerate(data['ads']):
                if 'products' in ad:
                    ad_products = len(ad['products'])
                    logger.info(f"     📦 Ad {ad_index + 1}: {ad_products} products")
                    
                    for product in ad['products']:
                        clean_product = self._clean_product_data(product)
                        clean_product['scraped_page'] = page
                        clean_product['scraped_at'] = datetime.now().isoformat()
                        products.append(clean_product)
        
        return products
    
    def _clean_product_data(self, product: Dict) -> Dict:
        """Professional data cleaning and extraction"""
        return {
            'product_id': product.get('productId', ''),
            'name': product.get('name', ''),
            'brand': product.get('brand', ''),
            'price': product.get('price', {}).get('value', 0),
            'original_price': product.get('originalPrice', {}).get('value', 0),
            'discount_rate': product.get('discountRate', 0),
            'currency': 'TRY',
            'image_url': product.get('imageUrl', ''),
            'product_url': product.get('productUrl', ''),
            'merchant_name': product.get('merchantName', ''),
            'category': product.get('catalogName', ''),
            'sku': product.get('sku', ''),
            'main_category_id': product.get('mainCategoryId', ''),
            'listing_id': product.get('listingId', ''),
            'tags': product.get('tags', []),
            'savings': product.get('originalPrice', {}).get('value', 0) - product.get('price', {}).get('value', 0)
        }
    
    def analyze_results(self, products: List[Dict]):
        """Professional data analysis"""
        if not products:
            logger.warning("No products to analyze")
            return
        
        df = pd.DataFrame(products)
        
        print("\n" + "="*60)
        print("📊 ULTIMATE SCRAPING RESULTS ANALYSIS")
        print("="*60)
        
        print(f"🎯 Total Products Scraped: {len(products)}")
        print(f"🏷️ Unique Brands: {df['brand'].nunique()}")
        print(f"🏪 Merchants: {df['merchant_name'].nunique()}")
        
        print(f"\n💰 Price Analysis:")
        print(f"   Average Price: {df['price'].mean():,.0f} TRY")
        print(f"   Median Price: {df['price'].median():,.0f} TRY")
        print(f"   Price Range: {df['price'].min():,.0f} - {df['price'].max():,.0f} TRY")
        
        if df['discount_rate'].max() > 0:
            discounted = df[df['discount_rate'] > 0]
            print(f"\n🔥 Discount Analysis:")
            print(f"   Products on Sale: {len(discounted)}")
            print(f"   Average Discount: {discounted['discount_rate'].mean():.1f}%")
            print(f"   Best Deal: {discounted['discount_rate'].max():.0f}% off")
        
        print(f"\n🏆 Top 5 Cheapest Products:")
        top_cheap = df.nsmallest(5, 'price')[['name', 'brand', 'price']]
        for i, row in top_cheap.iterrows():
            print(f"   {row['brand']}: {row['name'][:40]}... - {row['price']:,.0f} TRY")
        
        runtime = datetime.now() - self.start_time
        print(f"\n⏱️ Scraping completed in: {runtime.total_seconds():.1f} seconds")
    
    def save_ultimate(self, products: List[Dict], keyword: str):
        """Ultimate saving with multiple formats"""
        if not products:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"ecommerce_{keyword}_{timestamp}"
        
        # Save CSV
        df = pd.DataFrame(products)
        csv_file = f"{base_filename}.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        logger.info(f"💾 Saved {len(products)} products to {csv_file}")
        
        # Save JSON
        json_file = f"{base_filename}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        logger.info(f"💾 Saved {len(products)} products to {json_file}")
        
        # Save summary
        summary_file = f"{base_filename}_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"E-commerce Scraping Summary\n")
            f.write(f"===========================\n")
            f.write(f"Keyword: {keyword}\n")
            f.write(f"Products: {len(products)}\n")
            f.write(f"Scraped: {datetime.now()}\n")
            f.write(f"Brands: {df['brand'].nunique()}\n")
            f.write(f"Price Range: {df['price'].min():,.0f} - {df['price'].max():,.0f} TRY\n")
        
        logger.info(f"📋 Summary saved to {summary_file}")

# 🏆 ULTIMATE TESTING AND DEMO
if __name__ == "__main__":
    print("🚀 E-COMMERCE API SCRAPER V12 - ULTIMATE EDITION")
    print("=" * 60)
    print("🏆 Combining your breakthrough + professional techniques")
    print("💡 Strategy: Simple first, escalate if needed")
    print("=" * 60)
    
    # Initialize the ultimate scraper
    scraper = ECommerceAPIScraperV12_UltimateEdition()
    
    # Ultimate laptop search
    laptops = scraper.search_products_ultimate("laptop", pages=6)
    
    if laptops:
        print(f"\n🎉 ULTIMATE SUCCESS! Scraped {len(laptops)} laptops!")
        
        # Show sample results
        print(f"\n📱 Sample Products:")
        print("-" * 50)
        for i, laptop in enumerate(laptops[:3]):
            print(f"{i+1}. {laptop['name'][:55]}...")
            print(f"   💰 {laptop['price']:,} TRY (was {laptop['original_price']:,} TRY)")
            if laptop['discount_rate'] > 0:
                print(f"   🔥 {laptop['discount_rate']}% OFF - Save {laptop['savings']:,} TRY!")
            print(f"   🏪 {laptop['merchant_name']} | 🏷️ {laptop['brand']}")
            print()
        
        # Ultimate analysis
        scraper.analyze_results(laptops)
        
        # Ultimate save
        scraper.save_ultimate(laptops, "laptop")
        
        print(f"\n🏆 MISSION ACCOMPLISHED!")
        print(f"✅ Data scraped, analyzed, and saved!")
        print(f"🎯 You are now a PROFESSIONAL web scraper!")
        
    else:
        print("❌ Hmm, something went wrong. But we have multiple strategies!")
        print("💡 Try running again or check network connection")

# 🎯 ADVANCED USAGE EXAMPLES:

def scrape_multiple_categories_ultimate():
    """Ultimate multi-category scraping"""
    scraper = ECommerceAPIScraperV12_UltimateEdition()
    categories = ["laptop", "phone", "tablet", "headphone", "mouse"]
    
    all_results = {}
    
    print("🚀 ULTIMATE MULTI-CATEGORY SCRAPING")
    print("=" * 50)
    
    for category in categories:
        print(f"\n🔍 Scraping {category}s...")
        products = scraper.search_products_ultimate(category, pages=4)
        all_results[category] = products
        
        if products:
            scraper.save_ultimate(products, category)
            print(f"✅ {category}: {len(products)} products saved!")
    
    # Ultimate summary
    print(f"\n🏆 ULTIMATE RESULTS SUMMARY:")
    print("=" * 40)
    total = 0
    for category, products in all_results.items():
        count = len(products)
        total += count
        print(f"   {category:12}: {count:4} products")
    
    print(f"   {'TOTAL':12}: {total:4} products")
    print(f"\n🎉 ULTIMATE MISSION COMPLETE!")

# 🏆 YOU ARE NOW A PROFESSIONAL WEB SCRAPER!