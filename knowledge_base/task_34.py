import os
import json
import importlib
import sys

class PersistentMemory:
    """
    Manages persistent memory for the AI Core, storing data in a JSON file.
    """
    def __init__(self, filepath="memory.json"):
        self.filepath = filepath
        self.data = self._load_memory()

    def _load_memory(self):
        """Loads memory from the JSON file."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {self.filepath}. Starting with empty memory.")
                return {}
        return {}

    def _save_memory(self):
        """Saves current memory to the JSON file."""
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=4)

    def set(self, key, value):
        """Sets a key-value pair in memory."""
        self.data[key] = value
        self._save_memory()

    def get(self, key, default=None):
        """Gets a value from memory by key."""
        return self.data.get(key, default)

    def delete(self, key):
        """Deletes a key-value pair from memory."""
        if key in self.data:
            del self.data[key]
            self._save_memory()

    def list_keys(self):
        """Returns a list of all keys currently in memory."""
        return list(self.data.keys())

    def clear(self):
        """Clears all memory."""
        self.data = {}
        self._save_memory()

class DynamicLogicLoader:
    """
    Manages loading and unloading of dynamic logic modules.
    """
    def __init__(self, module_dir="logic_modules"):
        self.module_dir = module_dir
        self.loaded_modules = {}
        os.makedirs(self.module_dir, exist_ok=True)
        # Ensure the module directory is in Python's search path
        if self.module_dir not in sys.path:
            sys.path.insert(0, self.module_dir)

    def _get_module_name(self, filepath):
        """Converts a filepath to a Python module name."""
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        return base_name

    def load_module(self, module_name):
        """Loads a module if it's not already loaded."""
        if module_name not in self.loaded_modules:
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, 'process'):
                    self.loaded_modules[module_name] = module
                    print(f"Successfully loaded logic module: {module_name}")
                else:
                    print(f"Warning: Module '{module_name}' does not have a 'process' function. Skipping.")
            except ImportError:
                print(f"Error: Could not import module '{module_name}'. Make sure it's in the '{self.module_dir}' directory.")
            except Exception as e:
                print(f"An unexpected error occurred while loading module '{module_name}': {e}")
        return self.loaded_modules.get(module_name)

    def unload_module(self, module_name):
        """Unloads a module."""
        if module_name in self.loaded_modules:
            del self.loaded_modules[module_name]
            # In a more complex system, you might want to unregister from sys.modules
            # or handle other cleanup. For this example, simply removing from our cache is enough.
            print(f"Unloaded logic module: {module_name}")

    def get_loaded_module(self, module_name):
        """Returns a loaded module by name."""
        return self.loaded_modules.get(module_name)

    def discover_and_load_modules(self):
        """Discovers and loads all .py files in the module directory."""
        print(f"\nDiscovering and loading modules from '{self.module_dir}'...")
        for filename in os.listdir(self.module_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = self._get_module_name(filename)
                self.load_module(module_name)
        print("Module discovery complete.")


class AICore:
    """
    The central AI Core that orchestrates memory and dynamic logic.
    """
    def __init__(self, memory_filepath="memory.json", logic_module_dir="logic_modules"):
        self.memory = PersistentMemory(filepath=memory_filepath)
        self.logic_loader = DynamicLogicLoader(module_dir=logic_module_dir)
        self.logic_loader.discover_and_load_modules()

    def run(self, input_text: str) -> dict:
        """
        Processes an input text through the AI Core.
        It iterates through loaded logic modules, allowing them to respond.
        The first module that returns a non-None result dictates the core's output.
        A fallback module can be used for general responses.
        """
        context = {
            "input": input_text,
            "memory": self.memory,
            "core": self # Provide access to the core itself if needed by modules
        }

        response_data = None
        final_response_message = "I'm not sure how to respond to that." # Default fallback

        # Iterate through loaded modules to find a match
        for module_name, module in self.logic_loader.loaded_modules.items():
            try:
                result = module.process(context)
                if result:
                    response_data = result
                    # Prioritize specific messages from modules
                    if "message" in result:
                        final_response_message = result["message"]
                    elif "response" in result:
                        final_response_message = result["response"]
                    elif "echo" in result:
                        final_response_message = result["echo"]
                    else:
                        # If a module responded but didn't specify a message, use a generic one
                        final_response_message = f"Module '{module_name}' processed the input."
                    break # Stop processing once a module has responded
            except Exception as e:
                print(f"Error processing input with module '{module_name}': {e}")
                # Continue to try other modules if one fails

        # If no module returned a specific response, use a general fallback
        if response_data is None:
            # Consider a "simple_responder" as a last resort if it exists and is loaded
            simple_responder = self.logic_loader.get_loaded_module("simple_responder")
            if simple_responder:
                try:
                    result = simple_responder.process(context)
                    if result and "echo" in result:
                        final_response_message = result["echo"]
                        response_data = result
                    elif result and "response" in result:
                        final_response_message = result["response"]
                        response_data = result
                except Exception as e:
                    print(f"Error processing input with fallback module 'simple_responder': {e}")

        return {
            "input": input_text,
            "raw_response_data": response_data,
            "final_response": final_response_message,
            "memory_state_after": self.memory.data.copy()
        }

def create_dummy_logic_modules():
    """Creates dummy Python files in the logic_modules directory for demonstration."""
    os.makedirs("logic_modules", exist_ok=True)

    # greeting_module.py
    with open("logic_modules/greeting_module.py", "w") as f:
        f.write("""
def process(context):
    input_text = context.get("input", "").lower()
    memory = context.get("memory")

    if "hello" in input_text or "hi" in input_text:
        response = "Hello there! How can I help you today?"
        # Example of using memory within a module
        if memory:
            memory.set("last_interaction_type", "greeting")
            # Example of storing a response for later reference
            memory.set("last_greeting_response", response)
        return {"response": response, "module": "greeting_module"}
    elif "how are you" in input_text:
        response = "I am a program, so I don't have feelings, but I'm functioning well!"
        if memory:
            memory.set("last_interaction_type", "query_state")
        return {"response": response, "module": "greeting_module"}
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
                return {"action": "memory_set", "key": "remembered_item", "value": item_to_remember, "message": f"Okay, I'll remember '{item_to_remember}'.", "module": "task_executor"}
    elif "what did i ask you to remember" in input_text:
        if memory:
            remembered = memory.get("remembered_item")
            if remembered:
                return {"action": "memory_get", "key": "remembered_item", "value": remembered, "message": f"You asked me to remember: '{remembered}'.", "module": "task_executor"}
            else:
                return {"message": "You haven't asked me to remember anything yet.", "module": "task_executor"}
    return None # No specific task logic matched
""")

    # simple_responder.py - a fallback or general module
    with open("logic_modules/simple_responder.py", "w") as f:
        f.write("""
def process(context):
    input_text = context.get("input", "")
    # This module acts as a simple echo or fallback if no other module matches
    # It should have a lower priority or be explicitly called as a fallback.
    # For this demo, it will be tried if other modules don't respond.
    if input_text:
        # Only return an echo if the input is not empty, otherwise it might
        # interfere with modules that don't require input but expect an empty context.
        return {"echo": f"You said: {input_text}", "module": "simple_responder"}
    return None
""")

def run_demo():
    """
    Main function to run the AI Core demonstration.
    """
    # Clean up previous memory file for a fresh start if needed
    if os.path.exists("memory.json"):
        os.remove("memory.json")
        print("Removed existing memory.json for a fresh start.")

    create_dummy_logic_modules() # Ensure logic modules exist for the demo

    core = AICore()

    print("\n--- AI Core Demonstration ---")

    # Interaction 1: Greeting
    print("\n[User]: Hello!")
    result1 = core.run("Hello!")
    print(f"\nCore Output for Interaction 1: {result1['final_response']}")
    print(f"Module Used: {result1['raw_response_data'].get('module') if result1['raw_response_data'] else 'None'}")
    print(f"Memory Keys After Interaction 1: {core.memory.list_keys()}")
    print(f"Memory 'last_interaction_type': {core.memory.get('last_interaction_type')}")
    print(f"Memory 'last_greeting_response': {core.memory.get('last_greeting_response')}")


    # Interaction 2: Asking "how are you"
    print("\n[User]: How are you?")
    result2 = core.run("How are you?")
    print(f"\nCore Output for Interaction 2: {result2['final_response']}")
    print(f"Module Used: {result2['raw_response_data'].get('module') if result2['raw_response_data'] else 'None'}")
    print(f"Memory Keys After Interaction 2: {core.memory.list_keys()}") # 'last_interaction_type' should be updated
    print(f"Memory 'last_interaction_type': {core.memory.get('last_interaction_type')}")

    # Interaction 3: Asking to remember something
    print("\n[User]: Please remember my favorite color is blue.")
    result3 = core.run("Please remember my favorite color is blue.")
    print(f"\nCore Output for Interaction 3: {result3['final_response']}")
    print(f"Module Used: {result3['raw_response_data'].get('module') if result3['raw_response_data'] else 'None'}")
    print(f"Memory Keys After Interaction 3: {core.memory.list_keys()}")
    print(f"Memory 'remembered_item': {core.memory.get('remembered_item')}")

    # Interaction 4: Asking about the remembered item
    print("\n[User]: What did I ask you to remember?")
    result4 = core.run("What did I ask you to remember?")
    print(f"\nCore Output for Interaction 4: {result4['final_response']}")
    print(f"Module Used: {result4['raw_response_data'].get('module') if result4['raw_response_data'] else 'None'}")
    print(f"Memory Keys After Interaction 4: {core.memory.list_keys()}")

    # Interaction 5: Another greeting to show memory persistence and module loading
    print("\n[User]: Hi again!")
    result5 = core.run("Hi again!")
    print(f"\nCore Output for Interaction 5: {result5['final_response']}")
    print(f"Module Used: {result5['raw_response_data'].get('module') if result5['raw_response_data'] else 'None'}")
    print(f"Memory Keys After Interaction 5: {core.memory.list_keys()}")
    print(f"Memory 'last_greeting_response': {core.memory.get('last_greeting_response')}") # Should be updated

    # Interaction 6: Unmatched input to trigger fallback (simple_responder)
    print("\n[User]: This is an unknown query.")
    result6 = core.run("This is an unknown query.")
    print(f"\nCore Output for Interaction 6: {result6['final_response']}")
    print(f"Module Used: {result6['raw_response_data'].get('module') if result6['raw_response_data'] else 'None'}")
    print(f"Memory Keys After Interaction 6: {core.memory.list_keys()}")

    # Interaction 7: Another unknown query, but this time simple_responder is deleted to show no fallback
    print("\n[User]: Another query to test without fallback.")
    core.logic_loader.unload_module("simple_responder")
    print("Unloaded 'simple_responder' module.")
    result7 = core.run("Another query to test without fallback.")
    print(f"\nCore Output for Interaction 7: {result7['final_response']}")
    print(f"Module Used: {result7['raw_response_data'].get('module') if result7['raw_response_data'] else 'None'}")
    print(f"Memory Keys After Interaction 7: {core.memory.list_keys()}")


    print("\n--- Demonstration Complete ---")
    print("Persistent memory is stored in 'memory.json'.")
    print("Dynamic logic modules are in the 'logic_modules' directory.")
    print("You can add or modify Python files in 'logic_modules' to change AI behavior.")

if __name__ == "__main__":
    run_demo()
