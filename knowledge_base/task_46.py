import bz2
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import requests

# --- Core AI Architecture Components ---

class CoreMemory:
    """Simulates core memory capabilities for the AI."""
    def __init__(self):
        self.data = {"capabilities": []}

    def add_capability(self, capability_name: str, description: str):
        """Adds a new capability to the core memory."""
        self.data["capabilities"].append({"name": capability_name, "description": description})
        print(f"CoreMemory: Added capability '{capability_name}'")

    def get_capabilities(self):
        """Retrieves all capabilities from core memory."""
        return self.data.get("capabilities", [])

class ModuleLoader:
    """Manages loading, unloading, and running AI modules."""
    def __init__(self, module_directory: Path = Path("ai_modules")):
        self.module_directory = module_directory
        self.loaded_modules = {}
        if not self.module_directory.exists():
            self.module_directory.mkdir(parents=True, exist_ok=True)

    def _get_module_path(self, module_name: str) -> Path:
        """Constructs the expected file path for a module."""
        return self.module_directory / f"{module_name}.py"

    def load_module(self, module_name: str, module_path: Path = None) -> bool:
        """
        Loads a Python module into the system.

        Args:
            module_name: The name of the module to load (e.g., 'my_task').
            module_path: The explicit path to the module file. If None,
                         it will look for '<module_directory>/<module_name>.py'.

        Returns:
            True if the module was loaded successfully, False otherwise.
        """
        if module_name in self.loaded_modules:
            print(f"ModuleLoader: Module '{module_name}' is already loaded.")
            return True

        if module_path is None:
            module_path = self._get_module_path(module_name)

        if not module_path.is_file():
            print(f"ModuleLoader: Module file not found at '{module_path}'.")
            return False

        try:
            # Dynamically import the module
            import importlib.util
            spec = importlib.util.spec_from_file_location(module_name, str(module_path))
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module  # Add to sys.modules for potential later imports
            spec.loader.exec_module(module)
            self.loaded_modules[module_name] = module
            print(f"ModuleLoader: Successfully loaded module '{module_name}' from '{module_path}'.")
            return True
        except Exception as e:
            print(f"ModuleLoader: Error loading module '{module_name}' from '{module_path}': {e}")
            return False

    def unload_module(self, module_name: str) -> bool:
        """
        Unloads a previously loaded module.

        Args:
            module_name: The name of the module to unload.

        Returns:
            True if the module was unloaded, False if it wasn't loaded.
        """
        if module_name in self.loaded_modules:
            del self.loaded_modules[module_name]
            # Optionally remove from sys.modules if it was added and not a built-in
            if module_name in sys.modules and sys.modules[module_name].__file__.startswith(str(self.module_directory)):
                 del sys.modules[module_name]
            print(f"ModuleLoader: Unloaded module '{module_name}'.")
            return True
        else:
            print(f"ModuleLoader: Module '{module_name}' was not loaded.")
            return False

    def get_available_module_names(self) -> list[str]:
        """Returns a list of names of all currently loaded modules."""
        return list(self.loaded_modules.keys())

    def run_module(self, module_name: str, *args, **kwargs):
        """
        Runs a function within a loaded module.

        If the module is not loaded, it attempts to load it first.
        Assumes the module has a function named 'run' or a function matching
        the module name itself.

        Args:
            module_name: The name of the module to run.
            *args: Positional arguments to pass to the module's run function.
            **kwargs: Keyword arguments to pass to the module's run function.

        Returns:
            The result of the module's run function, or None if the module
            cannot be loaded or doesn't have a suitable run function.
        """
        if module_name not in self.loaded_modules:
            print(f"ModuleLoader: Module '{module_name}' not loaded. Attempting to load...")
            if not self.load_module(module_name):
                print(f"ModuleLoader: Failed to load module '{module_name}'. Cannot run.")
                return None

        module = self.loaded_modules[module_name]
        run_function = None

        if hasattr(module, 'run'):
            run_function = module.run
        elif hasattr(module, module_name):
            run_function = getattr(module, module_name)
        else:
            print(f"ModuleLoader: Module '{module_name}' does not have a 'run' function or a '{module_name}' function.")
            return None

        try:
            print(f"ModuleLoader: Running module '{module_name}' with args: {args}, kwargs: {kwargs}")
            return run_function(*args, **kwargs)
        except Exception as e:
            print(f"ModuleLoader: Error running function in module '{module_name}': {e}")
            return None

