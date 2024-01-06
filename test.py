import os

for file_name in os.listdir("../scraping"):
    if file_name.startswith("scraped_data_dataset_"):
        scraped_dataset = file_name