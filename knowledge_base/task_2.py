# PHOENIX CORE - Module Loader (task_1)
import importlib
import os

class ModuleLoader:
    def __init__(self, core_memory, tasks_directory="phoenix_tasks"):
        self.core_memory = core_memory
        self.tasks_directory = tasks_directory
        self.loaded_modules = {}
        self._ensure_tasks_directory()
        self._load_all_available_modules()

    def _ensure_tasks_directory(self):
        if not os.path.exists(self.tasks_directory):
            os.makedirs(self.tasks_directory)
            print(f"Created tasks directory: {self.tasks_directory}")

    def _load_module(self, module_name):
        module_path = os.path.join(self.tasks_directory, f"{module_name}.py")
        if os.path.exists(module_path):
            try:
                # Dynamically add the tasks directory to sys.path for importlib
                import sys
                if self.tasks_directory not in sys.path:
                    sys.path.insert(0, self.tasks_directory)

                module = importlib.import_module(module_name)
                if hasattr(module, 'run') and callable(module.run):
                    self.loaded_modules[module_name] = module
                    print(f"Successfully loaded module: {module_name}")
                    return module
                else:
                    print(f"Warning: Module '{module_name}' does not have a callable 'run()' function.")
                    return None
            except ImportError as e:
                print(f"Error importing module '{module_name}': {e}")
                return None
            except Exception as e:
                print(f"An unexpected error occurred while loading module '{module_name}': {e}")
                return None
        else:
            print(f"Module file not found: {module_path}")
            return None

    def _load_all_available_modules(self):
        # Scan the tasks directory for .py files and attempt to load them
        for filename in os.listdir(self.tasks_directory):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # Remove .py extension
                self._load_module(module_name)

    def get_loaded_module(self, module_name):
        return self.loaded_modules.get(module_name)

    def get_available_module_names(self):
        return list(self.loaded_modules.keys())

    def run_module(self, module_name, *args, **kwargs):
        module = self.get_loaded_module(module_name)
        if module:
            try:
                return module.run(*args, **kwargs)
            except Exception as e:
                print(f"Error running module '{module_name}': {e}")
                return None
        else:
            print(f"Error: Module '{module_name}' not loaded or does not exist.")
            return None

    def add_new_module(self, module_name, module_content):
        module_path = os.path.join(self.tasks_directory, f"{module_name}.py")
        if not os.path.exists(module_path):
            try:
                with open(module_path, "w") as f:
                    f.write(module_content)
                print(f"Created new module file: {module_path}")
                # Reload modules to include the new one
                self._load_module(module_name)
                # Update core memory with new capability if desired (optional, depends on system design)
                # This assumes a convention where capability is related to module name
                if module_name not in self.core_memory.data.get("capabilities", []):
                    if "capabilities" not in self.core_memory.data:
                        self.core_memory.data["capabilities"] = []
                    self.core_memory.data["capabilities"].append(module_name)
                    self.core_memory.save()
                    print(f"Added '{module_name}' as a new capability.")
                return True
            except IOError as e:
                print(f"Error writing module file '{module_path}': {e}")
                return False
        else:
            print(f"Error: Module '{module_name}' already exists.")
            return False

if __name__ == "__main__":
    # This part is for testing the module in isolation.
    from task_0_phoenix_core_dna_module import CoreMemory # Assuming task_0 is in this file

    # Create a dummy tasks directory and a sample module for testing
    if not os.path.exists("phoenix_tasks"):
        os.makedirs("phoenix_tasks")

    sample_module_content = """
def run(message):
    print(f"Hello from Sample Module! You said: {message}")
    return f"Processed: {message}"
"""
    with open("phoenix_tasks/sample_task.py", "w") as f:
        f.write(sample_module_content)

    print("--- Testing ModuleLoader ---")
    mem = CoreMemory()
    loader = ModuleLoader(mem)

    print("\nInitial loaded modules:", loader.get_available_module_names())

    print("\nRunning 'sample_task':")
    result = loader.run_module("sample_task", "This is a test message.")
    print("Result:", result)

    print("\nAdding a new module 'greeting_task':")
    greeting_module_content = """
def run(name="World"):
    greeting = f"Greetings, {name}!"
    print(greeting)
    return greeting
"""
    loader.add_new_module("greeting_task", greeting_module_content)

    print("\nUpdated loaded modules:", loader.get_available_module_names())

    print("\nRunning 'greeting_task':")
    result = loader.run_module("greeting_task", name="Phoenix")
    print("Result:", result)

    print("\nRunning non-existent task:")
    result = loader.run_module("non_existent_task", "data")
    print("Result:", result)

    print("\nCore Memory Capabilities:", mem.data.get("capabilities"))

    # Clean up dummy files and directory
    os.remove("phoenix_tasks/sample_task.py")
    os.remove("phoenix_tasks/greeting_task.py")
    os.rmdir("phoenix_tasks")
    print("\n--- Testing Complete ---")
