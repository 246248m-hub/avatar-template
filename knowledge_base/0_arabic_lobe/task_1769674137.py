import os
import shutil
import subprocess
from pathlib import Path

# Assume these constants and functions are defined elsewhere and are accessible.
# For the purpose of this snippet, we'll define placeholders where necessary.

# Placeholder for potential knowledge base directory
KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
if not KNOWLEDGE_BASE_DIR.exists():
    KNOWLEDGE_BASE_DIR.mkdir()

# Placeholder for base Android project structure
ANDROID_PROJECT_TEMPLATE_DIR = Path("./android_project_template")
if not ANDROID_PROJECT_TEMPLATE_DIR.exists():
    # In a real scenario, this would be a valid Android project template
    # For demonstration, we'll create a minimal structure
    ANDROID_PROJECT_TEMPLATE_DIR.mkdir()
    (ANDROID_PROJECT_TEMPLATE_DIR / "app").mkdir()
    (ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src").mkdir()
    (ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main").mkdir()
    (ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "java").mkdir()
    (ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "java" / "com").mkdir()
    (ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "java" / "com" / "example").mkdir()
    (ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "java" / "com" / "example" / "myapp").mkdir()
    (ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "java" / "com" / "example" / "myapp" / "MainActivity.java").touch()
    (ANDROID_PROJECT_TEMPLATE_DIR / "app" / "build.gradle").touch()
    (ANDROID_PROJECT_TEMPLATE_DIR / "build.gradle").touch()
    (ANDROID_PROJECT_TEMPLATE_DIR / "settings.gradle").touch()
    (ANDROID_PROJECT_TEMPLATE_DIR / "gradlew").touch()
    (ANDROID_PROJECT_TEMPLATE_DIR / "gradlew.bat").touch()
    (ANDROID_PROJECT_TEMPLATE_DIR / "gradle").mkdir()
    (ANDROID_PROJECT_TEMPLATE_DIR / "gradle" / "wrapper").mkdir()
    (ANDROID_PROJECT_TEMPLATE_DIR / "gradle" / "wrapper" / "gradle-wrapper.jar").touch()
    (ANDROID_PROJECT_TEMPLATE_DIR / "gradle" / "wrapper" / "gradle-wrapper.properties").touch()


# Placeholder for Android SDK path
ANDROID_SDK_ROOT = Path(os.environ.get("ANDROID_SDK_ROOT", "/path/to/android/sdk")) # This should be set to your actual SDK path
if not ANDROID_SDK_ROOT.exists():
    print(f"Warning: ANDROID_SDK_ROOT not found at {ANDROID_SDK_ROOT}. APK compilation may fail.")
    # For demonstration, create dummy SDK tools if not found
    if not (ANDROID_SDK_ROOT / "cmdline-tools" / "latest" / "bin" / "sdkmanager").exists():
        (ANDROID_SDK_ROOT / "cmdline-tools" / "latest" / "bin").mkdir(parents=True, exist_ok=True)
        (ANDROID_SDK_ROOT / "cmdline-tools" / "latest" / "bin" / "sdkmanager").touch()
    if not (ANDROID_SDK_ROOT / "platform-tools" / "adb").exists():
        (ANDROID_SDK_ROOT / "platform-tools").mkdir(parents=True, exist_ok=True)
        (ANDROID_SDK_ROOT / "platform-tools" / "adb").touch()
    if not (ANDROID_SDK_ROOT / "build-tools").exists():
        (ANDROID_SDK_ROOT / "build-tools").mkdir(parents=True, exist_ok=True)
    if not (ANDROID_SDK_ROOT / "platforms").exists():
        (ANDROID_SDK_ROOT / "platforms").mkdir(parents=True, exist_ok=True)


class ArabicNLPProcessor:
    """
    Processes Arabic natural language input to extract semantic meaning
    relevant for Android application generation.
    """
    def __init__(self, knowledge_base_path: Path = KNOWLEDGE_BASE_DIR):
        self.knowledge_base = knowledge_base_path
        # In a real implementation, this would load and process Arabic NLP models
        # e.g., using Farasa, CAMeL Tools, or other libraries.
        print(f"ArabicNLPProcessor initialized with knowledge base: {self.knowledge_base}")

    def parse_arabic_intent(self, arabic_text: str) -> dict:
        """
        Parses Arabic text to identify the user's intent and extract parameters.

        Args:
            arabic_text: The natural language Arabic input string.

        Returns:
            A dictionary representing the parsed intent, e.g.,
            {'action': 'create_app', 'app_name': 'MyArabicApp', 'features': ['button', 'text_view']}
        """
        print(f"Parsing Arabic text: '{arabic_text}'")
        # This is a simplified mock. A real implementation would involve
        # sophisticated NLP techniques:
        # 1. Tokenization
        # 2. Part-of-Speech Tagging
        # 3. Named Entity Recognition (for app names, feature names)
        # 4. Intent Recognition (what the user wants to do)
        # 5. Slot Filling (extracting parameters for the intent)

        parsed_data = {}
        arabic_text_lower = arabic_text.lower()

        if "إنشاء تطبيق" in arabic_text_lower or "اصنع تطبيق" in arabic_text_lower:
            parsed_data['action'] = 'create_app'
            # Extract app name (simplified: looking for words after 'تطبيق')
            parts = arabic_text.split("إنشاء تطبيق")
            if len(parts) > 1:
                app_name_part = parts[1].strip()
                # Try to find a common naming convention or just take the first few words
                words = app_name_part.split()
                if words:
                    # Filter out common Arabic conjunctions or prepositions if any
                    common_fillers = ["باسم", "اسمه", "اسمه"]
                    filtered_words = [w for w in words if w not in common_fillers]
                    if filtered_words:
                        parsed_data['app_name'] = "".join(filtered_words[:3]) # Take first 3 words as app name
                    else:
                        parsed_data['app_name'] = "DefaultApp"
                else:
                    parsed_data['app_name'] = "DefaultApp"
            else:
                parsed_data['app_name'] = "DefaultApp"

            features = []
            if "زر" in arabic_text_lower:
                features.append("button")
            if "نص" in arabic_text_lower or "حقل نصي" in arabic_text_lower:
                features.append("text_view")
            if "صورة" in arabic_text_lower:
                features.append("image_view")
            if "قائمة" in arabic_text_lower:
                features.append("list_view")

            if features:
                parsed_data['features'] = features
            else:
                parsed_data['features'] = ["button"] # Default feature if none specified

        elif "إضافة زر" in arabic_text_lower:
            parsed_data['action'] = 'add_feature'
            parsed_data['feature_type'] = 'button'
            # Extract button label if specified
            parts = arabic_text.split("باسم")
            if len(parts) > 1:
                button_label = parts[1].strip()
                parsed_data['button_label'] = button_label
            else:
                parsed_data['button_label'] = "Click Me"

        elif "إضافة حقل نصي" in arabic_text_lower:
            parsed_data['action'] = 'add_feature'
            parsed_data['feature_type'] = 'text_view'
            parts = arabic_text.split("باسم")
            if len(parts) > 1:
                text_hint = parts[1].strip()
                parsed_data['text_hint'] = text_hint
            else:
                parsed_data['text_hint'] = "Enter text"

        else:
            parsed_data['action'] = 'unknown'
            parsed_data['original_text'] = arabic_text

        print(f"Parsed intent: {parsed_data}")
        return parsed_data

    def extract_ui_elements_from_description(self, arabic_description: str) -> list:
        """
        Extracts UI elements and their properties from a descriptive Arabic text.

        Args:
            arabic_description: A natural language description of UI elements.

        Returns:
            A list of dictionaries, where each dictionary describes a UI element.
            Example: [{'type': 'button', 'text': 'اضغط هنا', 'id': 'my_button'}, ...]
        """
        print(f"Extracting UI elements from description: '{arabic_description}'")
        ui_elements = []
        # This is a highly simplified mock. Real implementation would be complex.
        # It would involve identifying patterns for buttons, text fields, labels, etc.
        # and extracting attributes like text content, IDs, visibility, etc.

        # Example patterns:
        # "زر اسمه 'ابدأ'" -> button with text 'ابدأ' and id 'abda'
        # "حقل نصي بتلميح 'أدخل اسمك'" -> text field with hint 'أدخل اسمك' and id 'enter_your_name'
        # "عنوان نصي 'مرحباً بالعالم'" -> text view with text 'مرحباً بالعالم' and id 'hello_world'

        import re

        # Basic pattern for a button with a label
        button_matches = re.findall(r"زر اسمه '([^']+)'", arabic_description)
        for label in button_matches:
            ui_elements.append({'type': 'button', 'text': label, 'id': label.lower().replace(" ", "_")})

        # Basic pattern for a text view with content
        textview_matches = re.findall(r"عنوان نصي '([^']+)'", arabic_description)
        for content in textview_matches:
            ui_elements.append({'type': 'text_view', 'text': content, 'id': content.lower().replace(" ", "_")})

        # Basic pattern for a text input field with a hint
        textfield_matches = re.findall(r"حقل نصي بتلميح '([^']+)'", arabic_description)
        for hint in textfield_matches:
            ui_elements.append({'type': 'edit_text', 'hint': hint, 'id': hint.lower().replace(" ", "_").replace("'", "")})

        print(f"Extracted UI elements: {ui_elements}")
        return ui_elements

    def generate_arabic_code_snippets(self, ui_elements: list, language_preference: str = "java") -> dict:
        """
        Generates code snippets for UI elements in the preferred language.

        Args:
            ui_elements: A list of dictionaries describing UI elements.
            language_preference: The programming language for code generation ('java', 'kotlin').

        Returns:
            A dictionary where keys are UI element IDs and values are the generated code snippets.
        """
        print(f"Generating code snippets for {language_preference} for {len(ui_elements)} UI elements.")
        code_snippets = {}

        # This is a simplified mock. A real implementation would use templates
        # and logic to generate accurate code for Java/Kotlin Android.

        if language_preference.lower() == "java":
            for element in ui_elements:
                element_id = element.get('id', f"element_{len(code_snippets)}")
                code = f"// Generated for {element.get('type')}\n"
                if element.get('type') == 'button':
                    code += f"Button {element_id} = findViewById(R.id.{element_id});\n"
                    code += f"{element_id}.setText(\"{element.get('text', 'Button')}\");\n"
                    code += f"{element_id}.setOnClickListener(v -> {{ /* TODO: Add action */ }});\n"
                elif element.get('type') == 'text_view':
                    code += f"TextView {element_id} = findViewById(R.id.{element_id});\n"
                    code += f"{element_id}.setText(\"{element.get('text', '')}\");\n"
                elif element.get('type') == 'edit_text':
                    code += f"EditText {element_id} = findViewById(R.id.{element_id});\n"
                    code += f"{element_id}.setHint(\"{element.get('hint', '')}\");\n"
                else:
                    code += f"// Unknown UI element type: {element.get('type')}\n"
                code_snippets[element_id] = code
        else:
            # Placeholder for Kotlin generation
            print("Kotlin code generation not yet implemented in this mock.")
            for element in ui_elements:
                element_id = element.get('id', f"element_{len(code_snippets)}")
                code_snippets[element_id] = f"// Kotlin code generation for {element.get('type')} not implemented."

        print(f"Generated {len(code_snippets)} code snippets.")
        return code_snippets


# Lobe 0_arabic_lobe - Placeholder for the Arabic parsing and generation logic
class Lobe0ArabicLobe:
    def __init__(self):
        self.nlp_processor = ArabicNLPProcessor()
        print("--- Lobe 0: Arabic Lobe Initialized ---")

    def process_arabic_request(self, arabic_prompt: str) -> dict:
        """
        Processes an Arabic natural language request to generate an APK structure.

        Args:
            arabic_prompt: The user's request in Arabic.

        Returns:
            A dictionary containing parsed intent and initial UI elements.
        """
        print(f"\n--- Lobe 0: Processing Arabic Request ---")
        parsed_intent = self.nlp_processor.parse_arabic_intent(arabic_prompt)

        # If the intent is to create an app, further parse for UI elements
        if parsed_intent.get('action') == 'create_app':
            # In a more advanced scenario, the prompt might also contain descriptions
            # of UI elements directly, or we might need to query the user for them.
            # For this demo, we'll assume the prompt might imply some UI.
            # Example: "إنشاء تطبيق اسمه 'حاسبة' مع أزرار للأرقام وحقل للعرض"
            # This part would ideally be handled by more sophisticated parsing
            # or follow-up prompts.
            app_name = parsed_intent.get('app_name', 'NewApp')
            features = parsed_intent.get('features', [])

            # Mocking UI element extraction based on features
            mock_ui_description = ""
            if 'button' in features:
                mock_ui_description += "زر اسمه 'حساب' "
            if 'text_view' in features:
                mock_ui_description += "عنوان نصي 'النتيجة' "
            if 'edit_text' in features:
                mock_ui_description += "حقل نصي بتلميح 'أدخل قيمة' "

            if mock_ui_description:
                ui_elements = self.nlp_processor.extract_ui_elements_from_description(mock_ui_description)
                parsed_intent['ui_elements'] = ui_elements
            else:
                parsed_intent['ui_elements'] = []

        print(f"--- Lobe 0: Arabic Request Processed ---")
        return parsed_intent


# Lobe 4_code_generation_lobe - Placeholder for code generation
class Lobe4CodeGenerationLobe:
    def __init__(self):
        self.nlp_processor = ArabicNLPProcessor() # Re-using NLP for its code generation capabilities
        print("--- Lobe 4: Code Generation Lobe Initialized ---")

    def generate_android_code(self, parsed_data: dict) -> dict:
        """
        Generates Android specific code snippets based on parsed data.

        Args:
            parsed_data: A dictionary containing parsed intent and UI elements.

        Returns:
            A dictionary containing generated code snippets (e.g., for MainActivity).
        """
        print("\n--- Lobe 4: Generating Android Code ---")
        code_snippets = {}
        language = "java" # Default to Java

        if parsed_data.get('action') == 'create_app':
            app_name = parsed_data.get('app_name', 'GeneratedApp')
            ui_elements = parsed_data.get('ui_elements', [])

            # Generate UI element declarations and initializations
            activity_code_elements = self.nlp_processor.generate_arabic_code_snippets(ui_elements, language_preference=language)

            # Construct a basic MainActivity structure
            main_activity_java_code = f"""
package com.example.{app_name.lower().replace(" ", "_")};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{app_name.lower().replace(" ", "_")}_activity); // Assuming layout file name convention

        // Declare and initialize UI elements
"""
            for element_id, code in activity_code_elements.items():
                main_activity_java_code += f"        {code.strip().replace('// Generated for', '// ')}\n"

            main_activity_java_code += f"""
        // TODO: Add more specific logic based on intent and features
        // For example, setting up click listeners or data handling.

    }}
}}
"""
            code_snippets['MainActivity.java'] = main_activity_java_code
            code_snippets['R.layout.{app_name.lower().replace(" ", "_")}_activity.xml'] = self._generate_layout_xml(ui_elements, app_name)

        elif parsed_data.get('action') == 'add_feature':
            # Logic to add a feature to an existing structure (more complex)
            print("Adding feature to existing app structure is a complex operation, not fully implemented in this mock.")
            pass

        else:
            print(f"Unknown action for code generation: {parsed_data.get('action')}")

        print(f"--- Lobe 4: Generated {len(code_snippets)} code artifacts ---")
        return code_snippets

    def _generate_layout_xml(self, ui_elements: list, app_name: str) -> str:
        """
        Generates a basic XML layout file for an Android Activity.
        This is a simplified mock.
        """
        print(f"Generating layout XML for {app_name}...")
        xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{app_name.lower().replace(' ', '_').capitalize()}Activity">
"""
        y_offset = 50
        for i, element in enumerate(ui_elements):
            element_id = element.get('id', f"element_{i}")
            element_type = element.get('type')
            xml_content += f'    <{"Button" if element_type == "button" else "TextView" if element_type == "text_view" else "EditText"} android:id="@+id/{element_id}"\n'
            xml_content += f'        android:layout_width="wrap_content"\n'
            xml_content += f'        android:layout_height="wrap_content"\n'
            xml_content += f'        app:layout_constraintTop_toTopOf="parent"\n'
            xml_content += f'        app:layout_constraintStart_toStartOf="parent"\n'
            xml_content += f'        app:layout_constraintEnd_toEndOf="parent"\n'
            xml_content += f'        app:layout_constraintHorizontal_bias="0.5"\n'
            xml_content += f'        app:layout_constraintVertical_bias="{0.1 + (i * 0.2)}"\n' # Distribute vertically

            if element_type == 'button':
                xml_content += f'        android:text="{element.get("text", "Button")}" />\n'
            elif element_type == 'text_view':
                xml_content += f'        android:text="{element.get("text", "")}" />\n'
            elif element_type == 'edit_text':
                xml_content += f'        android:hint="{element.get("hint", "")}" />\n'
            else:
                xml_content += f'        tools:text="Unknown Element"\n'
                xml_content += f'        />\n'

        xml_content += "</androidx.constraintlayout.widget.ConstraintLayout>"
        return xml_content


# Lobe 8_apk_compiler_lobe - Placeholder for APK compilation
class Lobe8ApkCompilerLobe:
    def __init__(self, android_sdk_path: Path = ANDROID_SDK_ROOT,
                 android_project_template: Path = ANDROID_PROJECT_TEMPLATE_DIR):
        self.android_sdk_path = android_sdk_path
        self.android_project_template = android_project_template
        self.gradle_wrapper_path = self.android_project_template / "gradlew"
        if not self.gradle_wrapper_path.exists():
            print(f"Error: Gradle wrapper not found at {self.gradle_wrapper_path}")
            # Attempt to find gradlew in template dir if structure varies
            possible_gradlew = list(self.android_project_template.glob("**/gradlew"))
            if possible_gradlew:
                self.gradle_wrapper_path = possible_gradlew[0]
                print(f"Found gradlew at: {self.gradle_wrapper_path}")
            else:
                raise FileNotFoundError("Gradle wrapper (gradlew) not found in the project template.")

        self.java_home = os.environ.get("JAVA_HOME")
        if not self.java_home:
            print("Warning: JAVA_HOME environment variable not set. Gradle build may fail.")
            # Try to find a common JDK path if not set
            possible_java_homes = ["/usr/lib/jvm/java-11-openjdk-amd64", "/usr/lib/jvm/default-java", "/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home"]
            for path in possible_java_homes:
                if Path(path).exists():
                    self.java_home = path
                    print(f"Auto-detected JAVA_HOME: {self.java_home}")
                    break
            if not self.java_home:
                print("Error: JAVA_HOME is not set and could not be auto-detected. Please set JAVA_HOME.")


        print(f"--- Lobe 8: APK Compiler Lobe Initialized ---")
        print(f"Android SDK Path: {self.android_sdk_path}")
        print(f"Project Template: {self.android_project_template}")
        print(f"Gradle Wrapper: {self.gradle_wrapper_path}")

    def build_apk(self, project_root: Path, build_variant: str = "debug") -> Path:
        """
        Compiles an Android project into an APK.

        Args:
            project_root: The root directory of the Android project.
            build_variant: The build variant to compile (e.g., 'debug', 'release').

        Returns:
            The path to the generated APK file.
        """
        print(f"\n--- Lobe 8: Compiling APK for project: {project_root} ---")

        if not self.android_sdk_path.exists():
            raise FileNotFoundError(f"Android SDK not found at {self.android_sdk_path}. Please set ANDROID_SDK_ROOT.")
        if not self.gradle_wrapper_path.exists():
            raise FileNotFoundError(f"Gradle wrapper (gradlew) not found at {self.gradle_wrapper_path}.")
        if not self.java_home or not Path(self.java_home).exists():
            raise FileNotFoundError(f"JAVA_HOME not set or invalid: {self.java_home}. Please set JAVA_HOME.")

        # Set JAVA_HOME for the subprocess if it's not already in the environment
        env = os.environ.copy()
        if "JAVA_HOME" not in env or env["JAVA_HOME"] != self.java_home:
            env["JAVA_HOME"] = self.java_home
            # Also add JAVA_HOME/bin to PATH for the subprocess
            env["PATH"] = f"{self.java_home}/bin:{env.get('PATH', '')}"

        build_command = [
            str(self.gradle_wrapper_path),
            f"assemble{build_variant.capitalize()}"
        ]

        try:
            print(f"Executing command: {' '.join(build_command)}")
            # Use capture_output=True to get stdout/stderr if needed for debugging
            process = subprocess.run(
                build_command,
                cwd=project_root,
                check=True,
                capture_output=True,
                text=True,
                env=env
            )
            print("Gradle build output:\n", process.stdout)
            if process.stderr:
                print("Gradle build errors:\n", process.stderr)

            # Locate the generated APK
            # The path varies slightly depending on Gradle version and project structure
            apk_path_debug = project_root / "app" / "build" / "outputs" / "apk" / build_variant / f"app-{build_variant}.apk"
            apk_path_release = project_root / "app" / "build" / "outputs" / "apk" / "release" / f"app-release.apk"

            if apk_path_debug.exists():
                print(f"APK generated successfully at: {apk_path_debug}")
                return apk_path_debug
            elif apk_path_release.exists() and build_variant == "release":
                print(f"APK generated successfully at: {apk_path_release}")
                return apk_path_release
            else:
                raise FileNotFoundError(f"APK file not found in expected location after build. Searched for {apk_path_debug} and {apk_path_release}.")

        except subprocess.CalledProcessError as e:
            print(f"Error during Gradle build: {e}")
            print("--- STDOUT ---")
            print(e.stdout)
            print("--- STDERR ---")
            print(e.stderr)
            raise RuntimeError(f"APK compilation failed: {e}") from e
        except Exception as e:
            print(f"An unexpected error occurred during APK compilation: {e}")
            raise


# --- DEMO SECTION ---
# This section demonstrates how these lobes might interact.
# In a real system, the GRAND OBJECTIVE would orchestrate these.

def demo_apk_generation_from_arabic():
    """
    Demonstrates the end-to-end process of generating an APK from an Arabic prompt.
    """
    print("\n" + "="*50)
    print("--- STARTING FULL APK GENERATION DEMO ---")
    print("="*50)

    arabic_prompt = "إنشاء تطبيق اسمه 'حاسبة بسيطة' يحتوي على زر للجمع وحقل لعرض النتيجة."
    print(f"User Arabic Prompt: \"{arabic_prompt}\"")

    # Define temporary directories for project generation
    DUMMY_PROJECT_ROOT = Path("./generated_android_project")
    if DUMMY_PROJECT_ROOT.exists():
        print(f"Removing existing dummy project directory: {DUMMY_PROJECT_ROOT}")
        shutil.rmtree(DUMMY_PROJECT_ROOT)
    DUMMY_PROJECT_ROOT.mkdir()

    try:
        # Step 1: Arabic Lobe to parse the request
        lobe0 = Lobe0ArabicLobe()
        parsed_data = lobe0.process_arabic_request(arabic_prompt)
        print(f"\nParsed Data from Lobe 0: {parsed_data}")

        # Step 2: Code Generation Lobe to create project files
        lobe4 = Lobe4CodeGenerationLobe()
        generated_code = lobe4.generate_android_code(parsed_data)
        print(f"\nGenerated Code Artifacts from Lobe 4: {list(generated_code.keys())}")

        # Step 3: Integrate generated code into a temporary project structure
        print("\n--- Creating temporary Android project structure ---")
        # Copy template project
        shutil.copytree(ANDROID_PROJECT_TEMPLATE_DIR, DUMMY_PROJECT_ROOT, dirs_exist_ok=True)

        # Overwrite or create necessary files
        app_module_path = DUMMY_PROJECT_ROOT / "app"
        src_main_path = app_module_path / "src" / "main"
        java_dir = src_main_path / "java"
        res_dir = src_main_path / "res"
        layout_dir = res_dir / "layout"

        # Ensure directories exist
        if not java_dir.exists():
            java_dir.mkdir(parents=True)
        if not layout_dir.exists():
            layout_dir.mkdir(parents=True)

        app_name_for_package = parsed_data.get('app_name', 'GeneratedApp').lower().replace(" ", "_")
        package_name_base = f"com.example.{app_name_for_package}"

        # Create package directories
        package_path_parts = package_name_base.split('.')
        current_java_path = java_dir
        for part in package_path_parts:
            current_java_path = current_java_path / part
        current_java_path.mkdir(parents=True, exist_ok=True)

        # Write Java MainActivity
        main_activity_code = generated_code.get('MainActivity.java', '')
        if main_activity_code:
            # Update package name in MainActivity.java
            main_activity_code = main_activity_code.replace("package com.example.generatedapp;", f"package {package_name_base};") # Mock update
            with open(current_java_path / "MainActivity.java", "w", encoding="utf-8") as f:
                f.write(main_activity_code)
            print(f"Wrote MainActivity.java to {current_java_path / 'MainActivity.java'}")

        # Write Layout XML
        layout_xml_code = generated_code.get('R.layout.generated_app_activity.xml', '') # Adjust key if naming convention differs
        if layout_xml_code:
            layout_filename = f"{app_name_for_package}_activity.xml"
            with open(layout_dir / layout_filename, "w", encoding="utf-8") as f:
                f.write(layout_xml_code)
            print(f"Wrote {layout_filename} to {layout_dir}")

        # Update build.gradle for app name if necessary (simplified)
        build_gradle_path = app_module_path / "build.gradle"
        if build_gradle_path.exists():
            with open(build_gradle_path, "r", encoding="utf-8") as f:
                build_gradle_content = f.read()
            # Simple replacement for application ID
            build_gradle_content = build_gradle_content.replace("applicationId \"com.example.myapp\"", f"applicationId \"{package_name_base}\"")
            with open(build_gradle_path, "w", encoding="utf-8") as f:
                f.write(build_gradle_content)
            print(f"Updated {build_gradle_path} with new application ID.")

        # Step 4: APK Compiler Lobe to build the APK
        # Ensure ANDROID_SDK_ROOT and JAVA_HOME are set in your environment
        # or provide them directly if not set globally.
        try:
            apk_compiler = Lobe8ApkCompilerLobe(
                android_sdk_path=Path(os.environ.get("ANDROID_SDK_ROOT", "/path/to/your/android/sdk")),
                android_project_template=ANDROID_PROJECT_TEMPLATE_DIR # Use the template base
            )
            generated_apk_path = apk_compiler.build_apk(DUMMY_PROJECT_ROOT, build_variant="debug")
            print(f"\nSuccessfully generated APK: {generated_apk_path}")
            # In a real scenario, you might want to return this path or further process it.
            # For this demo, we just report its existence.

        except FileNotFoundError as fnf_error:
            print(f"\nAPK compilation failed due to missing files: {fnf_error}")
            print("Please ensure ANDROID_SDK_ROOT and JAVA_HOME are correctly set in your environment.")
            print("Also, ensure the ANDROID_PROJECT_TEMPLATE_DIR points to a valid Android project structure.")
        except RuntimeError as rt_error:
            print(f"\nRuntime error during APK Generator demo: {rt_error}")
        except Exception as e:
            print(f"\nAn unexpected error occurred during APK Generator demo: {e}")

    finally:
        # Clean up dummy project directory
        if DUMMY_PROJECT_ROOT.exists():
            print(f"\n--- Cleaning up dummy project directory: {DUMMY_PROJECT_ROOT} ---")
            # shutil.rmtree(DUMMY_PROJECT_ROOT) # Uncomment to auto-cleanup


    print("\n" + "="*50)
    print("--- FULL APK GENERATION DEMO FINISHED ---")
    print("="*50)

if __name__ == "__main__":
    # This block allows running the demo directly if the script is executed.
    # In a larger system, these lobes would be called by an orchestrator.
    demo_apk_generation_from_arabic()