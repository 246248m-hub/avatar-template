import os
import importlib
import json
import inspect

class PersistentMemory:
    """
    Manages persistent storage for the AI core, using a JSON file.
    """
    def __init__(self, filepath="memory.json"):
        self.filepath = filepath
        self.data = self._load_memory()

    def _load_memory(self):
        """Loads memory from the JSON file."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading memory file '{self.filepath}': {e}. Starting with empty memory.")
                return {}
        return {}

    def _save_memory(self):
        """Saves current memory state to the JSON file."""
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            print(f"Error saving memory to file '{self.filepath}': {e}")

    def set(self, key, value):
        """Sets a value in memory."""
        self.data[key] = value
        self._save_memory()

    def get(self, key, default=None):
        """Gets a value from memory."""
        return self.data.get(key, default)

    def delete(self, key):
        """Deletes a key from memory."""
        if key in self.data:
            del self.data[key]
            self._save_memory()

    def list_keys(self):
        """Returns a list of all keys in memory."""
        return list(self.data.keys())

    def clear(self):
        """Clears all memory."""
        self.data = {}
        self._save_memory()

class DynamicLogicProcessor:
    """
    Dynamically loads and executes logic modules from a specified directory.
    """
    def __init__(self, module_dir="logic_modules"):
        self.module_dir = module_dir
        self.modules = {}
        self._load_modules()

    def _load_modules(self):
        """Loads all Python files from the module directory as logic modules."""
        if not os.path.exists(self.module_dir):
            print(f"Module directory '{self.module_dir}' not found. No logic modules will be loaded.")
            return

        for filename in os.listdir(self.module_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # Remove .py extension
                filepath = os.path.join(self.module_dir, filename)
                try:
                    spec = importlib.util.spec_from_file_location(module_name, filepath)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    # Find the 'process' function within the module
                    if hasattr(module, 'process') and inspect.isfunction(module.process):
                        self.modules[module_name] = module.process
                        print(f"Loaded logic module: '{module_name}'")
                    else:
                        print(f"Warning: Module '{module_name}' in '{filename}' does not have a 'process' function.")
                except Exception as e:
                    print(f"Error loading module '{module_name}' from '{filename}': {e}")

    def get_module_names(self):
        """Returns a list of available module names."""
        return list(self.modules.keys())

    def execute_module(self, module_name, context):
        """
        Executes a specific logic module with the given context.
        Returns the result from the module's process function.
        """
        if module_name in self.modules:
            try:
                # Pass memory object to the context for modules to use
                context['memory'] = self.modules.get('memory_manager') # Assuming memory is accessible
                return self.modules[module_name](context)
            except Exception as e:
                print(f"Error executing module '{module_name}': {e}")
                return None
        else:
            print(f"Error: Module '{module_name}' not found.")
            return None

class AICore:
    """
    The central AI core that orchestrates persistent memory and dynamic logic.
    """
    def __init__(self, module_dir="logic_modules", memory_filepath="memory.json"):
        self.memory = PersistentMemory(filepath=memory_filepath)
        self.logic_processor = DynamicLogicProcessor(module_dir=module_dir)

        # Make memory accessible to logic modules by adding it as a module itself
        # This is a simplified approach; a more robust system might use dependency injection
        self.logic_processor.modules['memory_manager'] = self.memory

        # Keep track of available logic modules
        self.available_modules = self.logic_processor.get_module_names()
        print(f"AI Core initialized. Available logic modules: {self.available_modules}")

    def run(self, user_input, context=None):
        """
        Processes user input through the AI core.

        Args:
            user_input (str): The input from the user.
            context (dict, optional): Additional context to pass to logic modules. Defaults to None.

        Returns:
            dict: A dictionary containing results from logic modules.
        """
        if context is None:
            context = {}

        context['input'] = user_input
        context['memory'] = self.memory  # Ensure memory is in context for all modules

        logic_results = {}

        # --- Dynamic Logic Execution ---
        # Iterate through loaded modules to find one that can process the input.
        # A more sophisticated routing or decision-making layer could be implemented here.
        # For now, we try modules in the order they were loaded or a predefined order.

        # Define an order of execution for demonstration, or implement a more intelligent router
        execution_order = ["greetings_handler", "task_executor", "simple_responder"]
        processed = False

        for module_name in execution_order:
            if module_name in self.logic_processor.modules:
                print(f"Attempting to process with module: '{module_name}'")
                result = self.logic_processor.execute_module(module_name, context.copy()) # Pass a copy of context

                if result is not None:
                    logic_results[module_name] = result
                    print(f"  -> Module '{module_name}' returned: {result}")
                    # Basic stopping condition: if a module returns a meaningful result,
                    # we might stop processing further modules for this input.
                    # This logic can be made more complex.
                    if any(key in result for key in ["response", "message", "action", "echo"]):
                        processed = True
                        # If a specific action is returned that suggests completion or redirection,
                        # we might break or handle it specifically.
                        # For now, we'll allow chained effects but store the first successful response.
                        break
            else:
                print(f"Module '{module_name}' not found in loaded modules.")

        if not processed:
            print("No specific logic module handled the input. Falling back to general processing if any.")
            # If no specific module handled it, we could trigger a default/fallback module
            if "simple_responder" in self.logic_processor.modules:
                 print("Attempting to process with fallback module: 'simple_responder'")
                 result = self.logic_processor.execute_module("simple_responder", context.copy())
                 if result is not None:
                     logic_results["simple_responder"] = result
                     print(f"  -> Fallback module 'simple_responder' returned: {result}")
            else:
                print("No fallback module available.")


        # --- Output Handling and Memory Update (can be expanded) ---
        # This part could also be a dedicated module or function for output generation.
        # For now, let's process the collected logic results.
        final_response = "I'm not sure how to respond to that."
        if logic_results:
            # Prioritize 'response' or 'message' fields from the first processed module
            for module_name, result_data in logic_results.items():
                if isinstance(result_data, dict):
                    if "response" in result_data:
                        final_response = result_data["response"]
                        break # Use the first found response
                    elif "message" in result_data:
                        final_response = result_data["message"]
                        break # Use the first found message


        # Example of processing and potentially overriding the final response based on memory
        # Or based on specific flags returned by modules.
        if self.memory.get("last_interaction_type") == "greeting" and "Hello there!" in final_response:
            # Maybe adjust response if it's a repeated greeting
            pass

        # Print internal details for debugging
        # print(f"Raw Logic Results: {logic_results}")
        # print(f"Final Response determined: {final_response}")

        # Print responses from specific modules for user visibility
        for result in logic_results.values():
            if isinstance(result, dict):
                if "response" in result:
                    print(f"  -> {result['response']}")
                elif "message" in result:
                    print(f"  -> {result['message']}")
                elif "echo" in result:
                    print(f"  -> {result['echo']}")
                elif "action" in result: # For task executor specific outputs
                    if "message" in result:
                        print(f"  -> {result['message']}")

        # Return results and updated context (optional)
        return {
            "logic_results": logic_results,
            "final_response": final_response,
            "memory_state": self.memory.data # For inspection
        }

# --- Example Usage ---

def create_dummy_logic_modules():
    """
    Creates placeholder logic modules in the 'logic_modules' directory
    for demonstration purposes.
    """
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
            # Example of storing a response for later reference
            memory.set("last_greeting_response", response)
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

    # simple_responder.py - a fallback or general module
    with open("logic_modules/simple_responder.py", "w") as f:
        f.write("""
