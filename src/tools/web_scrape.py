import requests
from src.core.logger import get_logger

logger = get_logger(__name__)


def get_text_requests(url_to_scrape):
    try:
        response = requests.get(
            'http://host.docker.internal:8001/scrape_requests',
            params={'url': url_to_scrape}
        )
        # Check if the request was successful
        response.raise_for_status()
        # Return the content of the response as a string
        return response.text
    except requests.RequestException as e:
        # Handle any errors that occur during the request
        logger.error(f'An error occurred while scraping {url_to_scrape}: {e}')
        return ""
    
    
def get_text_selenium(url_to_scrape):
    try:
        response = requests.get(
            'http://host.docker.internal:8001/scrape_selenium',
            params={'url': url_to_scrape}
        )
        # Check if the request was successful
        response.raise_for_status()
        # Return the content of the response as a string
        return response.text
    except requests.RequestException as e:
        # Handle any errors that occur during the request
        logger.error(f'An error occurred while scraping {url_to_scrape}: {e}')
        return ""