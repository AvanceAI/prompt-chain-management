from src.tools.web_scrape import get_text_requests, get_text_selenium

def test_get_text_requests():
    """Test the get_text_requests function."""
    url_to_scrape = "https://www.google.com"
    result = get_text_requests(url_to_scrape=url_to_scrape)
    assert len(result) > 0

def test_get_text_selenium():
    """Test the get_text_selenium function."""
    url_to_scrape = "https://www.google.com"
    result = get_text_selenium(url_to_scrape=url_to_scrape)
    assert len(result) > 0
