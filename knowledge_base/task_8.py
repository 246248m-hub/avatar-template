import importlib
import os
import sys
from typing import Any, Dict, List

# Assuming CoreMemory is defined elsewhere and has a 'data' attribute (a dictionary)
# and a 'save' method. For this example, we'll create a placeholder.

class CoreMemory:
    def __init__(self, initial_data: Dict = None):
        self.data = initial_data if initial_data is not None else {}

    def save(self):
        print("CoreMemory: Data saved.")
        # In a real scenario, this would persist self.data to disk or a database

class ModuleLoader:
    """
    Manages the loading, unloading, and execution of AI modules.
    Modules are Python files located within a designated task directory.
    """
    def __init__(self, core_memory: CoreMemory, task_directory: str = "phoenix_tasks"):
        """
        Initializes the ModuleLoader.

        Args:
            core_memory: An instance of CoreMemory to store and retrieve state.
            task_directory: The directory where AI modules are stored.
        """
        self.core_memory = core_memory
        self.task_directory = os.path.abspath(task_directory)
        self.loaded_modules: Dict[str, Any] = {}  # Stores loaded module objects
        self._ensure_task_directory_exists()
        self._load_initial_modules()

    def _ensure_task_directory_exists(self):
        """Ensures the task directory exists, creating it if necessary."""
        if not os.path.exists(self.task_directory):
            os.makedirs(self.task_directory)
            print(f"Created task directory: {self.task_directory}")

    def _module_path_to_name(self, filepath: str) -> str:
        """Converts a module file path to its importable name."""
        # Assumes module files are directly under task_directory and have a .py extension
        base_name = os.path.basename(filepath)
        return os.path.splitext(base_name)[0]

    def _load_initial_modules(self):
        """Loads all Python modules found in the task directory at initialization."""
        print(f"Scanning for modules in: {self.task_directory}")
        for filename in os.listdir(self.task_directory):
            if filename.endswith(".py"):
                filepath = os.path.join(self.task_directory, filename)
                self._load_module_from_file(filepath)

    def get_available_module_names(self) -> List[str]:
        """Returns a list of names of all currently loaded modules."""
        return list(self.loaded_modules.keys())

    def add_new_module(self, module_name: str, module_content: str):
        """
        Creates a new Python module file, loads it, and updates core memory.

        Args:
            module_name: The desired name for the new module (without .py extension).
            module_content: The Python code content for the new module.
        """
        module_filename = f"{module_name}.py"
        module_filepath = os.path.join(self.task_directory, module_filename)

        # Check if module already exists
        if module_name in self.loaded_modules:
            print(f"Warning: Module '{module_name}' is already loaded. Overwriting...")
            # Optionally, add logic here to unload the existing module first
            # if self.unload_module(module_name):
            #     print(f"Unloaded existing module '{module_name}'.")
            # else:
            #     print(f"Failed to unload existing module '{module_name}'. Aborting add.")
            #     return

        h = os.path.join(self.task_directory, module_filename)

        try:
            with open(module_filepath, "w") as f:
                f.write(module_content)
            print(f"Created module file: {module_filepath}")

            # Load the newly added module
            if self._load_module_from_file(module_filepath):
                # Update capabilities in memory if this is a new capability
                if "module_loader_v1" not in self.core_memory.data.get("capabilities", []):
                    self.core_memory.data.setdefault("capabilities", []).append("module_loader_v1")
                    self.core_memory.save()
                    print("Added capability: module_loader_v1")
            else:
                print(f"Failed to load newly added module '{module_name}'.")


        except IOError as e:
            print(f"Error writing module file {module_filepath}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while adding module {module_name}: {e}")

    def _load_module_from_file(self, filepath: str) -> bool:
        """Loads a Python module from its file path."""
        module_name = self._module_path_to_name(filepath)
        
        # Add the task directory to sys.path to allow importing
        # Use insert(0, ...) to ensure it's prioritized
        if self.task_directory not in sys.path:
            sys.path.insert(0, self.task_directory)
            added_to_path = True
        else:
            added_to_path = False # It was already there, no need to remove later if it wasn't the first element

        try:
            # Import the module. If it's already loaded, importlib will return the existing module.
            # We might want to force reload if the file has changed, but for simplicity,
            # we'll assume importlib handles this or we manage reloads explicitly if needed.
            if module_name in self.loaded_modules:
                # If the module is already loaded, we might want to reload it if the file has changed.
                # For simplicity, we'll just acknowledge it's loaded. A more robust solution
                # would involve checking file modification times.
                print(f"Module '{module_name}' was already loaded. Re-using existing instance.")
                # Or, to force a reload:
                # importlib.reload(self.loaded_modules[module_name])
            else:
                module = importlib.import_module(module_name)
                self.loaded_modules[module_name] = module
                print(f"Successfully loaded module: {module_name}")
            return True
        except ImportError as e:
            print(f"Error importing module '{module_name}' from {filepath}: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred during import of {module_name}: {e}")
            return False
        finally:
            # Clean up sys.path if we added it and it was the first element
            if added_to_path and sys.path[0] == self.task_directory:
                sys.path.pop(0)
                # print(f"Cleaned sys.path: removed {self.task_directory}")


    def run_module(self, module_name: str, *args, **kwargs) -> Any:
        """
        Executes the 'run' function of a specified loaded module.

        Args:
            module_name: The name of the module to run.
            *args: Positional arguments to pass to the module's 'run' function.
            **kwargs: Keyword arguments to pass to the module's 'run' function.

        Returns:
            The result of the module's 'run' function, or None if an error occurs.
        """
        if module_name not in self.loaded_modules:
            print(f"Error: Module '{module_name}' is not loaded.")
            return None

        module = self.loaded_modules[module_name]

        if not hasattr(module, 'run') or not callable(getattr(module, 'run')):
            print(f"Error: Module '{module_name}' does not have a callable 'run' function.")
            return None

        try:
            print(f"Running module: {module_name} with args={args}, kwargs={kwargs}")
            result = module.run(*args, **kwargs)
            return result
        except Exception as e:
            print(f"Error executing 'run' function in module '{module_name}': {e}")
            return None

    def unload_module(self, module_name: str) -> bool:
        """
        Unloads a specified module from memory.

        Args:
            module_name: The name of the module to unload.

        Returns:
            True if the module was successfully unloaded, False otherwise.
        """
        if module_name not in self.loaded_modules:
            print(f"Error: Module '{module_name}' is not loaded, cannot unload.")
            return False

        try:
            # Remove from loaded_modules dictionary
            del self.loaded_modules[module_name]

            # Remove from sys.modules to allow for complete garbage collection and reloading
            if module_name in sys.modules:
                del sys.modules[module_name]
                print(f"Successfully unloaded module: {module_name} (removed from sys.modules)")
            else:
                print(f"Successfully unloaded module: {module_name} (was not found in sys.modules)")
            return True
        except KeyError:
            print(f"Error: Module '{module_name}' not found in loaded_modules during unload.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred while unloading module '{module_name}': {e}")
            return False

