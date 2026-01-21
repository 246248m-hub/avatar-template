import os
import importlib
import json
from typing import Dict, Any, Optional, List

# --- Persistent Memory ---

class PersistentMemory:
    """Manages persistent storage for the AI core using a JSON file."""
    def __init__(self, filename: str = "memory.json"):
        self.filename = filename
        self.data = self._load_memory()

    def _load_memory(self) -> Dict[str, Any]:
        """Loads memory from the JSON file. Creates if it doesn't exist."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted or empty, start with fresh memory
                return {}
        return {}

    def _save_memory(self) -> None:
        """Saves the current memory to the JSON file."""
        try:
            with open(self.filename, "w") as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            print(f"Error saving memory to {self.filename}: {e}")

    def set(self, key: str, value: Any) -> None:
        """Sets a key-value pair in memory."""
        self.data[key] = value
        self._save_memory()

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """Gets the value associated with a key. Returns default if key not found."""
        return self.data.get(key, default)

    def delete(self, key: str) -> None:
        """Deletes a key-value pair from memory."""
        if key in self.data:
            del self.data[key]
            self._save_memory()

    def list_keys(self) -> List[str]:
        """Returns a list of all keys currently in memory."""
        return list(self.data.keys())

    def clear(self) -> None:
        """Clears all memory."""
        self.data = {}
        self._save_memory()

# --- Dynamic Logic Loading ---

class LogicLoader:
    """Manages loading, unloading, and executing dynamic logic modules."""
    def __init__(self, module_dir: str = "logic_modules"):
        self.module_dir = module_dir
        self.loaded_modules: Dict[str, Any] = {}
        self.module_paths: Dict[str, str] = {} # Map module name to its file path
        self._ensure_module_dir()
        self._load_initial_modules()

    def _ensure_module_dir(self) -> None:
        """Ensures the directory for logic modules exists."""
        if not os.path.exists(self.module_dir):
            os.makedirs(self.module_dir)
            print(f"Created module directory: {self.module_dir}")

    def _load_initial_modules(self) -> None:
        """Loads all .py files from the module directory upon initialization."""
        print(f"Scanning for logic modules in: {self.module_dir}")
        for filename in os.listdir(self.module_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3] # Remove .py extension
                self.load_module(module_name)

    def get_module_path(self, module_name: str) -> str:
        """Constructs the expected file path for a module."""
        return os.path.join(self.module_dir, f"{module_name}.py")

    def load_module(self, module_name: str) -> bool:
        """
        Loads a Python module from the specified directory.
        Expects modules to have a 'process(context)' function.
        """
        module_path = self.get_module_path(module_name)
        if not os.path.exists(module_path):
            print(f"Module file not found: {module_path}")
            return False

        try:
            # Dynamically import the module
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Check if the module has the required 'process' function
            if not hasattr(module, "process") or not callable(module.process):
                print(f"Module '{module_name}' does not have a callable 'process' function.")
                return False

            self.loaded_modules[module_name] = module
            self.module_paths[module_name] = module_path
            print(f"Loaded logic module: '{module_name}' from {module_path}")
            return True
        except Exception as e:
            print(f"Error loading module '{module_name}' from {module_path}: {e}")
            return False

    def unload_module(self, module_name: str) -> bool:
        """Unloads a previously loaded module."""
        if module_name in self.loaded_modules:
            del self.loaded_modules[module_name]
            if module_name in self.module_paths:
                del self.module_paths[module_name]
            print(f"Unloaded logic module: '{module_name}'")
            return True
        else:
            print(f"Module '{module_name}' was not loaded.")
            return False

    def get_loaded_module_names(self) -> List[str]:
        """Returns a list of names of all currently loaded modules."""
        return list(self.loaded_modules.keys())

    def list_available_module_files(self) -> List[str]:
        """Lists all Python files in the module directory that could be loaded."""
        files = []
        for filename in os.listdir(self.module_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                files.append(filename[:-3]) # Return module name
        return files

    def execute_module(self, module_name: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Executes the 'process' function of a specific loaded module.
        Returns the module's output or None if the module is not loaded or fails.
        """
        if module_name in self.loaded_modules:
            try:
                module = self.loaded_modules[module_name]
                result = module.process(context)
                if result is not None:
                    # Ensure the module returns a dict for consistency
                    if not isinstance(result, dict):
                        print(f"Warning: Module '{module_name}' returned non-dict type: {type(result)}")
                        return {"error": "Module returned invalid format"}
                    # Add module name to its output for tracking
                    if "module" not in result:
                        result["module"] = module_name
                return result
            except Exception as e:
                print(f"Error executing module '{module_name}': {e}")
                return {"error": f"Execution error in module {module_name}"}
        else:
            print(f"Module '{module_name}' is not loaded.")
            return None

# --- AI Core ---

