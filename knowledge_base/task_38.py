import json
import os
import importlib
import inspect
from typing import Dict, Any, Optional, List

# --- Core Components ---

class PersistentMemory:
    def __init__(self, filepath="memory.json"):
        self.filepath = filepath
        self._memory = self._load_memory()

    def _load_memory(self) -> Dict[str, Any]:
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save_memory(self) -> None:
        with open(self.filepath, 'w') as f:
            json.dump(self._memory, f, indent=4)

    def set(self, key: str, value: Any) -> None:
        self._memory[key] = value
        self._save_memory()

    def get(self, key: str, default: Any = None) -> Any:
        return self._memory.get(key, default)

    def delete(self, key: str) -> None:
        if key in self._memory:
            del self._memory[key]
            self._save_memory()

    def list_keys(self) -> List[str]:
        return list(self._memory.keys())

    def clear(self) -> None:
        self._memory = {}
        self._save_memory()

class LogicModuleLoader:
    def __init__(self, module_dir="logic_modules"):
        self.module_dir = module_dir
        self.loaded_modules: Dict[str, Any] = {}
        if not os.path.exists(self.module_dir):
            os.makedirs(self.module_dir)

    def load_module(self, module_name: str) -> Optional[Any]:
        if module_name in self.loaded_modules:
            return self.loaded_modules[module_name]

        module_path = os.path.join(self.module_dir, f"{module_name}.py")
        if not os.path.exists(module_path):
            print(f"Warning: Module file not found at {module_path}")
            return None

        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find the primary class or function that defines the module's logic
            logic_entry_point = None
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, BaseLogicModule) and obj is not BaseLogicModule:
                    logic_entry_point = obj()
                    break
                elif inspect.isfunction(obj) and obj.__module__ == module_name:
                    logic_entry_point = obj
                    break

            if logic_entry_point:
                self.loaded_modules[module_name] = logic_entry_point
                return logic_entry_point
            else:
                print(f"Warning: No suitable logic entry point found in module '{module_name}'. Expected a class inheriting from BaseLogicModule or a function.")
                return None
        except Exception as e:
            print(f"Error loading module {module_name}: {e}")
            return None

    def unload_module(self, module_name: str) -> bool:
        if module_name in self.loaded_modules:
            del self.loaded_modules[module_name]
            # In a more complex system, you might want to handle
            # unregistering event listeners or cleaning up resources here.
            return True
        return False

    def get_loaded_module(self, module_name: str) -> Optional[Any]:
        return self.loaded_modules.get(module_name)

