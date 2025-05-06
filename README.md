# Forum Scraper

A flexible Python script to scrape forum topics, questions, replies, images, and video links from forums with similar structures to control.com.

## Requirements

- Python 3.x
- ChromeDriver (matching your Chrome version)
- Libraries: `selenium`, `beautifulsoup4`, `pandas`, `argparse`

Install dependencies:
```bash
pip install selenium beautifulsoup4 pandas
Usage
Download ChromeDriver from here and note its path.

Run the scraper with command-line arguments:

bash
python forum_scraper.py \
  --base_url "FORUM_BASE_URL" \
  --start_page START_PAGE \
  --end_page END_PAGE \
  --driver_path "PATH_TO_CHROMEDRIVER" \
  --output "output.csv"
Example:
bash
python forum_scraper.py \
  --base_url "https://control.com/forums/forums/hmi.8" \
  --start_page 1 \
  --end_page 5 \
  --driver_path "/path/to/chromedriver" \
  --output "hmi_data.xlsx"
Arguments:
--base_url: URL of the forum (e.g., https://example.com/forums/topic.1).

--start_page: First page to scrape (default: 1).

--end_page: Last page to scrape (required).

--topic_selector: CSS class for topic containers (default: structItem-cell structItem-cell--main).

--reply_selector: CSS class for reply containers (default: message-cell message-cell--main).

--driver_path: Path to ChromeDriver executable.

--output: Output filename (supports .csv or .xlsx).

--delay: Delay between requests in seconds (default: 10).

Notes
Respect robots.txt and avoid aggressive scraping.

Adjust selectors (--topic_selector, --reply_selector) based on the target forum's HTML structure.

Run in headless mode by default; remove options.add_argument('--headless') in code for debugging.


---

**How to Use:**

1. **Install ChromeDriver** and note its path (e.g., `/usr/bin/chromedriver`).
2. **Run the script** with appropriate arguments. Example:
   ```bash
   python forum_scraper.py --base_url "https://example.com/forums/tech" --end_page 3 --driver_path "chromedriver.exe" --output "tech_forum.xlsx"
Check the output file (tech_forum.xlsx) for scraped data.

This setup makes the scraper adaptable to any forum with similar HTML structure by allowing users to specify CSS selectors and URLs.
