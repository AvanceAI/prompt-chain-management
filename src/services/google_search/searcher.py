from dotenv import load_dotenv
load_dotenv()

import os
import requests
from ...utils.utils import save_json

API_ENDPOINT = "https://www.googleapis.com/customsearch/v1"

CSE_ID = os.environ["CSE_ID"]
CSE_API_KEY = os.environ["CSE_API_KEY"]


class Searcher:
    def __init__(self, run_id, save_dir="outputs", max_results_per_query=10, total_results=20):
        self.run_id = run_id
        self.save_dir = os.path.join(save_dir, run_id)
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        self.max_results_per_query = max_results_per_query
        self.total_results = total_results
        
    def run(self, query, step_id):
        search_results = self.google_search(query=query)
        save_path = os.path.join(self.save_dir, f"{step_id}.json")
        print(f"Saving results to {save_path}")
        save_json(filepath=save_path, data={"data": search_results})
        return search_results

    def google_search(self, query):
        search_results = {}
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
                for k, item in enumerate(json_data.get('items', [])):
                    title = item.get('title')
                    description = item.get('snippet')
                    href = item.get('link')
                    search_results[i+k] = {
                        'title': title,
                        'description': description,
                        'href': href
                    }
            else:
                print("Error occurred on fetching results starting from position:", i + 1)
                break
        return search_results
