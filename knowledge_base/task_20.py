import json
import os
import importlib
from collections import deque

class PersistentMemory:
    """
    A simple persistent memory system that stores and retrieves data from a file.
    """
    def __init__(self, filepath="memory.json"):
        self.filepath = filepath
        self.data = self._load_memory()

    def _load_memory(self):
        """Loads data from the specified file."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted or unreadable, start with empty memory
                return {}
        else:
            return {}

    def _save_memory(self):
        """Saves the current data to the specified file."""
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            print(f"Error saving memory: {e}")

    def get(self, key, default=None):
        """Retrieves a value from memory by key."""
        return self.data.get(key, default)

    def set(self, key, value):
        """Sets or updates a value in memory."""
        self.data[key] = value
        self._save_memory()

    def delete(self, key):
        """Deletes a key-value pair from memory."""
        if key in self.data:
            del self.data[key]
            self._save_memory()

    def list_keys(self):
        """Returns a list of all keys in memory."""
        return list(self.data.keys())

class DynamicLogicProcessor:
    """
    Processes dynamic logic modules, allowing for flexible rule execution.
    """
    def __init__(self, logic_directory="logic_modules"):
        self.logic_directory = logic_directory
        self.loaded_modules = {}
        self._ensure_logic_directory_exists()
        self._load_all_modules()

    def _ensure_logic_directory_exists(self):
        """Creates the logic directory if it doesn't exist."""
        if not os.path.exists(self.logic_directory):
            os.makedirs(self.logic_directory)
            # Create a placeholder if directory is new
            with open(os.path.join(self.logic_directory, "__init__.py"), "w") as f:
                pass

    def _load_module(self, module_name):
        """Loads a single logic module from the specified directory."""
        try:
            # Construct the module path
            module_path = f"{self.logic_directory}.{module_name}"
            module = importlib.import_module(module_path)
            self.loaded_modules[module_name] = module
            print(f"Loaded logic module: {module_name}")
        except ImportError as e:
            print(f"Could not load logic module '{module_name}': {e}")
        except Exception as e:
            print(f"An unexpected error occurred loading module '{module_name}': {e}")

    def _load_all_modules(self):
        """Scans the logic directory and loads all available modules."""
        for item_name in os.listdir(self.logic_directory):
            if item_name.endswith(".py") and not item_name.startswith("__"):
                module_name = item_name[:-3]  # Remove .py extension
                self._load_module(module_name)

    def reload_module(self, module_name):
        """Reloads a specific logic module."""
        if module_name in self.loaded_modules:
            try:
                importlib.reload(self.loaded_modules[module_name])
                print(f"Reloaded logic module: {module_name}")
            except Exception as e:
                print(f"Error reloading module '{module_name}': {e}")
        else:
            print(f"Module '{module_name}' not found for reloading.")

    def process(self, input_data, context=None):
        """
        Processes the input data against all loaded logic modules.
        Each module is expected to have a 'process' function.
        """
        results = []
        for module_name, module in self.loaded_modules.items():
            if hasattr(module, 'process'):
                try:
                    # Pass memory and input data to the logic module
                    module_context = {
                        "memory": context.get("memory") if context else None,
                        "input": input_data
                    }
                    if context:
                        module_context.update(context) # Include any additional context

                    output = module.process(module_context)
                    if output is not None:
                        results.append({"module": module_name, "output": output})
                except Exception as e:
                    print(f"Error processing with module '{module_name}': {e}")
            else:
                print(f"Module '{module_name}' does not have a 'process' function.")
        return results

class AICore:
    """
    The main AI Core, orchestrating memory and dynamic logic.
    """
    def __init__(self, memory_filepath="memory.json", logic_directory="logic_modules"):
        self.memory = PersistentMemory(filepath=memory_filepath)
        self.logic_processor = DynamicLogicProcessor(logic_directory=logic_directory)

    def run(self, input_data, context=None):
        """
        The main execution loop for the AI Core.
        Processes input_data using dynamic logic and updates memory.
        """
        print(f"AI Core received input: {input_data}")

        # Prepare context for the logic processor
        current_context = {
            "memory": self.memory,
            "input": input_data
        }
        if context:
            current_context.update(context)

        # Process input through dynamic logic
        logic_results = self.logic_processor.process(input_data, context=current_context)

        print("Logic processing results:")
        for result in logic_results:
            print(f"  - {result['module']}: {result['output']}")
            # Example: Update memory based on some logic results
            # This is a simplified example, real AI would have more sophisticated logic
            if result['module'] == "greetings_handler": # Assuming such a module exists
                if isinstance(result['output'], dict) and "response" in result['output']:
                    self.memory.set("last_greeting_response", result['output']['response'])

        # Return results and updated context (optional)
        return {
            "logic_results": logic_results,
            "memory_state": self.memory.data # For inspection
        }

