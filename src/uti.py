import requests
import json
from datetime import datetime
import time
import os
from typing import List, Dict, Any
from pathlib import Path

def fetch_page_with_retry(url: str, max_retries: int = 5) -> Dict[str, Any]:
    """
    Fetch data from URL with retry logic
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, json.JSONDecodeError) as e:
            if attempt == max_retries - 1:  # Last attempt
                print(f"Failed to fetch {url} after {max_retries} attempts: {str(e)}")
                return {"rows": []}  # Return empty rows on complete failure
            time.sleep(1 * (attempt + 1))  # Exponential backoff
    return {"rows": []}

def fetch_all_uti_data() -> List[Dict[str, Any]]:
    """
    Fetch all data from UTI MF API by iterating through pages
    """
    base_url = "https://www.utimf.com/api/statutory-disclosure/scheme-dashboard"
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    all_rows = []
    page = 0
    
    while True:
        url = f"{base_url}?date[min]=2015-01-01&date[max]={current_date}&page={page}"
        print(f"Fetching page {page}...")
        
        response_data = fetch_page_with_retry(url)
        rows = response_data.get("rows", [])
        
        if not rows:
            break
            
        all_rows.extend(rows)
        page += 1
        
        time.sleep(1)
    
    return [    
        {
            "title": row.get("title"),
            "view_node": row.get("view_node"),
            "file_url": row.get("file_url"),
            "field_date": row.get("field_date"),
        }
        for row in all_rows
    ]

def main():
    all_data = fetch_all_uti_data()
    
    output_file = output_dir / "uti.json"
    print(f"Saving {len(all_data)} rows to {output_file}...")
    
    with open(output_file, "w") as f:
        json.dump(all_data, f, indent=2)
    
    print("Data fetch complete!")

if __name__ == "__main__":
    main()