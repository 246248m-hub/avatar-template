import os
import bz2
import requests
import shutil
from concurrent.futures import ThreadPoolExecutor

def download_and_decompress_arwiki(output_dir="."):
    """
    Downloads the arwiki-latest-pages-articles.xml.bz2 file and decompresses it.

    Args:
        output_dir (str): The directory where the downloaded and decompressed
                          files will be saved. Defaults to the current directory.
    """
    url = "https://dumps.wikimedia.org/other/arwiki-latest-pages-articles.xml.bz2"
    compressed_filename = "arwiki-latest-pages-articles.xml.bz2"
    decompressed_filename = "arwiki-latest-pages-articles.xml"
    compressed_filepath = os.path.join(output_dir, compressed_filename)
    decompressed_filepath = os.path.join(output_dir, decompressed_filename)

    os.makedirs(output_dir, exist_ok=True)

    print(f"Downloading {compressed_filename} from {url}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        with open(compressed_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {compressed_filename} to {compressed_filepath}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return

    print(f"Decompressing {compressed_filename} to {decompressed_filepath}...")
    try:
        with bz2.BZ2File(compressed_filepath, 'rb') as f_in:
            with open(decompressed_filepath, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"Decompressed file saved to {decompressed_filepath}")
    except IOError as e:
        print(f"Error during decompression: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during decompression: {e}")

    # Optional: Clean up the compressed file after successful decompression
    # try:
    #     os.remove(compressed_filepath)
    #     print(f"Removed temporary compressed file: {compressed_filepath}")
    # except OSError as e:
    #     print(f"Error removing compressed file: {e}")

if __name__ == "__main__":
    # Example usage:
    download_dir = "arwiki_data"
    download_and_decompress_arwiki(output_dir=download_dir)

    print("\n--- Download and Decompression Complete ---")
    print(f"Check the '{download_dir}' directory for the decompressed file.")

    # You can now process the 'arwiki-latest-pages-articles.xml' file.
    # For example, to get the size of the decompressed file:
    decompressed_file_path = os.path.join(download_dir, "arwiki-latest-pages-articles.xml")
    if os.path.exists(decompressed_file_path):
        file_size = os.path.getsize(decompressed_file_path)
        print(f"Size of decompressed file: {file_size} bytes")
    else:
        print("Decompressed file not found.")

    # Example of how to potentially use ThreadPoolExecutor for decompression if needed,
    # though bz2.BZ2File often handles this efficiently on its own.
    # This is more illustrative if you had multiple files to decompress.

    # def decompress_single_file(input_path, output_path):
    #     print(f"Decompressing {input_path} to {output_path} in a thread...")
    #     try:
    #         with bz2.BZ2File(input_path, 'rb') as f_in:
    #             with open(output_path, 'wb') as f_out:
    #                 shutil.copyfileobj(f_in, f_out)
    #         print(f"Successfully decompressed {input_path}")
    #         return True
    #     except Exception as e:
    #         print(f"Error decompressing {input_path}: {e}")
    #         return False

    # if os.path.exists(compressed_filepath):
    #     print("\nDemonstrating potential multi-threaded decompression (if needed)...")
    #     with ThreadPoolExecutor(max_workers=2) as executor:
    #         future_decompress = executor.submit(
    #             decompress_single_file,
    #             compressed_filepath,
    #             decompressed_filepath + "_threaded"
    #         )
    #         if future_decompress.result():
    #             print("Threaded decompression finished successfully.")
    #         else:
    #             print("Threaded decompression encountered an error.")