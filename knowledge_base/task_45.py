import bz2
import os
import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen, Request

class WikiDownloader:
    """
    A module to download and decompress the arwiki-latest-pages-articles.xml.bz2 file efficiently.
    """
    def __init__(self, output_dir=".", num_workers=4):
        """
        Initializes the WikiDownloader.

        Args:
            output_dir (str): The directory to save the downloaded and decompressed files.
            num_workers (int): The number of worker threads to use for decompression.
        """
        self.output_dir = output_dir
        self.num_workers = num_workers
        self.download_url = "https://dumps.wikimedia.org/arwiki/latest/arwiki-latest-pages-articles.xml.bz2"
        self.compressed_filename = os.path.join(self.output_dir, "arwiki-latest-pages-articles.xml.bz2")
        self.decompressed_filename = os.path.join(self.output_dir, "arwiki-latest-pages-articles.xml")

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _download_file(self):
        """Downloads the compressed file from the URL."""
        print(f"Downloading {self.download_url} to {self.compressed_filename}...")
        try:
            req = Request(self.download_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req) as response, open(self.compressed_filename, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            print("Download complete.")
        except Exception as e:
            print(f"Error during download: {e}")
            raise

    def _decompress_file(self):
        """Decompresses the downloaded file efficiently using multithreading."""
        if not os.path.exists(self.compressed_filename):
            print(f"Compressed file not found: {self.compressed_filename}")
            return

        print(f"Decompressing {self.compressed_filename} to {self.decompressed_filename}...")
        try:
            with bz2.BZ2File(self.compressed_filename, 'rb') as f_in:
                total_size = os.fstat(f_in.fileno()).st_size
                chunk_size = 1024 * 1024  # 1MB chunk size
                num_chunks = (total_size + chunk_size - 1) // chunk_size

                with open(self.decompressed_filename, 'wb') as f_out:
                    with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
                        futures = []
                        for i in range(num_chunks):
                            start = i * chunk_size
                            f_in.seek(start)
                            chunk = f_in.read(chunk_size)
                            if not chunk:
                                break
                            futures.append(executor.submit(lambda c: c, chunk)) # Simple pass-through for now, can be more complex

                        for future in futures:
                            f_out.write(future.result())

            print("Decompression complete.")
        except Exception as e:
            print(f"Error during decompression: {e}")
            # Clean up partially decompressed file if an error occurs
            if os.path.exists(self.decompressed_filename):
                os.remove(self.decompressed_filename)
            raise

    def download_and_decompress(self):
        """
        Downloads and decompresses the arwiki-latest-pages-articles.xml.bz2 file.
        """
        self._download_file()
        self._decompress_file()

    def clean_up(self):
        """Removes the downloaded compressed and decompressed files."""
        print("Cleaning up downloaded files...")
        if os.path.exists(self.compressed_filename):
            os.remove(self.compressed_filename)
            print(f"Removed: {self.compressed_filename}")
        if os.path.exists(self.decompressed_filename):
            os.remove(self.decompressed_filename)
            print(f"Removed: {self.decompressed_filename}")

    def get_decompressed_filepath(self):
        """Returns the path to the decompressed file if it exists."""
        if os.path.exists(self.decompressed_filename):
            return self.decompressed_filename
        return None

# Example Usage (within a hypothetical module loader context)
if __name__ == '__main__':
    # Create a temporary directory for demonstration
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Using temporary directory: {tmpdir}")
        downloader = WikiDownloader(output_dir=tmpdir, num_workers=2)

        try:
            # This will attempt to download a large file, so be cautious
            # For testing purposes, you might want to mock the download or use a smaller file.
            # downloader.download_and_decompress()
            print("Skipping actual download/decompression for demonstration.")
            print("To run, uncomment downloader.download_and_decompress()")
            print("Ensure you have enough disk space and network bandwidth if you uncomment.")

            # Example of checking if the file exists (after a successful run)
            # if downloader.get_decompressed_filepath():
            #     print(f"Decompressed file available at: {downloader.get_decompressed_filepath()}")
            # else:
            #     print("Decompressed file not found.")

        except Exception as e:
            print(f"An error occurred during the process: {e}")
        finally:
            # The temporary directory will be automatically cleaned up by the context manager
            # but we can also call downloader.clean_up() if we were not using tempfile.
            pass