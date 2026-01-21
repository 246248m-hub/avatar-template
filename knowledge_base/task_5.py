import os
import sys
import importlib
from typing import Any, Dict, List

# --- Core Components ---

class CoreMemory:
    """
    Represents the persistent memory of the AI core.
    Stores configuration, state, and learned information.
    """
    def __init__(self, data_file: str = "core_memory.json"):
        self.data_file = data_file
        self.data = self._load_from_file()

    def _load_from_file(self) -> Dict[str, Any]:
        """Loads data from the JSON file."""
        if os.path.exists(self.data_file):
            try:
                import json
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading core memory from {self.data_file}: {e}. Starting with empty memory.")
                return {}
        return {}

    def save(self) -> None:
        """Saves the current data to the JSON file."""
        try:
            import json
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=4)
            print("Core memory saved.")
        except IOError as e:
            print(f"Error saving core memory to {self.data_file}: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a value from memory."""
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Sets a value in memory."""
        self.data[key] = value

    def update_capability(self, capability_name: str) -> None:
        """Adds a capability if it doesn't exist and saves."""
        capabilities = self.data.setdefault("capabilities", [])
        if capability_name not in capabilities:
            capabilities.append(capability_name)
            self.save()
            print(f"Capability '{capability_name}' added to memory.")

class DynamicLogicProcessor:
    """
    Manages and executes dynamic logic units (modules).
    Handles loading, unloading, and running module code.
    """
    def __init__(self, core_memory: CoreMemory, task_directory: str = "ai_modules"):
        self.core_memory = core_memory
        self.task_directory = task_directory
        self.loaded_modules: Dict[str, Any] = {}  # Stores loaded module objects

        if not os.path.exists(self.task_directory):
            os.makedirs(self.task_directory)
            print(f"Created task directory: {self.task_directory}")

        # Load any modules that were previously registered and should be available
        self._load_initial_modules()

    def _module_path_to_name(self, filepath: str) -> str:
        """Converts a file path to a module name."""
        base_name = os.path.basename(filepath)
        module_name, _ = os.path.splitext(base_name)
        return module_name

    def _load_initial_modules(self) -> None:
        """Loads modules that are already present in the task directory."""
        print(f"Scanning for existing modules in '{self.task_directory}'...")
        for filename in os.listdir(self.task_directory):
            if filename.endswith(".py"):
                filepath = os.path.join(self.task_directory, filename)
                self._load_module_from_file(filepath)

    def add_new_module(self, module_name: str, module_content: str) -> bool:
        """
        Creates a new Python module file, loads it, and updates capabilities.
        Returns True if successful, False otherwise.
        """
        module_filename = f"{module_name}.py"
        module_filepath = os.path.join(self.task_directory, module_filename)

        try:
            with open(module_filepath, "w") as f:
                f.write(module_content)
            print(f"Created module file: {module_filepath}")

            # Load the newly added module
            if self._load_module_from_file(module_filepath):
                # Update capabilities in memory
                self.core_memory.update_capability("module_loader_v1")
                return True
            else:
                print(f"Failed to load newly added module: {module_name}")
                return False

        except IOError as e:
            print(f"Error writing module file {module_filepath}: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred while adding module {module_name}: {e}")
            return False

    def _load_module_from_file(self, filepath: str) -> bool:
        """Loads a Python module from its file path."""
        module_name = self._module_path_to_name(filepath)
        if module_name in self.loaded_modules:
            print(f"Module '{module_name}' is already loaded.")
            return True

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
            print(f"An unexpected error occurred during module import {module_name}: {e}")
            return False
        finally:
            # Clean up sys.path if it was modified
            if sys.path and sys.path[0] == self.task_directory:
                sys.path.pop(0)

    def get_available_module_names(self) -> List[str]:
        """Returns a list of names of all loaded modules."""
        return list(self.loaded_modules.keys())

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

    def unload_module(self, module_name: str) -> bool:
        """
        Unloads a module from memory.
        Returns True if successful, False otherwise.
        """
        if module_name not in self.loaded_modules:
            print(f"Error: Module '{module_name}' is not loaded and cannot be unloaded.")
            return False

        try:
            del self.loaded_modules[module_name]
            # Attempt to remove from sys.modules to fully unload
            if module_name in sys.modules:
                del sys.modules[module_name]
            print(f"Successfully unloaded module: {module_name}")
            return True
        except Exception as e:
            print(f"Error unloading module '{module_name}': {e}")
            return False


# --- AI Core Orchestrator ---

class AIArcadeCore:
    """
    The central orchestrator of the AI core.
    Integrates persistent memory and dynamic logic processing.
    """
    def __init__(self, memory_file: str = "core_memory.json", module_dir: str = "ai_modules"):
        print("Initializing AI Core...")
        self.core_memory = CoreMemory(data_file=memory_file)
        self.logic_processor = DynamicLogicProcessor(core_memory=self.core_memory, task_directory=module_dir)
        print("AI Core initialized.")

    def add_new_module(self, module_name: str, module_content: str) -> bool:
        """
        Delegates the creation and loading of a new module to the logic processor.
        """
        return self.logic_processor.add_new_module(module_name, module_content)

    def run_module(self, module_name: str, *args, **kwargs) -> Any:
        """
        Delegates module execution to the logic processor.
        """
        return self.logic_processor.run_module(module_name, *args, **kwargs)

    def get_available_modules(self) -> List[str]:
        """
        Returns a list of available module names.
        """
        return self.logic_processor.get_available_module_names()

    def unload_module(self, module_name: str) -> bool:
        """
        Delegates module unloading to the logic processor.
        """
        return self.logic_processor.unload_module(module_name)

    def get_capability(self, capability_name: str) -> Any:
        """
        Retrieves information about a capability from core memory.
        """
        return self.core_memory.get(capability_name)

    def save_core_state(self) -> None:
        """
        Saves the current state of the core memory.
        """
        self.core_memory.save()

# --- Example Usage / Testing ---

if __name__ == "__main__":
    # Clean up previous test artifacts if they exist
    if os.path.exists("core_memory.json"):
        os.remove("core_memory.json")
    if os.path.exists("ai_modules"):
        import shutil
        shutil.rmtree("ai_modules")

    # 1. Initialize the core
    print("\n--- Initializing Core ---")
    core = AIArcadeCore(memory_file="core_memory.json", module_dir="ai_modules")

    # 2. Add some initial modules
    print("\n--- Adding Initial Modules ---")

    greeting_module_content = """
def run(name="World"):
    greeting = f"Hello, {name}!"
    print(f"Inside greeting_module: {greeting}")
    return greeting
"""
    core.add_new_module("greeting_module", greeting_module_content)

    math_module_content = """
def run(a, b, operation='+'):
    if operation == '+':
        result = a + b
    elif operation == '-':
        result = a - b
    elif operation == '*':
        result = a * b
    elif operation == '/':
        result = a / b
    else:
        result = 'Unknown operation'
    print(f"Inside math_module: {a} {operation} {b} = {result}")
    return result
"""
    core.add_new_module("math_module", math_module_content)

    # 3. Check available modules
    print(f"\nAvailable modules: {core.get_available_modules()}")

    # 4. Run modules
    print("\n--- Running Modules ---")
    greeting_result = core.run_module("greeting_module", name="Phoenix")
    print(f"Result from greeting_module: {greeting_result}")

    math_result_add = core.run_module("math_module", 10, 5, operation='+')
    print(f"Result from math_module (add): {math_result_add}")

    math_result_multiply = core.run_module("math_module", 7, 6, operation='*')
    print(f"Result from math_module (multiply): {math_result_multiply}")

    # 5. Add a new module dynamically
    print("\n--- Adding Dynamic Module ---")
    logger_module_content = """
def run(message, level="INFO"):
    log_entry = f"[{level}] {message}"
    print(f"Logger: {log_entry}")
    return log_entry
"""
    core.add_new_module("logger_module", logger_module_content)
    print(f"Available modules after adding logger: {core.get_available_modules()}")

    # 6. Run the newly added logger module
    print("\n--- Running Dynamic Module ---")
    log_entry = core.run_module("logger_module", "System startup complete.", level="INFO")
    print(f"Logged entry: {log_entry}")

    # 7. Try to run a non-existent module
    print("\n--- Running Non-Existent Module ---")
    core.run_module("non_existent_module", "data")

    # 8. Unload a module
    print("\n--- Unloading a Module ---")
    core.unload_module("greeting_module")
    print(f"Available modules after unloading: {core.get_available_modules()}")
    core.run_module("greeting_module", "test") # This should now fail

    # 9. Save core state
    print("\n--- Saving Core State ---")
    core.save_core_state()

    # 10. Re-initialize core to test persistence
    print("\n--- Re-initializing Core to Test Persistence ---")
    core_reloaded = AIArcadeCore(memory_file="core_memory.json", module_dir="ai_modules")
    print(f"Available modules after reload: {core_reloaded.get_available_modules()}")
    # The greeting_module should NOT be available if unloaded correctly
    # The logger_module and math_module should be available if they were added before saving

    print("\n--- Testing Complete ---")
