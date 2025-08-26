import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import os
import time
import logging
from urllib.parse import urlparse, urljoin

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, use regular environment variables

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiWebScraper:
    def __init__(self, api_key: str = None):
        """Initialize the Gemini Web Scraper"""
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("Google API key not found. Set GOOGLE_API_KEY environment variable.")
        
        # Initialize Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=self.api_key,
            temperature=0.1
        )
        
        # Request headers to avoid blocking
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def fetch_webpage(self, url: str) -> tuple[str, str]:
        """
        Fetch webpage content with error handling
        Returns: (content, status_message)
        """
        try:
            # Validate URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = 'https://' + url
            
            logger.info(f"Fetching: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
            
            # Extract main content
            content = soup.get_text()
            # Clean up whitespace
            content = '\n'.join(line.strip() for line in content.splitlines() if line.strip())
            
            # Limit content size (Gemini has token limits)
            if len(content) > 10000:
                content = content[:10000] + "\n\n[Content truncated...]"
            
            return content, f"SUCCESS: Successfully scraped {len(content)} characters"
            
        except requests.exceptions.RequestException as e:
            error_msg = f"ERROR: Network error: {str(e)}"
            logger.error(error_msg)
            return "", error_msg
        except Exception as e:
            error_msg = f"ERROR: Parsing error: {str(e)}"
            logger.error(error_msg)
            return "", error_msg
    
    def analyze_content(self, content: str, user_prompt: str) -> str:
        """
        Use Gemini to analyze the scraped content based on user prompt
        """
        if not content:
            return "ERROR: No content to analyze. Please check if the webpage loaded correctly."
        
        try:
            # Construct the analysis prompt
            analysis_prompt = f"""
            You are a helpful web content analyst. Please analyze the following webpage content and respond to the user's request.
            
            User Request: {user_prompt}
            
            Webpage Content:
            {content}
            
            Instructions:
            - Focus specifically on what the user asked for
            - Provide clear, structured information
            - If the requested information isn't available, say so clearly
            - Be concise but comprehensive
            - Use bullet points or numbered lists when appropriate
            """
            
            # Get response from Gemini
            message = HumanMessage(content=analysis_prompt)
            response = self.llm.invoke([message])
            
            return response.content
            
        except Exception as e:
            error_msg = f"ERROR: AI Analysis error: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def scrape_and_analyze(self, url: str, user_prompt: str) -> dict:
        """
        Complete pipeline: scrape webpage and analyze with user prompt
        """
        start_time = time.time()
        
        # Step 1: Fetch content
        content, fetch_status = self.fetch_webpage(url)
        
        # Step 2: Analyze with Gemini
        if content:
            analysis = self.analyze_content(content, user_prompt)
        else:
            analysis = "Cannot analyze - no content retrieved."
        
        processing_time = time.time() - start_time
        
        return {
            'content': content,
            'analysis': analysis,
            'fetch_status': fetch_status,
            'processing_time': round(processing_time, 2),
            'content_length': len(content)
        }

def main():
    st.set_page_config(
        page_title="Gemini Web Scraper",
        page_icon=":spider:",
        layout="wide"
    )
    
    st.title("Gemini AI Web Scraper")
    st.markdown("### Scrape any website and ask questions in natural language!")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Google API Key",
            type="password",
            help="Enter your Google AI Studio API key",
            value=os.getenv('GOOGLE_API_KEY', '')
        )
        
        if api_key:
            os.environ['GOOGLE_API_KEY'] = api_key
        
        st.markdown("---")
        st.markdown("**How it works:**")
        st.markdown("""
        1. Enter a website URL
        2. Ask what you want to know
        3. AI scrapes and analyzes the content
        4. Get intelligent insights!
        """)
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        url_input = st.text_input(
            "Website URL:",
            placeholder="https://example.com or just example.com",
            help="Enter the website you want to scrape"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
        
    user_prompt = st.text_area(
        "What do you want to know?",
        placeholder="Examples:\n• Summarize the main points\n• Extract all contact information\n• Find pricing details\n• List all product features",
        height=100,
        help="Ask anything about the webpage content in natural language"
    )
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        scrape_button = st.button("Scrape & Analyze", type="primary")
    
    with col2:
        if st.button("Clear"):
            st.experimental_rerun()
    
    # Process request
    if scrape_button:
        if not api_key:
            st.error("ERROR: Please enter your Google API key in the sidebar!")
            return
            
        if not url_input or not user_prompt:
            st.error("ERROR: Please enter both a URL and your question!")
            return
        
        try:
            # Initialize scraper
            scraper = GeminiWebScraper(api_key)
            
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Fetching webpage...")
            progress_bar.progress(25)
            
            # Scrape and analyze
            result = scraper.scrape_and_analyze(url_input, user_prompt)
            
            status_text.text("Analyzing with Gemini AI...")
            progress_bar.progress(75)
            
            status_text.text("Complete!")
            progress_bar.progress(100)
            
            # Display results
            st.success(f"Processing completed in {result['processing_time']} seconds")
            
            # Main analysis result
            st.markdown("## Analysis Result")
            st.markdown(result['analysis'])
            
            # Details in expander
            with st.expander("Scraping Details"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Content Length", f"{result['content_length']:,} chars")
                with col2:
                    st.metric("Processing Time", f"{result['processing_time']}s")
                with col3:
                    st.metric("Status", "Success" if result['content'] else "Failed")
                
                st.markdown("**Fetch Status:**")
                st.info(result['fetch_status'])
                
                if result['content']:
                    st.markdown("**Raw Content Preview:**")
                    st.text_area(
                        "First 1000 characters of scraped content:",
                        result['content'][:1000] + "..." if len(result['content']) > 1000 else result['content'],
                        height=200,
                        disabled=True
                    )
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
        except Exception as e:
            st.error(f"ERROR: {str(e)}")
            logger.error(f"Streamlit error: {e}")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p><strong>Gemini Web Scraper</strong> | Built with Streamlit + LangChain + Google Gemini</p>
        <p><em>Simple HTTP scraping - no browser automation needed!</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()