# --- Example Usage and Testing ---
if __name__ == "__main__":
    # Mock CoreMemory for testing
    class MockCoreMemory:
        def __init__(self):
            self.data = {"capabilities": []}
            print("MockCoreMemory initialized.")
        def save(self):
            print("MockCoreMemory: Data saved.")

    import shutil

    # Define a temporary task directory for testing
    TEST_TASK_DIR = "test_phoenix_tasks"
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
    os.makedirs(TEST_TASK_DIR)
    print(f"Created temporary task directory: {TEST_TASK_DIR}")

    # --- Test Case 1: Initialization and Loading Existing Modules ---
    print("\n--- Test Case 1: Initialization ---")
    # Create a dummy module file
    sample_module_content = """
def run(data):
    print(f"Executing sample_module.run with: {data}")
    return f"Processed: {data.upper()}"

def helper_function():
    return "This is a helper."
"""
    with open(os.path.join(TEST_TASK_DIR, "sample_module.py"), "w") as f:
        f.write(sample_module_content)
    print("Created dummy 'sample_module.py'")

    mock_mem = MockCoreMemory()
    module_loader = ModuleLoader(mock_mem, task_directory=TEST_TASK_DIR)

    print("\nInitial loaded modules:", module_loader.get_available_module_names())
    assert "sample_module" in module_loader.get_available_module_names()
    assert len(module_loader.loaded_modules) == 1

    # --- Test Case 2: Running an Existing Module ---
    print("\n--- Test Case 2: Running Existing Module ---")
    result = module_loader.run_module("sample_module", "hello world")
    print("Result:", result)
    assert result == "Processed: HELLO WORLD"

    # --- Test Case 3: Adding a New Module ---
    print("\n--- Test Case 3: Adding New Module ---")
    new_module_content = """
def run(name="Guest"):
    message = f"Hello, {name}!"
    print(f"Executing greeting_module.run for {name}")
    return message
"""
    module_loader.add_new_module("greeting_module", new_module_content)

    print("\nModules after adding 'greeting_module':", module_loader.get_available_module_names())
    assert "greeting_module" in module_loader.get_available_module_names()
    assert len(module_loader.loaded_modules) == 2

    # Run the newly added module
    result_greeting = module_loader.run_module("greeting_module", name="Architect AI")
    print("Result:", result_greeting)
    assert result_greeting == "Hello, Architect AI!"

    # Run with default name
    result_default_greeting = module_loader.run_module("greeting_module")
    print("Result:", result_default_greeting)
    assert result_default_greeting == "Hello, Guest!"

    # Check core memory capabilities
    print("Core Memory Capabilities:", mock_mem.data.get("capabilities"))
    assert "module_loader_v1" in mock_mem.data.get("capabilities", [])

    # --- Test Case 4: Handling Errors ---
    print("\n--- Test Case 4: Handling Errors ---")
    # Running a non-existent module
    result_nonexistent = module_loader.run_module("non_existent_module", "test")
    print("Result (non-existent):", result_nonexistent)
    assert result_nonexistent is None

    # Running a module without a 'run' function
    error_module_content = "def process(): return 'ok'"
    module_loader.add_new_module("no_run_module", error_module_content)
    result_no_run = module_loader.run_module("no_run_module", "test")
    print("Result (no run function):", result_no_run)
    assert result_no_run is None

    # --- Test Case 5: Unloading a Module ---
    print("\n--- Test Case 5: Unloading Module ---")
    unloaded = module_loader.unload_module("sample_module")
    print(f"Unloaded 'sample_module': {unloaded}")
    assert unloaded is True
    assert "sample_module" not in module_loader.get_available_module_names()
    assert len(module_loader.loaded_modules) == 1

    # Try running the unloaded module
    result_after_unload = module_loader.run_module("sample_module", "test")
    print("Result (after unload):", result_after_unload)
    assert result_after_unload is None

    # Try unloading a non-existent module
    unloaded_nonexistent = module_loader.unload_module("another_non_existent")
    print(f"Unloaded 'another_non_existent': {unloaded_nonexistent}")
    assert unloaded_nonexistent is False

    # --- Cleanup ---
    print("\nCleaning up test directory...")
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Removed test directory: {TEST_TASK_DIR}")

    print("\n--- All Test Cases Completed ---")
