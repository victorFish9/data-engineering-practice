import requests

import gzip
import shutil

def main():
    url = 'https://data.commoncrawl.org/crawl-data/CC-MAIN-2022-05/wet.paths.gz'
    local_filename = 'wet.paths.gz'

    print(f"Verifying access to URL: {url}")

    head_reponse = requests.head(url)
    if head_reponse.status_code == 200:
        print("URL is accessible. Proceeding to download the file.")
        
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(local_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

        print(f"File downloaded successfully and saved as '{local_filename}'.")
    else:
        print(f"Failed to access the URL. Status code: {head_reponse.status_code}")

    with gzip.open(local_filename, 'rb') as f_in:
        with open('wet.paths.txt', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            print("File decompressed successfully and saved as 'wet.paths.txt'.")



if __name__ == "__main__":
    main()
