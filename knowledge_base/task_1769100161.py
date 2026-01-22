import os
import shutil
import sys
from unittest import mock

# Mock implementations for essential components
class MockCoreMemory:
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

class MockCPU:
    def execute(self, instruction_pointer):
        # Simulate a simple instruction execution
        if instruction_pointer == 0x1000:
            return "CPU Executed Instruction"
        return "CPU Finished"

class MockFileSystem:
    def read(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            return None

    def write(self, filepath, data):
        with open(filepath, 'wb') as f:
            f.write(data)

    def exists(self, filepath):
        return os.path.exists(filepath)

    def delete(self, filepath):
        if os.path.exists(filepath):
            os.remove(filepath)

class MockModuleManager:
    def __init__(self):
        self.loaded_modules = {}
        self.module_path = "modules"
        os.makedirs(self.module_path, exist_ok=True)

    def _get_module_filepath(self, module_name):
        return os.path.join(self.module_path, f"{module_name}.py")

    def load_module(self, module_name):
        filepath = self._get_module_filepath(module_name)
        if not self.core_memory.get("file_system").exists(filepath):
            return False

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                module_code = f.read()
            
            module_globals = {
                "core_memory": self.core_memory,
                "cpu": self.cpu,
                "file_system": self.core_memory.get("file_system"),
                "print": print # Allow modules to use print
            }
            
            exec(module_code, module_globals)
            
            if 'run' in module_globals and callable(module_globals['run']):
                self.loaded_modules[module_name] = module_globals['run']
                return True
            else:
                print(f"Error: Module '{module_name}' does not have a 'run' function.")
                return False
        except Exception as e:
            print(f"Error loading module '{module_name}': {e}")
            return False

    def unload_module(self, module_name):
        if module_name in self.loaded_modules:
            del self.loaded_modules[module_name]
            return True
        return False

    def get_available_module_names(self):
        return list(self.loaded_modules.keys())

    def run_module(self, module_name, *args, **kwargs):
        if module_name not in self.loaded_modules:
            if not self.load_module(module_name):
                print(f"Module '{module_name}' not found or failed to load.")
                return None
        
        try:
            return self.loaded_modules[module_name](*args, **kwargs)
        except Exception as e:
            print(f"Error running module '{module_name}': {e}")
            return None

# Main Execution Block
if __name__ == "__main__":
    # --- Setup ---
    print("--- Setting up Test Environment ---")
    core_memory = MockCoreMemory()
    cpu = MockCPU()
    file_system = MockFileSystem()
    module_loader = MockModuleManager()

    # Inject dependencies
    core_memory.set("cpu", cpu)
    core_memory.set("file_system", file_system)
    module_loader.core_memory = core_memory
    module_loader.cpu = cpu

    TEST_TASK_DIR = "test_modules"
    os.makedirs(TEST_TASK_DIR, exist_ok=True)
    module_loader.module_path = TEST_TASK_DIR # Use a specific directory for tests

    # --- Create a dummy module file ---
    sample_module_code = """
def run(data):
    print(f"Sample module received: {data}")
    # Simulate some processing
    processed_data = data.upper()
    core_memory.set("last_processed", processed_data)
    return f"Processed: {processed_data}"
"""
    sample_module_path = os.path.join(module_loader.module_path, "sample_module.py")
    with open(sample_module_path, "w", encoding='utf-8') as f:
        f.write(sample_module_code)
    print(f"Created dummy module: {sample_module_path}")

    # --- Test Cases ---
    print("\n--- Running Test Cases ---")

    # Test 1: Load and run a module
    print("\nRunning 'sample_module' for the first time:")
    result1 = module_loader.run_module("sample_module", "hello world")
    print("Result:", result1)
    assert result1 == "Processed: HELLO WORLD"
    assert "sample_module" in module_loader.get_available_module_names()
    assert core_memory.get("last_processed") == "HELLO WORLD"

    # Test 2: Run an already loaded module
    print("\nRunning 'sample_module' again (should be already loaded):")
    result2 = module_loader.run_module("sample_module", "another test")
    print("Result:", result2)
    assert result2 == "Processed: ANOTHER TEST"
    assert "sample_module" in module_loader.get_available_module_names()
    assert core_memory.get("last_processed") == "ANOTHER TEST"

    # Test 3: Run a non-existent module
    print("\nRunning non-existent module 'non_existent_module':")
    result3 = module_loader.run_module("non_existent_module", "this should fail")
    print("Result:", result3)
    assert result3 is None
    assert "non_existent_module" not in module_loader.get_available_module_names()

    # Test 4: Unload a module
    print("\nUnloading 'sample_module':")
    unloaded = module_loader.unload_module("sample_module")
    print(f"Unloaded 'sample_module': {unloaded}")
    assert unloaded is True
    assert "sample_module" not in module_loader.get_available_module_names()
    assert len(module_loader.loaded_modules) == 0

    # Test 5: Try to run an unloaded module (should load it automatically)
    print("\nRunning unloaded module 'sample_module' to test on-demand loading...")
    result_on_demand = module_loader.run_module("sample_module", "on demand test")
    print("Result (on demand):", result_on_demand)
    assert result_on_demand == "Processed: ON DEMAND TEST"
    assert "sample_module" in module_loader.get_available_module_names() # Should be loaded again

    # Test 6: Unload again
    print("\nUnloading 'sample_module' again:")
    unloaded_again = module_loader.unload_module("sample_module")
    print(f"Unloaded 'sample_module': {unloaded_again}")
    assert unloaded_again is True
    assert "sample_module" not in module_loader.get_available_module_names()

    # Test 7: Unload a non-existent module
    print("\nTrying to unload non-existent module 'another_non_existent':")
    unloaded_nonexistent = module_loader.unload_module("another_non_existent")
    print(f"Unloaded 'another_non_existent': {unloaded_nonexistent}")
    assert unloaded_nonexistent is False

    # --- Cleanup ---
    print("\nCleaning up test directory...")
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Removed test directory: {TEST_TASK_DIR}")

    print("\n--- All Test Cases Completed ---")