# --- AI Module: ARWiki Downloader ---

class ARWikiDownloader:
    """
    A module to download and decompress the ARWiki pages XML.BZ2 file.
    """
    def __init__(self, core_memory: CoreMemory):
        self.core_memory = core_memory
        self.download_url = "https://dumps.wikimedia.org/arwiki/latest/arwiki-latest-pages-articles.xml.bz2"
        self.core_memory.add_capability("arwiki_downloader", "Downloads and decompresses ARWiki XML data.")

    def download_file(self, url: str, destination_path: Path):
        """Downloads a file from a URL to a specified path."""
        print(f"ARWikiDownloader: Downloading from {url} to {destination_path}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an exception for bad status codes
            with open(destination_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"ARWikiDownloader: Successfully downloaded to {destination_path}.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"ARWikiDownloader: Error downloading file: {e}")
            return False

    def decompress_bz2(self, input_path: Path, output_path: Path):
        """Decompresses a .bz2 file."""
        print(f"ARWikiDownloader: Decompressing {input_path} to {output_path}...")
        try:
            with bz2.BZ2File(input_path, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f"ARWikiDownloader: Successfully decompressed to {output_path}.")
            return True
        except (bz2.BZ2Error, IOError) as e:
            print(f"ARWikiDownloader: Error during decompression: {e}")
            return False

    def run(self, download_dir: str = ".", output_filename: str = "arwiki-latest-pages-articles.xml"):
        """
        Main function to download and decompress the ARWiki XML.

        Args:
            download_dir: The directory to save the downloaded and decompressed files.
            output_filename: The desired name for the decompressed XML file.

        Returns:
            Path to the decompressed XML file if successful, None otherwise.
        """
        download_dir_path = Path(download_dir)
        download_dir_path.mkdir(parents=True, exist_ok=True)

        compressed_file_path = download_dir_path / Path(self.download_url).name
        decompressed_file_path = download_dir_path / output_filename

        if decompressed_file_path.exists():
            print(f"ARWikiDownloader: Decompressed file already exists at {decompressed_file_path}. Skipping download and decompression.")
            return decompressed_file_path

        if not self.download_file(self.download_url, compressed_file_path):
            return None

        if not self.decompress_bz2(compressed_file_path, decompressed_file_path):
            # Clean up the partially downloaded compressed file if decompression failed
            if compressed_file_path.exists():
                compressed_file_path.unlink()
            return None

        # Optionally remove the compressed file after successful decompression
        try:
            compressed_file_path.unlink()
            print(f"ARWikiDownloader: Removed compressed file: {compressed_file_path}")
        except OSError as e:
            print(f"ARWikiDownloader: Error removing compressed file {compressed_file_path}: {e}")

        return decompressed_file_path

# --- Example Usage and Testing ---

class TestAIArchitecture(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.module_dir = self.temp_dir / "ai_modules"
        self.module_dir.mkdir()

        self.core_memory = CoreMemory()
        self.module_loader = ModuleLoader(module_directory=self.module_dir)

        # Create a dummy module for testing
        self.sample_module_content = """
import sys

def run(data, name="World"):
    '''A sample module function.'''
    print(f"SampleModule: Received data='{data}', name='{name}'")
    processed_data = data.upper()
    return f"Processed: {processed_data} by {name}"

def another_function():
    return "This is another function."
"""
        (self.module_dir / "sample_module.py").write_text(self.sample_module_content)

        # Create a module with a function named after the module itself
        self.named_module_content = """
def greeting_task(name="Guest"):
    return f"Hello, {name}!"
"""
        (self.module_dir / "greeting_task.py").write_text(self.named_module_content)

    def tearDown(self):
        """Clean up test environment."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_core_memory(self):
        """Tests CoreMemory functionality."""
        print("\n--- Testing Core Memory ---")
        self.assertEqual(self.core_memory.get_capabilities(), [])
        self.core_memory.add_capability("test_cap", "A test capability")
        self.assertEqual(len(self.core_memory.get_capabilities()), 1)
        self.assertEqual(self.core_memory.get_capabilities()[0]["name"], "test_cap")
        print("--- Core Memory Test Complete ---")

    def test_module_loader_load_unload(self):
        """Tests module loading and unloading."""
        print("\n--- Testing Module Loader: Load/Unload ---")
        self.assertEqual(self.module_loader.get_available_module_names(), [])

        # Load a module
        loaded = self.module_loader.load_module("sample_module")
        self.assertTrue(loaded)
        self.assertIn("sample_module", self.module_loader.get_available_module_names())
        self.assertEqual(len(self.module_loader.loaded_modules), 1)

        # Try loading again
        loaded_again = self.module_loader.load_module("sample_module")
        self.assertTrue(loaded_again)
        self.assertEqual(len(self.module_loader.loaded_modules), 1) # Should not increase

        # Load another module
        loaded_greeting = self.module_loader.load_module("greeting_task")
        self.assertTrue(loaded_greeting)
        self.assertIn("greeting_task", self.module_loader.get_available_module_names())
        self.assertEqual(len(self.module_loader.loaded_modules), 2)

        # Unload a module
        unloaded = self.module_loader.unload_module("sample_module")
        self.assertTrue(unloaded)
        self.assertNotIn("sample_module", self.module_loader.get_available_module_names())
        self.assertEqual(len(self.module_loader.loaded_modules), 1)

        # Try unloading a non-existent module
        unloaded_nonexistent = self.module_loader.unload_module("non_existent_module")
        self.assertFalse(unloaded_nonexistent)
        self.assertEqual(len(self.module_loader.loaded_modules), 1)

        # Unload remaining module
        self.assertTrue(self.module_loader.unload_module("greeting_task"))
        self.assertEqual(len(self.module_loader.loaded_modules), 0)
        print("--- Module Loader: Load/Unload Test Complete ---")

    def test_module_loader_run(self):
        """Tests running functions within modules."""
        print("\n--- Testing Module Loader: Run ---")
        # Load sample_module
        self.assertTrue(self.module_loader.load_module("sample_module"))

        # Run the 'run' function with arguments
        result_run = self.module_loader.run_module("sample_module", "test data", name="Phoenix")
        self.assertEqual(result_run, "Processed: TEST DATA by Phoenix")

        # Run with default argument
        result_default = self.module_loader.run_module("sample_module", "another test")
        self.assertEqual(result_default, "Processed: ANOTHER TEST by World")

        # Load greeting_task and run its function named after the module
        self.assertTrue(self.module_loader.load_module("greeting_task"))
        result_greeting_named = self.module_loader.run_module("greeting_task", name="Alice")
        self.assertEqual(result_greeting_named, "Hello, Alice!")

        # Try running a non-existent module
        result_nonexistent = self.module_loader.run_module("non_existent_module", "some data")
        self.assertIsNone(result_nonexistent)

        # Test running a module that has no 'run' or name-matching function
        # Create a dummy module for this test
        (self.module_dir / "no_run_module.py").write_text("def only_this(): pass")
        self.assertTrue(self.module_loader.load_module("no_run_module"))
        result_no_run = self.module_loader.run_module("no_run_module", "data")
        self.assertIsNone(result_no_run)
        print("--- Module Loader: Run Test Complete ---")

    def test_arwiki_downloader_module(self):
        """Tests the ARWikiDownloader module."""
        print("\n--- Testing ARWiki Downloader Module ---")

        # Mock requests.get to avoid actual download during unit tests
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b"bz2 compressed data dummy"]
        mock_response.raise_for_status.return_value = None

        mock_bz2_file = MagicMock()
        mock_bz2_file.read.return_value = b"decompressed xml data dummy"
        mock_bz2_file.open.return_value.__enter__.return_value = mock_bz2_file # Mock BZ2File context manager

        mock_open_out = MagicMock()
        mock_open_out.return_value.__enter__.return_value.write = MagicMock() # Mock file write

        with patch('requests.get', return_value=mock_response) as mock_get, \
             patch('bz2.BZ2File', return_value=mock_bz2_file) as mock_bz2_file_constructor, \
             patch('builtins.open', side_effect=lambda filename, mode: \
                   mock_open_out() if filename.endswith('.xml') else unittest.mock.mock_open(read_data=b'')(filename, mode) \
             ) as mock_open:

            # Ensure the mock for the compressed file doesn't interfere with the output file open
            def side_effect_open(filename, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
                if filename.endswith('.xml.bz2'):
                    return unittest.mock.mock_open(read_data=b'')()
                elif filename.endswith('.xml'):
                    return mock_open_out()
                else:
                    return unittest.mock.mock_open()(filename, mode, buffering, encoding, errors, newline, closefd, opener)
            mock_open.side_effect = side_effect_open

            downloader = ARWikiDownloader(self.core_memory)
            download_test_dir = self.temp_dir / "downloads"
            download_test_dir.mkdir()

            result_path = downloader.run(download_dir=str(download_test_dir))

            self.assertIsNotNone(result_path)
            self.assertTrue(result_path.exists())
            self.assertEqual(result_path.name, "arwiki-latest-pages-articles.xml")

            # Verify that download and decompression were attempted
            mock_get.assert_called_once_with(downloader.download_url, stream=True)
            mock_bz2_file_constructor.assert_called_once_with(ANY, 'rb') # ANY because the path is constructed internally
            mock_open_out.return_value.__enter__.return_value.write.assert_called_once_with(b"decompressed xml data dummy")

            # Clean up dummy downloaded file if it was created before mock logic
            compressed_file_check = download_test_dir / Path(downloader.download_url).name
            if compressed_file_check.exists():
                compressed_file_check.unlink()

        print("--- ARWiki Downloader Module Test Complete ---")

    def test_download_and_decompress_actual_data(self):
        """
        Tests the ARWikiDownloader module with actual file operations.
        This test will download and decompress a file, so it can be slow.
        It's recommended to run this test selectively or ensure you have
        sufficient disk space and network bandwidth.
        """
        print("\n--- Testing ARWiki Downloader Module (Actual Download) ---")
        print("WARNING: This test will download ~1GB and decompress it (~5GB).")
        print("         It may take a significant amount of time and disk space.")
        print("         If you want to skip this, you can comment out this test method.")

        # Define a temporary directory for the download
        actual_download_dir = self.temp_dir / "actual_downloads"
        actual_download_dir.mkdir()

        # Check if disk space is sufficient (heuristic)
        # This is a rough check and might not be perfect.
        # Target file size after decompression is around 5GB.
        # We check if there's at least 10GB available for safety.
        try:
            free_space = shutil.disk_usage(str(self.temp_dir)).free
            if free_space < 10 * 1024**3: # Less than 10 GB free
                print(f"Skipping actual download test due to insufficient free disk space ({free_space / (1024**3):.2f} GB free).")
                self.skipTest("Insufficient disk space for actual download test.")
        except Exception as e:
            print(f"Could not check disk space: {e}. Proceeding with caution.")


        downloader = ARWikiDownloader(self.core_memory)

        # Use a known small file for initial testing if available,
        # otherwise proceed with the large one.
        # For this example, we will proceed with the large file but
        # add a conditional check for safety.

        confirm = input("Do you want to proceed with the actual download and decompression? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Actual download test aborted by user.")
            self.skipTest("Actual download test aborted by user.")
            return

        # This will actually download the file
        decompressed_file_path = downloader.run(download_dir=str(actual_download_dir))

        self.assertIsNotNone(decompressed_file_path, "Actual download and decompression failed.")
        self.assertTrue(decompressed_file_path.exists(), f"Decompressed file not found at {decompressed_file_path}")
        self.assertTrue(decompressed_file_path.stat().st_size > 0, "Decompressed file is empty.")
        print(f"Successfully downloaded and decompressed ARWiki data to: {decompressed_file_path}")
        print(f"Decompressed file size: {decompressed_file_path.stat().st_size / (1024**3):.2f} GB")

        # Clean up the downloaded files
        print("Cleaning up downloaded files...")
        if actual_download_dir.exists():
            shutil.rmtree(actual_download_dir)
            print(f"Removed directory: {actual_download_dir}")

        print("--- ARWiki Downloader Module (Actual Download) Test Complete ---")

# --- Main Execution Block ---
if __name__ == "__main__":
    # Example of using the AI Architecture components
    print("--- AI Architecture Demonstration ---")

    # 1. Initialize Core Memory
    core_memory = CoreMemory()
    print("Core Memory initialized.")

    # 2. Initialize Module Loader
    # We'll create a temporary directory for modules to keep things clean
    module_storage_path = Path("./temp_ai_modules")
    if module_storage_path.exists():
        shutil.rmtree(module_storage_path)
    module_storage_path.mkdir()
    module_loader = ModuleLoader(module_directory=module_storage_path)
    print(f"Module Loader initialized with directory: {module_storage_path.resolve()}")

    # 3. Create and load the ARWiki Downloader module
    # For demonstration, we'll instantiate the class directly.
    # In a real scenario, you might save this class to a file in module_storage_path
    # and then load it via module_loader.load_module("arwiki_downloader").
    # For simplicity here, we'll just instantiate and use it.

    # Create a dummy module file for ARWikiDownloader to be discoverable by loader
    # In a real system, this class would be in its own file, e.g., arwiki_downloader.py
    arwiki_downloader_module_content = """
import bz2
import os
import shutil
import requests
from pathlib import Path

class ARWikiDownloader:
    def __init__(self, core_memory):
        self.core_memory = core_memory
        self.download_url = "https://dumps.wikimedia.org/arwiki/latest/arwiki-latest-pages-articles.xml.bz2"
        self.core_memory.add_capability("arwiki_downloader", "Downloads and decompresses ARWiki XML data.")

    def download_file(self, url: str, destination_path: Path):
        print(f"ARWikiDownloader: Downloading from {url} to {destination_path}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(destination_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"ARWikiDownloader: Successfully downloaded to {destination_path}.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"ARWikiDownloader: Error downloading file: {e}")
            return False

    def decompress_bz2(self, input_path: Path, output_path: Path):
        print(f"ARWikiDownloader: Decompressing {input_path} to {output_path}...")
        try:
            with bz2.BZ2File(input_path, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f"ARWikiDownloader: Successfully decompressed to {output_path}.")
            return True
        except (bz2.BZ2Error, IOError) as e:
            print(f"ARWikiDownloader: Error during decompression: {e}")
            return False

    def run(self, download_dir: str = ".", output_filename: str = "arwiki-latest-pages-articles.xml"):
        download_dir_path = Path(download_dir)
        download_dir_path.mkdir(parents=True, exist_ok=True)

        compressed_file_path = download_dir_path / Path(self.download_url).name
        decompressed_file_path = download_dir_path / output_filename

        if decompressed_file_path.exists():
            print(f"ARWikiDownloader: Decompressed file already exists at {decompressed_file_path}. Skipping download and decompression.")
            return decompressed_file_path

        if not self.download_file(self.download_url, compressed_file_path):
            return None

        if not self.decompress_bz2(compressed_file_path, decompressed_file_path):
            if compressed_file_path.exists():
                compressed_file_path.unlink()
            return None

        try:
            compressed_file_path.unlink()
            print(f"ARWikiDownloader: Removed compressed file: {compressed_file_path}")
        except OSError as e:
            print(f"ARWikiDownloader: Error removing compressed file {compressed_file_path}: {e}")

        return decompressed_file_path
"""
    (module_storage_path / "arwiki_downloader.py").write_text(arwiki_downloader_module_content)
    print("Created dummy 'arwiki_downloader.py' module file.")


    # Load the ARWikiDownloader module
    if module_loader.load_module("arwiki_downloader"):
        print("ARWiki Downloader module loaded successfully.")

        # Instantiate the ARWikiDownloader class from the loaded module
        # The loaded module is accessible via sys.modules or from module_loader.loaded_modules
        arwiki_downloader_instance = module_loader.loaded_modules["arwiki_downloader"].ARWikiDownloader(core_memory)

        # 4. Run the ARWiki Downloader task
        print("\n--- Running ARWiki Downloader Task ---")
        # You can specify a directory to save the files.
        # For demonstration, we'll create a subdirectory within the temporary module storage.
        download_destination = module_storage_path / "arwiki_data"
        print(f"Files will be saved to: {download_destination.resolve()}")

        # To avoid actually downloading ~1GB during a quick demo run,
        # we will mock the download and decompression parts for the main execution block.
        # If you want to run the actual download, uncomment the lines below and comment out the mock.

        # try:
        #     # Uncomment the following lines to perform the actual download
        #     print("\n--- Performing ACTUAL ARWiki Download and Decompression ---")
        #     print("This will take time and requires internet connection and disk space.")
        #     result_file_path = arwiki_downloader_instance.run(download_dir=str(download_destination))
        #     if result_file_path:
        #         print(f"\nARWiki download and decompression successful! Data saved to: {result_file_path}")
        #         print(f"File size: {result_file_path.stat().st_size / (1024**2):.2f} MB")
        #     else:
        #         print("\nARWiki download and decompression failed.")
        # except Exception as e:
        #     print(f"\nAn error occurred during the actual download/decompression: {e}")

        print("\n--- Mocking ARWiki Downloader Task for Demonstration ---")
        # Mocking for a quick demo run:
        mock_download_dir = module_storage_path / "mock_arwiki_data"
        mock_download_dir.mkdir(exist_ok=True)
        mock_compressed_file = mock_download_dir / "arwiki-latest-pages-articles.xml.bz2"
        mock_decompressed_file = mock_download_dir / "arwiki-latest-pages-articles.xml"

        # Create dummy files
        mock_compressed_file.write_bytes(b"dummy bz2 content")
        mock_decompressed_file.write_bytes(b"<mediawiki><page><title>Test Page</title><revision><text>This is a test page.</text></revision></page></mediawiki>")
        print(f"Created mock compressed file: {mock_compressed_file}")
        print(f"Created mock decompressed file: {mock_decompressed_file}")

        # To make arwiki_downloader_instance.run use the mock files,
        # we can either mock its internal methods or simply check if the files exist.
        # For this demo, we'll simulate a successful run by ensuring the output file exists.
        print("Simulating successful run of ARWiki Downloader...")
        # We bypass the actual download/decompress calls for this demo execution.
        # In a real scenario, you would let arwiki_downloader_instance.run execute.
        # Here, we just confirm the expected output state.
        if mock_decompressed_file.exists():
            print(f"Mock ARWiki data is available at: {mock_decompressed_file}")
            print("ARWiki Downloader task simulated successfully.")
        else:
            print("Mock ARWiki data was not found. Simulation failed.")

        # Optionally, remove the mock files and directory after demonstration
        # print("\nCleaning up mock ARWiki data...")
        # if mock_download_dir.exists():
        #     shutil.rmtree(mock_download_dir)
        #     print("Mock data directory removed.")


        # 5. Check Core Memory Capabilities
        print("\n--- Checking Core Memory Capabilities ---")
        capabilities = core_memory.get_capabilities()
        print("Current capabilities:", capabilities)
        self.assertIn({"name": "arwiki_downloader", "description": "Downloads and decompresses ARWiki XML data."}, capabilities)

        # 6. Unload the ARWiki Downloader module
        print("\n--- Unloading ARWiki Downloader Module ---")
        module_loader.unload_module("arwiki_downloader")
        print("Loaded modules after unload:", module_loader.get_available_module_names())

    else:
        print("Failed to load ARWiki Downloader module.")

    print("\n--- Running Unit Tests ---")
    # Run the unit tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

    # Clean up the temporary module directory
    print("\n--- Cleaning up temporary module directory ---")
    if module_storage_path.exists():
        shutil.rmtree(module_storage_path)
        print(f"Removed temporary directory: {module_storage_path}")

    print("\n--- AI Architecture Demonstration Complete ---")