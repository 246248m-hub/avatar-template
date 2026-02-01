import os
import shutil
import subprocess
from pathlib import Path

# Assume these constants are defined elsewhere and accessible
# For demonstration purposes, let's define them here
KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
ARABIC_CODE_TO_APK_DIR = Path("./arabic_code_to_apk")
ANDROID_PROJECT_TEMPLATE_DIR = Path("./android_project_template")
OUTPUT_APKS_DIR = Path("./output_apks")

# --- Lobe 1_arabic_parsing_lobe ---
# This lobe focuses on parsing natural language Arabic into a structured representation.

class ArabicInstructionParser:
    """
    Parses natural language Arabic instructions into a structured format
    suitable for code generation.
    """
    def __init__(self, knowledge_base_path: Path):
        self.knowledge_base_path = knowledge_base_path
        # In a real scenario, this would load and process linguistic resources
        # from the knowledge_base_path. For this example, we'll use a simple mapping.

    def parse(self, arabic_text: str) -> dict:
        """
        Parses Arabic text into a structured instruction dictionary.

        Args:
            arabic_text: The natural language Arabic instruction.

        Returns:
            A dictionary representing the parsed instruction.
            Example:
            {
                "action": "create",
                "element": "button",
                "properties": {
                    "text": "اضغط هنا",
                    "on_click": "show_message('مرحبا')
                }
            }
        """
        parsed_instruction = {}
        arabic_text = arabic_text.strip()

        # Basic keyword matching for demonstration
        if "إنشاء" in arabic_text or "أضف" in arabic_text:
            parsed_instruction["action"] = "create"
        elif "عرض" in arabic_text or "إظهار" in arabic_text:
            parsed_instruction["action"] = "display"
        elif "تغيير" in arabic_text or "تعديل" in arabic_text:
            parsed_instruction["action"] = "modify"
        elif "حذف" in arabic_text or "إزالة" in arabic_text:
            parsed_instruction["action"] = "delete"

        if "زر" in arabic_text:
            parsed_instruction["element"] = "button"
            # Extract text for button
            if "النص" in arabic_text:
                try:
                    text_index = arabic_text.index("النص") + len("النص")
                    button_text_end = arabic_text.find("الذي", text_index) if "الذي" in arabic_text[text_index:] else len(arabic_text)
                    button_text = arabic_text[text_index:button_text_end].strip()
                    parsed_instruction["properties"] = {"text": button_text}
                except ValueError:
                    pass # Handle cases where 'النص' is present but no value follows

            if "عند النقر" in arabic_text:
                try:
                    onclick_index = arabic_text.index("عند النقر") + len("عند النقر")
                    onclick_code_part = arabic_text[onclick_index:].strip()
                    # Simple extraction for function calls
                    if "عرض رسالة" in onclick_code_part:
                        message_start = onclick_code_part.index("عرض رسالة") + len("عرض رسالة")
                        message_end = onclick_code_part.find("'", message_start) if "'" in onclick_code_part[message_start:] else len(onclick_code_part)
                        message_content = onclick_code_part[message_start:message_end].strip()
                        if "properties" not in parsed_instruction:
                            parsed_instruction["properties"] = {}
                        parsed_instruction["properties"]["on_click"] = f"show_message('{message_content}')"
                except ValueError:
                    pass # Handle cases where 'عند النقر' is present but no value follows


        elif "تسمية" in arabic_text or "نص" in arabic_text: # Assuming 'نص' can refer to a label/text view
             parsed_instruction["element"] = "label"
             if "النص" in arabic_text:
                try:
                    text_index = arabic_text.index("النص") + len("النص")
                    label_text_end = arabic_text.find("حيث", text_index) if "حيث" in arabic_text[text_index:] else len(arabic_text)
                    label_text = arabic_text[text_index:label_text_end].strip()
                    if "properties" not in parsed_instruction:
                        parsed_instruction["properties"] = {}
                    parsed_instruction["properties"]["text"] = label_text
                except ValueError:
                    pass

        return parsed_instruction

