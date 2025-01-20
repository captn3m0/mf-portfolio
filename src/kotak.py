from typing import List, Dict, Optional
from dataclasses import dataclass
from curl_cffi import requests
from requests import RequestException
import csv
import os
from pathlib import Path
from urllib.parse import urljoin
import json
from typing import TypedDict

class APIResponse(TypedDict):
    status: str
    statusCode: str
    dataList: List[str]

@dataclass
class FileEntry:
    path: str
    filename: str

class KotakScraper:
    BASE_URL = "https://www.kotakmf.com/api/kotakapi/portfolio/folderlist"
    
    def __init__(self, output_file: str = "out/kotak.csv"):
        self.output_file = Path(output_file)
        self.session = requests.Session()
        self.discovered_files: List[FileEntry] = []

    def fetch_directory(self, scheme: str = "") -> Optional[APIResponse]:
        """Fetch directory listing from the API."""
        try:
            response = self.session.get(
                self.BASE_URL,
                params={"scheme": scheme},
                timeout=10,
                impersonate="chrome"
            )
            response.raise_for_status()
            # sleep for 5 seconds
            import time
            time.sleep(5)
            return response.json()
        except RequestException as e:
            print(f"Error fetching {scheme}: {e}")
            print(response.text)
            return None

    def is_file(self, name: str) -> bool:
        """Check if the item is a file based on extension."""
        return any(name.lower().endswith(ext) for ext in ['.xls', '.xlsx', '.pdf'])

    def explore_directory(self, current_path: str = "") -> None:
        """Recursively explore directories and collect file information."""
        response = self.fetch_directory(current_path)
        
        if not response:
            return

        for item in response['dataList']:
            new_path = f"{current_path}/{item}" if current_path else item
            
            if self.is_file(item):
                self.discovered_files.append(
                    FileEntry(
                        path=str(Path(current_path)),
                        filename=item
                    )
                )
            else:
                self.explore_directory(new_path)

    def save_results(self) -> None:
        """Save discovered files to CSV, sorted by path."""
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Sort the discovered files by path
        sorted_files = sorted(self.discovered_files, key=lambda x: (x.path, x.filename))
        
        with open(self.output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['path', 'filename'])
            
            for entry in sorted_files:
                writer.writerow([entry.path, entry.filename])

def main() -> None:
    scraper = KotakScraper()
    print("Starting Kotak MF Portfolio scraping...")
    scraper.explore_directory()
    scraper.save_results()
    print(f"Scraping complete. Results saved to {scraper.output_file}")

if __name__ == "__main__":
    main()