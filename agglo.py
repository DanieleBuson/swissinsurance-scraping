

# #################################################################################
# ############Section in use for the project (First Time and every month)##########
# #################################################################################
# import requests
# import xml.etree.ElementTree as ET
# import json
# from time import sleep
# from datetime import datetime
# import os
# def once_a_month_get_data():

#     # List of sitemap URLs
#     sitemap_urls = [
#         'https://www.concordia.ch/en.sitemap.xml'
#     ]

#     ''',
#         'https://www.css.ch/en.sitemap.xml',
#         'https://www.helsana.ch/sitemap.en.xml',
#         'https://www.sanitas.com/en.sitemap.xml',
#         'https://www.swica.ch/en/sitemap.xml',
#         'https://www.admin.ch',
#         'https://www.ch.ch/en/'
#         '''
#     #https://www.admin.ch
#     #https://www.ch.ch/en/


#     # List of additional query links
#     #query_links = ['swiss obligatory health insurance','swiss health insurance regulations']
#     #query_links = []
#     # Namespace for parsing XML
#     namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

#     # Function to fetch HTML content
#     def fetch_html_content(url):
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 return response.text
#             else:
#                 return 'Failed to retrieve content'
#         except requests.RequestException:
#             return 'Request failed'

#     # Directory where JSON files will be saved
#     output_directory = '/Users/mortazakiani/dwh_aws_project'

#     # Process and save data to a file with the current date in the filename
#     def save_data(base_filename, data):
#         date_str = datetime.now().strftime("%Y-%m-%01")
#         filename = f"{base_filename}_{date_str}.json"
#         filepath = os.path.join(output_directory, filename)  # Construct the full file path
#         with open(filepath, 'w') as file:
#             json.dump(data, file, indent=4)

#     # Function to update or add new data to final_data
#     def update_final_data(final_data, url, new_record):
#         if url in final_data:
#             # Check if this date is already in the records
#             if not any(record['lastmod'] == new_record['lastmod'] for record in final_data[url]):
#                 final_data[url].append(new_record)
#         else:
#             final_data[url] = [new_record]


#     def save_sitemap_data(base_filename, sitemap_data):
#         date_str = datetime.now().strftime("%Y-%m-%d")
#         filename = f"{base_filename}_sitemap_{date_str}.json"
#         filepath = os.path.join(output_directory, filename)
#         with open(filepath, 'w') as file:
#             json.dump(sitemap_data, file, indent=4)

#     # Main processing function
#     def process_sitemaps_and_query_links():
#         url_data = {}

#         # Process sitemap URLs
#         for sitemap_url in sitemap_urls:
#             response = requests.get(sitemap_url)
#             if response.status_code == 200:
#                 sitemap = ET.fromstring(response.content)
#                 for url_entry in sitemap.findall('.//sitemap:url', namespace):
#                     loc = url_entry.find('sitemap:loc', namespace).text
#                     lastmod = url_entry.find('sitemap:lastmod', namespace)
#                     lastmod_text = lastmod.text if lastmod is not None else "1970-01-01" #for those that have no date
#                     url_data[loc] = {'lastmod': lastmod_text}
#         # Save the sitemap data
#         save_sitemap_data('sitemap_data', url_data)

#         # Process additional query links
#         #for url in query_links:
#         #    url_data[url] = {'lastmod': '1970-01-01'}

#         # Fetch HTML content and update data incrementally
#         final_data = {}
#         total_urls = len(url_data)
#         processed_urls = 0

#         for url, info in url_data.items():
#             html_content = fetch_html_content(url)
#             sleep(0.3 if 'swica' in url else 0.5)
#             new_record = {'lastmod': info['lastmod'], 'content': html_content}

#             update_final_data(final_data, url, new_record)

#             save_data('scraped_data_dataset', final_data)
#             processed_urls += 1
#             print(f"Processed {processed_urls}/{total_urls} URLs")


#     process_sitemaps_and_query_links()

# #################################################################################
# ##########################First time and Monthly full dataset download###########
# #################################################################################
# import os
# import re
# from datetime import datetime


# directory = '/Users/mortazakiani/dwh_aws_project'
# file_pattern = re.compile(r'scraped_data_dataset_(\d{4}-\d{2}-\d{2})\.json')

# latest_date = None
# latest_file_name = None

# # Iterate over files in the directory and the one 
# for file_name in os.listdir(directory):
#     match = file_pattern.match(file_name)
#     if match:
#         file_date_str = match.group(1)
#         file_date = datetime.strptime(file_date_str, '%Y-%m-%d')
#         if not latest_date or file_date > latest_date:
#             latest_date = file_date
#             latest_file_name = file_name

# # Check if the latest file's month matches the current month
# if latest_file_name:
#     file_month = latest_date.month
#     current_month = datetime.now().month

#     if file_month == current_month:
#         print("No need for a new scraped_data_dataset file for this month")
#     else:
#         print("a scraped_data_dataset being created")
#         once_a_month_get_data()
# else:
#     print("No files found matching the pattern. A file is being created")
#     once_a_month_get_data()


