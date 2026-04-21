# import requests
import os

import aiohttp
import asyncio
import zipfile

import time
from pathlib import Path


download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

directory_name = "downloads"

def create_directory():
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except Exception as e:
        print(f"An error occurred while creating the directory: {e}")


async def download_file(session, url, dest_dir):
    filename=url.split("/")[-1]
    filepath=os.path.join(dest_dir, filename)

    try:
        async with session.get(url) as response:
            if response.status == 200:
                with open(filepath, 'wb') as f:
                    async for chunk in response.content.iter_chunked(1024*1024):
                        f.write(chunk)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download {filename}. Status code: {response.status}")
    except Exception as e:
        print(f"An error occurred while downloading {filename}: {e}")

    
async def download_all(urls, dest_dir):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(download_file(session, url, dest_dir))
            tasks.append(task)
        await asyncio.gather(*tasks)

def extract_zip_files(dest_dir):
    dest_dir = Path(dest_dir)
    for zip_file in dest_dir.glob('*.zip'):
        print(f"Extracting {zip_file}...")
        try:
            with zipfile.ZipFile(zip_file, 'r') as z:
                csv_files=[z for z in z.namelist() if z.endswith('.csv')]

                if csv_files:
                    for csv in csv_files:
                        z.extract(csv, dest_dir)
                        print(f"Extracted {csv} from {zip_file}")

                    zip_file.unlink()  # Delete the zip file after extraction
                    print(f"Deleted {zip_file} after extraction.")
                else:
                    print(f"No CSV files found in {zip_file}")
        except zipfile.BadZipFile:
            print(f"Error: {zip_file} is not a valid zip file.")
        except Exception as e:
            print(f"An error occurred while extracting {zip_file}: {e}")
    print("All zip files have been processed.")
        
       

def main():
    create_directory()

    print("Starting downloads...")
    start_time = time.time()

    asyncio.run(download_all(download_uris, directory_name))

    elapsed_time = time.time() - start_time
    print(f"All downloads completed in {elapsed_time:.2f} seconds.")
    extract_zip_files(directory_name)
if __name__ == "__main__":
    main()
