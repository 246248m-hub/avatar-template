import os
import json
import bz2
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, Callable, List

class MemoryManager:
    """Manages persistent memory for the AI Core."""

    def __init__(self, memory_file: str = "memory.json"):
        self.memory_file = memory_file
        self.memory: Dict[str, Any] = self._load_memory()

    def _load_memory(self) -> Dict[str, Any]:
        """Loads memory from the JSON file."""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def save_memory(self):
        """Saves the current memory to the JSON file."""
        with open(self.memory_file, "w") as f:
            json.dump(self.memory, f, indent=4)

    def set(self, key: str, value: Any):
        """Sets a value in memory."""
        self.memory[key] = value
        self.save_memory()

    def get(self, key: str, default: Any = None) -> Any:
        """Gets a value from memory, returning default if not found."""
        return self.memory.get(key, default)

    def delete(self, key: str):
        """Deletes a key from memory."""
        if key in self.memory:
            del self.memory[key]
            self.save_memory()

    def list_keys(self) -> List[str]:
        """Returns a list of all keys in memory."""
        return list(self.memory.keys())

class LogicLoader:
    """Dynamically loads and manages logic modules."""

    def __init__(self, module_dir: str = "logic_modules"):
        self.module_dir = module_dir
        self.loaded_modules: Dict[str, Callable] = {}
        self._ensure_module_dir()
        self._load_initial_modules()

    def _ensure_module_dir(self):
        """Ensures the module directory exists."""
        if not os.path.exists(self.module_dir):
            os.makedirs(self.module_dir)
            print(f"Created module directory: {self.module_dir}")

    def _load_module_from_file(self, module_name: str, filepath: str) -> Optional[Callable]:
        """Loads a callable function from a Python file."""
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # Assuming each module exposes a function with the same name as the module
            if hasattr(module, module_name) and callable(getattr(module, module_name)):
                return getattr(module, module_name)
            else:
                print(f"Warning: Module '{module_name}' in '{filepath}' does not expose a callable function named '{module_name}'.")
                return None
        except Exception as e:
            print(f"Error loading module '{module_name}' from '{filepath}': {e}")
            return None

    def _load_initial_modules(self):
        """Loads modules from the module directory on initialization."""
        if not os.path.exists(self.module_dir):
            return
        for filename in os.listdir(self.module_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]  # Remove .py extension
                filepath = os.path.join(self.module_dir, filename)
                loaded_func = self._load_module_from_file(module_name, filepath)
                if loaded_func:
                    self.loaded_modules[module_name] = loaded_func
                    print(f"Loaded module: {module_name}")

    def load_module(self, module_name: str, module_path: str) -> bool:
        """Loads a module from a specific path."""
        if module_name in self.loaded_modules:
            print(f"Module '{module_name}' is already loaded.")
            return False
        loaded_func = self._load_module_from_file(module_name, module_path)
        if loaded_func:
            self.loaded_modules[module_name] = loaded_func
            print(f"Successfully loaded module '{module_name}' from {module_path}")
            return True
        return False

    def unload_module(self, module_name: str) -> bool:
        """Unloads a module by its name."""
        if module_name in self.loaded_modules:
            del self.loaded_modules[module_name]
            print(f"Unloaded module: {module_name}")
            return True
        print(f"Module '{module_name}' not found or not loaded.")
        return False

    def get_module(self, module_name: str) -> Optional[Callable]:
        """Returns a loaded module function by its name."""
        return self.loaded_modules.get(module_name)

    def list_loaded_modules(self) -> List[str]:
        """Returns a list of names of currently loaded modules."""
        return list(self.loaded_modules.keys())

