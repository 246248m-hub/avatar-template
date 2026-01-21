# CORE_MODULE: persistent_memory.py
# DESCRIPTION: Manages the core's persistent state and data.

import json
import os
import threading

class CoreMemory:
    """
    Manages the persistent storage of the AI core's state,
    configuration, and learned information.
    """
    def __init__(self, storage_path="core_memory.json"):
        self.storage_path = storage_path
        self.data = {}
        self._lock = threading.Lock()
        self._load()
        print(f"CoreMemory initialized. Storage: {self.storage_path}")

    def _load(self):
        """Loads data from the persistent storage file."""
        with self._lock:
            if os.path.exists(self.storage_path):
                try:
                    with open(self.storage_path, 'r') as f:
                        self.data = json.load(f)
                    print("CoreMemory: Data loaded successfully.")
                except (json.JSONDecodeError, IOError) as e:
                    print(f"CoreMemory: Error loading data from {self.storage_path}: {e}. Starting with empty memory.")
                    self.data = {}
            else:
                print("CoreMemory: Storage file not found. Initializing with empty memory.")
                self.data = {}

    def save(self):
        """Saves the current state of the data to the persistent storage file."""
        with self._lock:
            try:
                with open(self.storage_path, 'w') as f:
                    json.dump(self.data, f, indent=4)
                # print("CoreMemory: Data saved successfully.") # Verbose, commented out for cleaner logs
            except IOError as e:
                print(f"CoreMemory: Error saving data to {self.storage_path}: {e}")

    def get(self, key, default=None):
        """Retrieves a value from memory."""
        with self._lock:
            return self.data.get(key, default)

    def set(self, key, value):
        """Sets a value in memory and triggers a save."""
        with self._lock:
            self.data[key] = value
        self.save()
        # print(f"CoreMemory: Set '{key}'.") # Verbose

    def update(self, key, updater_func, *args, **kwargs):
        """
        Retrieves a value, applies an update function to it, and saves the result.
        Useful for modifying mutable objects like lists or dictionaries.
        """
        with self._lock:
            current_value = self.data.get(key)
            updated_value = updater_func(current_value, *args, **kwargs)
            self.data[key] = updated_value
        self.save()
        # print(f"CoreMemory: Updated '{key}'.") # Verbose

    def append_to_list(self, key, item):
        """Appends an item to a list associated with a key."""
        def _append(current_list, new_item):
            if current_list is None:
                return [new_item]
            elif isinstance(current_list, list):
                current_list.append(new_item)
                return current_list
            else:
                print(f"CoreMemory Warning: Expected a list for key '{key}', but found {type(current_list)}. Cannot append.")
                return current_list # Return original value to avoid overwriting with wrong type

        self.update(key, _append, new_item=item)

    def remove_from_list(self, key, item_to_remove):
        """Removes the first occurrence of an item from a list associated with a key."""
        def _remove(current_list, item):
            if current_list is None:
                return None
            elif isinstance(current_list, list):
                try:
                    current_list.remove(item)
                    return current_list
                except ValueError:
                    print(f"CoreMemory Warning: Item '{item}' not found in list for key '{key}'.")
                    return current_list # Item not found, return original list
            else:
                print(f"CoreMemory Warning: Expected a list for key '{key}', but found {type(current_list)}. Cannot remove.")
                return current_list

        self.update(key, _remove, item=item_to_remove)

    def delete(self, key):
        """Deletes a key-value pair from memory."""
        with self._lock:
            if key in self.data:
                del self.data[key]
                self.save()
                # print(f"CoreMemory: Deleted '{key}'.") # Verbose
                return True
            else:
                # print(f"CoreMemory: Key '{key}' not found for deletion.") # Verbose
                return False

    def clear(self):
        """Clears all data from memory and saves an empty state."""
        with self._lock:
            self.data = {}
        self.save()
        print("CoreMemory: All data cleared.")

    def get_all_data(self):
        """Returns a copy of all stored data."""
        with self._lock:
            return self.data.copy()

