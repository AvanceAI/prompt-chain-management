from dotenv import load_dotenv
load_dotenv()

import os
import requests
from ...utils.utils import save_json

API_ENDPOINT = "https://www.googleapis.com/customsearch/v1"

CSE_ID = os.environ["CSE_ID"]
CSE_API_KEY = os.environ["CSE_API_KEY"]


class Searcher:
    def __init__(self, max_results_per_query=10, total_results=20):
        self.max_results_per_query = max_results_per_query
        self.total_results = total_results
        
    def _filter_search_results(self, search_results):
        filtered_results = []
        for item in search_results:
            if ".gov" in item["href"]:
                filtered_results.append(item)
        return filtered_results
        
    def run(self, query, save_path):
        search_results = self.google_search(query=query)
        search_results = self._filter_search_results(search_results=search_results)
        save_json(filepath=save_path, data={"search_results": search_results})
        return search_results

    def google_search(self, query):
        search_results = []
        for i in range(0, self.total_results, self.max_results_per_query):
            params = {
                'q': query,
                'cx': CSE_ID,
                'key': CSE_API_KEY,
                'num': self.max_results_per_query,
                'start': i + 1
            }

            response = requests.get(API_ENDPOINT, params=params)

            if response.status_code == 200:
                json_data = response.json()
                for item in json_data.get('items', []):
                    title = item.get('title')
                    description = item.get('snippet')
                    href = item.get('link')
                    search_results.append({
                        'title': title,
                        'description': description,
                        'href': href
                    })
            else:
                print("Error occurred on fetching results starting from position:", i + 1)
                break
        return search_results
