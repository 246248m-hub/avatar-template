import os
import sys
import importlib
import shutil

# --- Core Components ---

class CoreMemory:
    """
    Simulates persistent memory for the AI core.
    Stores data and capabilities.
    """
    def __init__(self):
        self._data = {}
        self._capabilities = set()
        print("CoreMemory initialized.")

    def set(self, key, value):
        """Sets a key-value pair in memory."""
        self._data[key] = value
        print(f"CoreMemory: Set '{key}' = {value}")

    def get(self, key, default=None):
        """Gets the value for a key, or returns default if not found."""
        value = self._data.get(key, default)
        # print(f"CoreMemory: Get '{key}' -> {value}") # Verbose logging
        return value

    def has(self, key):
        """Checks if a key exists in memory."""
        return key in self._data

    def add_capability(self, capability_name):
        """Adds a new capability to the core."""
        if capability_name not in self._capabilities:
            self._capabilities.add(capability_name)
            print(f"CoreMemory: Added capability '{capability_name}'")
            # Update memory with current capabilities
            self.set("capabilities", list(self._capabilities))

    def get_capabilities(self):
        """Returns the set of current capabilities."""
        return self._capabilities

class ModuleLoader:
    """
    Manages the loading, unloading, and execution of AI modules.
    Modules are expected to be Python files containing a 'run' function.
    """
    def __init__(self, core_memory, task_directory="modules"):
        self.core_memory = core_memory
        self.task_directory = task_directory
        self.loaded_modules = {}  # Stores loaded module objects {module_name: module_object}
        self.module_paths = {}    # Stores module file paths {module_name: file_path}

        if not os.path.exists(self.task_directory):
            os.makedirs(self.task_directory)
            print(f"Module directory '{self.task_directory}' created.")

        self._scan_and_load_initial_modules()
        self.core_memory.add_capability("module_loader_v1")
        print(f"ModuleLoader initialized. Task directory: '{self.task_directory}'")

    def _get_module_path(self, module_name):
        """Constructs the expected file path for a module."""
        return os.path.join(self.task_directory, f"{module_name}.py")

    def _scan_and_load_initial_modules(self):
        """Scans the task directory and loads any existing Python files as modules."""
        print("Scanning for initial modules...")
        if not os.path.exists(self.task_directory):
            return

        for filename in os.listdir(self.task_directory):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # Remove .py extension
                module_path = os.path.join(self.task_directory, filename)
                if self._load_module_from_path(module_name, module_path):
                    print(f"Successfully loaded initial module: '{module_name}'")

    def _load_module_from_path(self, module_name, module_path):
        """Loads a module from a given file path."""
        if module_name in self.loaded_modules:
            print(f"Module '{module_name}' is already loaded.")
            return False

        try:
            # Add the directory to sys.path to allow importing
            if self.task_directory not in sys.path:
                sys.path.insert(0, self.task_directory)

            # Import the module
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Store the loaded module and its path
            self.loaded_modules[module_name] = module
            self.module_paths[module_name] = module_path
            print(f"Loaded module '{module_name}' from '{module_path}'.")
            return True

        except Exception as e:
            print(f"Error loading module '{module_name}' from '{module_path}': {e}")
            # Clean up sys.path if it was added
            if self.task_directory in sys.path and sys.path[0] == self.task_directory:
                 sys.path.pop(0)
            return False
        finally:
            # Ensure sys.path is clean if the module was not successfully loaded or if no longer needed
            if self.task_directory in sys.path and module_name not in self.loaded_modules:
                 if sys.path[0] == self.task_directory:
                    sys.path.pop(0)


    def add_new_module(self, module_name, module_code):
        """
        Creates a new module file with the given code and loads it.
        Returns the loaded module object on success, None otherwise.
        """
        if module_name in self.loaded_modules:
            print(f"Module '{module_name}' already exists and is loaded.")
            return self.loaded_modules[module_name]

        module_path = self._get_module_path(module_name)
        try:
            with open(module_path, "w") as f:
                f.write(module_code)
            print(f"Created new module file: '{module_path}'")

            if self._load_module_from_path(module_name, module_path):
                return self.loaded_modules[module_name]
            else:
                # Clean up the created file if loading failed
                if os.path.exists(module_path):
                    os.remove(module_path)
                    print(f"Removed failed module file: '{module_path}'")
                return None

        except Exception as e:
            print(f"Error adding new module '{module_name}': {e}")
            return None

    def run_module(self, module_name, *args, **kwargs):
        """
        Runs the 'run' function of a loaded module.
        Handles on-demand loading if the module is not currently loaded.
        Returns the result of the 'run' function, or None if the module
        or its 'run' function doesn't exist or an error occurs.
        """
        if module_name not in self.loaded_modules:
            print(f"Module '{module_name}' not loaded. Attempting to load on demand...")
            module_path = self._get_module_path(module_name)
            if os.path.exists(module_path):
                if not self._load_module_from_path(module_name, module_path):
                    print(f"Failed to load module '{module_name}' on demand.")
                    return None
            else:
                print(f"Module file not found for '{module_name}' at '{module_path}'.")
                return None

        if module_name not in self.loaded_modules:
            print(f"Module '{module_name}' still not available after attempted load.")
            return None

        module = self.loaded_modules[module_name]

        if hasattr(module, 'run') and callable(module.run):
            try:
                print(f"Executing module '{module_name}' with args: {args}, kwargs: {kwargs}")
                # Pass core_memory to the module if it accepts it
                if 'core_memory' in module.run.__code__.co_varnames:
                    result = module.run(*args, core_memory=self.core_memory, **kwargs)
                else:
                    result = module.run(*args, **kwargs)
                print(f"Module '{module_name}' execution finished.")
                return result
            except Exception as e:
                print(f"Error running module '{module_name}': {e}")
                return None
        else:
            print(f"Module '{module_name}' does not have a callable 'run' function.")
            return None

    def unload_module(self, module_name):
        """Unloads a module by name."""
        if module_name in self.loaded_modules:
            try:
                # Remove from loaded modules
                del self.loaded_modules[module_name]
                module_path = self.module_paths.pop(module_name, None)

                # Remove from sys.modules to ensure a clean slate if reloaded
                if module_name in sys.modules:
                    del sys.modules[module_name]

                # Remove from sys.path if it was added specifically for this module's dir
                # This is a simplified approach; a more robust solution might track added paths
                if self.task_directory in sys.path and sys.path[0] == self.task_directory:
                    sys.path.pop(0)

                # Optionally, remove the file from disk if it was dynamically added
                # For now, we assume files in task_directory persist
                # if module_path and module_path.startswith(os.path.abspath(self.task_directory)):
                #     os.remove(module_path)
                #     print(f"Removed module file: '{module_path}'")

                print(f"Unloaded module '{module_name}'.")
                return True
            except Exception as e:
                print(f"Error unloading module '{module_name}': {e}")
                return False
        else:
            print(f"Module '{module_name}' is not loaded.")
            return False

    def get_available_module_names(self):
        """Returns a list of names of currently loaded modules."""
        return list(self.loaded_modules.keys())

