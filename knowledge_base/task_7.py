import importlib
import os
import sys
from typing import Any, Dict, List

# Assume CoreMemory is defined elsewhere and has a 'data' attribute (dict)
# and a 'save' method. For demonstration, we'll mock it if not provided.
try:
    from core_memory import CoreMemory
except ImportError:
    class CoreMemory:
        def __init__(self):
            self.data = {"capabilities": []}
        def save(self):
            print("MockCoreMemory: Data saved.")

class ModuleLoader:
    """
    Manages the loading, unloading, and execution of Python modules dynamically.
    Modules are expected to reside in a designated task directory and have a 'run' function.
    """
    def __init__(self, core_memory: CoreMemory, task_directory: str = "phoenix_tasks"):
        """
        Initializes the ModuleLoader.

        Args:
            core_memory: An instance of CoreMemory to store and retrieve AI state.
            task_directory: The directory where modules are stored and loaded from.
        """
        self.core_memory = core_memory
        self.task_directory = os.path.abspath(task_directory)
        self.loaded_modules: Dict[str, Any] = {}  # Stores loaded module objects
        self._ensure_task_directory_exists()
        self._load_initial_modules()

    def _ensure_task_directory_exists(self):
        """Ensures the task directory exists, creating it if necessary."""
        if not os.path.exists(self.task_directory):
            try:
                os.makedirs(self.task_directory)
                print(f"Created task directory: {self.task_directory}")
            except OSError as e:
                print(f"Error creating task directory {self.task_directory}: {e}")

    def _module_path_to_name(self, filepath: str) -> str:
        """Converts a module file path to a Python module name."""
        # Remove the task directory prefix and the .py extension
        relative_path = os.path.relpath(filepath, self.task_directory)
        module_name = os.path.splitext(relative_path)[0]
        # Replace directory separators with dots for nested modules (if any)
        return module_name.replace(os.sep, '.')

    def _load_initial_modules(self):
        """Loads all .py files found in the task directory at initialization."""
        print(f"Scanning for initial modules in: {self.task_directory}")
        for filename in os.listdir(self.task_directory):
            if filename.endswith(".py") and not filename.startswith("__"): # Ignore __init__.py and other special files
                filepath = os.path.join(self.task_directory, filename)
                self._load_module_from_file(filepath)

    def add_new_module(self, module_name: str, module_content: str):
        """
        Creates a new module file, loads it, and updates core capabilities.

        Args:
            module_name: The base name for the new module (e.g., "my_task").
            module_content: The Python code content of the module.
        """
        # Ensure the module name is valid and doesn't contain path separators
        if os.sep in module_name or "/" in module_name or "\\" in module_name:
            print(f"Error: Invalid module name '{module_name}'. Cannot contain path separators.")
            return

        module_filename = f"{module_name}.py"
        module_filepath = os.path.join(self.task_directory, module_filename)
        h = os.path.join(self.task_directory, module_filename) # Redundant variable, but kept for consistency with original code

        try:
            with open(module_filepath, "w") as f:
                f.write(module_content)
            print(f"Created module file: {module_filepath}")

            # Load the newly added module
            if self._load_module_from_file(module_filepath):
                # Update capabilities in memory if loading was successful
                capability_name = f"{module_name}_v1" # Example: "greeting_task_v1"
                if capability_name not in self.core_memory.data.get("capabilities", []):
                    self.core_memory.data.setdefault("capabilities", []).append(capability_name)
                    self.core_memory.save()
                    print(f"Added capability: {capability_name}")

        except IOError as e:
            print(f"Error writing module file {module_filepath}: {e}")
        except Exception as e:
            print(f"Error loading newly added module {module_name}: {e}")


    def _load_module_from_file(self, filepath: str) -> bool:
        """Loads a Python module from its file path."""
        module_name = self._module_path_to_name(filepath)
        # Add the task directory to sys.path to allow importing
        if self.task_directory not in sys.path:
            sys.path.insert(0, self.task_directory)

        try:
            # Import the module
            module = importlib.import_module(module_name)
            self.loaded_modules[module_name] = module
            print(f"Successfully loaded module: {module_name}")
            return True
        except ImportError as e:
            print(f"Error importing module {module_name} from {filepath}: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred while importing {module_name}: {e}")
            return False
        finally:
            # Clean up sys.path if it was modified and we are the first entry
            if sys.path and sys.path[0] == self.task_directory:
                sys.path.pop(0)


    def run_module(self, module_name: str, *args, **kwargs) -> Any:
        """
        Executes the 'run' function of a specified loaded module.

        Args:
            module_name: The name of the module to execute.
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
        Unloads a module from memory.

        Args:
            module_name: The name of the module to unload.

        Returns:
            True if the module was successfully unloaded, False otherwise.
        """
        if module_name in self.loaded_modules:
            # Remove from loaded modules dictionary
            del self.loaded_modules[module_name]

            # Attempt to remove from sys.modules to free up memory
            # This is more complex and can have side effects if other modules depend on it.
            # For simplicity here, we'll rely on Python's garbage collection after removing from our dict.
            # A more robust unload would involve careful dependency checking.

            print(f"Module '{module_name}' unloaded.")
            return True
        else:
            print(f"Error: Module '{module_name}' is not currently loaded.")
            return False

    def get_available_module_names(self) -> List[str]:
        """Returns a list of names of all currently loaded modules."""
        return list(self.loaded_modules.keys())

