import os
from urllib.request import urlretrieve
import zipfile
from pathlib import Path
import aiohttp
import asyncio
#import requests

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]
download_uris_test = "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip"


def main():
    directory_name = "downloads"
    download_path=Path("./downloads")
    filename="/Users/admin/Desktop/portfolio/data-engineering-practice/Exercises/Exercise-1/downloads/"

    #create a directory to store the downloaded files
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except Exception as e:
        print(f"An error occurred while creating the directory: {e}")
        return
    
    #download the files from the provided URIs
    for uri in download_uris:
        print(filename + uri[-23::])
        urlretrieve(uri, filename + uri[-23::])

        if os.path.exists(filename + uri[-23::]):
            print(f"File '{filename + uri[-23::]}' downloaded successfully.")
        else:
            print(f"Failed to download the file '{filename + uri[-23::]}'.")
    
    #unzip the downloaded files and delete the zip files
    for zip_file in download_path.glob("*.zip"):
        print(f"Working on: {zip_file.name}")
        try:
            with zipfile.ZipFile(zip_file, 'r') as z:
                csv_files=[f for f in z.namelist() if f.endswith('.csv')]

                if csv_files:
                    for csv in csv_files:
                        z.extract(csv, download_path)
                        print(f"Extracted: {csv}")
                    
                    zip_file.unlink()
                    print(f"Deleted: {zip_file.name}")

                else:
                    print(f"No CSV files found in {zip_file.name}")
        except zipfile.BadZipFile:
            print(f"Error: '{zip_file.name}' is not a valid zip file.")
        except Exception as e:
            print(f"An error occurred while processing '{zip_file.name}': {e}")
    print("All zip files processed.")
    
    
    



if __name__ == "__main__":
    main()