# --- Mock Components for Testing ---

class MockCoreMemory(CoreMemory):
    """A simplified CoreMemory for testing purposes."""
    def __init__(self):
        super().__init__()
        self._data = {"capabilities": []} # Initialize with empty capabilities list
        print("MockCoreMemory initialized.")

    def set(self, key, value):
        if key == "capabilities":
            self._capabilities = set(value) # Ensure it's a set internally
        super().set(key, value)

    def add_capability(self, capability_name):
        if capability_name not in self._capabilities:
            self._capabilities.add(capability_name)
            self.set("capabilities", list(self._capabilities)) # Update memory as list

# --- Test Cases ---

def run_module_loader_tests():
    print("\n--- Starting ModuleLoader Tests ---")

    TEST_TASK_DIR = "test_modules"
    # Clean up previous test runs
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Cleaned up existing test directory: {TEST_TASK_DIR}")

    os.makedirs(TEST_TASK_DIR, exist_ok=True)
    print(f"Created test directory: {TEST_TASK_DIR}")

    # --- Test Case 1: Initialization and Basic Loading ---
    print("\n--- Test Case 1: Initialization and Basic Loading ---")

    # Create dummy module files
    sample_module_content = """
import os

def run(input_string):
    print(f"Processing: {input_string}")
    return input_string.upper()

def helper_function():
    return "This is a helper."
"""
    with open(os.path.join(TEST_TASK_DIR, "sample_module.py"), "w") as f:
        f.write(sample_module_content)
    print("Created dummy 'sample_module.py'")

    error_module_content = """
def some_other_function(value):
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
    # error_module should load even without a 'run' function, but running it will fail.
    assert len(module_loader.loaded_modules) == 2

    # Check if CoreMemory capabilities were updated
    print("CoreMemory Capabilities:", mock_mem.get("capabilities"))
    assert "module_loader_v1" in mock_mem.get("capabilities", [])

    # --- Test Case 2: Running an Existing Module ---
    print("\n--- Test Case 2: Running Existing Module ---")
    result = module_loader.run_module("sample_module", "hello world")
    print("Result:", result)
    assert result == "HELLO WORLD"

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

def farewell(name="Guest"):
    return f"Goodbye, {name}!"
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

    # Try calling another function in the module (should not work via run_module)
    result_other_func = module_loader.run_module("greeting_module", "farewell", name="Test")
    print("Result (calling other func via run_module):", result_other_func)
    assert result_other_func is None # run_module specifically calls 'run'

    # --- Test Case 4: Handling Errors ---
    print("\n--- Test Case 4: Handling Errors ---")
    # Running a non-existent module
    result_nonexistent = module_loader.run_module("non_existent_module", "test")
    print("Result (non-existent):", result_nonexistent)
    assert result_nonexistent is None

    # Attempting to add a module with invalid code (simulated)
    invalid_module_code = "def run(self):\n print('invalid syntax')" # Missing colon and incorrect indentation
    print("Attempting to add invalid module...")
    invalid_module = module_loader.add_new_module("invalid_module", invalid_module_code)
    assert invalid_module is None # Should fail to load
    assert "invalid_module" not in module_loader.get_available_module_names()

    # Running a module that raises an exception
    exception_module_content = """