# #################################################################################
# ##########################Index version of saved data############################
# #################################################################################

# ##Creating an index version for saved json file

# import json

# output_directory = '/Users/mortazakiani/dwh_aws_project'
# # Path to your original JSON file
# base_filename= 'scraped_data_dataset'
# date_str = datetime.now().strftime("%Y-%m-%d")
# filename = f"{base_filename}_{date_str}.json"
# filepath = os.path.join(output_directory, filename)
# input_file_path = filepath

# # Path to the new JSON file (output)
# base_filename2= 'scraped_data_index'
# date_str2 = datetime.now().strftime("%Y-%m-%d")
# filename2 = f"{base_filename2}_{date_str2}.json"
# filepath2 = os.path.join(output_directory, filename2)
# output_file_path = filepath2

# # Reading the original JSON file
# with open(input_file_path, 'r') as file:
#     data = json.load(file)

# # Modifying the data
# for url, records in data.items():
#     for record in records:
#         # Remove the "content" key from each record
#         if "content" in record:
#             del record["content"]

# # Writing to a new JSON file
# with open(output_file_path, 'w') as file:
#     json.dump(data, file, indent=4)

# print("New JSON file created without 'content' key.")









# #################################################################################
# ##########################code to get new sitemap as urls########################
# #################################################################################

# ###Sitemap handeling
# import xml.etree.ElementTree as ET
# import requests
# import json
# from datetime import datetime

# # List of sitemap URLs
# sitemap_urls = [
#     'https://www.concordia.ch/en.sitemap.xml'
# ]

# # Namespace for parsing XML
# namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

# url_data = {}

# # Function to update or add new data to url_data
# def update_url_data(url_data, url, new_record):
#     if url in url_data:
#         # Check if this date is already in the records
#         if not any(record['lastmod'] == new_record['lastmod'] for record in url_data[url]):
#             url_data[url].append(new_record)
#     else:
#         url_data[url] = [new_record]

# # Process sitemap URLs
# for sitemap_url in sitemap_urls:
#     response = requests.get(sitemap_url)
#     if response.status_code == 200:
#         sitemap = ET.fromstring(response.content)
#         for url_entry in sitemap.findall('.//sitemap:url', namespace):
#             loc = url_entry.find('sitemap:loc', namespace).text
#             lastmod = url_entry.find('sitemap:lastmod', namespace)
#             lastmod_text = lastmod.text if lastmod is not None else "1970-01-01" #for those that have no date

#             # Create a new record
#             new_record = {'lastmod': lastmod_text}

#             # Update url_data with the new record
#             update_url_data(url_data, loc, new_record)



# #################################################################################
# ##########################Path of latest index file##############################
# #################################################################################

# import os
# import glob
# from datetime import datetime

# # Directory where the files are stored
# directory = '/Users/mortazakiani/dwh_aws_project'

# # Pattern to match the files of interest
# pattern = 'scraped_data_index_*.json'

# # Get a list of all matching files in the directory
# file_paths = glob.glob(os.path.join(directory, pattern))

# def extract_date(file_name):
#     try:
#         # Extracting the date from the file name
#         date_str = file_name.split('_')[-1].split('.')[0]
#         return datetime.strptime(date_str, '%Y-%m-%d')
#     except ValueError:
#         return None

# # Process the files to find the one with the latest date
# latest_file = None
# latest_date = datetime.min

# for file_path in file_paths:
#     file_date = extract_date(os.path.basename(file_path))
#     if file_date and file_date > latest_date:
#         latest_date = file_date
#         latest_file = file_path

# if latest_file:
#     print(f"The latest file is: {latest_file}")
# else:
#     print("No matching files found.")



# #################################################################################
# ##############Index version comparison with new sitemap date#####################
# #################################################################################
# # Index version is the same as main dataset only without content
# import json
# import os
# from datetime import datetime

# # Assuming output_directory is defined
# output_directory = '/Users/mortazakiani/dwh_aws_project'

# def compare_sitemaps(new_sitemap_file, index_file):
    
#     new_sitemap = new_sitemap_file
        
#     with open(index_file, 'r') as file:
#         index_data = json.load(file)

#     updated_urls = {}
#     for url, new_records in new_sitemap.items():
#         # Get the most recent lastmod date from index_data, if exists
#         if url in index_data:
#             index_lastmod_dates = [datetime.strptime(record['lastmod'], "%Y-%m-%d") for record in index_data[url]]
#             index_most_recent = max(index_lastmod_dates) if index_lastmod_dates else datetime.min
#         else:
#             index_most_recent = datetime.min

#         # Compare with new_sitemap lastmod dates
#         for new_record in new_records:
#             new_record_date = datetime.strptime(new_record['lastmod'], "%Y-%m-%d")
#             if new_record_date > index_most_recent:
#                 if url not in updated_urls:
#                     updated_urls[url] = []
#                 updated_urls[url].append(new_record)

#     return updated_urls

