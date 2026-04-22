import requests
import pandas
from bs4 import BeautifulSoup
import re

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

def main():
    web_scraping()
     


if __name__ == "__main__":
    main()