# CORE_MODULE: dynamic_logic.py
# DESCRIPTION: Provides the engine for processing dynamic logic and executing tasks.

import importlib
import sys
import traceback

class ModuleLoader:
    """
    Manages loading, unloading, and executing modules within the AI core.
    Modules are expected to be Python files in a designated task directory.
    """
    def __init__(self, core_memory, task_directory="phoenix_tasks"):
        self.core_memory = core_memory
        self.task_directory = task_directory
        self.loaded_modules = {}  # Stores module_name: module_object
        self._ensure_task_directory()
        self._load_initial_modules()
        self.core_memory.append_to_list("capabilities", "module_loader_v1")
        print(f"ModuleLoader initialized. Task directory: {self.task_directory}")

    def _ensure_task_directory(self):
        """Ensures the task directory exists."""
        if not os.path.exists(self.task_directory):
            try:
                os.makedirs(self.task_directory)
                print(f"Created task directory: {self.task_directory}")
            except OSError as e:
                print(f"Error creating task directory {self.task_directory}: {e}")
                # Continue, as modules might be loaded from elsewhere or not needed immediately

    def _get_module_path(self, module_name):
        """Constructs the full path to a module file."""
        return os.path.join(self.task_directory, f"{module_name}.py")

    def _load_module_from_file(self, module_name, file_path):
        """Loads a single module from its file path."""
        if module_name in self.loaded_modules:
            print(f"Module '{module_name}' is already loaded.")
            return self.loaded_modules[module_name]

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            print(f"Error: Could not create module spec for {file_path}")
            return None

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module  # Add to sys.modules to avoid re-importing issues

        try:
            spec.loader.exec_module(module)
            self.loaded_modules[module_name] = module
            print(f"Successfully loaded module: {module_name}")
            return module
        except Exception as e:
            print(f"Error executing module {file_path}: {e}")
            traceback.print_exc()
            if module_name in sys.modules:
                del sys.modules[module_name] # Clean up sys.modules if loading failed
            return None

    def _load_initial_modules(self):
        """Loads all .py files from the task directory on initialization."""
        print("Loading initial modules...")
        if not os.path.isdir(self.task_directory):
            print(f"Task directory '{self.task_directory}' does not exist or is not a directory. Skipping initial load.")
            return

        for filename in os.listdir(self.task_directory):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]  # Remove .py extension
                file_path = os.path.join(self.task_directory, filename)
                self._load_module_from_file(module_name, file_path)
        print("Initial module loading complete.")

    def add_new_module(self, module_name, module_code):
        """
        Adds a new module dynamically by writing its code to a file
        and then loading it.
        """
        file_path = self._get_module_path(module_name)
        if os.path.exists(file_path):
            print(f"Module '{module_name}' already exists at {file_path}. Overwriting.")

        try:
            with open(file_path, "w") as f:
                f.write(module_code)
            print(f"Wrote new module code to: {file_path}")
            return self._load_module_from_file(module_name, file_path)
        except IOError as e:
            print(f"Error writing module code to {file_path}: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while adding module '{module_name}': {e}")
            return None


    def get_available_module_names(self):
        """Returns a list of names of currently loaded modules."""
        return list(self.loaded_modules.keys())

    def run_module(self, module_name, *args, **kwargs):
        """
        Executes the 'run' function of a loaded module.
        The 'run' function should accept arguments and return a result.
        """
        if module_name not in self.loaded_modules:
            print(f"Error: Module '{module_name}' is not loaded.")
            # Attempt to load it if it exists in the directory
            file_path = self._get_module_path(module_name)
            if os.path.exists(file_path):
                print(f"Attempting to load '{module_name}' on demand...")
                module = self._load_module_from_file(module_name, file_path)
                if module is None:
                    return None # Loading failed
            else:
                return None # Module doesn't exist

        module = self.loaded_modules.get(module_name)
        if module is None:
            print(f"Error: Module '{module_name}' could not be loaded or found.")
            return None

        if not hasattr(module, 'run'):
            print(f"Error: Module '{module_name}' does not have a 'run' function.")
            return None

        try:
            print(f"Executing module '{module_name}' with args: {args}, kwargs: {kwargs}")
            result = module.run(*args, **kwargs)
            print(f"Module '{module_name}' executed successfully.")
            return result
        except Exception as e:
            print(f"Error executing 'run' function in module '{module_name}': {e}")
            traceback.print_exc()
            return None

    def unload_module(self, module_name):
        """Unloads a module by name."""
        if module_name in self.loaded_modules:
            try:
                module = self.loaded_modules.pop(module_name)
                if module_name in sys.modules:
                    del sys.modules[module_name]
                print(f"Successfully unloaded module: {module_name} (removed from loaded_modules and sys.modules)")
                return True
            except KeyError:
                print(f"Error: Module '{module_name}' not found in loaded_modules during internal cleanup.")
                return False
            except Exception as e:
                print(f"An unexpected error occurred while unloading module '{module_name}': {e}")
                return False
        else:
            print(f"Module '{module_name}' not found in loaded modules. Cannot unload.")
            return False