def run(value):
    raise ValueError("This is a simulated error!")
    return value
"""
    module_loader.add_new_module("exception_module", exception_module_content)
    result_exception = module_loader.run_module("exception_module", 10)
    print("Result (exception module):", result_exception)
    assert result_exception is None

    # --- Test Case 5: Unloading a Module ---
    print("\n--- Test Case 5: Unloading Module ---")
    unloaded = module_loader.unload_module("sample_module")
    print(f"Unloaded 'sample_module': {unloaded}")
    assert unloaded is True
    assert "sample_module" not in module_loader.get_available_module_names()
    assert len(module_loader.loaded_modules) == 3 # greeting_module, error_module, exception_module remain

    # Try running the unloaded module
    result_after_unload = module_loader.run_module("sample_module", "test")
    print("Result (after unload):", result_after_unload)
    assert result_after_unload == "TEST" # Should load it on demand again
    assert "sample_module" in module_loader.get_available_module_names() # Should be loaded again

    # Unload it again to test the 'already unloaded' case
    unloaded_again = module_loader.unload_module("sample_module")
    print(f"Unloaded 'sample_module' again: {unloaded_again}")
    assert unloaded_again is True
    assert "sample_module" not in module_loader.get_available_module_names()

    # Try unloading a non-existent module
    unloaded_nonexistent = module_loader.unload_module("another_non_existent")
    print(f"Unloaded 'another_non_existent': {unloaded_nonexistent}")
    assert unloaded_nonexistent is False

    # Unload the last added module
    unloaded_greeting = module_loader.unload_module("greeting_module")
    print(f"Unloaded 'greeting_module': {unloaded_greeting}")
    assert unloaded_greeting is True
    assert len(module_loader.loaded_modules) == 2 # error_module, exception_module remain

    # --- Test Case 6: CoreMemory Integration ---
    print("\n--- Test Case 6: CoreMemory Integration ---")
    # Create a module that uses CoreMemory
    mem_module_content = """