# --- Testing Section (for standalone execution) ---
if __name__ == "__main__":
    # Mock CoreMemory for testing
    class MockCoreMemory:
        def __init__(self):
            self.data = {"capabilities": []}
        def save(self):
            print("MockCoreMemory: Data saved.")
        def load(self): # Added a load method for completeness if needed
            print("MockCoreMemory: Data loaded.")


    import os
    import shutil

    # Create dummy task directory and files for testing
    TASK_DIR = "phoenix_tasks_test" # Use a distinct directory for testing
    if os.path.exists(TASK_DIR):
        shutil.rmtree(TASK_DIR)
    os.makedirs(TASK_DIR)


    sample_task_content = """
def run(message):
    print(f"Inside sample_task: {message}")
    return f"Processed by sample_task: {message}"
"""
    with open(os.path.join(TASK_DIR, "sample_task.py"), "w") as f:
        f.write(sample_task_content)

    print("--- Testing ModuleLoader ---")

    mock_mem = MockCoreMemory()
    loader = ModuleLoader(mock_mem, task_directory=TASK_DIR)

    print("\nInitial loaded modules:", loader.get_available_module_names())

    print("\nRunning 'sample_task':")
    result = loader.run_module("sample_task", "Hello from the outside!")
    print("Result:", result)

    print("\nAdding a new module 'greeting_task':")
    greeting_task_content = """
def run(name="World"):
    greeting = f"Greetings, {name}!"
    print(f"Inside greeting_task: {greeting}")
    return greeting
"""
    loader.add_new_module("greeting_task", greeting_task_content)

    print("\nUpdated loaded modules:", loader.get_available_module_names())

    print("\nRunning 'greeting_task' with custom name:")
    result = loader.run_module("greeting_task", name="Phoenix AI")
    print("Result:", result)

    print("\nRunning 'greeting_task' with default name:")
    result = loader.run_module("greeting_task")
    print("Result:", result)

    print("\nRunning non-existent task:")
    result = loader.run_module("non_existent_task", "some data")
    print("Result:", result)

    print("\nMock Core Memory Capabilities after adding module:", mock_mem.data.get("capabilities"))

    print("\nUnloading 'sample_task':")
    loader.unload_module("sample_task")
    print("Current loaded modules:", loader.get_available_module_names())

    print("\nTrying to run unloaded 'sample_task':")
    result = loader.run_module("sample_task", "This should fail")
    print("Result:", result)

    # Clean up dummy files and directory
    print("\nCleaning up dummy files...")
    if os.path.exists(TASK_DIR):
        shutil.rmtree(TASK_DIR)
    print("--- Testing Complete ---")
