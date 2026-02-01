import os
import shutil
import re
from pathlib import Path

# Define directories for the Arabic language module
ARABIC_NL_TO_CODE_DIR = Path("./arabic_nl_to_code")
ARABIC_CODE_TO_APK_DIR = Path("./arabic_code_to_apk")
ARABIC_KNOWLEDGE_BASE_DIR = Path("./arabic_knowledge_base")

# Ensure directories exist
ARABIC_NL_TO_CODE_DIR.mkdir(parents=True, exist_ok=True)
ARABIC_CODE_TO_APK_DIR.mkdir(parents=True, exist_ok=True)
ARABIC_KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)

class ArabicNLPToCodeConverter:
    """
    Converts natural language Arabic prompts into intermediate code representations.
    This module focuses on understanding the intent and extracting key components
    from Arabic descriptions of desired APK functionality.
    """

    def __init__(self):
        self.language = "arabic"
        # Placeholder for knowledge base loading if needed
        self.knowledge_base = {}

    def parse_arabic_prompt(self, prompt: str) -> dict:
        """
        Parses an Arabic natural language prompt to extract actionable components.

        Args:
            prompt: The natural language input in Arabic.

        Returns:
            A dictionary representing the parsed intent, e.g.,
            {'action': 'create_app', 'components': ['display_message', 'get_user_input'], 'details': {'message': 'Hello World', 'input_label': 'Your Name'}}
        """
        print(f"Parsing Arabic prompt: '{prompt}'")

        parsed_intent = {'action': 'create_app', 'components': [], 'details': {}}

        # Simple keyword-based parsing for demonstration
        if "تطبيقاً بسيطاً" in prompt or "تطبيق" in prompt:
            parsed_intent['action'] = 'create_app'

        if "يعرض رسالة" in prompt or "عرض رسالة" in prompt:
            parsed_intent['components'].append('display_message')
            # Attempt to extract the message content
            message_match = re.search(r"رسالة (.*?) للمستخدم", prompt)
            if message_match:
                parsed_intent['details']['message'] = message_match.group(1).strip()

        if "يطلب اسمه" in prompt or "طلب اسمه" in prompt:
            parsed_intent['components'].append('get_user_input')
            parsed_intent['details']['input_label'] = "اسم المستخدم" # Default label

        if "يطلب بيانات" in prompt or "طلب بيانات" in prompt:
            parsed_intent['components'].append('get_user_input')
            data_match = re.search(r"يطلب (.*?) من المستخدم", prompt)
            if data_match:
                parsed_intent['details']['input_label'] = data_match.group(1).strip()

        print(f"Parsed intent: {parsed_intent}")
        return parsed_intent

    def generate_intermediate_code(self, parsed_intent: dict) -> str:
        """
        Generates an intermediate code representation (e.g., JSON, YAML, or a custom DSL)
        from the parsed Arabic intent. This serves as a bridge to the code generation lobe.

        Args:
            parsed_intent: The dictionary representing the parsed user intent.

        Returns:
            A string representing the intermediate code.
        """
        print("Generating intermediate code from parsed intent...")
        import json
        intermediate_code = json.dumps(parsed_intent, indent=4, ensure_ascii=False)
        intermediate_code_path = ARABIC_NL_TO_CODE_DIR / "intermediate_code.json"
        with open(intermediate_code_path, "w", encoding="utf-8") as f:
            f.write(intermediate_code)
        print(f"Intermediate code saved to: {intermediate_code_path}")
        return str(intermediate_code_path)

    def process_arabic_prompt(self, arabic_prompt: str) -> str:
        """
        Orchestrates the process of parsing an Arabic prompt and generating intermediate code.

        Args:
            arabic_prompt: The natural language input in Arabic.

        Returns:
            The path to the generated intermediate code file.
        """
        parsed_data = self.parse_arabic_prompt(arabic_prompt)
        intermediate_code_file = self.generate_intermediate_code(parsed_data)
        return intermediate_code_file

