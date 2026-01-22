import bz2
import os
import requests
import shutil
import tempfile
from typing import Optional, Dict, Any

# Define the URL for the dataset
WIKI_DUMP_URL = "https://dumps.wikimedia.org/arwiki/latest/arwiki-latest-pages-articles.xml.bz2"
# Define the default download directory
DEFAULT_DOWNLOAD_DIR = tempfile.gettempdir()
# Define the default output directory for decompressed file
DEFAULT_OUTPUT_DIR = tempfile.gettempdir()

def download_and_decompress_wiki_dump(
    url: str = WIKI_DUMP_URL,
    download_dir: str = DEFAULT_DOWNLOAD_DIR,
    output_dir: str = DEFAULT_OUTPUT_DIR,
    chunk_size: int = 8192  # Bytes
) -> Optional[str]:
    """
    Downloads a bz2 compressed file from a given URL and decompresses it.

    Args:
        url (str): The URL of the bz2 file to download.
        download_dir (str): The directory to save the downloaded file.
        output_dir (str): The directory to save the decompressed file.
        chunk_size (int): The size of chunks to read/write during download and decompression.

    Returns:
        Optional[str]: The absolute path to the decompressed file if successful,
                       otherwise None.
    """
    if not url.endswith(".bz2"):
        print(f"Error: The provided URL does not point to a .bz2 file: {url}")
        return None

    # Create directories if they don't exist
    os.makedirs(download_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Extract filename from URL
    filename = url.split('/')[-1]
    compressed_filepath = os.path.join(download_dir, filename)
    decompressed_filename = filename.replace(".bz2", "")
    decompressed_filepath = os.path.join(output_dir, decompressed_filename)

    print(f"Attempting to download: {url}")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()  # Raise an exception for bad status codes
            total_size = int(r.headers.get('content-length', 0))
            downloaded_size = 0
            print(f"Downloading to: {compressed_filepath}")
            with open(compressed_filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    # Optional: Print download progress
                    if total_size > 0:
                        progress = (downloaded_size / total_size) * 100
                        print(f"  Downloaded {downloaded_size}/{total_size} bytes ({progress:.2f}%)", end='\r')
                    else:
                        print(f"  Downloaded {downloaded_size} bytes", end='\r')
        print("\nDownload complete.")

    except requests.exceptions.RequestException as e:
        print(f"Error during download: {e}")
        # Clean up partially downloaded file if any
        if os.path.exists(compressed_filepath):
            os.remove(compressed_filepath)
        return None
    except Exception as e:
        print(f"An unexpected error occurred during download: {e}")
        if os.path.exists(compressed_filepath):
            os.remove(compressed_filepath)
        return None

    print(f"Attempting to decompress: {compressed_filepath}")
    try:
        with bz2.BZ2File(compressed_filepath, 'rb') as f_in:
            with open(decompressed_filepath, 'wb') as f_out:
                while True:
                    chunk = f_in.read(chunk_size)
                    if not chunk:
                        break
                    f_out.write(chunk)
        print(f"Decompression complete. Decompressed file saved to: {decompressed_filepath}")
        return decompressed_filepath

    except FileNotFoundError:
        print(f"Error: Compressed file not found at {compressed_filepath}")
        return None
    except OSError as e:
        print(f"Error during decompression (IO error): {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during decompression: {e}")
        return None
    finally:
        # Clean up the compressed file after successful decompression (optional)
        if os.path.exists(compressed_filepath):
            try:
                os.remove(compressed_filepath)
                print(f"Removed compressed file: {compressed_filepath}")
            except OSError as e:
                print(f"Error removing compressed file {compressed_filepath}: {e}")


if __name__ == '__main__':
    # Example usage:
    print("--- Starting Wiki Dump Download and Decompression ---")

    # Use a specific directory for testing if needed
    # test_download_dir = "./temp_downloads"
    # test_output_dir = "./temp_decompressed"

    # Ensure directories exist for the example
    os.makedirs(DEFAULT_DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)

    # Download and decompress the arwiki dump
    decompressed_file_path = download_and_decompress_wiki_dump()

    if decompressed_file_path:
        print(f"\nSuccessfully downloaded and decompressed. File path: {decompressed_file_path}")
        # You can now process the decompressed XML file
        # For demonstration, we'll just check if the file exists and its size.
        if os.path.exists(decompressed_file_path):
            file_size = os.path.getsize(decompressed_file_path)
            print(f"Decompressed file size: {file_size} bytes")
            # Example of opening and reading a small part
            try:
                with open(decompressed_file_path, 'r', encoding='utf-8') as f:
                    print("\nFirst 500 characters of the decompressed file:")
                    print(f.read(500))
            except Exception as e:
                print(f"Could not read the decompressed file: {e}")
        else:
            print("Error: Decompressed file path does not exist.")
    else:
        print("\nFailed to download and decompress the wiki dump.")

    # --- Cleanup ---
    # It's good practice to clean up the decompressed file if it's only for temporary use.
    # Be cautious if you intend to keep the decompressed file.
    if decompressed_file_path and os.path.exists(decompressed_file_path):
        try:
            os.remove(decompressed_file_path)
            print(f"\nCleaned up decompressed file: {decompressed_file_path}")
        except OSError as e:
            print(f"Error cleaning up decompressed file {decompressed_file_path}: {e}")

    # If you used specific test directories, clean them up here.
    # if os.path.exists("./temp_downloads"):
    #     shutil.rmtree("./temp_downloads")
    # if os.path.exists("./temp_decompressed"):
    #     shutil.rmtree("./temp_decompressed")

    print("\n--- Script Finished ---")