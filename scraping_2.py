import os 
import datetime
import json
import xml.etree.ElementTree as ET
import requests
import glob

output_directory = '/home/daniele/Scrivania/HSLU/datawarehouseAndDatalake/scraping'
# Path to your original JSON file
base_filename= 'scraped_data_dataset'
date_str = datetime.datetime.now().strftime("%Y-%m-%d")
filename = f"{base_filename}_{date_str}.json"
filepath = os.path.join(output_directory, filename)
input_file_path = filepath

# Path to the new JSON file (output)
base_filename2= 'scraped_data_index'
date_str2 = datetime.datetime.now().strftime("%Y-%m-%d")
filename2 = f"{base_filename2}_{date_str2}.json"
filepath2 = os.path.join(output_directory, filename2)
output_file_path = filepath2

# Reading the original JSON file
with open(input_file_path, 'r') as file:
    data = json.load(file)

# Modifying the data
for url, records in data.items():
    for record in records:
        # Remove the "content" key from each record
        if "content" in record:
            del record["content"]

# Writing to a new JSON file
with open(output_file_path, 'w') as file:
    json.dump(data, file, indent=4)

print("New JSON file created without 'content' key.")

# List of sitemap URLs
sitemap_urls = [
    'https://www.concordia.ch/en.sitemap.xml'
]

# Namespace for parsing XML
namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

url_data = {}

# Function to update or add new data to url_data
def update_url_data(url_data, url, new_record):
    if url in url_data:
        # Check if this date is already in the records
        if not any(record['lastmod'] == new_record['lastmod'] for record in url_data[url]):
            url_data[url].append(new_record)
    else:
        url_data[url] = [new_record]

# Process sitemap URLs
for sitemap_url in sitemap_urls:
    response = requests.get(sitemap_url)
    if response.status_code == 200:
        sitemap = ET.fromstring(response.content)
        for url_entry in sitemap.findall('.//sitemap:url', namespace):
            loc = url_entry.find('sitemap:loc', namespace).text
            lastmod = url_entry.find('sitemap:lastmod', namespace)
            lastmod_text = lastmod.text if lastmod is not None else "1970-01-01" #for those that have no date

            # Create a new record
            new_record = {'lastmod': lastmod_text}

            # Update url_data with the new record
            update_url_data(url_data, loc, new_record)

# Directory where the files are stored
directory = '/home/daniele/Scrivania/HSLU/datawarehouseAndDatalake/scraping'

# Pattern to match the files of interest
pattern = 'scraped_data_index_*.json'

# Get a list of all matching files in the directory
file_paths = glob.glob(os.path.join(directory, pattern))

def extract_date(file_name):
    try:
        # Extracting the date from the file name
        date_str = file_name.split('_')[-1].split('.')[0]
        return datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None

# Process the files to find the one with the latest date
latest_file = None
latest_date = datetime.datetime.min

for file_path in file_paths:
    file_date = extract_date(os.path.basename(file_path))
    if file_date and file_date > latest_date:
        latest_date = file_date
        latest_file = file_path

if latest_file:
    print(f"The latest file is: {latest_file}")
else:
    print("No matching files found.")

output_directory = '/home/daniele/Scrivania/HSLU/datawarehouseAndDatalake/scraping'

def compare_sitemaps(new_sitemap_file, index_file):
    
    new_sitemap = new_sitemap_file
        
    with open(index_file, 'r') as file:
        index_data = json.load(file)

    updated_urls = {}
    for url, new_records in new_sitemap.items():
        # Get the most recent lastmod date from index_data, if exists
        if url in index_data:
            index_lastmod_dates = [datetime.datetime.strptime(record['lastmod'], "%Y-%m-%d") for record in index_data[url]]
            index_most_recent = max(index_lastmod_dates) if index_lastmod_dates else datetime.datetime.min
        else:
            index_most_recent = datetime.datetime.min

        # Compare with new_sitemap lastmod dates
        for new_record in new_records:
            new_record_date = datetime.datetime.strptime(new_record['lastmod'], "%Y-%m-%d")
            if new_record_date > index_most_recent:
                if url not in updated_urls:
                    updated_urls[url] = []
                updated_urls[url].append(new_record)

    return updated_urls

def save_updated_data(base_filename, updated_data):
    filename = f"{base_filename}_updated.json"
    filepath = os.path.join(output_directory, filename)
    with open(filepath, 'w') as file:
        json.dump(updated_data, file, indent=4)

# Usage
new_sitemap_file = url_data
index_file = latest_file
updated_urls = compare_sitemaps(new_sitemap_file, index_file)
save_updated_data('updated_urls', updated_urls)

def fetch_html_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return 'Failed to retrieve content'
    except requests.RequestException:
        return 'Request failed'

def save_data(base_filename, data):
    #date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{base_filename}.json"
    output_directory = '/home/daniele/Scrivania/HSLU/datawarehouseAndDatalake/scraping'
    filepath = os.path.join(output_directory, filename)
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def process_sitemaps_and_index_differences():
    # Assuming final_data is the existing data loaded from a JSON file
    # final_data = { 'https://www.example.com/page1': [{'lastmod': '2023-12-17', 'content': '...'}], ... }
    
    final_data = {}  # Replace with the actual data loading logic as per your application
    total_urls = sum(len(records) for records in updated_urls.values())
    processed_urls = 0

    for url, records in updated_urls.items():
        for record in records:
            new_lastmod_date = datetime.datetime.strptime(record['lastmod'], "%Y-%m-%d")

            # Check if the URL already exists in final_data
            if url not in final_data:
                final_data[url] = []
                html_content = fetch_html_content(url)
                final_data[url].append({'lastmod': record['lastmod'], 'content': html_content})
            else:
                # Add the new data with content only if the lastmod is more recent
                existing_lastmod_dates = [datetime.datetime.strptime(item['lastmod'], "%Y-%m-%d") for item in final_data[url]]
                if new_lastmod_date > max(existing_lastmod_dates):
                    html_content = fetch_html_content(url)
                    final_data[url].append({'lastmod': record['lastmod'], 'content': html_content})

            processed_urls += 1
            print(f"Processed {processed_urls}/{total_urls} URLs")
            save_data('diffs_Index_and_new_sitemap', final_data)
    return final_data

finaldata= process_sitemaps_and_index_differences()

directory = '/home/daniele/Scrivania/HSLU/datawarehouseAndDatalake/scraping'

# Pattern to match the files of interest
pattern = 'scraped_data_dataset_*.json'

# Get a list of all matching files in the directory
file_paths = glob.glob(os.path.join(directory, pattern))

def extract_date(file_name):
    try:
        # Extracting the date from the file name
        date_str = file_name.split('_')[-1].split('.')[0]
        return datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None

# Process the files to find the one with the latest date
latest_file = None
latest_date = datetime.datetime.min

for file_path in file_paths:
    file_date = extract_date(os.path.basename(file_path))
    if file_date and file_date > latest_date:
        latest_date = file_date
        latest_file = file_path

if latest_file:
    print(f"The latest file is: {latest_file}")
else:
    print("No matching files found.")

