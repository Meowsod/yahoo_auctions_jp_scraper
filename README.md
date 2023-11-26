# Yahoo Auctions JP Scraper

Fork of leoloman's [yjp_scraper](https://github.com/leoloman/yjp_scraper) modified for automatically scraping all pages, utilizing selectolax instead of beautifulsoup and outputting to JSON instead of panda.

## Features
* Scraping Yahoo Auctions Japan trough Buyee
* Writing a JSON file out of the results

## Usage
Add in your GET headers to the Headers dictionary within the script and further modify it to your needs.

Requirements for base script:
* json
* requests
* selectolax
