# Web Scraping and Data Storage

This repository contains a Python script for web scraping and data storage in AWS S3. It fetches data from various websites, stores it locally, and then uploads it to an AWS S3 bucket. The script is designed to run once a month and fetches data from a predefined list of websites.

## Prerequisites

Before running the script, ensure you have the following set up:

- Python 3.x
- Required Python packages (install using `pip`): `requests`, `xml.etree.ElementTree`, `json`, `dotenv`, `boto3`

## Usage

1. Clone the repository to your local machine:

git clone https://github.com/DanieleBuson/swissinsurance-scraping.git

2. Navigate to the project directory:

cd web-scraping-and-data-storage

3. Create a `.env` file and add your AWS S3 credentials:

AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key


4. Run the script (script1 was the one mainly used)
This script will fetch data from the specified websites, store it locally, and upload it to the specified AWS S3 bucket.


## Configuration

- You can customize the list of websites to scrape by modifying the `sitemap_urls` list in the script.