# --- Mock Objects and Setup for Testing ---
class MockCoreMemory:
    def __init__(self):
        self.data = {"capabilities": []}
        print("MockCoreMemory initialized.")

    def save(self):
        print("MockCoreMemory: Data saved.")

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def update(self, key, updater_func, *args, **kwargs):
        current_value = self.data.get(key)
        updated_value = updater_func(current_value, *args, **kwargs)
        self.data[key] = updated_value
        self.save()

    def append_to_list(self, key, item):
        def _append(current_list, new_item):
            if current_list is None: return [new_item]
            if isinstance(current_list, list):
                current_list.append(new_item)
                return current_list
            else: return current_list
        self.update(key, _append, new_item=item)

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self.save()
            return True
        return False

    def clear(self):
        self.data = {}
        self.save()
        print("MockCoreMemory: Cleared.")

    def get_all_data(self):
        return self.data.copy()


# --- Example Usage and Testing ---
if __name__ == "__main__":
    import shutil
    import os

    # Define a temporary task directory for testing
    TEST_TASK_DIR = "test_ai_modules"
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
    os.makedirs(TEST_TASK_DIR)
    print(f"Created temporary task directory: {TEST_TASK_DIR}")

    # --- Test Case 1: Initialization and Loading Existing Modules ---
    print("\n--- Test Case 1: Initialization ---")
    # Create dummy module files
    sample_module_content = """
def run(data):
    print(f"Executing sample_module.run with: {data}")
    return f"Processed: {str(data).upper()}"

def helper_function():
    return "This is a helper."
"""
    with open(os.path.join(TEST_TASK_DIR, "sample_module.py"), "w") as f:
        f.write(sample_module_content)
    print("Created dummy 'sample_module.py'")

    error_module_content = """
def process_data(value):
    print(f"Processing: {value}")
    return value * 2
"""
    with open(os.path.join(TEST_TASK_DIR, "error_module.py"), "w") as f:
        f.write(error_module_content)
    print("Created dummy 'error_module.py'")


    mock_mem = MockCoreMemory()
    module_loader = ModuleLoader(mock_mem, task_directory=TEST_TASK_DIR)

    print("\nInitial loaded modules:", module_loader.get_available_module_names())
    assert "sample_module" in module_loader.get_available_module_names()
    assert "error_module" in module_loader.get_available_module_names()
    assert len(module_loader.loaded_modules) == 2

    # Check if CoreMemory capabilities were updated
    print("CoreMemory Capabilities:", mock_mem.get("capabilities"))
    assert "module_loader_v1" in mock_mem.get("capabilities", [])

    # --- Test Case 2: Running an Existing Module ---
    print("\n--- Test Case 2: Running Existing Module ---")
    result = module_loader.run_module("sample_module", "hello world")
    print("Result:", result)
    assert result == "Processed: HELLO WORLD"

    # Running a module that doesn't have a 'run' function
    result_no_run = module_loader.run_module("error_module", 5)
    print("Result (module without 'run'):", result_no_run)
    assert result_no_run is None # Expect None because 'run' is missing

    # --- Test Case 3: Adding a New Module Dynamically ---
    print("\n--- Test Case 3: Adding New Module ---")
    greeting_module_content = """
def run(name="Guest"):
    message = f"Hello, {name}!"
    print(f"Executing greeting_module.run for {name}")
    return message
"""
    added_module = module_loader.add_new_module("greeting_module", greeting_module_content)
    assert added_module is not None
    assert "greeting_module" in module_loader.get_available_module_names()
    assert len(module_loader.loaded_modules) == 3

    # Run the newly added module
    result_greeting = module_loader.run_module("greeting_module", name="Architect AI")
    print("Result:", result_greeting)
    assert result_greeting == "Hello, Architect AI!"

    # Run with default name
    result_default_greeting = module_loader.run_module("greeting_module")
    print("Result:", result_default_greeting)
    assert result_default_greeting == "Hello, Guest!"

    # --- Test Case 4: Handling Errors ---
    print("\n--- Test Case 4: Handling Errors ---")
    # Running a non-existent module
    result_nonexistent = module_loader.run_module("non_existent_module", "test")
    print("Result (non-existent):", result_nonexistent)
    assert result_nonexistent is None

    # Attempting to add a module with invalid code (simulated)
    invalid_module_code = "def run(self):\n print('invalid syntax')"
    print("Attempting to add invalid module...")
    invalid_module = module_loader.add_new_module("invalid_module", invalid_module_code)
    assert invalid_module is None # Should fail to load
    assert "invalid_module" not in module_loader.get_available_module_names()

    # --- Test Case 5: Unloading a Module ---
    print("\n--- Test Case 5: Unloading Module ---")
    unloaded = module_loader.unload_module("sample_module")
    print(f"Unloaded 'sample_module': {unloaded}")
    assert unloaded is True
    assert "sample_module" not in module_loader.get_available_module_names()
    assert len(module_loader.loaded_modules) == 2

    # Try running the unloaded module
    result_after_unload = module_loader.run_module("sample_module", "test")
    print("Result (after unload):", result_after_unload)
    assert result_after_unload is None # Should be None as it's unloaded

    # Try unloading a non-existent module
    unloaded_nonexistent = module_loader.unload_module("another_non_existent")
    print(f"Unloaded 'another_non_existent': {unloaded_nonexistent}")
    assert unloaded_nonexistent is False

    # Unload the last added module
    unloaded_greeting = module_loader.unload_module("greeting_module")
    print(f"Unloaded 'greeting_module': {unloaded_greeting}")
    assert unloaded_greeting is True
    assert len(module_loader.loaded_modules) == 1

    # --- Test Case 6: Load module on demand ---
    print("\n--- Test Case 6: Load Module On Demand ---")
    # Ensure it's unloaded first
    module_loader.unload_module("sample_module")
    assert "sample_module" not in module_loader.get_available_module_names()

    # Now try to run it - should load it automatically
    print("Running unloaded module 'sample_module' to test on-demand loading...")
    result_on_demand = module_loader.run_module("sample_module", "on demand test")
    print("Result (on demand):", result_on_demand)
    assert result_on_demand == "Processed: ON DEMAND TEST"
    assert "sample_module" in module_loader.get_available_module_names() # Should be loaded again


    # --- Cleanup ---
    print("\nCleaning up test directory...")
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Removed test directory: {TEST_TASK_DIR}")

    print("\n--- All Test Cases Completed ---")