# --- Lobe 0_arabic_lobe (Conceptual Extension) ---
# This lobe would orchestrate the Arabic parsing and initial code generation.
# We are building a functional module that could be part of this lobe.

class ArabicModule:
    """
    The core module for handling Arabic natural language to APK generation.
    This is a conceptual representation of what Lobe 0_arabic_lobe might encompass.
    """
    def __init__(self, knowledge_base_path: Path, output_dir: Path):
        self.parser = ArabicInstructionParser(knowledge_base_path)
        self.code_generator = None # Placeholder, will be provided by Lobe 4
        self.apk_compiler = None   # Placeholder, will be provided by Lobe 8
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def process_instruction(self, arabic_instruction_nl: str) -> Path:
        """
        Processes a single Arabic natural language instruction,
        parses it, generates intermediate code, and potentially compiles to APK.

        Args:
            arabic_instruction_nl: The natural language Arabic instruction.

        Returns:
            Path to the generated APK if successful, otherwise None.
        """
        print(f"Processing Arabic instruction: '{arabic_instruction_nl}'")
        parsed_data = self.parser.parse(arabic_instruction_nl)
        print(f"Parsed data: {parsed_data}")

        if not parsed_data:
            print("Failed to parse instruction.")
            return None

        # In a full system, this would call Lobe 4 to generate code
        # and then Lobe 8 to compile it. For now, we simulate this.
        generated_code = self._generate_intermediate_code(parsed_data)
        if generated_code:
            print(f"Generated intermediate code:\n{generated_code}")
            # In a real flow, this generated_code would be passed to Lobe 4
            # and then to Lobe 8.
            # For this specific task, we'll assume the code generation part
            # will produce a Python script that can be compiled into an APK.
            # Let's simulate the output of code generation.
            temp_code_file = self.output_dir / "generated_app.py"
            temp_code_file.write_text(generated_code)
            print(f"Intermediate code saved to: {temp_code_file}")

            # Simulate APK compilation using a placeholder function from Lobe 8
            # In a real scenario, this would be a call to self.apk_compiler.compile(...)
            apk_path = self._simulate_apk_compilation(temp_code_file)
            return apk_path
        else:
            print("Failed to generate intermediate code.")
            return None

    def _generate_intermediate_code(self, parsed_data: dict) -> str:
        """
        Simulates the generation of intermediate code (e.g., Python for Kivy/BeeWare).
        This logic would be part of Lobe 4_code_generation_lobe.
        """
        if not parsed_data.get("action") or not parsed_data.get("element"):
            return ""

        element = parsed_data["element"]
        action = parsed_data["action"]
        properties = parsed_data.get("properties", {})

        code_lines = []
        code_lines.append("from kivymd.app import MDApp")
        code_lines.append("from kivymd.uix.screen import MDScreen")
        code_lines.append("from kivymd.uix.button import MDRaisedButton")
        code_lines.append("from kivymd.uix.label import MDLabel")
        code_lines.append("from kivymd.uix.dialog import MDDialog")
        code_lines.append("from kivy.lang import Builder\n")

        code_lines.append("KV = '''")
        code_lines.append("<MainScreen>:")
        code_lines.append("    md_bg_color: app.theme_cls.backgroundColor")

        # Add elements based on parsed data
        if element == "button":
            button_text = properties.get("text", "زر")
            onclick_action = properties.get("on_click", "")
            code_lines.append(f"    MDRaisedButton:")
            code_lines.append(f"        text: '{button_text}'")
            code_lines.append(f"        pos_hint: {{'center_x': 0.5, 'center_y': 0.5}}")
            if onclick_action:
                # Kivy/KivyMD often uses direct method calls or event binding.
                # For simplicity, we'll assume a direct method call is defined in the app.
                code_lines.append(f"        on_release: app.handle_button_click('{onclick_action}')")
        elif element == "label":
            label_text = properties.get("text", "نص")
            code_lines.append(f"    MDLabel:")
            code_lines.append(f"        text: '{label_text}'")
            code_lines.append(f"        halign: 'center'")
            code_lines.append(f"        pos_hint: {{'center_x': 0.5, 'center_y': 0.6}}") # Slightly above center

        code_lines.append("'''\n")

        code_lines.append("class MainScreen(MDScreen):")
        code_lines.append("    pass\n")

        code_lines.append("class GeneratedApp(MDApp):")
        code_lines.append("    def build(self):")
        code_lines.append("        self.theme_cls.theme_style = 'Dark'")
        code_lines.append("        self.screen = MainScreen()")
        code_lines.append("        return self.screen\n")

        code_lines.append("    def handle_button_click(self, action):")
        code_lines.append("        # This method would parse and execute the action string")
        code_lines.append("        print(f'Executing action: {action}')")
        code_lines.append("        if action.startswith('show_message('):")
        code_lines.append("            message = action[action.find('(') + 1 : action.rfind(')')].strip(\"'\")")
        code_lines.append("            self.show_alert_dialog('رسالة', message)")
        code_lines.append("\n    def show_alert_dialog(self, title, text):")
        code_lines.append("        dialog = MDDialog(")
        code_lines.append("            title=title,")
        code_lines.append("            text=text,")
        code_lines.append("            md_bg_color=self.theme_cls.bg_dark,")
        code_lines.append("            buttons=[")
        code_lines.append("                MDDialog(dismiss=False),") # Placeholder, typically has buttons
        code_lines.append("            ]")
        code_lines.append("        )")
        code_lines.append("        dialog.open()\n")

        code_lines.append("if __name__ == '__main__':")
        code_lines.append("    GeneratedApp().run()")

        return "\n".join(code_lines)


    def _simulate_apk_compilation(self, python_script_path: Path) -> Path:
        """
        Simulates the APK compilation process.
        This logic would be part of Lobe 8_apk_compiler_lobe.
        It assumes a tool like Buildozer or Briefcase is available.
        For demonstration, we'll just create a dummy APK file.
        """
        print(f"Simulating APK compilation for: {python_script_path}")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        apk_filename = python_script_path.stem + ".apk"
        dummy_apk_path = self.output_dir / apk_filename

        # In a real scenario, you'd use a build tool here.
        # Example with Buildozer (conceptual):
        # try:
        #     # Create a basic .buildozer/spec file if it doesn't exist
        #     buildozer_dir = Path("./.buildozer")
        #     buildozer_dir.mkdir(exist_ok=True)
        #     spec_file = buildozer_dir / "spec"
        #     if not spec_file.exists():
        #         spec_file.write_text(f"[app]\n\
        # title = Generated Arabic App\n\
        # package.name = com.example.arabicapp\n\
        # package.domain = example\n\
        # source.dir = .\n\
        # source.include_exts = py,png,jpg,kv,atlas\n\
        # version = 0.1\n\
        # python_version = 3.8\n\
        # requirements = python3,kivy\n\
        # android.sdk_path = /path/to/android/sdk\n\
        # android.ndk_path = /path/to/android/ndk")
        #
        #     # Copy the generated python script to the root of the simulated buildozer project
        #     shutil.copy(python_script_path, ".")
        #
        #     # Run buildozer
        #     # Ensure buildozer is installed: pip install buildozer
        #     # Ensure Android SDK/NDK are set up and pointed to in the spec file.
        #     subprocess.run(["buildozer", "-f", str(spec_file), "android", "debug"], check=True, cwd=".")
        #
        #     # Find the generated APK (this path might vary)
        #     # For example, it might be in bin/
        #     generated_apk_path = Path("./bin") / f"{spec_file.parts[-1].split('.')[0]}-0.1-debug.apk"
        #     if generated_apk_path.exists():
        #         shutil.move(generated_apk_path, dummy_apk_path)
        #         print(f"Successfully compiled APK to: {dummy_apk_path}")
        #     else:
        #         print("Buildozer finished, but APK not found in expected location.")
        #         return None
        #
        # except FileNotFoundError:
        #     print("Buildozer command not found. Please ensure Buildozer is installed and in your PATH.")
        #     return None
        # except subprocess.CalledProcessError as e:
        #     print(f"Buildozer failed: {e}")
        #     return None
        # except Exception as e:
        #     print(f"An unexpected error occurred during Buildozer execution: {e}")
        #     return None


        # Dummy APK creation for demonstration if buildozer is not configured/available
        try:
            with open(dummy_apk_path, "w") as f:
                f.write(f"This is a dummy APK file for {python_script_path.name}\n")
                f.write(f"Generated from parsed Arabic: {python_script_path.stem}\n")
            print(f"Created dummy APK file at: {dummy_apk_path}")
            return dummy_apk_path
        except Exception as e:
            print(f"Error creating dummy APK: {e}")
            return None

    def cleanup_arabic_temp_files(self):
        """Cleans up temporary files generated by the Arabic module."""
        print("\n--- Cleaning up Arabic Module temporary files ---")
        if self.output_dir.exists():
            for item in self.output_dir.iterdir():
                if item.is_file():
                    try:
                        item.unlink()
                        print(f"Removed temporary file: {item}")
                    except OSError as e:
                        print(f"Error removing file {item}: {e}")
                elif item.is_dir():
                    try:
                        shutil.rmtree(item)
                        print(f"Removed temporary directory: {item}")
                    except OSError as e:
                        print(f"Error removing directory {item}: {e}")

        # Also clean up mock output if it exists
        if ARABIC_CODE_TO_APK_DIR.exists():
            shutil.rmtree(ARABIC_CODE_TO_APK_DIR)
            print(f"Removed directory: {ARABIC_CODE_TO_APK_DIR}")

        print("\n--- Arabic Module Temporary File Cleanup Finished ---")