# def save_updated_data(base_filename, updated_data):
#     filename = f"{base_filename}_updated.json"
#     filepath = os.path.join(output_directory, filename)
#     with open(filepath, 'w') as file:
#         json.dump(updated_data, file, indent=4)

# # Usage
# new_sitemap_file = url_data
# index_file = latest_file
# updated_urls = compare_sitemaps(new_sitemap_file, index_file)
# save_updated_data('updated_urls', updated_urls)





# #################################################################################
# ##############Download Diffs from index and new sitemap##########################
# #################################################################################

# import requests
# from time import sleep
# import json
# import os
# from datetime import datetime

# # Assume updated_urls is defined and filled with the new data


# def fetch_html_content(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.text
#         else:
#             return 'Failed to retrieve content'
#     except requests.RequestException:
#         return 'Request failed'

# def save_data(base_filename, data):
#     #date_str = datetime.now().strftime("%Y-%m-%d")
#     filename = f"{base_filename}.json"
#     output_directory = '/Users/mortazakiani/dwh_aws_project'
#     filepath = os.path.join(output_directory, filename)
#     with open(filepath, 'w') as file:
#         json.dump(data, file, indent=4)

# def process_sitemaps_and_index_differences():
#     # Assuming final_data is the existing data loaded from a JSON file
#     # final_data = { 'https://www.example.com/page1': [{'lastmod': '2023-12-17', 'content': '...'}], ... }
    
#     final_data = {}  # Replace with the actual data loading logic as per your application
#     total_urls = sum(len(records) for records in updated_urls.values())
#     processed_urls = 0

#     for url, records in updated_urls.items():
#         for record in records:
#             new_lastmod_date = datetime.strptime(record['lastmod'], "%Y-%m-%d")

#             # Check if the URL already exists in final_data
#             if url not in final_data:
#                 final_data[url] = []
#                 html_content = fetch_html_content(url)
#                 final_data[url].append({'lastmod': record['lastmod'], 'content': html_content})
#             else:
#                 # Add the new data with content only if the lastmod is more recent
#                 existing_lastmod_dates = [datetime.strptime(item['lastmod'], "%Y-%m-%d") for item in final_data[url]]
#                 if new_lastmod_date > max(existing_lastmod_dates):
#                     html_content = fetch_html_content(url)
#                     final_data[url].append({'lastmod': record['lastmod'], 'content': html_content})

#             processed_urls += 1
#             print(f"Processed {processed_urls}/{total_urls} URLs")
#             save_data('diffs_Index_and_new_sitemap', final_data)
#     return final_data

# finaldata= process_sitemaps_and_index_differences()



# #################################################################################
# ##########################Path of latest dataset file############################
# #################################################################################

# import os
# import glob
# from datetime import datetime

# # Directory where the files are stored
# directory = '/Users/mortazakiani/dwh_aws_project'

# # Pattern to match the files of interest
# pattern = 'scraped_data_dataset_*.json'

# # Get a list of all matching files in the directory
# file_paths = glob.glob(os.path.join(directory, pattern))

# def extract_date(file_name):
#     try:
#         # Extracting the date from the file name
#         date_str = file_name.split('_')[-1].split('.')[0]
#         return datetime.strptime(date_str, '%Y-%m-%d')
#     except ValueError:
#         return None

# # Process the files to find the one with the latest date
# latest_file = None
# latest_date = datetime.min

# for file_path in file_paths:
#     file_date = extract_date(os.path.basename(file_path))
#     if file_date and file_date > latest_date:
#         latest_date = file_date
#         latest_file = file_path

# if latest_file:
#     print(f"The latest file is: {latest_file}")
# else:
#     print("No matching files found.")



# #################################################################################
# ##########################Update Dataset in the storage##########################
# #################################################################################
# import json
# from datetime import datetime

# def merge_json_files(old_file, new_file):
#     # Load the old data
#     with open(old_file, 'r') as file:
#         old_data = json.load(file)

#     # Load the new data
#     with open(new_file, 'r') as file:
#         new_data = json.load(file)

#     # Iterate through each URL in the new data
#     for url, new_records in new_data.items():
#         # If the URL does not exist in old data, add it directly
#         if url not in old_data:
#             print(f"Adding new URL not in old data: {url}")
#             old_data[url] = new_records
#         else:
#             # If the URL exists, iterate through its records
#             for new_record in new_records:
#                 new_date = datetime.strptime(new_record["lastmod"], "%Y-%m-%d")
#                 old_dates = [datetime.strptime(record["lastmod"], "%Y-%m-%d") for record in old_data[url]]
#                 # Add the new record if its date is more recent
#                 if new_date > max(old_dates):
#                     print(f"Updating existing URL with new record: {url}")
#                     old_data[url].append(new_record)

#     # Write the merged data to the output file
#     with open(old_file, 'w') as file:
#         json.dump(old_data, file, indent=4)

# # Function usage
# merge_json_files(old_file=latest_file, new_file='/Users/mortazakiani/dwh_aws_project/diffs_Index_and_new_sitemap.json')
