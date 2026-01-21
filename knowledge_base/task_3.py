# PHOENIX CORE - MODULE LOADER (task_1_module_loader.py)
# REQUIREMENTS:
# - Relies on CoreMemory from task_0.
# - Can load modules dynamically from a 'phoenix_tasks' directory.
# - Modules must have a 'run(message)' function.
# - Stores loaded module references and their names.

import os
import importlib
import sys
from typing import Dict, Any

# Assuming CoreMemory is available from task_0
# from task_0_phoenix_core_dna_module import CoreMemory

class ModuleLoader:
    def __init__(self, core_memory):
        self.core_memory = core_memory
        self.task_directory = "phoenix_tasks"
        self.loaded_modules: Dict[str, Any] = {}
        self._ensure_task_directory()
        self._load_predefined_modules()

    def _ensure_task_directory(self):
        """Ensures the task directory exists."""
        if not os.path.exists(self.task_directory):
            os.makedirs(self.task_directory)
            print(f"Created task directory: {self.task_directory}")

    def _load_predefined_modules(self):
        """Loads modules that are expected to be present at core initialization."""
        # For now, this is a placeholder. In a more robust system,
        # this might scan the directory or load from memory.
        pass

    def get_available_module_names(self) -> list[str]:
        """Returns a list of names of currently loaded modules."""
        return list(self.loaded_modules.keys())

    def _module_path_to_name(self, module_path: str) -> str:
        """Converts a file path to a module name."""
        base_name = os.path.basename(module_path)
        return os.path.splitext(base_name)[0]

    def add_new_module(self, module_name: str, module_content: str):
        """
        Adds a new module by writing its content to a file and loading it.
        Assumes module_name is a valid Python identifier for a filename.
        """
        module_filename = f"{module_name}.py"
        module_filepath = os.path.join(self.task_directory, module_filename)

        try:
            with open(module_filepath, "w") as f:
                f.write(module_content)
            print(f"Created module file: {module_filepath}")

            # Load the newly added module
            self._load_module_from_file(module_filepath)

            # Update capabilities in memory
            if "module_loader_v1" not in self.core_memory.data.get("capabilities", []):
                self.core_memory.data.setdefault("capabilities", []).append("module_loader_v1")
                self.core_memory.save()
                print("Added capability: module_loader_v1")

        except IOError as e:
            print(f"Error writing module file {module_filepath}: {e}")
        except Exception as e:
            print(f"Error loading newly added module {module_name}: {e}")


    def _load_module_from_file(self, filepath: str):
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
        finally:
            # Clean up sys.path if it was modified
            if self.task_directory in sys.path and sys.path[0] == self.task_directory:
                sys.path.pop(0)


    def run_module(self, module_name: str, *args, **kwargs) -> Any:
        """
        Executes the 'run' function of a specified loaded module.
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

# --- Testing Section (for standalone execution) ---
if __name__ == "__main__":
    # Mock CoreMemory for testing
    class MockCoreMemory:
        def __init__(self):
            self.data = {"capabilities": []}
        def save(self):
            print("MockCoreMemory: Data saved.")

    import os
    import shutil

    # Create dummy task directory and files for testing
    TASK_DIR = "phoenix_tasks"
    if not os.path.exists(TASK_DIR):
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
    loader = ModuleLoader(mock_mem)

    # Test loading an existing module (if present in the directory structure)
    # For this isolated test, we manually add the sample task to ensure it's discoverable
    loader._load_module_from_file(os.path.join(TASK_DIR, "sample_task.py"))


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

    # Clean up dummy files and directory
    print("\nCleaning up dummy files...")
    if os.path.exists(TASK_DIR):
        shutil.rmtree(TASK_DIR)
    print("--- Testing Complete ---")
