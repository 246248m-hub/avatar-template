import os
import json
from typing import Any, Dict, List

class CoreMemory:
    """
    Persistent memory for the AI core.
    Manages storing and retrieving core data.
    """
    def __init__(self, filepath: str = "core_memory.json"):
        self.filepath = filepath
        self.data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        """Loads data from the JSON file."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {self.filepath}. Starting with empty memory.")
                return {}
            except IOError as e:
                print(f"Error loading core memory from {self.filepath}: {e}. Starting with empty memory.")
                return {}
        return {}

    def save(self) -> None:
        """Saves the current data to the JSON file."""
        try:
            with open(self.filepath, "w") as f:
                json.dump(self.data, f, indent=4)
            print(f"Core memory saved to {self.filepath}")
        except IOError as e:
            print(f"Error saving core memory to {self.filepath}: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a value from memory."""
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Sets a value in memory."""
        self.data[key] = value
        self.save()

    def add_to_list(self, key: str, item: Any) -> None:
        """Adds an item to a list in memory, creating the list if it doesn't exist."""
        if key not in self.data:
            self.data[key] = []
        if not isinstance(self.data[key], list):
            print(f"Warning: Key '{key}' in memory is not a list. Overwriting with a new list.")
            self.data[key] = []
        if item not in self.data[key]:
            self.data[key].append(item)
            self.save()
        else:
            print(f"Item '{item}' already exists in list '{key}'.")

    def remove_from_list(self, key: str, item: Any) -> None:
        """Removes an item from a list in memory."""
        if key in self.data and isinstance(self.data[key], list):
            if item in self.data[key]:
                self.data[key].remove(item)
                self.save()
            else:
                print(f"Item '{item}' not found in list '{key}'.")
        else:
            print(f"Key '{key}' not found or is not a list in memory.")

    def clear_key(self, key: str) -> None:
        """Removes a key-value pair from memory."""
        if key in self.data:
            del self.data[key]
            self.save()
        else:
            print(f"Key '{key}' not found in memory.")

    def get_all(self) -> Dict[str, Any]:
        """Returns all data from memory."""
        return self.data.copy()


# --- Testing Section (for standalone execution) ---
if __name__ == "__main__":
    print("--- Testing CoreMemory ---")

    # Clean up any existing memory file from previous runs
    if os.path.exists("core_memory.json"):
        os.remove("core_memory.json")
        print("Removed existing core_memory.json")

    memory = CoreMemory()

    print("\nInitial memory state:", memory.get_all())

    # Test setting and getting values
    memory.set("ai_name", "PhoenixAI")
    memory.set("version", "0.1.0")
    print("Memory after setting 'ai_name' and 'version':", memory.get_all())

    print(f"AI Name: {memory.get('ai_name')}")
    print(f"Version: {memory.get('version')}")
    print(f"Non-existent key: {memory.get('non_existent', 'default_value')}")

    # Test list operations
    memory.add_to_list("capabilities", "module_loader_v1")
    memory.add_to_list("capabilities", "core_memory_v1")
    memory.add_to_list("capabilities", "module_loader_v1") # Test adding duplicate
    print("Memory after adding capabilities:", memory.get_all())

    print(f"Capabilities: {memory.get('capabilities')}")

    memory.remove_from_list("capabilities", "core_memory_v1")
    print("Memory after removing 'core_memory_v1':", memory.get_all())

    memory.remove_from_list("capabilities", "non_existent_capability") # Test removing non-existent

    # Test clearing a key
    memory.clear_key("version")
    print("Memory after clearing 'version':", memory.get_all())

    memory.clear_key("non_existent_key") # Test clearing non-existent key

    # Test overwriting a non-list with a list
    memory.set("my_setting", "initial_value")
    print("Memory before list overwrite:", memory.get_all())
    memory.add_to_list("my_setting", "new_item")
    print("Memory after overwriting non-list with list:", memory.get_all())

    # Test loading from an existing file (simulate by creating one)
    print("\n--- Simulating loading from existing file ---")
    existing_memory_data = {
        "ai_name": "SimulatedAI",
        "loaded_modules": ["task_a", "task_b"],
        "config": {"log_level": "INFO"}
    }
    with open("core_memory.json", "w") as f:
        json.dump(existing_memory_data, f, indent=4)
    print("Created dummy core_memory.json")

    new_memory_instance = CoreMemory()
    print("Memory loaded from dummy file:", new_memory_instance.get_all())

    # Clean up the dummy memory file
    if os.path.exists("core_memory.json"):
        os.remove("core_memory.json")
        print("Cleaned up dummy core_memory.json")

    print("\n--- CoreMemory Testing Complete ---")