class AICore:
    """
    The central AI engine, combining persistent memory and dynamic logic.
    It orchestrates the loading of modules and processes user input.
    """
    def __init__(self, memory_file: str = "memory.json", module_dir: str = "logic_modules"):
        self.memory = PersistentMemory(filename=memory_file)
        self.logic_loader = LogicLoader(module_dir=module_dir)
        # A fallback module that is always available if nothing else matches
        self.fallback_module_name = "simple_responder"
        self._ensure_fallback_module()

    def _ensure_fallback_module(self) -> None:
        """Ensures the simple_responder module exists for fallback."""
        fallback_path = self.logic_loader.get_module_path(self.fallback_module_name)
        if not os.path.exists(fallback_path):
            print(f"Ensuring fallback module '{self.fallback_module_name}' exists.")
            try:
                with open(fallback_path, "w") as f:
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
                self.logic_loader.load_module(self.fallback_module_name)
            except IOError as e:
                print(f"Error creating fallback module: {e}")

    def _get_module_processing_order(self) -> List[str]:
        """
        Determines the order in which modules should be considered.
        In this basic implementation, it's alphabetical, but could be more complex (e.g., based on priority).
        The fallback module is always tried last.
        """
        module_names = sorted(self.logic_loader.get_loaded_module_names())
        # Move fallback module to the end if it's present
        if self.fallback_module_name in module_names:
            module_names.remove(self.fallback_module_name)
            module_names.append(self.fallback_module_name)
        return module_names

    def run(self, user_input: str) -> Dict[str, Any]:
        """
        Processes user input, attempting to match it with loaded logic modules.
        """
        context = {
            "input": user_input,
            "memory": self.memory, # Provide memory object to modules
            "loaded_modules": self.logic_loader.get_loaded_module_names() # List of available modules
        }

        processing_order = self._get_module_processing_order()
        raw_response_data = None
        final_response = "I don't understand." # Default response

        # Iterate through modules in the determined order
        for module_name in processing_order:
            # Ensure module is still loaded before attempting execution
            if module_name not in self.logic_loader.loaded_modules:
                continue

            # Execute the module
            module_output = self.logic_loader.execute_module(module_name, context)

            # If a module returns a valid, non-None response, we consider it handled
            if module_output is not None and not module_output.get("error"):
                raw_response_data = module_output
                # Construct final response based on module output
                if "response" in module_output:
                    final_response = module_output["response"]
                elif "echo" in module_output:
                    final_response = module_output["echo"]
                elif "message" in module_output:
                    final_response = module_output["message"]
                elif "data" in module_output: # If module just stores data, provide a generic confirmation
                    final_response = f"Understood. (Module: {module_name})"

                # If a module successfully processed, stop trying other modules
                break

        # Update memory with interaction context if a module responded
        if raw_response_data:
            self.memory.set("last_interaction_type", raw_response_data.get("module"))
            # Modules can set specific memory items, e.g., 'last_greeting_response'
            if "last_greeting_response" in raw_response_data:
                self.memory.set("last_greeting_response", raw_response_data["last_greeting_response"])
            if "remembered_item" in raw_response_data:
                self.memory.set("remembered_item", raw_response_data["remembered_item"])

        return {
            "final_response": final_response,
            "raw_response_data": raw_response_data,
            "module_used": raw_response_data.get("module") if raw_response_data else None
        }

# --- Dummy Module Creation ---

def create_dummy_logic_modules():
    """Creates some initial dummy logic modules for demonstration."""
    os.makedirs("logic_modules", exist_ok=True)

    # greetings.py
    with open("logic_modules/greetings.py", "w") as f:
        f.write("""
def process(context):
    input_text = context.get("input", "").lower()
    memory = context.get("memory")

    if "hello" in input_text or "hi" in input_text:
        response = "Hello there!"
        if memory:
            memory.set("last_greeting_response", response)
        return {"response": response, "module": "greetings", "last_greeting_response": response}
    elif "how are you" in input_text:
        response = "I'm a humble AI, always ready to help."
        if memory:
            memory.set("last_interaction_type", "greeting_status")
        return {"response": response, "module": "greetings", "last_interaction_type": "greeting_status"}
    return None
""")

    # memory_manager.py
    with open("logic_modules/memory_manager.py", "w") as f:
        f.write("""
import re

def process(context):
    input_text = context.get("input", "")
    memory = context.get("memory")

    # Pattern to capture "remember X is Y" or "remember X"
    match_remember = re.search(r"remember my (.*) is (.*)", input_text, re.IGNORECASE)
    if match_remember:
        key = match_remember.group(1).strip()
        value = match_remember.group(2).strip()
        if memory:
            memory.set(key, value)
        return {"response": f"Okay, I'll remember that your {key} is {value}.", "module": "memory_manager", "remembered_item": {key: value}}

    match_remember_simple = re.search(r"remember (.*)", input_text, re.IGNORECASE)
    if match_remember_simple:
        value_to_remember = match_remember_simple.group(1).strip()
        if memory:
            memory.set("remembered_item", value_to_remember) # Use a general key for simple remembers
        return {"response": f"Got it, I've remembered: {value_to_remember}", "module": "memory_manager", "remembered_item": value_to_remember}

    match_recall = re.search(r"what did i ask you to remember\??", input_text, re.IGNORECASE)
    if match_recall:
        if memory:
            remembered = memory.get("remembered_item")
            if remembered:
                return {"response": f"You asked me to remember: {remembered}", "module": "memory_manager"}
            else:
                return {"response": "You haven't asked me to remember anything yet.", "module": "memory_manager"}
    
    # Recall specific keys
    match_recall_specific = re.search(r"what is my (.*)\??", input_text, re.IGNORECASE)
    if match_recall_specific:
        key_to_recall = match_recall_specific.group(1).strip()
        if memory:
            value = memory.get(key_to_recall)
            if value is not None:
                return {"response": f"Your {key_to_recall} is: {value}", "module": "memory_manager"}
            else:
                return {"response": f"I don't remember your {key_to_recall}.", "module": "memory_manager"}

    return None # No specific memory operation matched
""")

    # simple_responder.py (already created in the demo setup, but good to ensure it's defined here)
    fallback_module_path = "logic_modules/simple_responder.py"
    if not os.path.exists(fallback_module_path):
        with open(fallback_module_path, "w") as f:
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

# --- Main Demonstration Function ---

import os # Ensure os is imported for the demo function

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
    print(f"Memory 'remembered_item': {core.memory.get('remembered_item')}") # This will store the entire dict if key exists, or the string
    print(f"Memory 'favorite color': {core.memory.get('favorite color')}") # Specific key retrieval


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
