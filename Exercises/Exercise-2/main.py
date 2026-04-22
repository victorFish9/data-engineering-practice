import requests
import pandas

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

import os
import sys

URL='https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/'

def web_scraping():
    print("Scraping the web page...")
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    target_item="2024-01-19 15:33"

    time_element=soup.find(string=re.compile(target_item))

    if time_element:
        parent_row=time_element.find_parent('tr')

        if parent_row:
            file_link=parent_row.find('a')
            print(f"Found the file link: {file_link['href']}")
        else:
            previous_link=time_element.find_previous('a')
            if previous_link:
                print(f"Found the file link: {previous_link['href']}")
    else:
        print("Target item not found in the web page.")

    download_file(file_link)

def download_file(file_link):
    file_name=file_link['href']
    file_url=urljoin(URL, file_name)
    print(f"Downloading the file from: {file_url}")
    file_response=requests.get(file_url)

    if file_response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(file_response.content)
        print(f"File '{file_name}' downloaded successfully.")
        full_path=os.path.abspath(file_name)
        print(f"Full path to the downloaded file: {full_path}")
        extract_data_from_file(file_name)
    else:
        print(f"Failed to download the file. Status code: {file_response.status_code}")

def extract_data_from_file(file_name):
    print(f"Extracting data from the file: {file_name}")
    data = pandas.read_csv(file_name)

    
    max_temp = data['HourlyDryBulbTemperature'].max()
    print("Data extracted successfully.")
    print(max_temp)

    #print the max temperature to the console (stdout)
    sys.stdout.write('The highest HourlyDryBulbTemperature: ' + str(max_temp) + '\n')
def main():
    web_scraping()
    
     


if __name__ == "__main__":
    main()