# Example Usage (for testing this module in isolation):
if __name__ == "__main__":
    # Setup dummy directories if they don't exist
    KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)
    ARABIC_CODE_TO_APK_DIR.mkdir(exist_ok=True)
    ANDROID_PROJECT_TEMPLATE_DIR.mkdir(exist_ok=True)
    OUTPUT_APKS_DIR.mkdir(exist_ok=True)

    # Initialize the Arabic module
    arabic_module = ArabicModule(KNOWLEDGE_BASE_DIR, OUTPUT_APKS_DIR)

    # Test cases
    test_prompt_1 = "أضف زرًا بنص \"اضغط هنا\" وعند النقر عرض رسالة 'مرحبا بالعالم'"
    test_prompt_2 = "إنشاء تسمية بالنص 'اسم التطبيق'"
    test_prompt_3 = "أضف زرًا بنص 'إرسال'"
    test_prompt_4 = "عرض نص 'هذه رسالة توضيحية'"

    print("\n--- Running Arabic Module Demo ---")

    apk_path_1 = arabic_module.process_instruction(test_prompt_1)
    if apk_path_1:
        print(f"Generated APK for prompt 1: {apk_path_1}")

    apk_path_2 = arabic_module.process_instruction(test_prompt_2)
    if apk_path_2:
        print(f"Generated APK for prompt 2: {apk_path_2}")

    apk_path_3 = arabic_module.process_instruction(test_prompt_3)
    if apk_path_3:
        print(f"Generated APK for prompt 3: {apk_path_3}")

    apk_path_4 = arabic_module.process_instruction(test_prompt_4)
    if apk_path_4:
        print(f"Generated APK for prompt 4: {apk_path_4}")


    # Clean up generated files
    arabic_module.cleanup_arabic_temp_files()

    # Clean up dummy directories created for demo
    if KNOWLEDGE_BASE_DIR.exists():
        shutil.rmtree(KNOWLEDGE_BASE_DIR)
    if OUTPUT_APKS_DIR.exists():
        shutil.rmtree(OUTPUT_APKS_DIR)
    if ANDROID_PROJECT_TEMPLATE_DIR.exists():
        shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)


    print("\n--- Arabic Module Demo Finished ---")