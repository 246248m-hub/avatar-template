import os
import json

class ArabicCodeGenerator:
    """
    This module is responsible for generating Python code snippets
    based on Arabic natural language descriptions processed by
    Lobe 0_language_lobe and Lobe 0_arabic_lobe.
    It acts as a bridge between natural language understanding and
    code generation for APK development.
    """

    def __init__(self, knowledge_base_dir="knowledge_base"):
        """
        Initializes the ArabicCodeGenerator.

        Args:
            knowledge_base_dir (str): The directory where knowledge bases are stored.
        """
        self.knowledge_base_dir = knowledge_base_dir
        self.arabic_to_python_mapping = self._load_mapping()
        self.generated_code = ""

    def _load_mapping(self):
        """
        Loads the Arabic to Python code mapping from a JSON file.
        This file should contain key-value pairs where keys are
        Arabic phrases/commands and values are corresponding Python code snippets.
        """
        mapping_file = os.path.join(self.knowledge_base_dir, "arabic_code_mapping.json")
        if not os.path.exists(mapping_file):
            # Create a dummy mapping if it doesn't exist for initial setup
            os.makedirs(self.knowledge_base_dir, exist_ok=True)
            default_mapping = {
                "إنشاء شاشة رئيسية": "print('Creating main screen...')\n# TODO: Implement actual screen creation logic",
                "إضافة زر": "print('Adding a button...')\n# TODO: Implement button addition logic",
                "تحديد نص": "print('Setting text...')\n# TODO: Implement text setting logic",
                "حفظ البيانات": "print('Saving data...')\n# TODO: Implement data saving logic"
            }
            with open(mapping_file, 'w', encoding='utf-8') as f:
                json.dump(default_mapping, f, ensure_ascii=False, indent=4)
            print(f"Created default mapping file at: {mapping_file}")
        
        with open(mapping_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def generate_python_code(self, arabic_description):
        """
        Generates Python code based on the provided Arabic description.
        It tries to find direct mappings in its knowledge base.
        If no direct mapping is found, it will indicate that the command
        is not yet supported.

        Args:
            arabic_description (str): The Arabic natural language description of the desired functionality.

        Returns:
            str: The generated Python code snippet or a message indicating lack of support.
        """
        self.generated_code = ""
        # Simple approach: look for exact matches in the mapping
        if arabic_description in self.arabic_to_python_mapping:
            self.generated_code = self.arabic_to_python_mapping[arabic_description]
        else:
            # Attempt to find keywords or partial matches (more advanced NLP would be needed here)
            # For this example, we'll stick to direct mapping for clarity.
            self.generated_code = f"# Unsupported command: '{arabic_description}'. Please add it to the mapping."
            print(f"Warning: No direct mapping found for '{arabic_description}'.")
        return self.generated_code

    def integrate_with_nlp(self, nlp_output):
        """
        Integrates the output from the NLP lobes (which should be a structured
        representation or a processed Arabic string ready for code generation).
        This is a placeholder for a more complex integration where nlp_output
        might be a list of commands, parameters, etc.

        Args:
            nlp_output (str or dict or list): Processed output from NLP modules.
                                             For this example, we assume it's a string
                                             that can be directly passed to
                                             generate_python_code.
        """
        if isinstance(nlp_output, str):
            self.generate_python_code(nlp_output)
        elif isinstance(nlp_output, dict) and 'arabic_text' in nlp_output:
            # Example: if NLP lobe returns a dict with the Arabic text
            self.generate_python_code(nlp_output['arabic_text'])
        elif isinstance(nlp_output, list):
            # Example: if NLP lobe returns a list of commands
            for command in nlp_output:
                self.generated_code += self.generate_python_code(command) + "\n"
        else:
            print("Error: Unexpected NLP output format. Expected string, dict, or list.")
            self.generated_code = "# Error in NLP integration."

    def get_generated_code(self):
        """
        Returns the last generated Python code.
        """
        return self.generated_code

    def save_generated_code(self, filepath="generated_app_logic.py"):
        """
        Saves the generated Python code to a file.

        Args:
            filepath (str): The path to save the generated code.
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.generated_code)
        print(f"Generated Python code saved to: {filepath}")

    def cleanup_resources(self):
        """
        Placeholder for any cleanup operations specific to this module.
        """
        print("ArabicCodeGenerator cleanup operations completed.")


# --- Simulation and Integration Example ---

if __name__ == "__main__":
    print("--- Initiating Lobe 4_code_generation_lobe ---")

    # Initialize the ArabicCodeGenerator
    code_generator = ArabicCodeGenerator()

    # --- Simulate input from Lobe 0_arabic_lobe (e.g., "إنشاء شاشة رئيسية") ---
    # This would typically be the output from the Arabic NLP processing.
    simulated_arabic_input_1 = "إنشاء شاشة رئيسية"
    print(f"\nSimulating Arabic input: '{simulated_arabic_input_1}'")
    generated_code_1 = code_generator.generate_python_code(simulated_arabic_input_1)
    print(f"Generated Code 1:\n{generated_code_1}")

    # --- Simulate another input ---
    simulated_arabic_input_2 = "إضافة زر"
    print(f"\nSimulating Arabic input: '{simulated_arabic_input_2}'")
    generated_code_2 = code_generator.generate_python_code(simulated_arabic_input_2)
    print(f"Generated Code 2:\n{generated_code_2}")
    
    # --- Simulate input for an unsupported command ---
    simulated_arabic_input_3 = "تغيير لون الخلفية"
    print(f"\nSimulating Arabic input: '{simulated_arabic_input_3}'")
    generated_code_3 = code_generator.generate_python_code(simulated_arabic_input_3)
    print(f"Generated Code 3:\n{generated_code_3}")

    # --- Simulate integration with NLP output (assuming NLP returns a list of commands) ---
    simulated_nlp_output_list = ["إنشاء شاشة رئيسية", "إضافة زر", "تحديد نص"]
    print(f"\nSimulating integration with NLP output (list): {simulated_nlp_output_list}")
    code_generator.integrate_with_nlp(simulated_nlp_output_list)
    integrated_code = code_generator.get_generated_code()
    print(f"Integrated Generated Code:\n{integrated_code}")

    # --- Save the generated code ---
    code_generator.save_generated_code("app_ui_logic.py")

    # --- Cleanup ---
    code_generator.cleanup_resources()

    print("\n--- Lobe 4_code_generation_lobe Demo Finished ---")
    print("\n--- Initiating next step: Lobe 8_apk_compiler_lobe ---")
    # In a real scenario, 'integrated_code' would be passed to Lobe 8_apk_compiler_lobe
    # or a subsequent processing step.