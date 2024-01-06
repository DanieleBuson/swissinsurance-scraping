import requests
import xml.etree.ElementTree as ET
import json
from time import sleep
from datetime import datetime
import os
import re
from datetime import datetime
import json


def once_a_month_get_data():

    # List of sitemap URLs
    sitemap_urls = [
        'https://www.concordia.ch/en.sitemap.xml'
    ]

    ''',
        'https://www.css.ch/en.sitemap.xml',
        'https://www.helsana.ch/sitemap.en.xml',
        'https://www.sanitas.com/en.sitemap.xml',
        'https://www.swica.ch/en/sitemap.xml',
        'https://www.admin.ch',
        'https://www.ch.ch/en/'
        '''
    #https://www.admin.ch
    #https://www.ch.ch/en/


    # List of additional query links
    #query_links = ['swiss obligatory health insurance','swiss health insurance regulations']
    #query_links = []
    # Namespace for parsing XML
    namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    # Function to fetch HTML content
    def fetch_html_content(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                return 'Failed to retrieve content'
        except requests.RequestException:
            return 'Request failed'

    # Directory where JSON files will be saved
    output_directory = ''

    # Process and save data to a file with the current date in the filename
    def save_data(base_filename, data):
        date_str = datetime.now().strftime("%Y-%m-%01")
        filename = f"{base_filename}_{date_str}.json"
        filepath = os.path.join(output_directory, filename)  # Construct the full file path
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)

    # Function to update or add new data to final_data
    def update_final_data(final_data, url, new_record):
        if url in final_data:
            # Check if this date is already in the records
            if not any(record['lastmod'] == new_record['lastmod'] for record in final_data[url]):
                final_data[url].append(new_record)
        else:
            final_data[url] = [new_record]


    def save_sitemap_data(base_filename, sitemap_data):
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{base_filename}_sitemap_{date_str}.json"
        filepath = os.path.join(output_directory, filename)
        with open(filepath, 'w') as file:
            json.dump(sitemap_data, file, indent=4)

    # Main processing function
    def process_sitemaps_and_query_links():
        url_data = {}

        # Process sitemap URLs
        for sitemap_url in sitemap_urls:
            response = requests.get(sitemap_url)
            if response.status_code == 200:
                sitemap = ET.fromstring(response.content)
                for url_entry in sitemap.findall('.//sitemap:url', namespace):
                    loc = url_entry.find('sitemap:loc', namespace).text
                    lastmod = url_entry.find('sitemap:lastmod', namespace)
                    lastmod_text = lastmod.text if lastmod is not None else "1970-01-01" #for those that have no date
                    url_data[loc] = {'lastmod': lastmod_text}
        # Save the sitemap data
        save_sitemap_data('sitemap_data', url_data)

        # Process additional query links
        #for url in query_links:
        #    url_data[url] = {'lastmod': '1970-01-01'}

        # Fetch HTML content and update data incrementally
        final_data = {}
        total_urls = len(url_data)
        processed_urls = 0

        for url, info in url_data.items():
            html_content = fetch_html_content(url)
            sleep(0.3 if 'swica' in url else 0.5)
            new_record = {'lastmod': info['lastmod'], 'content': html_content}

            update_final_data(final_data, url, new_record)

            save_data('scraped_data_dataset', final_data)
            processed_urls += 1
            print(f"Processed {processed_urls}/{total_urls} URLs")


    process_sitemaps_and_query_links()

directory = '/home/daniele/Scrivania/HSLU/datawarehouseAndDatalake/scraping'
file_pattern = re.compile(r'scraped_data_dataset_(\d{4}-\d{2}-\d{2})\.json')

latest_date = None
latest_file_name = None

# Iterate over files in the directory and the one 
for file_name in os.listdir(directory):
    match = file_pattern.match(file_name)
    if match:
        file_date_str = match.group(1)
        file_date = datetime.strptime(file_date_str, '%Y-%m-%d')
        if not latest_date or file_date > latest_date:
            latest_date = file_date
            latest_file_name = file_name

# Check if the latest file's month matches the current month
if latest_file_name:
    file_month = latest_date.month
    current_month = datetime.now().month

    if file_month == current_month:
        print("No need for a new scraped_data_dataset file for this month")
    else:
        print("a scraped_data_dataset being created")
        once_a_month_get_data()
else:
    print("No files found matching the pattern. A file is being created")
    once_a_month_get_data()

import boto3
import logging
from botocore.exceptions import ClientError

bucket_name = "swissinsurance-bucket-scraping-dw"

try:
    s3 = boto3.client(
        's3',
        aws_access_key_id='AKIA4Y4XR5MNJVERIPCS',
        aws_secret_access_key='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'
    )
    s3.list_objects_v2(Bucket=bucket_name)
    print("Connection to S3 bucket was successful.")
except:
    print("Credentials not available for AWS S3.")

def upload_to_s3(bucket_name, file_name, folder='scraping-folder'):
    """
    Upload a file to a specific folder in an S3 bucket

    :param bucket_name: Bucket to upload to
    :param file_name: File to upload
    :param folder: Folder in the bucket to upload to
    :return: True if file was uploaded, else False
    """
    # Extract the base file name from the file path
    base_file_name = os.path.basename(file_name)

    # Construct the full S3 object name
    object_name = f"{folder}/{base_file_name}"


    try:
        s3.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

for file_name in os.listdir("../scraping"):
    if file_name.startswith("scraped_data_dataset_"):
        scraped_dataset = file_name

upload_to_s3(bucket_name, scraped_dataset)