class AICore:
    """The main AI Core that orchestrates logic modules and memory."""

    def __init__(self, memory_file: str = "memory.json", module_dir: str = "logic_modules"):
        self.memory = MemoryManager(memory_file)
        self.logic_loader = LogicLoader(module_dir)
        self.module_priority: List[str] = [] # Order of module execution

    def add_module_to_priority(self, module_name: str, position: int = -1):
        """
        Adds a module to the execution priority list.
        position: -1 to append, 0 for the beginning, positive integer for specific index.
        """
        if module_name not in self.logic_loader.list_loaded_modules():
            print(f"Error: Module '{module_name}' is not loaded. Cannot add to priority.")
            return

        if position == -1:
            if module_name not in self.module_priority:
                self.module_priority.append(module_name)
        elif position == 0:
            if module_name not in self.module_priority:
                self.module_priority.insert(0, module_name)
        else:
            if module_name not in self.module_priority:
                self.module_priority.insert(position, module_name)
            else:
                # If already exists, move it to the new position
                self.module_priority.remove(module_name)
                self.module_priority.insert(position, module_name)
        print(f"Module '{module_name}' added/moved to priority at position {position if position != -1 else len(self.module_priority)-1}.")


    def run(self, input_text: str) -> Dict[str, Any]:
        """
        Processes user input, delegates to logic modules based on priority,
        and returns the final response.
        """
        raw_response_data = None
        final_response = "I'm not sure how to respond to that."

        # Iterate through modules based on priority
        for module_name in self.module_priority:
            module_func = self.logic_loader.get_module(module_name)
            if module_func:
                try:
                    # Modules are expected to accept input_text and return a dict
                    # with 'response' and potentially other data.
                    # They can also return None to indicate they didn't handle the input.
                    response = module_func(input_text, self.memory)
                    if response is not None and response.get("response"):
                        raw_response_data = response
                        final_response = response["response"]
                        # Update memory with any relevant keys from the module's response
                        for key, value in response.items():
                            if key != "response":
                                self.memory.set(key, value)
                        break # Stop processing if a module responded
                except Exception as e:
                    print(f"Error executing module '{module_name}': {e}")
                    # Continue to the next module in case of an error

        # Fallback mechanism if no module responded
        if raw_response_data is None and "simple_responder" in self.logic_loader.list_loaded_modules():
            simple_responder = self.logic_loader.get_module("simple_responder")
            if simple_responder:
                try:
                    response = simple_responder(input_text, self.memory)
                    if response is not None and response.get("response"):
                        raw_response_data = response
                        final_response = response["response"]
                        for key, value in response.items():
                            if key != "response":
                                self.memory.set(key, value)
                except Exception as e:
                    print(f"Error executing fallback module 'simple_responder': {e}")


        # General memory update for context if no specific module handled it
        if raw_response_data is None:
            self.memory.set("last_unhandled_input", input_text)
            self.memory.set("last_interaction_type", "unhandled")
        else:
            self.memory.set("last_interaction_type", raw_response_data.get("module", "unknown")) # Store the module that responded

        return {
            "final_response": final_response,
            "raw_response_data": raw_response_data if raw_response_data else {}
        }

# --- Utility Functions ---