class ArabicCodeToAPKConverter:
    """
    Takes intermediate code representations generated from Arabic prompts
    and orchestrates the conversion to an APK. This module interacts with
    code generation and compilation lobes.
    """

    def __init__(self):
        self.language = "arabic"
        self.nl_to_code_converter = ArabicNLPToCodeConverter()
        # Placeholders for future integrations with other lobes
        self.code_generation_lobe = None # Will be set by integration
        self.apk_compiler_lobe = None   # Will be set by integration

    def set_code_generation_lobe(self, lobe):
        self.code_generation_lobe = lobe

    def set_apk_compiler_lobe(self, lobe):
        self.apk_compiler_lobe = lobe

    def convert_nl_to_apk(self, arabic_prompt: str) -> str:
        """
        Converts an Arabic natural language prompt directly into an APK file.

        Args:
            arabic_prompt: The natural language input in Arabic.

        Returns:
            The path to the generated APK file, or None if an error occurred.
        """
        print(f"\n--- Initiating Arabic NL to APK conversion for: '{arabic_prompt}' ---")

        # Step 1: Use NLP lobe to parse Arabic and generate intermediate code
        intermediate_code_path = self.nl_to_code_converter.process_arabic_prompt(arabic_prompt)

        if not intermediate_code_path:
            print("Error: Failed to generate intermediate code.")
            return None

        # Step 2: Use Code Generation lobe to create source code from intermediate code
        if not self.code_generation_lobe:
            print("Error: Code Generation Lobe is not set.")
            return None
        print("\n--- Interacting with Lobe 4_code_generation_lobe ---")
        source_code_dir = self.code_generation_lobe.generate_code_from_intermediate(intermediate_code_path)

        if not source_code_dir:
            print("Error: Failed to generate source code.")
            return None
        print(f"Source code generated in: {source_code_dir}")

        # Step 3: Use APK Compiler lobe to build the APK from source code
        if not self.apk_compiler_lobe:
            print("Error: APK Compiler Lobe is not set.")
            return None
        print("\n--- Interacting with Lobe 8_apk_compiler_lobe ---")
        apk_path = self.apk_compiler_lobe.compile_apk_from_source(source_code_dir)

        if not apk_path:
            print("Error: Failed to compile APK.")
            return None

        print(f"Successfully generated APK: {apk_path}")
        print("\n--- Arabic NL to APK conversion finished ---")
        return str(apk_path)

    def cleanup_arabic_temp_files(self):
        """Cleans up temporary files created by the Arabic NLP module."""
        print("\n--- Cleaning up temporary Arabic module files ---")
        if ARABIC_NL_TO_CODE_DIR.exists():
            shutil.rmtree(ARABIC_NL_TO_CODE_DIR)
            print(f"Removed directory: {ARABIC_NL_TO_CODE_DIR}")
        if ARABIC_CODE_TO_APK_DIR.exists():
            shutil.rmtree(ARABIC_CODE_TO_APK_DIR)
            print(f"Removed directory: {ARABIC_CODE_TO_APK_DIR}")
        if ARABIC_KNOWLEDGE_BASE_DIR.exists():
            # Be cautious with cleaning KB, but for demo purposes, we might clear it.
            # For real use, this should be more selective.
            pass # Keeping KB for potential reuse


# Example Usage (requires other lobes to be initialized and passed)
if __name__ == "__main__":
    # This block is for demonstration and testing purposes.
    # In a real scenario, 'unified_mind' would orchestrate these lobes.

    print("--- Testing Arabic NLP to Code Converter ---")
    arabic_converter_nl_to_code = ArabicNLPToCodeConverter()
    test_arabic_prompt = "أريد تطبيقاً بسيطاً يعرض رسالة ترحيب للمستخدم ويطلب اسمه."
    intermediate_file = arabic_converter_nl_to_code.process_arabic_prompt(test_arabic_prompt)
    print(f"Intermediate code file generated: {intermediate_file}")

    print("\n--- Testing Arabic Code to APK Converter (Mocked) ---")

    # Mocking other lobes for demonstration
    class MockCodeGenerationLobe:
        def generate_code_from_intermediate(self, intermediate_code_path):
            print(f"MockCodeGenerationLobe: Generating code from {intermediate_code_path}")
            mock_source_dir = ARABIC_CODE_TO_APK_DIR / "mock_android_project"
            mock_source_dir.mkdir(parents=True, exist_ok=True)
            (mock_source_dir / "MainActivity.java").write_text("public class MainActivity {}")
            (mock_source_dir / "AndroidManifest.xml").write_text("<manifest></manifest>")
            return str(mock_source_dir)

    class MockApkCompilerLobe:
        def compile_apk_from_source(self, source_code_dir):
            print(f"MockApkCompilerLobe: Compiling APK from {source_code_dir}")
            output_apk_dir = ARABIC_CODE_TO_APK_DIR / "output_apks"
            output_apk_dir.mkdir(parents=True, exist_ok=True)
            apk_file = output_apk_dir / "my_app.apk"
            apk_file.write_text("This is a mock APK file.")
            return str(apk_file)

    mock_code_gen_lobe = MockCodeGenerationLobe()
    mock_apk_compiler_lobe = MockApkCompilerLobe()

    arabic_converter_code_to_apk = ArabicCodeToAPKConverter()
    arabic_converter_code_to_apk.set_code_generation_lobe(mock_code_gen_lobe)
    arabic_converter_code_to_apk.set_apk_compiler_lobe(mock_apk_compiler_lobe)

    generated_apk_path = arabic_converter_code_to_apk.convert_nl_to_apk(test_arabic_prompt)

    if generated_apk_path:
        print(f"\nMock APK generated successfully at: {generated_apk_path}")

    # Clean up dummy files created during the test
    arabic_converter_nl_to_code.cleanup_arabic_temp_files()
    # Also clean up mock output
    if ARABIC_CODE_TO_APK_DIR.exists():
        shutil.rmtree(ARABIC_CODE_TO_APK_DIR)
        print(f"Removed directory: {ARABIC_CODE_TO_APK_DIR}")

    print("\n--- Arabic Module Demo Finished ---")