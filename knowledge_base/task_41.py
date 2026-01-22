import bz2
import requests
import os
import shutil
import sys
import importlib

class ModuleLoader:
    def __init__(self, task_dir="tasks"):
        self.task_dir = task_dir
        self.loaded_modules = {}
        self.module_paths = {}
        self._ensure_task_dir()

    def _ensure_task_dir(self):
        if not os.path.exists(self.task_dir):
            os.makedirs(self.task_dir)
            # Create an __init__.py to make it a package
            with open(os.path.join(self.task_dir, "__init__.py"), "w") as f:
                f.write("# Module directory")

    def add_module_path(self, module_name, file_path):
        """Adds a module to the loader, specifying its file path."""
        if not os.path.exists(file_path):
            print(f"Error: Module file not found at {file_path}", file=sys.stderr)
            return

        module_dir = os.path.dirname(file_path)
        module_filename = os.path.basename(file_path)
        module_short_name = os.path.splitext(module_filename)[0]

        # Add the directory to sys.path if it's not already there
        if module_dir not in sys.path:
            sys.path.insert(0, module_dir)

        # Store the module name and its original path for potential unloading
        self.module_paths[module_short_name] = {
            "file_path": file_path,
            "original_path": module_dir
        }
        print(f"Module path '{module_short_name}' added: {file_path}")

    def load_module(self, module_name):
        """Loads a module by name if it exists in the specified paths."""
        if module_name in self.loaded_modules:
            print(f"Module '{module_name}' is already loaded.")
            return True

        if module_name not in self.module_paths:
            print(f"Error: Module '{module_name}' has not been added to the loader.", file=sys.stderr)
            return False

        module_info = self.module_paths[module_name]
        module_file_path = module_info["file_path"]
        module_dir = module_info["original_path"]
        
        # Ensure the module's directory is in sys.path
        if module_dir not in sys.path:
            sys.path.insert(0, module_dir)

        try:
            # Import the module
            module = importlib.import_module(module_name)
            self.loaded_modules[module_name] = module
            print(f"Module '{module_name}' loaded successfully.")
            return True
        except ImportError as e:
            print(f"Error importing module '{module_name}': {e}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"An unexpected error occurred while loading module '{module_name}': {e}", file=sys.stderr)
            return False

    def run_module(self, module_name, *args, **kwargs):
        """Runs a task function within a loaded module."""
        if module_name not in self.loaded_modules:
            print(f"Module '{module_name}' not loaded. Attempting to load on demand...")
            if not self.load_module(module_name):
                print(f"Failed to load module '{module_name}' for execution.", file=sys.stderr)
                return None

        module = self.loaded_modules[module_name]

        # Assuming the task function is named 'task' or 'run'
        task_function = None
        if hasattr(module, 'task'):
            task_function = module.task
        elif hasattr(module, 'run'):
            task_function = module.run

        if not task_function:
            print(f"Error: No task function ('task' or 'run') found in module '{module_name}'.", file=sys.stderr)
            return None

        try:
            return task_function(*args, **kwargs)
        except Exception as e:
            print(f"Error executing task in module '{module_name}': {e}", file=sys.stderr)
            return None

    def unload_module(self, module_name):
        """Unloads a module from memory."""
        if module_name in self.loaded_modules:
            del self.loaded_modules[module_name]
            # In a more complex scenario, you might want to remove from sys.path
            # or handle unregistering any hooks the module might have added.
            # For this simple loader, just removing from loaded_modules is sufficient.
            print(f"Module '{module_name}' unloaded.")
            return True
        else:
            print(f"Module '{module_name}' is not currently loaded.")
            return False

    def get_available_module_names(self):
        """Returns a list of module names that have been added to the loader."""
        return list(self.module_paths.keys())

    def get_loaded_module_names(self):
        """Returns a list of module names that are currently loaded in memory."""
        return list(self.loaded_modules.keys())

    def download_and_decompress_bz2(self, url, output_filename):
        """
        Downloads a .bz2 file from a URL and decompresses it.

        Args:
            url (str): The URL of the .bz2 file.
            output_filename (str): The desired name for the decompressed file.

        Returns:
            str: The path to the decompressed file if successful, None otherwise.
        """
        print(f"Downloading from {url}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an exception for bad status codes

            compressed_filepath = f"{output_filename}.bz2"
            decompressed_filepath = output_filename

            with open(compressed_filepath, 'wb') as f_compressed:
                for chunk in response.iter_content(chunk_size=8192):
                    f_compressed.write(chunk)
            print(f"Downloaded to {compressed_filepath}")

            print(f"Decompressing {compressed_filepath} to {decompressed_filepath}...")
            with bz2.BZ2File(compressed_filepath, 'rb') as f_in, open(decompressed_filepath, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            print(f"Decompressed successfully to {decompressed_filepath}")

            # Clean up the compressed file
            os.remove(compressed_filepath)
            print(f"Removed temporary compressed file: {compressed_filepath}")

            return decompressed_filepath

        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}", file=sys.stderr)
            return None
        except bz2.BZ2Error as e:
            print(f"Error during decompression: {e}", file=sys.stderr)
            return None
        except IOError as e:
            print(f"File I/O error: {e}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            return None

# Example Usage:
if __name__ == "__main__":
    # Create a dummy task module for demonstration
    TASK_DIR = "my_tasks"
    os.makedirs(TASK_DIR, exist_ok=True)

    # Create a sample_task.py
    sample_task_code = """
def task(name="World"):
    return f"Hello, {name}!"

def another_task():
    return "This is another task."
"""
    with open(os.path.join(TASK_DIR, "sample_task.py"), "w") as f:
        f.write(sample_task_code)

    # Create a greeting_task.py
    greeting_task_code = """
def greeting_task(name="Guest"):
    return f"Greetings, {name}!"
"""
    with open(os.path.join(TASK_DIR, "greeting_task.py"), "w") as f:
        f.write(greeting_task_code)

    loader = ModuleLoader(task_dir=TASK_DIR)

    # Add module paths
    loader.add_module_path("sample_task", os.path.join(TASK_DIR, "sample_task.py"))
    loader.add_module_path("greeting_task", os.path.join(TASK_DIR, "greeting_task.py"))

    print("--- Initial State ---")
    print("Available modules:", loader.get_available_module_names())
    print("Loaded modules:", loader.get_loaded_module_names())

    print("\n--- Running 'greeting_task' with custom name ---")
    result = loader.run_module("greeting_task", name="Phoenix AI")
    print("Result:", result)
    assert result == "Greetings, Phoenix AI!"

    print("\n--- Running 'greeting_task' with default name ---")
    result = loader.run_module("greeting_task")
    print("Result:", result)
    assert result == "Greetings, Guest!"

    print("\n--- Running 'sample_task' ---")
    result = loader.run_module("sample_task", name="Module Architect")
    print("Result:", result)
    assert result == "Hello, Module Architect!"

    print("\n--- Running non-existent task ---")
    result = loader.run_module("non_existent_task", "some data")
    print("Result:", result)
    assert result is None

    print("\n--- Current State ---")
    print("Available modules:", loader.get_available_module_names())
    print("Loaded modules:", loader.get_loaded_module_names())
    assert "sample_task" in loader.get_loaded_module_names()
    assert "greeting_task" in loader.get_loaded_module_names()

    print("\n--- Unloading 'sample_task' ---")
    unloaded = loader.unload_module("sample_task")
    print(f"Unloaded 'sample_task': {unloaded}")
    assert unloaded is True
    assert "sample_task" not in loader.get_loaded_module_names()
    print("Loaded modules after unload:", loader.get_loaded_module_names())

    print("\n--- Trying to run unloaded 'sample_task' (should load on demand) ---")
    result = loader.run_module("sample_task", "This should be reloaded")
    print("Result:", result)
    assert result == "Hello, This should be reloaded!"
    assert "sample_task" in loader.get_loaded_module_names()

    print("\n--- Trying to unload a non-existent module ---")
    unloaded_nonexistent = loader.unload_module("another_non_existent_module")
    print(f"Unloaded 'another_non_existent_module': {unloaded_nonexistent}")
    assert unloaded_nonexistent is False

    # Example for downloading and decompressing
    print("\n--- Downloading and Decompressing ARWiki Data ---")
    arwiki_url = "https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2" # Using a smaller example if available or a placeholder
    # For a real large file, consider using a smaller test file or a known reliable source
    # For demonstration, let's use a placeholder or instruct user to provide one
    # A very small bz2 file for testing decompression:
    # You can create a dummy text file, compress it with bz2, and host it or use it locally.
    # Example: echo "This is a test file." > test.txt && bzip2 test.txt

    # For demonstration purposes, we'll skip the actual download of the large ARWiki file
    # as it's very big. Instead, we'll simulate the process or use a much smaller file.

    # --- Method 1: Simulate with a placeholder URL (won't actually download) ---
    print("Skipping actual download of large ARWiki file for this example.")
    print("If you want to test, replace 'placeholder_url' with a valid .bz2 file URL.")
    # test_output_file = "arwiki-latest-pages-articles.xml"
    # decompressed_path = loader.download_and_decompress_bz2(
    #     "http://example.com/path/to/your/small_test_file.xml.bz2",
    #     test_output_file
    # )
    # if decompressed_path:
    #     print(f"Decompressed file available at: {decompressed_path}")
    #     # Example: You could then process this XML file

    # --- Method 2: Using a locally created small bz2 file (if available) ---
    local_bz2_file = "test_small.xml.bz2"
    local_decompressed_file = "test_small.xml"
    if os.path.exists(local_bz2_file):
        print(f"\nTesting decompression of local file: {local_bz2_file}")
        try:
            with bz2.BZ2File(local_bz2_file, 'rb') as f_in, open(local_decompressed_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            print(f"Decompressed local file successfully to {local_decompressed_file}")
            if os.path.exists(local_decompressed_file):
                print(f"Content of {local_decompressed_file}:\n", open(local_decompressed_file, 'r').read())
            # Clean up local decompressed file
            if os.path.exists(local_decompressed_file):
                os.remove(local_decompressed_file)
        except Exception as e:
            print(f"Error during local decompression test: {e}", file=sys.stderr)
    else:
        print(f"\nLocal test file '{local_bz2_file}' not found. Skipping local decompression test.")
        print("To run this test, create a small .bz2 file named 'test_small.xml.bz2'.")


    # Clean up dummy files and directory
    print("\nCleaning up dummy files and directory...")
    if os.path.exists(TASK_DIR):
        shutil.rmtree(TASK_DIR)
        print(f"Removed directory: {TASK_DIR}")

    print("\n--- Testing Complete ---")