def download_and_decompress_xml(url: str, output_path: str):
    """
    Downloads a bz2 compressed XML file from a URL and decompresses it.
    """
    try:
        import requests
        print(f"Downloading from {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status() # Raise an exception for bad status codes

        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192 # 8KB
        downloaded_size = 0

        with bz2.BZ2File(output_path.replace('.bz2', '.xml'), 'wb') as f_out:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk: # filter out keep-alive new chunks
                    f_out.write(chunk)
                    downloaded_size += len(chunk)
                    if total_size > 0:
                        progress = (downloaded_size / total_size) * 100
                        print(f"Downloaded: {downloaded_size}/{total_size} bytes ({progress:.2f}%)", end='\r')
        print("\nDownload complete.")

        print(f"Decompressing {output_path.replace('.bz2', '.xml')}...")
        # The above code directly writes decompressed data using bz2.BZ2File in write mode.
        # If the intent was to download a .bz2 file *first*, then decompress it:
        # with open(output_path, 'wb') as f_download:
        #     for chunk in response.iter_content(chunk_size=block_size):
        #         if chunk:
        #             f_download.write(chunk)
        #             downloaded_size += len(chunk)
        #             if total_size > 0:
        #                 progress = (downloaded_size / total_size) * 100
        #                 print(f"Downloaded: {downloaded_size}/{total_size} bytes ({progress:.2f}%)", end='\r')
        # print("\nDownload complete.")
        #
        # print(f"Decompressing {output_path}...")
        # with bz2.BZ2File(output_path, 'rb') as f_in, open(output_path.replace('.bz2', '.xml'), 'wb') as f_out:
        #     for chunk in f_in:
        #         f_out.write(chunk)
        # print("Decompression complete.")

        print(f"Successfully downloaded and decompressed to {output_path.replace('.bz2', '.xml')}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
    except IOError as e:
        print(f"Error writing decompressed file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# --- Dummy Logic Module Creation for Demonstration ---

def create_dummy_logic_modules():
    """Creates dummy Python files in the logic_modules directory for demonstration."""
    logic_modules_dir = "logic_modules"
    os.makedirs(logic_modules_dir, exist_ok=True)

    # Greeting Module
    greeting_module_content = """
def greeting(input_text: str, memory: MemoryManager) -> dict:
    if input_text.lower() in ["hello", "hi", "hey", "greetings"]:
        response_text = "Hello there! How can I assist you today?"
        memory.set("last_greeting_response", response_text)
        return {"response": response_text, "module": "greeting"}
    return None
"""
    with open(os.path.join(logic_modules_dir, "greeting.py"), "w") as f:
        f.write(greeting_module_content)

    # HowAreYou Module
    how_are_you_module_content = """
def how_are_you(input_text: str, memory: MemoryManager) -> dict:
    if input_text.lower() == "how are you":
        response_text = "I'm an AI, so I don't have feelings, but I'm functioning optimally! How about you?"
        memory.set("last_interaction_type", "query_state")
        memory.set("last_how_are_you_response", response_text)
        return {"response": response_text, "module": "how_are_you"}
    return None
"""
    with open(os.path.join(logic_modules_dir, "how_are_you.py"), "w") as f:
        f.write(how_are_you_module_content)

    # Remember Module
    remember_module_content = """
def remember(input_text: str, memory: MemoryManager) -> dict:
    if input_text.lower().startswith("please remember my favorite color is "):
        color = input_text.split("please remember my favorite color is ")[1].strip().rstrip('.')
        memory.set("favorite_color", color)
        memory.set("last_remembered_item", {"type": "favorite_color", "value": color})
        return {"response": f"Okay, I'll remember your favorite color is {color}.", "module": "remember", "remembered_key": "favorite_color", "remembered_value": color}
    elif input_text.lower().startswith("please remember that "):
        parts = input_text.lower().split("please remember that ", 1)[1].split(" is ", 1)
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip().rstrip('.')
            memory.set(key, value)
            memory.set("last_remembered_item", {"type": key, "value": value})
            return {"response": f"Okay, I'll remember that {key} is {value}.", "module": "remember", "remembered_key": key, "remembered_value": value}
    return None
"""
    with open(os.path.join(logic_modules_dir, "remember.py"), "w") as f:
        f.write(remember_module_content)

    # Recall Module
    recall_module_content = """
def recall(input_text: str, memory: MemoryManager) -> dict:
    if input_text.lower() == "what did i ask you to remember?":
        last_item = memory.get("last_remembered_item")
        if last_item:
            return {"response": f"You asked me to remember that your {last_item['type']} is {last_item['value']}.", "module": "recall"}
        else:
            return {"response": "You haven't asked me to remember anything specific yet.", "module": "recall"}
    elif input_text.lower().startswith("what is my ") and input_text.lower().endswith("?"):
        key_to_recall = input_text.lower().split("what is my ")[1].split("?")[0].strip()
        if key_to_recall == "favorite color":
            color = memory.get("favorite_color")
            if color:
                return {"response": f"Your favorite color is {color}.", "module": "recall"}
            else:
                return {"response": "I don't remember your favorite color.", "module": "recall"}
        else:
            value = memory.get(key_to_recall)
            if value:
                return {"response": f"You told me that {key_to_recall} is {value}.", "module": "recall"}
            else:
                return {"response": f"I don't recall what {key_to_recall} is.", "module": "recall"}
    return None
"""
    with open(os.path.join(logic_modules_dir, "recall.py"), "w") as f:
        f.write(recall_module_content)

    # Simple Responder Module (Fallback)
    simple_responder_module_content = """
def simple_responder(input_text: str, memory: MemoryManager) -> dict:
    # This module acts as a fallback or a general echo if no other module handles the input.
    # It's considered lower priority or a fallback.
    if input_text:
        # Only return an echo if the input is not empty, otherwise it might
        # interfere with modules that don't require input but expect an empty context.
        memory.set("last_echo", input_text) # Store echo for potential future use
        return {"response": f"You said: {input_text}", "module": "simple_responder"}
    return None
"""
    with open(os.path.join(logic_modules_dir, "simple_responder.py"), "w") as f:
        f.write(simple_responder_module_content)

    print("Dummy logic modules created in 'logic_modules' directory.")

# --- Main Demonstration Function ---

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

    # Load modules and set priority
    core.logic_loader.load_module("greeting", os.path.join("logic_modules", "greeting.py"))
    core.logic_loader.load_module("how_are_you", os.path.join("logic_modules", "how_are_you.py"))
    core.logic_loader.load_module("remember", os.path.join("logic_modules", "remember.py"))
    core.logic_loader.load_module("recall", os.path.join("logic_modules", "recall.py"))
    core.logic_loader.load_module("simple_responder", os.path.join("logic_modules", "simple_responder.py"))

    # Set priority: higher priority modules are checked first.
    # Greeting should be high, remember/recall might be specific, simple_responder last.
    core.add_module_to_priority("greeting", 0) # Highest priority
    core.add_module_to_priority("how_are_you")
    core.add_module_to_priority("remember")
    core.add_module_to_priority("recall")
    core.add_module_to_priority("simple_responder") # Lowest priority/fallback


    print("\n--- AI Core Demonstration ---")

    # Interaction 1: Greeting
    print("\n[User]: Hello!")
    result1 = core.run("Hello!")
    print(f"\nCore Output for Interaction 1:")
    print(f"  Final Response: {result1['final_response']}")
    print(f"  Module Used: {result1['raw_response_data'].get('module') if result1['raw_response_data'] else 'None'}")
    print(f"  Memory Keys After Interaction 1: {core.memory.list_keys()}")
    print(f"  Memory 'last_interaction_type': {core.memory.get('last_interaction_type')}")
    print(f"  Memory 'last_greeting_response': {core.memory.get('last_greeting_response')}")


    # Interaction 2: Asking "how are you"
    print("\n[User]: How are you?")
    result2 = core.run("How are you?")
    print(f"\nCore Output for Interaction 2:")
    print(f"  Final Response: {result2['final_response']}")
    print(f"  Module Used: {result2['raw_response_data'].get('module') if result2['raw_response_data'] else 'None'}")
    print(f"  Memory Keys After Interaction 2: {core.memory.list_keys()}") # 'last_interaction_type' should be updated
    print(f"  Memory 'last_interaction_type': {core.memory.get('last_interaction_type')}")
    print(f"  Memory 'last_how_are_you_response': {core.memory.get('last_how_are_you_response')}")


    # Interaction 3: Asking to remember something (specific key)
    print("\n[User]: Please remember my favorite color is blue.")
    result3 = core.run("Please remember my favorite color is blue.")
    print(f"\nCore Output for Interaction 3:")
    print(f"  Final Response: {result3['final_response']}")
    print(f"  Module Used: {result3['raw_response_data'].get('module') if result3['raw_response_data'] else 'None'}")
    print(f"  Memory Keys After Interaction 3: {core.memory.list_keys()}")
    print(f"  Memory 'last_remembered_item': {core.memory.get('last_remembered_item')}")
    print(f"  Memory 'favorite_color': {core.memory.get('favorite_color')}") # Specific key retrieval


    # Interaction 4: Asking about the remembered item (general recall)
    print("\n[User]: What did I ask you to remember?")
    result4 = core.run("What did I ask you to remember?")
    print(f"\nCore Output for Interaction 4:")
    print(f"  Final Response: {result4['final_response']}")
    print(f"  Module Used: {result4['raw_response_data'].get('module') if result4['raw_response_data'] else 'None'}")
    print(f"  Memory Keys After Interaction 4: {core.memory.list_keys()}")

    # Interaction 5: Asking about the remembered item (specific recall)
    print("\n[User]: What is my favorite color?")
    result5 = core.run("What is my favorite color?")
    print(f"\nCore Output for Interaction 5:")
    print(f"  Final Response: {result5['final_response']}")
    print(f"  Module Used: {result5['raw_response_data'].get('module') if result5['raw_response_data'] else 'None'}")
    print(f"  Memory Keys After Interaction 5: {core.memory.list_keys()}")

    # Interaction 6: Another greeting to show memory persistence and module loading
    print("\n[User]: Hi again!")
    result6 = core.run("Hi again!")
    print(f"\nCore Output for Interaction 6:")
    print(f"  Final Response: {result6['final_response']}")
    print(f"  Module Used: {result6['raw_response_data'].get('module') if result6['raw_response_data'] else 'None'}")
    print(f"  Memory Keys After Interaction 6: {core.memory.list_keys()}")
    print(f"  Memory 'last_greeting_response': {core.memory.get('last_greeting_response')}") # Should be updated

    # Interaction 7: Unmatched input to trigger fallback (simple_responder)
    print("\n[User]: This is an unknown query.")
    result7 = core.run("This is an unknown query.")
    print(f"\nCore Output for Interaction 7:")
    print(f"  Final Response: {result7['final_response']}")
    print(f"  Module Used: {result7['raw_response_data'].get('module') if result7['raw_response_data'] else 'None'}")
    print(f"  Memory Keys After Interaction 7: {core.memory.list_keys()}")
    print(f"  Memory 'last_echo': {core.memory.get('last_echo')}")


    # Interaction 8: Another unknown query, but this time simple_responder is deleted to show no fallback
    print("\n[User]: Another query to test without fallback.")
    core.logic_loader.unload_module("simple_responder")
    print("Unloaded 'simple_responder' module.")
    result8 = core.run("Another query to test without fallback.")
    print(f"\nCore Output for Interaction 8:")
    print(f"  Final Response: {result8['final_response']}")
    print(f"  Module Used: {result8['raw_response_data'].get('module') if result8['raw_response_data'] else 'None'}")
    print(f"  Memory Keys After Interaction 8: {core.memory.list_keys()}")


    print("\n--- Demonstration Complete ---")
    print("Persistent memory is stored in 'memory.json'.")
    print("Dynamic logic modules are in the 'logic_modules' directory.")
    print("You can add or modify Python files in 'logic_modules' to change AI behavior.")

if __name__ == "__main__":
    run_demo()