# --- Example Usage ---

# Create dummy logic modules for demonstration
def create_dummy_logic_modules():
    if not os.path.exists("logic_modules"):
        os.makedirs("logic_modules")

    # greetings_handler.py
    with open("logic_modules/greetings_handler.py", "w") as f:
        f.write("""
def process(context):
    input_text = context.get("input", "").lower()
    memory = context.get("memory")

    if "hello" in input_text or "hi" in input_text:
        response = "Hello there! How can I help you today?"
        # Example of using memory within a module
        if memory:
            memory.set("last_interaction_type", "greeting")
        return {"response": response}
    elif "how are you" in input_text:
        return {"response": "I am a program, so I don't have feelings, but I'm functioning well!"}
    return None # No specific greeting logic matched
""")

    # task_executor.py
    with open("logic_modules/task_executor.py", "w") as f:
        f.write("""
def process(context):
    input_text = context.get("input", "").lower()
    memory = context.get("memory")

    if "remember" in input_text:
        parts = input_text.split("remember ", 1)
        if len(parts) > 1:
            item_to_remember = parts[1].strip()
            if memory:
                memory.set("remembered_item", item_to_remember)
                return {"action": "memory_set", "key": "remembered_item", "value": item_to_remember, "message": f"Okay, I'll remember '{item_to_remember}'."}
    elif "what did i ask you to remember" in input_text:
        if memory:
            remembered = memory.get("remembered_item")
            if remembered:
                return {"action": "memory_get", "key": "remembered_item", "value": remembered, "message": f"You asked me to remember: '{remembered}'."}
            else:
                return {"message": "You haven't asked me to remember anything yet."}
    return None # No specific task logic matched
""")

def run_ai_demo():
    """
    Demonstrates the AI Core's functionality.
    """
    create_dummy_logic_modules() # Ensure logic modules exist for the demo

    core = AICore()

    print("\n--- AI Core Demo ---")

    # Interaction 1: Greeting
    print("\n[User]: Hello!")
    result1 = core.run("Hello!")
    print(f"Memory Keys After Interaction 1: {core.memory.list_keys()}")
    print(f"Memory 'last_interaction_type': {core.memory.get('last_interaction_type')}")

    # Interaction 2: Asking "how are you"
    print("\n[User]: How are you?")
    result2 = core.run("How are you?")
    print(f"Memory Keys After Interaction 2: {core.memory.list_keys()}")

    # Interaction 3: Asking to remember something
    print("\n[User]: Please remember my favorite color is blue.")
    result3 = core.run("Please remember my favorite color is blue.")
    print(f"Memory Keys After Interaction 3: {core.memory.list_keys()}")
    print(f"Memory 'remembered_item': {core.memory.get('remembered_item')}")
    print(f"Memory 'last_interaction_type': {core.memory.get('last_interaction_type')}") # Should be None from this interaction

    # Interaction 4: Asking about the remembered item
    print("\n[User]: What did I ask you to remember?")
    result4 = core.run("What did I ask you to remember?")
    print(f"Memory Keys After Interaction 4: {core.memory.list_keys()}")

    # Interaction 5: Another greeting to show memory persistence
    print("\n[User]: Hi again!")
    result5 = core.run("Hi again!")
    print(f"Memory Keys After Interaction 5: {core.memory.list_keys()}")
    print(f"Memory 'last_greeting_response': {core.memory.get('last_greeting_response')}")

    print("\n--- Demo End ---")
    print("Check 'memory.json' to see the persistent storage.")
    print("Check the 'logic_modules' directory for dynamic logic.")

if __name__ == "__main__":
    run_ai_demo()