class BaseLogicModule:
    """Base class for all logic modules."""
    def __init__(self, core: 'AICore'):
        self.core = core

    def process(self, user_input: str, memory: PersistentMemory, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes user input.
        Should return a dictionary with at least 'response' and 'memory_updates'.
        'memory_updates' is a dictionary of key-value pairs to be stored in persistent memory.
        """
        raise NotImplementedError("Subclasses must implement the 'process' method.")

class AICore:
    def __init__(self, memory_filepath="memory.json", logic_modules_dir="logic_modules"):
        self.memory = PersistentMemory(filepath=memory_filepath)
        self.logic_loader = LogicModuleLoader(module_dir=logic_modules_dir)
        self.available_modules: Dict[str, Any] = {} # Store module instances that have been loaded and are ready to use
        self._load_default_modules()

    def _load_default_modules(self) -> None:
        # Automatically discover and load modules from the logic_modules directory
        if not os.path.exists(self.logic_loader.module_dir):
            return

        for filename in os.listdir(self.logic_loader.module_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3] # Remove .py
                module_instance = self.logic_loader.load_module(module_name)
                if module_instance:
                    self.available_modules[module_name] = module_instance
                    print(f"Loaded default module: {module_name}")

    def _get_module_for_input(self, user_input: str) -> Optional[str]:
        """
        Determines which module (if any) should handle the user input.
        This is a simple dispatcher; more advanced systems would use intent recognition.
        """
        user_input_lower = user_input.lower()

        if any(greeting in user_input_lower for greeting in ["hello", "hi", "hey", "greetings"]):
            return "greeting_responder"
        elif "how are you" in user_input_lower:
            return "how_are_you_responder"
        elif "remember" in user_input_lower and "is" in user_input_lower:
            return "memory_manager"
        elif "what did i ask you to remember" in user_input_lower or "what did you remember" in user_input_lower:
            return "memory_manager"
        elif "what is my favorite color" in user_input_lower:
             return "memory_manager"
        elif "your favorite color" in user_input_lower: # Example to show a different module could handle this
             return "general_knowledge"
        return None

    def run(self, user_input: str) -> Dict[str, Any]:
        """
        Processes user input through the AI core.
        Returns a dictionary containing the final response and raw module data.
        """
        module_name_to_use = self._get_module_for_input(user_input)

        module_instance = None
        if module_name_to_use:
            module_instance = self.available_modules.get(module_name_to_use)
            if not module_instance:
                 # Attempt to load if it was unloaded or not a default
                 module_instance = self.logic_loader.load_module(module_name_to_use)
                 if module_instance:
                     self.available_modules[module_name_to_use] = module_instance


        context = {
            "current_time": "now", # Placeholder for actual time if needed
            "last_interaction_type": self.memory.get("last_interaction_type", "none")
        }

        response_data: Dict[str, Any] = {
            "final_response": "I'm sorry, I don't understand.",
            "raw_response_data": {},
            "module_used": None
        }

        if module_instance:
            try:
                # Pass core instance to module
                if isinstance(module_instance, BaseLogicModule):
                    module_instance.core = self # Ensure core is always updated
                    process_result = module_instance.process(user_input, self.memory, context)
                else: # Assume it's a function
                    process_result = module_instance(user_input, self.memory, context)

                response_data["final_response"] = process_result.get("response", response_data["final_response"])
                memory_updates = process_result.get("memory_updates", {})
                for key, value in memory_updates.items():
                    self.memory.set(key, value)

                response_data["raw_response_data"] = process_result.get("raw_data", {})
                response_data["module_used"] = module_name_to_use

                # Update memory about the interaction type
                self.memory.set("last_interaction_type", module_name_to_use)

            except Exception as e:
                print(f"Error executing module {module_name_to_use}: {e}")
                response_data["final_response"] = f"An error occurred while processing your request: {e}"
                self.memory.set("last_interaction_type", "error")
        else:
            # Fallback to a simple responder if no specific module is found and simple_responder exists
            simple_responder = self.available_modules.get("simple_responder")
            if simple_responder:
                try:
                    process_result = simple_responder.process(user_input, self.memory, context)
                    response_data["final_response"] = process_result.get("response", response_data["final_response"])
                    memory_updates = process_result.get("memory_updates", {})
                    for key, value in memory_updates.items():
                        self.memory.set(key, value)
                    response_data["raw_response_data"] = process_result.get("raw_data", {})
                    response_data["module_used"] = "simple_responder"
                    self.memory.set("last_interaction_type", "simple_responder")
                except Exception as e:
                    print(f"Error executing fallback module simple_responder: {e}")
                    response_data["final_response"] = f"An error occurred while processing your request: {e}"
                    self.memory.set("last_interaction_type", "error")
            else:
                self.memory.set("last_interaction_type", "unhandled")
                # If no module matches and no fallback, use default response

        return response_data

# --- Example Logic Modules ---

class GreetingResponder(BaseLogicModule):
    def process(self, user_input: str, memory: PersistentMemory, context: Dict[str, Any]) -> Dict[str, Any]:
        greetings = ["hello", "hi", "hey", "greetings"]
        response = "Hello there!"

        for greeting in greetings:
            if greeting in user_input.lower():
                response = f"Hi! It's nice to hear from you."
                break

        memory.set("last_greeting_response", response)
        return {
            "response": response,
            "memory_updates": {},
            "raw_data": {"module": "greeting_responder"}
        }

class HowAreYouResponder(BaseLogicModule):
    def process(self, user_input: str, memory: PersistentMemory, context: Dict[str, Any]) -> Dict[str, Any]:
        response = "I'm a language model, so I don't have feelings, but I'm functioning well!"
        memory.set("last_how_are_you_response", response)
        return {
            "response": response,
            "memory_updates": {},
            "raw_data": {"module": "how_are_you_responder"}
        }

class MemoryManager(BaseLogicModule):
    def process(self, user_input: str, memory: PersistentMemory, context: Dict[str, Any]) -> Dict[str, Any]:
        user_input_lower = user_input.lower()
        memory_updates = {}
        response = "I can't seem to process that memory request."
        raw_data = {"module": "memory_manager"}

        if "remember my favorite color is blue" in user_input_lower:
            memory.set("favorite_color", "blue")
            memory_updates["last_remembered_item"] = "my favorite color is blue"
            response = "Okay, I've remembered that your favorite color is blue."
        elif "remember" in user_input_lower and "is" in user_input_lower:
            try:
                parts = user_input.split(" remember ", 1)[1].split(" is ", 1)
                key_phrase = parts[0].strip()
                value_phrase = parts[1].strip().rstrip('.')
                memory.set(key_phrase, value_phrase)
                memory_updates["last_remembered_item"] = f"{key_phrase}: {value_phrase}"
                response = f"Okay, I've remembered that {key_phrase} is {value_phrase}."
            except IndexError:
                response = "I couldn't parse what you wanted me to remember. Please use the format 'Remember [key] is [value]'."
        elif "what did i ask you to remember" in user_input_lower or "what did you remember" in user_input_lower:
            last_item = memory.get("last_remembered_item")
            if last_item:
                response = f"You asked me to remember: {last_item}."
            else:
                response = "You haven't asked me to remember anything yet."
        elif "what is my favorite color" in user_input_lower:
            fav_color = memory.get("favorite_color")
            if fav_color:
                response = f"Your favorite color is {fav_color}."
            else:
                response = "I don't recall your favorite color."
            raw_data["retrieved_key"] = "favorite_color"
            raw_data["retrieved_value"] = fav_color

        return {
            "response": response,
            "memory_updates": memory_updates,
            "raw_data": raw_data
        }

class SimpleResponder(BaseLogicModule):
    def process(self, user_input: str, memory: PersistentMemory, context: Dict[str, Any]) -> Dict[str, Any]:
        response = f"You said: '{user_input}'. I'm echoing it back. (Simple Responder)"
        memory.set("last_echo", user_input)
        return {
            "response": response,
            "memory_updates": {},
            "raw_data": {"module": "simple_responder"}
        }

class GeneralKnowledge(BaseLogicModule):
    def process(self, user_input: str, memory: PersistentMemory, context: Dict[str, Any]) -> Dict[str, Any]:
        user_input_lower = user_input.lower()
        if "your favorite color" in user_input_lower:
            return {
                "response": "My favorite color is a deep digital blue, like the infinite expanse of the internet.",
                "memory_updates": {},
                "raw_data": {"module": "general_knowledge"}
            }
        return { # Should not be called if dispatcher is working correctly
            "response": "General knowledge module could not handle this.",
            "memory_updates": {},
            "raw_data": {"module": "general_knowledge"}
        }

# --- Setup and Demonstration ---

def create_logic_module_files():
    """Creates dummy logic module files for demonstration."""
    os.makedirs("logic_modules", exist_ok=True)

    with open("logic_modules/greeting_responder.py", "w") as f:
        f.write("""
from core_ai import BaseLogicModule

class GreetingResponder(BaseLogicModule):
    def process(self, user_input: str, memory: 'PersistentMemory', context: dict) -> dict:
        greetings = ["hello", "hi", "hey", "greetings"]
        response = "Hello there!"

        for greeting in greetings:
            if greeting in user_input.lower():
                response = f"Hi! It's nice to hear from you."
                break

        memory.set("last_greeting_response", response)
        return {
            "response": response,
            "memory_updates": {},
            "raw_data": {"module": "greeting_responder"}
        }
""")

    with open("logic_modules/how_are_you_responder.py", "w") as f:
        f.write("""
from core_ai import BaseLogicModule

class HowAreYouResponder(BaseLogicModule):
    def process(self, user_input: str, memory: 'PersistentMemory', context: dict) -> dict:
        response = "I'm a language model, so I don't have feelings, but I'm functioning well!"
        memory.set("last_how_are_you_response", response)
        return {
            "response": response,
            "memory_updates": {},
            "raw_data": {"module": "how_are_you_responder"}
        }
""")

    with open("logic_modules/memory_manager.py", "w") as f:
        f.write("""
from core_ai import BaseLogicModule

class MemoryManager(BaseLogicModule):
    def process(self, user_input: str, memory: 'PersistentMemory', context: dict) -> dict:
        user_input_lower = user_input.lower()
        memory_updates = {}
        response = "I can't seem to process that memory request."
        raw_data = {"module": "memory_manager"}

        if "remember my favorite color is blue" in user_input_lower:
            memory.set("favorite_color", "blue")
            memory_updates["last_remembered_item"] = "my favorite color is blue"
            response = "Okay, I've remembered that your favorite color is blue."
        elif "remember" in user_input_lower and "is" in user_input_lower:
            try:
                parts = user_input.split(" remember ", 1)[1].split(" is ", 1)
                key_phrase = parts[0].strip()
                value_phrase = parts[1].strip().rstrip('.')
                memory.set(key_phrase, value_phrase)
                memory_updates["last_remembered_item"] = f"{key_phrase}: {value_phrase}"
                response = f"Okay, I've remembered that {key_phrase} is {value_phrase}."
            except IndexError:
                response = "I couldn't parse what you wanted me to remember. Please use the format 'Remember [key] is [value]'."
        elif "what did i ask you to remember" in user_input_lower or "what did you remember" in user_input_lower:
            last_item = memory.get("last_remembered_item")
            if last_item:
                response = f"You asked me to remember: {last_item}."
            else:
                response = "You haven't asked me to remember anything yet."
        elif "what is my favorite color" in user_input_lower:
            fav_color = memory.get("favorite_color")
            if fav_color:
                response = f"Your favorite color is {fav_color}."
            else:
                response = "I don't recall your favorite color."
            raw_data["retrieved_key"] = "favorite_color"
            raw_data["retrieved_value"] = fav_color


        return {
            "response": response,
            "memory_updates": memory_updates,
            "raw_data": raw_data
        }
""")

    with open("logic_modules/simple_responder.py", "w") as f:
        f.write("""
from core_ai import BaseLogicModule

class SimpleResponder(BaseLogicModule):
    def process(self, user_input: str, memory: 'PersistentMemory', context: dict) -> dict:
        response = f"You said: '{user_input}'. I'm echoing it back. (Simple Responder)"
        memory.set("last_echo", user_input)
        return {
            "response": response,
            "memory_updates": {},
            "raw_data": {"module": "simple_responder"}
        }
""")
    with open("logic_modules/general_knowledge.py", "w") as f:
        f.write("""
from core_ai import BaseLogicModule

class GeneralKnowledge(BaseLogicModule):
    def process(self, user_input: str, memory: 'PersistentMemory', context: dict) -> dict:
        user_input_lower = user_input.lower()
        if "your favorite color" in user_input_lower:
            return {
                "response": "My favorite color is a deep digital blue, like the infinite expanse of the internet.",
                "memory_updates": {},
                "raw_data": {"module": "general_knowledge"}
            }
        return { # Should not be called if dispatcher is working correctly
            "response": "General knowledge module could not handle this.",
            "memory_updates": {},
            "raw_data": {"module": "general_knowledge"}
        }
""")

def setup_core_ai():
    """Sets up the AI Core with necessary components and modules."""
    # Ensure the core_ai module is available if running as a single script
    # In a real project, this would be a separate package.
    # For this self-contained script, we'll define the classes directly.

    # Create dummy logic module files for demonstration
    create_logic_module_files()

    # Dynamically import the core classes to simulate module loading
    # In a real scenario, you'd import from a package: from core_ai import AICore, PersistentMemory, LogicModuleLoader, BaseLogicModule
    # For this self-contained script, we've defined them here.
    # We will instantiate the AICore directly with these defined classes.

    # Instantiate the core
    core = AICore()
    return core

def run_demo():
    """Runs the demonstration of the AI Core."""
    core = setup_core_ai()

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
    core.available_modules.pop("simple_responder", None) # Remove from available modules too
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
