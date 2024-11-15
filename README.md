# Flipkart-Product-Scraper
This Python project automates the process of scraping product information from Flipkart based on a search term. It retrieves data such as product names, prices, and ratings, and organizes it into a structured CSV file for easy analysis.



Project Features


Web Scraping: Uses BeautifulSoup to extract product details from Flipkart’s search results page.


Data Storage: Stores the scraped data (product name and price) in a Excel file using Pandas and send it to user email.


Dynamic Search: Enter any search term, and the script will fetch relevant product listings.


Custom Headers: Mimics a real browser request to avoid being blocked by the website.



How It Works



Search: The user provides a search query, which the script formats for the Flipkart URL.


Scrape: The script retrieves the HTML page and parses it to extract product information.


Save: Data is saved into a CSV file for easy access and analysis.

