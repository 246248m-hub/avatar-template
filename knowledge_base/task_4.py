import json
from typing import Any, Dict

class PersistentMemory:
    """
    Manages persistent storage for the AI core.
    This module handles saving and loading the core's state.
    """

    def __init__(self, storage_path: str = "core_memory.json"):
        """
        Initializes PersistentMemory.

        Args:
            storage_path (str): The path to the JSON file for storing memory.
        """
        self.storage_path = storage_path
        self.data: Dict[str, Any] = self._load_memory()

    def _load_memory(self) -> Dict[str, Any]:
        """Loads data from the persistent storage file."""
        try:
            with open(self.storage_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Memory file not found at {self.storage_path}. Starting with empty memory.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.storage_path}. Starting with empty memory.")
            return {}
        except Exception as e:
            print(f"An unexpected error occurred while loading memory: {e}")
            return {}

    def save(self) -> None:
        """Saves the current data to the persistent storage file."""
        try:
            with open(self.storage_path, "w") as f:
                json.dump(self.data, f, indent=4)
            print(f"AI core memory saved to {self.storage_path}")
        except IOError as e:
            print(f"Error saving AI core memory to {self.storage_path}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while saving memory: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a value from memory.

        Args:
            key (str): The key of the data to retrieve.
            default (Any): The default value to return if the key is not found.

        Returns:
            Any: The value associated with the key, or the default value.
        """
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Sets a value in memory.

        Args:
            key (str): The key to set.
            value (Any): The value to associate with the key.
        """
        self.data[key] = value
        self.save()
        print(f"Memory updated for key: '{key}'")

    def update(self, data_to_merge: Dict[str, Any]) -> None:
        """
        Updates the memory with new data, merging dictionaries.

        Args:
            data_to_merge (Dict[str, Any]): A dictionary containing the data to merge.
        """
        for key, value in data_to_merge.items():
            if isinstance(self.data.get(key), dict) and isinstance(value, dict):
                self.data[key].update(value)
            else:
                self.data[key] = value
        self.save()
        print(f"AI core memory updated with merged data.")

    def clear(self) -> None:
        """Clears all data from memory and saves an empty state."""
        self.data = {}
        self.save()
        print("AI core memory cleared.")

    def run(self, operation: str, **kwargs) -> Any:
        """
        Entry point for running operations on PersistentMemory.

        Args:
            operation (str): The operation to perform ('get', 'set', 'update', 'clear').
            **kwargs: Arguments for the operation.

        Returns:
            Any: The result of the operation.
        """
        if operation == "get":
            return self.get(kwargs.get("key"), kwargs.get("default"))
        elif operation == "set":
            self.set(kwargs.get("key"), kwargs.get("value"))
            return True
        elif operation == "update":
            self.update(kwargs.get("data", {}))
            return True
        elif operation == "clear":
            self.clear()
            return True
        else:
            print(f"Unsupported operation for PersistentMemory: {operation}")
            return None


class DynamicLogicProcessor:
    """
    Handles the execution of dynamic logic, potentially from loaded modules.
    This module acts as an interpreter or executor for various logic components.
    """

    def __init__(self, module_loader: Any, core_memory: PersistentMemory):
        """
        Initializes DynamicLogicProcessor.

        Args:
            module_loader (Any): An instance of a module loader that can load and run modules.
            core_memory (PersistentMemory): An instance of PersistentMemory to access core state.
        """
        self.module_loader = module_loader
        self.core_memory = core_memory
        # Initialize capabilities if they don't exist
        self.core_memory.data.setdefault("capabilities", [])

    def execute_logic(self, logic_identifier: str, *args, **kwargs) -> Any:
        """
        Executes logic based on its identifier. This could be a module name
        or a specific function within a module.

        Args:
            logic_identifier (str): The name of the module or a specific function path (e.g., "module_name.function_name").
            *args: Positional arguments to pass to the logic function.
            **kwargs: Keyword arguments to pass to the logic function.

        Returns:
            Any: The result of the logic execution.
        """
        module_name, *function_path = logic_identifier.split('.', 1)
        target_function_name = function_path[0] if function_path else 'run'

        # Check if the module is loaded
        if module_name not in self.module_loader.loaded_modules:
            print(f"Logic '{logic_identifier}' requires module '{module_name}', which is not loaded.")
            # Attempt to load the module if it's a known capability or available
            if module_name in self.module_loader.get_available_module_names():
                if self.module_loader._load_module_from_file(self.module_loader._module_path_to_name(module_name)): # This needs to be refactored to directly load by name if not file path
                    print(f"Attempted to load module '{module_name}' and succeeded.")
                else:
                    print(f"Failed to load module '{module_name}'.")
                    return None
            else:
                print(f"Module '{module_name}' is not available or cannot be loaded automatically.")
                return None

        module = self.module_loader.loaded_modules[module_name]

        # Dynamically get the target function
        if hasattr(module, target_function_name) and callable(getattr(module, target_function_name)):
            target_function = getattr(module, target_function_name)
            try:
                print(f"Executing logic: {logic_identifier} with args={args}, kwargs={kwargs}")
                result = target_function(*args, **kwargs)
                return result
            except Exception as e:
                print(f"Error executing '{logic_identifier}': {e}")
                return None
        else:
            print(f"Error: Logic component '{logic_identifier}' not found or not callable in module '{module_name}'.")
            return None

    def run(self, logic_identifier: str, *args, **kwargs) -> Any:
        """
        Alias for execute_logic, providing a standard 'run' entry point.

        Args:
            logic_identifier (str): The identifier for the logic to execute.
            *args: Positional arguments for the logic.
            **kwargs: Keyword arguments for the logic.

        Returns:
            Any: The result of the logic execution.
        """
        return self.execute_logic(logic_identifier, *args, **kwargs)
