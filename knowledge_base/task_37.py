import json
import os
import importlib
from collections import defaultdict

class PersistentMemory:
    def __init__(self, filepath="memory.json"):
        self.filepath = filepath
        self.data = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save_memory(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=4)

    def set(self, key, value):
        self.data[key] = value
        self._save_memory()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def list_keys(self):
        return list(self.data.keys())

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self._save_memory()

class LogicLoader:
    def __init__(self, module_dir="logic_modules"):
        self.module_dir = module_dir
        self.modules = {}
        os.makedirs(self.module_dir, exist_ok=True)
        self._load_initial_modules()

    def _load_module(self, module_name):
        try:
            module_path = os.path.join(self.module_dir, f"{module_name}.py")
            if not os.path.exists(module_path):
                return None

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            print(f"Error loading module {module_name}: {e}")
            return None

    def _load_initial_modules(self):
        for filename in os.listdir(self.module_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                module = self._load_module(module_name)
                if module:
                    self.modules[module_name] = module

    def load_module(self, module_name):
        if module_name not in self.modules:
            module = self._load_module(module_name)
            if module:
                self.modules[module_name] = module
                return True
        return False

    def unload_module(self, module_name):
        if module_name in self.modules:
            del self.modules[module_name]
            return True
        return False

    def get_module(self, module_name):
        return self.modules.get(module_name)

    def list_loaded_modules(self):
        return list(self.modules.keys())

class AICore:
    def __init__(self, memory_filepath="memory.json", logic_module_dir="logic_modules"):
        self.memory = PersistentMemory(filepath=memory_filepath)
        self.logic_loader = LogicLoader(module_dir=logic_module_dir)

    def run(self, user_input):
        response_data = {"final_response": "I'm not sure how to respond to that.", "raw_response_data": {}}

        # Simple heuristic for module selection (can be expanded)
        selected_module_name = None
        best_match_score = -1

        for module_name, module in self.logic_loader.modules.items():
            if hasattr(module, 'process_input'):
                try:
                    match_score, module_output = module.process_input(user_input, self.memory)
                    if match_score > best_match_score:
                        best_match_score = match_score
                        selected_module_name = module_name
                        response_data["raw_response_data"] = module_output if module_output is not None else {}
                except Exception as e:
                    print(f"Error in module {module_name}.process_input: {e}")

        if selected_module_name:
            response_data["final_response"] = response_data["raw_response_data"].get("response", "I processed that.")
            response_data["raw_response_data"]["module"] = selected_module_name
            # Update general memory keys after processing
            self.memory.set("last_interaction", user_input)
            self.memory.set("last_interaction_type", selected_module_name)
        else:
            # Fallback to a simple responder if no module matched
            if self.logic_loader.get_module("simple_responder"):
                try:
                    module = self.logic_loader.get_module("simple_responder")
                    match_score, module_output = module.process_input(user_input, self.memory)
                    if match_score > -1: # Assume simple_responder always matches
                        response_data["final_response"] = module_output.get("response", "I'm not sure how to respond to that.")
                        response_data["raw_response_data"] = module_output
                        response_data["raw_response_data"]["module"] = "simple_responder"
                        self.memory.set("last_interaction", user_input)
                        self.memory.set("last_interaction_type", "simple_responder")
                except Exception as e:
                    print(f"Error in fallback simple_responder module: {e}")
            else:
                self.memory.set("last_interaction", user_input)
                self.memory.set("last_interaction_type", "unknown")


        return response_data

def create_logic_modules_directory():
    os.makedirs("logic_modules", exist_ok=True)

    # Create a greeting module
    with open("logic_modules/greeting_module.py", "w") as f:
        f.write("""
import random

def process_input(user_input, memory):
    greetings = ["hello", "hi", "hey", "greetings"]
    if any(greet in user_input.lower() for greet in greetings):
        responses = [
            "Hello there!",
            "Hi! How can I help you today?",
            "Greetings!",
            "Hey! What's up?"
        ]
        response = random.choice(responses)
        memory.set("last_greeting_response", response)
        return 1.0, {"response": response, "module": "greeting_module"}
    return 0.0, None
""")

    # Create a how_are_you module
    with open("logic_modules/how_are_you_module.py", "w") as f:
        f.write("""
def process_input(user_input, memory):
    if "how are you" in user_input.lower():
        responses = [
            "I'm an AI, so I don't have feelings, but I'm functioning optimally!",
            "I'm doing great, thanks for asking!",
            "As a digital entity, I'm always running smoothly."
        ]
        response = random.choice(responses)
        memory.set("last_how_are_you_response", response)
        return 1.0, {"response": response, "module": "how_are_you_module"}
    return 0.0, None
""")

    # Create a memory module
    with open("logic_modules/memory_module.py", "w") as f:
        f.write("""
import re

def process_input(user_input, memory):
    # Module to handle remembering and recalling information
    if user_input.lower().startswith("please remember my "):
        match = re.search(r"please remember my (.+) is (.+)", user_input.lower())
        if match:
            key = match.group(1).strip().replace(" ", "_") # Convert to snake_case for keys
            value = match.group(2).strip()
            memory.set(key, value)
            response = f"Okay, I'll remember that your {key.replace('_', ' ')} is {value}."
            memory.set("last_remembered_item", {"key": key, "value": value})
            return 1.0, {"response": response, "module": "memory_module", "remembered_key": key, "remembered_value": value}
        else:
            return 0.5, {"response": "I'm not sure exactly what you want me to remember.", "module": "memory_module"}

    elif user_input.lower().startswith("what is my "):
        match = re.search(r"what is my (.+)", user_input.lower())
        if match:
            key_to_recall = match.group(1).strip().replace(" ", "_")
            retrieved_value = memory.get(key_to_recall)
            if retrieved_value is not None:
                response = f"You told me your {key_to_recall.replace('_', ' ')} is {retrieved_value}."
                return 1.0, {"response": response, "module": "memory_module", "recalled_key": key_to_recall, "recalled_value": retrieved_value}
            else:
                response = f"I don't seem to remember what your {key_to_recall.replace('_', ' ')} is."
                return 0.8, {"response": response, "module": "memory_module", "recalled_key": key_to_recall, "recalled_value": None}
        else:
            return 0.0, None # Let other modules handle if format is not recognized

    elif user_input.lower() == "what did i ask you to remember?":
        last_remembered = memory.get("last_remembered_item")
        if last_remembered:
            response = f"You asked me to remember that your {last_remembered['key'].replace('_', ' ')} is {last_remembered['value']}."
            return 1.0, {"response": response, "module": "memory_module", "last_remembered": last_remembered}
        else:
            response = "You haven't asked me to remember anything specific yet."
            return 0.5, {"response": response, "module": "memory_module"}
            
    return 0.0, None
""")

    # Create a simple responder module for fallback
    with open("logic_modules/simple_responder.py", "w") as f:
        f.write("""
import random

def process_input(user_input, memory):
    # A generic responder for unmatched inputs
    responses = [
        "I'm still learning, could you rephrase that?",
        "That's an interesting thought. What else is on your mind?",
        "I'm not sure how to handle that request yet. Can you try something else?",
        f"You said: '{user_input}'. I'll try to remember that.",
    ]
    
    response_text = random.choice(responses)
    
    if "you said" in response_text:
        memory.set("last_echo", user_input)

    return 1.0, {"response": response_text, "module": "simple_responder"}
""")


def run_demo():
    create_logic_modules_directory()

    core = AICore()

    # Interaction 1: Greeting
    print("\n--- AI Core Demonstration ---")
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
