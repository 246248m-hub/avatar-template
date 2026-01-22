import bz2
import os
import requests
import shutil
import threading
import time
from typing import Any, Dict, List, Optional

class AresDownloader:
    """
    A module to download and decompress the arwiki-latest-pages-articles.xml.bz2 file efficiently.
    """
    def __init__(self, download_dir: str = "data"):
        self.url = "https://dumps.wikimedia.org/arwiki/latest/arwiki-latest-pages-articles.xml.bz2"
        self.download_dir = download_dir
        self.bz2_filepath = os.path.join(self.download_dir, "arwiki-latest-pages-articles.xml.bz2")
        self.xml_filepath = os.path.join(self.download_dir, "arwiki-latest-pages-articles.xml")
        os.makedirs(self.download_dir, exist_ok=True)

    def download_file(self) -> bool:
        """
        Downloads the compressed file from the URL.
        Returns True if download is successful, False otherwise.
        """
        if os.path.exists(self.bz2_filepath):
            print(f"File already exists: {self.bz2_filepath}")
            return True

        print(f"Downloading {self.url} to {self.bz2_filepath}...")
        try:
            with requests.get(self.url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                block_size = 8192
                downloaded_size = 0
                with open(self.bz2_filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=block_size):
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        progress = (downloaded_size / total_size) * 100 if total_size else 0
                        print(f"Downloaded: {downloaded_size}/{total_size} bytes ({progress:.2f}%)", end='\r')
            print("\nDownload complete.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")
            return False

    def decompress_file(self) -> bool:
        """
        Decompresses the downloaded .bz2 file into an .xml file.
        Returns True if decompression is successful, False otherwise.
        """
        if os.path.exists(self.xml_filepath):
            print(f"Decompressed file already exists: {self.xml_filepath}")
            return True

        if not os.path.exists(self.bz2_filepath):
            print(f"Compressed file not found: {self.bz2_filepath}. Please download it first.")
            return False

        print(f"Decompressing {self.bz2_filepath} to {self.xml_filepath}...")
        try:
            with bz2.BZ2File(self.bz2_filepath, 'rb') as f_in, open(self.xml_filepath, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            print("Decompression complete.")
            return True
        except Exception as e:
            print(f"Error during decompression: {e}")
            return False

    def clean_up(self) -> None:
        """
        Removes the downloaded compressed and decompressed files.
        """
        if os.path.exists(self.bz2_filepath):
            os.remove(self.bz2_filepath)
            print(f"Removed: {self.bz2_filepath}")
        if os.path.exists(self.xml_filepath):
            os.remove(self.xml_filepath)
            print(f"Removed: {self.xml_filepath}")
        if not os.listdir(self.download_dir):
            os.rmdir(self.download_dir)
            print(f"Removed directory: {self.download_dir}")

    def run_task(self) -> Optional[str]:
        """
        Executes the download and decompression process.
        Returns a success message or an error message.
        """
        if not self.download_file():
            return "Error: Failed to download the compressed file."

        if not self.decompress_file():
            return "Error: Failed to decompress the file."

        return f"Successfully downloaded and decompressed to {self.xml_filepath}"

# Example of how to use this module within a hypothetical AI Architect framework
# This part is for demonstration and context, not part of the module itself.

class ModuleLoader:
    def __init__(self):
        self.loaded_modules: Dict[str, Any] = {}
        self.module_paths: Dict[str, str] = {}

    def add_module_path(self, module_name: str, module_path: str):
        self.module_paths[module_name] = module_path

    def load_module(self, module_name: str) -> Optional[Any]:
        if module_name in self.loaded_modules:
            return self.loaded_modules[module_name]

        if module_name not in self.module_paths:
            print(f"Error: Module path for '{module_name}' not found.")
            return None

        module_path = self.module_paths[module_name]
        try:
            # In a real scenario, you might use importlib or a more sophisticated loading mechanism
            # For simplicity, we'll assume the module_path points to a Python file
            # and the module itself has a class with the same name or a specific entry point.

            # This is a simplified example. A robust loader would handle different module structures.
            import importlib.util
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Assuming the module has a class with the same name or a default factory function
            if hasattr(module, module_name):
                instance = getattr(module, module_name)()
            elif hasattr(module, 'create_instance'):
                instance = module.create_instance()
            else:
                print(f"Error: Module '{module_name}' does not have a discoverable entry point (e.g., class '{module_name}' or 'create_instance').")
                return None

            self.loaded_modules[module_name] = instance
            print(f"Module '{module_name}' loaded successfully.")
            return instance
        except Exception as e:
            print(f"Error loading module '{module_name}' from {module_path}: {e}")
            return None

    def unload_module(self, module_name: str) -> bool:
        if module_name in self.loaded_modules:
            del self.loaded_modules[module_name]
            print(f"Module '{module_name}' unloaded.")
            return True
        print(f"Module '{module_name}' was not loaded.")
        return False

    def get_available_module_names(self) -> List[str]:
        return list(self.loaded_modules.keys())

    def run_module(self, module_name: str, *args: Any, **kwargs: Any) -> Any:
        module_instance = self.loaded_modules.get(module_name)
        if not module_instance:
            print(f"Module '{module_name}' not loaded. Attempting to load...")
            module_instance = self.load_module(module_name)
            if not module_instance:
                print(f"Failed to load module '{module_name}'. Cannot run task.")
                return None

        if hasattr(module_instance, 'run_task') and callable(module_instance.run_task):
            try:
                return module_instance.run_task(*args, **kwargs)
            except Exception as e:
                print(f"Error running task in module '{module_name}': {e}")
                return None
        else:
            print(f"Module '{module_name}' does not have a callable 'run_task' method.")
            return None

# Mock CoreMemory class for demonstration
class MockCoreMemory:
    def __init__(self):
        self.data = {"capabilities": []}

    def add_capability(self, capability: str):
        if capability not in self.data["capabilities"]:
            self.data["capabilities"].append(capability)

if __name__ == "__main__":
    # Create a dummy Python file for the AresDownloader module
    DUMMY_MODULE_CONTENT = """
import bz2
import os
import requests
import shutil
import time
from typing import Any, Optional

class AresDownloader:
    def __init__(self, download_dir: str = "data"):
        self.url = "https://dumps.wikimedia.org/arwiki/latest/arwiki-latest-pages-articles.xml.bz2"
        self.download_dir = download_dir
        self.bz2_filepath = os.path.join(self.download_dir, "arwiki-latest-pages-articles.xml.bz2")
        self.xml_filepath = os.path.join(self.download_dir, "arwiki-latest-pages-articles.xml")
        os.makedirs(self.download_dir, exist_ok=True)

    def download_file(self) -> bool:
        if os.path.exists(self.bz2_filepath):
            print(f"File already exists: {self.bz2_filepath}")
            return True
        print(f"Downloading {self.url} to {self.bz2_filepath}...")
        try:
            with requests.get(self.url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                block_size = 8192
                downloaded_size = 0
                with open(self.bz2_filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=block_size):
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        progress = (downloaded_size / total_size) * 100 if total_size else 0
                        print(f"Downloaded: {downloaded_size}/{total_size} bytes ({progress:.2f}%)", end='\\r')
            print("\\nDownload complete.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")
            return False

    def decompress_file(self) -> bool:
        if os.path.exists(self.xml_filepath):
            print(f"Decompressed file already exists: {self.xml_filepath}")
            return True
        if not os.path.exists(self.bz2_filepath):
            print(f"Compressed file not found: {self.bz2_filepath}. Please download it first.")
            return False
        print(f"Decompressing {self.bz2_filepath} to {self.xml_filepath}...")
        try:
            with bz2.BZ2File(self.bz2_filepath, 'rb') as f_in, open(self.xml_filepath, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            print("Decompression complete.")
            return True
        except Exception as e:
            print(f"Error during decompression: {e}")
            return False

    def clean_up(self) -> None:
        if os.path.exists(self.bz2_filepath):
            os.remove(self.bz2_filepath)
            print(f"Removed: {self.bz2_filepath}")
        if os.path.exists(self.xml_filepath):
            os.remove(self.xml_filepath)
            print(f"Removed: {self.xml_filepath}")
        if not os.listdir(self.download_dir):
            os.rmdir(self.download_dir)
            print(f"Removed directory: {self.download_dir}")

    def run_task(self, download_only: bool = False, decompress_only: bool = False) -> Optional[str]:
        if not download_only and not decompress_only:
            if not self.download_file():
                return "Error: Failed to download the compressed file."
            if not self.decompress_file():
                return "Error: Failed to decompress the file."
            return f"Successfully downloaded and decompressed to {self.xml_filepath}"
        elif download_only:
            if self.download_file():
                return f"Successfully downloaded to {self.bz2_filepath}"
            else:
                return "Error: Failed to download the compressed file."
        elif decompress_only:
            if self.decompress_file():
                return f"Successfully decompressed to {self.xml_filepath}"
            else:
                return "Error: Failed to decompress the file (ensure .bz2 exists)."
        return "Invalid parameters for run_task."

def create_instance():
    return AresDownloader()
"""
    TASK_DIR = "test_modules"
    MODULE_FILENAME = "ares_downloader_module.py"
    MODULE_PATH = os.path.join(TASK_DIR, MODULE_FILENAME)

    os.makedirs(TASK_DIR, exist_ok=True)
    with open(MODULE_PATH, "w") as f:
        f.write(DUMMY_MODULE_CONTENT)

    # --- Test Execution ---
    print("--- Starting AresDownloader Module Test ---")

    loader = ModuleLoader()
    mock_mem = MockCoreMemory()

    # Add the module path
    loader.add_module_path("AresDownloader", MODULE_PATH)
    mock_mem.add_capability("AresDownloader")

    print("\n--- Test Case 1: Initial State ---")
    print("Current loaded modules:", loader.get_available_module_names())
    print("Core Memory Capabilities:", mock_mem.data.get("capabilities"))

    print("\n--- Test Case 2: Running AresDownloader task for the first time ---")
    # This will download and decompress the file.
    # For a quick test, you might want to mock the download or use a smaller dummy file.
    # The actual download can take a significant amount of time and disk space.
    # We will simulate the process without a real download for the sake of this example execution.

    # To make this test runnable without actually downloading GBs of data:
    # 1. Create a small dummy bz2 file.
    # 2. Mock the requests.get call to return dummy content.
    # 3. Mock bz2.BZ2File and shutil.copyfileobj.

    # For this demonstration, we'll assume the file is already present or skip the actual download/decompression
    # and focus on the module loading and task execution flow.

    # Let's simulate a successful run_task by ensuring the file exists or mocking it.
    # In a real scenario, you'd uncomment the following and it would proceed with download/decompression.
    # result = loader.run_module("AresDownloader")
    # print("Result:", result)

    # To avoid actual download/decompression for the demo, we'll check if it's loaded
    # and if the run_task method exists.
    print("Loading AresDownloader module...")
    loaded_downloader = loader.load_module("AresDownloader")
    assert loaded_downloader is not None
    assert "AresDownloader" in loader.get_available_module_names()
    assert hasattr(loaded_downloader, 'run_task') and callable(loaded_downloader.run_task)

    print("\n--- Test Case 3: Running AresDownloader task with specific options ---")
    # Mocking run_task to return success without actual file operations for this test run
    original_run_task = AresDownloader.run_task
    def mock_run_task(self, download_only: bool = False, decompress_only: bool = False) -> Optional[str]:
        if download_only:
            print("Mock download_file called.")
            return f"Mock: Downloaded to {self.bz2_filepath}"
        elif decompress_only:
            print("Mock decompress_file called.")
            return f"Mock: Decompressed to {self.xml_filepath}"
        else:
            print("Mock download_file and decompress_file called.")
            return f"Mock: Successfully processed to {self.xml_filepath}"

    AresDownloader.run_task = mock_run_task # Monkey patch for testing

    print("Running AresDownloader with download_only=True:")
    result_download_only = loader.run_module("AresDownloader", download_only=True)
    print("Result:", result_download_only)
    assert "Mock: Downloaded to" in result_download_only

    print("\nRunning AresDownloader with decompress_only=True:")
    result_decompress_only = loader.run_module("AresDownloader", decompress_only=True)
    print("Result:", result_decompress_only)
    assert "Mock: Decompressed to" in result_decompress_only

    print("\nRunning AresDownloader with default options:")
    result_full_process = loader.run_module("AresDownloader")
    print("Result:", result_full_process)
    assert "Mock: Successfully processed to" in result_full_process

    AresDownloader.run_task = original_run_task # Restore original method

    print("\n--- Test Case 4: Mock Core Memory Capabilities after adding module ---")
    print("Core Memory Capabilities:", mock_mem.data.get("capabilities"))
    assert "AresDownloader" in mock_mem.data.get("capabilities")

    print("\n--- Test Case 5: Unloading Module ---")
    unloaded = loader.unload_module("AresDownloader")
    print(f"Unloaded 'AresDownloader': {unloaded}")
    assert unloaded is True
    assert "AresDownloader" not in loader.get_available_module_names()
    assert len(loader.loaded_modules) == 0

    print("\nTrying to run unloaded 'AresDownloader':")
    result_after_unload = loader.run_module("AresDownloader", "This should trigger loading")
    print("Result (after unload):", result_after_unload)
    # Since the actual download is not performed in this mocked test,
    # if it triggers loading it should return the mock result.
    assert result_after_unload is not None and "Mock:" in result_after_unload

    print("\nTrying to unload a non-existent module:")
    unloaded_nonexistent = loader.unload_module("NonExistentModule")
    print(f"Unloaded 'NonExistentModule': {unloaded_nonexistent}")
    assert unloaded_nonexistent is False

    # --- Cleanup ---
    print("\nCleaning up test directory...")
    if os.path.exists(TASK_DIR):
        shutil.rmtree(TASK_DIR)
        print(f"Removed test directory: {TASK_DIR}")

    # Clean up any potentially downloaded files from previous runs if not mocked
    downloader_instance = AresDownloader()
    downloader_instance.clean_up()

    print("\n--- AresDownloader Module Test Complete ---")