def run(core_memory, key, value):
    print(f"MemModule: Setting '{key}' to '{value}'")
    core_memory.set(key, value)
    return core_memory.get(key)

def read_mem(core_memory, key):
    return core_memory.get(key)
"""
    module_loader.add_new_module("mem_module", mem_module_content)
    assert "mem_module" in module_loader.get_available_module_names()

    # Test setting a value
    result_set = module_loader.run_module("mem_module", key="my_setting", value="test_value")
    print(f"Result (mem_module set): {result_set}")
    assert result_set == "test_value"
    assert mock_mem.get("my_setting") == "test_value"

    # Test reading a value
    result_read = module_loader.run_module("mem_module", "read_mem", key="my_setting")
    print(f"Result (mem_module read): {result_read}")
    assert result_read == "test_value"

    # Test reading a non-existent key
    result_read_nonexistent = module_loader.run_module("mem_module", "read_mem", key="non_existent")
    print(f"Result (mem_module read non-existent): {result_read_nonexistent}")
    assert result_read_nonexistent is None

    # Test capabilities update
    assert "module_loader_v1" in mock_mem.get("capabilities")
    assert "mem_module_v1" not in mock_mem.get("capabilities") # Make sure it doesn't add arbitrary capabilities

    # --- Cleanup ---
    print("\nCleaning up test directory...")
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Removed test directory: {TEST_TASK_DIR}")

    # Restore sys.path
    if TEST_TASK_DIR in sys.path and sys.path[0] == TEST_TASK_DIR:
        sys.path.pop(0)

    print("\n--- All ModuleLoader Test Cases Completed ---")

if __name__ == "__main__":
    # Example Usage:
    # Create a mock memory and module loader
    mock_memory = MockCoreMemory()
    # Use a temporary directory for modules
    current_dir = os.path.dirname(os.path.abspath(__file__))
    module_dir = os.path.join(current_dir, "ai_core_modules")
    if not os.path.exists(module_dir):
        os.makedirs(module_dir)

    module_manager = ModuleLoader(mock_memory, task_directory=module_dir)

    # Example: Add a simple module dynamically
    simple_module_code = """
def run(data):
    processed_data = data.lower()
    print(f"Simple module processed: {processed_data}")
    return processed_data
"""
    module_manager.add_new_module("simple_processor", simple_module_code)

    # Run the module
    result = module_manager.run_module("simple_processor", "HeLLo WoRLd")
    print(f"Result from simple_processor: {result}")

    # Example: Add a module that uses core memory
    memory_user_module_code = """
def run(core_memory, key, value):
    print(f"Memory user module: Setting key '{key}' to '{value}'")
    core_memory.set(key, value)
    return f"Set '{key}'. Value is now: {core_memory.get(key)}"
"""
    module_manager.add_new_module("memory_user", memory_user_module_code)
    result_mem = module_manager.run_module("memory_user", key="user_preference", value="dark_mode")
    print(f"Result from memory_user: {result_mem}")
    print(f"Value in mock_memory: {mock_memory.get('user_preference')}")

    # Run tests
    run_module_loader_tests()

    # --- Final Cleanup ---
    print("\nPerforming final cleanup...")
    if os.path.exists(module_dir):
        try:
            shutil.rmtree(module_dir)
            print(f"Removed module directory: {module_dir}")
        except OSError as e:
            print(f"Error removing module directory {module_dir}: {e}")

    # Restore sys.path if needed
    if module_dir in sys.path and sys.path[0] == module_dir:
        sys.path.pop(0)

    print("\nAI Core initialization and testing complete.")
