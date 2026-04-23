import requests

import gzip
import shutil
import io

import zlib

def main():
    url = 'https://data.commoncrawl.org/crawl-data/CC-MAIN-2022-05/wet.paths.gz'
    local_filename = 'wet.paths.gz'

    print(f"Verifying access to URL: {url}")

    response = requests.get(url, stream=True)
    response.raise_for_status()

    decompressor = zlib.decompressobj(32 + zlib.MAX_WBITS)

    line_count = 0
    leftover_text = ""

    for chunk in response.iter_content(chunk_size=1024):
        uncompressed_chunk = decompressor.decompress(chunk).decode('utf-8')

        text_data = leftover_text + uncompressed_chunk
        lines = text_data.split('\n')

        leftover_text = lines.pop()

        for line in lines:
            print(line)
            line_count += 1

            if line_count >= 5:  # Example condition to stop after 10 lines
                print("Stopping after 5 lines for demonstration.")
                response.close()
                return

    # file = io.BytesIO(response.content)

    # with gzip.GzipFile(fileobj=file) as decompressed_file:
    #     with open('wet.paths.txt', 'wb') as f_out:
    #         shutil.copyfileobj(decompressed_file, f_out)
    #         print("File downloaded and decompressed successfully, saved as 'wet.paths.txt'.")

    # if head_reponse.status_code == 200:
    #     print("URL is accessible. Proceeding to download the file.")
        
    #     with requests.get(url, stream=True) as response:
    #         response.raise_for_status()
    #         with open(local_filename, 'wb') as file:
    #             for chunk in response.iter_content(chunk_size=8192):
    #                 file.write(chunk)

    #     print(f"File downloaded successfully and saved as '{local_filename}'.")
    # else:
    #     print(f"Failed to access the URL. Status code: {head_reponse.status_code}")

    # with gzip.open(local_filename, 'rb') as f_in:
    #     with open('wet.paths.txt', 'wb') as f_out:
    #         shutil.copyfileobj(f_in, f_out)
    #         print("File decompressed successfully and saved as 'wet.paths.txt'.")



if __name__ == "__main__":
    main()
