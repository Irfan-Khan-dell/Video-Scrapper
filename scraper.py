import requests
from bs4 import BeautifulSoup
import re

def extract_text_from_url(url):
    """
    Scrapes a webpage and extracts the main readable text.
    This acts as the 'Context Enrichment' agent for our AI.
    """
    print(f"Scraping context from: {url}")
    
    # We use headers so websites don't block us thinking we are a basic bot
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        # Fetch the page
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Rip out the garbage: scripts, styles, headers, footers, and nav bars
        for element in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
            element.decompose()
            
        # Find all paragraph tags (where the actual article content usually lives)
        paragraphs = soup.find_all('p')
        
        # Join the text together
        raw_text = ' '.join([p.get_text() for p in paragraphs])
        
        # Clean up extra whitespace and line breaks using regex
        clean_text = re.sub(r'\s+', ' ', raw_text).strip()
        
        if not clean_text:
            print("Warning: Could not find any readable paragraph text on this page.")
            return None
            
        print("Scraping successful!")
        return clean_text
        
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

# --- Test the script ---
if __name__ == "__main__":
    # Let's test it on a standard Wikipedia page
    test_link = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    
    scraped_context = extract_text_from_url(test_link)
    
    if scraped_context:
        print("\n--- Extracted Web Text ---")
        print(scraped_context[:750] + "...\n\n[Output Truncated]")