def process(context):
    input_text = context.get("input", "")
    if input_text:
        # This module acts as a simple echo or fallback
        return {"echo": f"You said: {input_text}"}
    return None
""")

def run():
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
    print(f"Memory Keys After Interaction 1: {core.memory.list_keys()}")
    print(f"Memory 'last_interaction_type': {core.memory.get('last_interaction_type')}")

    # Interaction 2: Asking "how are you"
    print("\n[User]: How are you?")
    result2 = core.run("How are you?")
    print(f"\nCore Output for Interaction 2: {result2['final_response']}")
    print(f"Memory Keys After Interaction 2: {core.memory.list_keys()}") # 'last_interaction_type' should still be 'greeting'

    # Interaction 3: Asking to remember something
    print("\n[User]: Please remember my favorite color is blue.")
    result3 = core.run("Please remember my favorite color is blue.")
    print(f"\nCore Output for Interaction 3: {result3['final_response']}")
    print(f"Memory Keys After Interaction 3: {core.memory.list_keys()}")
    print(f"Memory 'remembered_item': {core.memory.get('remembered_item')}")
    print(f"Memory 'last_interaction_type': {core.memory.get('last_interaction_type')}") # Should still be 'greeting' from previous interaction

    # Interaction 4: Asking about the remembered item
    print("\n[User]: What did I ask you to remember?")
    result4 = core.run("What did I ask you to remember?")
    print(f"\nCore Output for Interaction 4: {result4['final_response']}")
    print(f"Memory Keys After Interaction 4: {core.memory.list_keys()}")

    # Interaction 5: Another greeting to show memory persistence and module loading
    print("\n[User]: Hi again!")
    result5 = core.run("Hi again!")
    print(f"\nCore Output for Interaction 5: {result5['final_response']}")
    print(f"Memory Keys After Interaction 5: {core.memory.list_keys()}")
    print(f"Memory 'last_greeting_response': {core.memory.get('last_greeting_response')}") # Should be updated

    # Interaction 6: Unmatched input to trigger fallback
    print("\n[User]: This is an unknown query.")
    result6 = core.run("This is an unknown query.")
    print(f"\nCore Output for Interaction 6: {result6['final_response']}")
    print(f"Memory Keys After Interaction 6: {core.memory.list_keys()}")


    print("\n--- Demonstration Complete ---")
    print("Persistent memory is stored in 'memory.json'.")
    print("Dynamic logic modules are in the 'logic_modules' directory.")
    print("You can add or modify Python files in 'logic_modules' to change AI behavior.")

if __name__ == "__main__":
    run()
