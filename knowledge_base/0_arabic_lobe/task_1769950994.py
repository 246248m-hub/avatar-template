import os
import json
import subprocess
from pathlib import Path

# Define constants for knowledge base and output directories
KNOWLEDGE_BASE_DIR = Path("knowledge_base")
SIMULATED_APK_OUTPUT_DIR = Path("simulated_apk_output")
ANDROID_PROJECT_TEMPLATE_DIR = Path("android_project_template")

def setup_directories():
    """Ensures necessary directories exist."""
    KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)
    SIMULATED_APK_OUTPUT_DIR.mkdir(exist_ok=True)
    ANDROID_PROJECT_TEMPLATE_DIR.mkdir(exist_ok=True)

def load_arabic_knowledge(file_path: Path) -> dict:
    """
    Loads Arabic language knowledge from a JSON file.
    Simulates fetching linguistic rules, grammar, and semantic mappings.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            knowledge = json.load(f)
        print(f"Successfully loaded Arabic knowledge from: {file_path}")
        return knowledge
    except FileNotFoundError:
        print(f"Error: Arabic knowledge file not found at {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return {}

def parse_arabic_instruction(instruction: str, arabic_knowledge: dict) -> dict:
    """
    Parses an Arabic natural language instruction using loaded knowledge.
    This is a placeholder for a complex NLP pipeline.
    It will identify intent, entities, and actions relevant to APK generation.
    """
    print(f"Parsing Arabic instruction: '{instruction}'")
    # In a real scenario, this would involve tokenization, POS tagging,
    # dependency parsing, named entity recognition, and semantic role labeling,
    # all tailored for Arabic and specific to APK generation tasks.

    # Simulated parsing: Check for keywords and map to structured commands
    parsed_command = {"intent": "unknown", "entities": {}}

    if "إنشاء تطبيق" in instruction or "بناء تطبيق" in instruction:
        parsed_command["intent"] = "create_app"
        if "اسم" in instruction:
            try:
                app_name_index = instruction.index("اسم") + len("اسم")
                app_name = instruction[app_name_index:].strip().split(' ')[0]
                parsed_command["entities"]["app_name"] = app_name
            except ValueError:
                pass # app_name not found after 'اسم'

    if "إضافة زر" in instruction or "أضف زر" in instruction:
        parsed_command["intent"] = "add_button"
        # Extract button properties like text, action, etc.
        if "نص" in instruction:
            try:
                text_index = instruction.index("نص") + len("نص")
                button_text = instruction[text_index:].strip().split(' ')[0]
                parsed_command["entities"]["button_text"] = button_text
            except ValueError:
                pass
        if "وظيفة" in instruction:
            try:
                function_index = instruction.index("وظيفة") + len("وظيفة")
                button_action = instruction[function_index:].strip().split(' ')[0]
                parsed_command["entities"]["button_action"] = button_action
            except ValueError:
                pass

    if "تغيير اللون" in instruction or "لون الشاشة" in instruction:
        parsed_command["intent"] = "change_color"
        # Extract color information
        if "إلى" in instruction:
            try:
                color_index = instruction.index("إلى") + len("إلى")
                color_value = instruction[color_index:].strip().split(' ')[0]
                parsed_command["entities"]["color"] = color_value
            except ValueError:
                pass

    print(f"Parsed command: {parsed_command}")
    return parsed_command

def generate_android_structure(app_name: str, parsed_instruction: dict) -> Path:
    """
    Generates a dummy Android project structure based on the parsed instruction.
    This function acts as a bridge to Lobe 4 (Code Generation) and Lobe 8 (APK Compiler).
    It creates placeholder files and directories that Lobe 8 can then process.
    """
    print(f"Generating Android project structure for app: '{app_name}'")
    project_path = ANDROID_PROJECT_TEMPLATE_DIR / app_name
    project_path.mkdir(parents=True, exist_ok=True)

    # Create a dummy Manifest file
    manifest_path = project_path / "AndroidManifest.xml"
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{app_name.lower().replace(' ', '_')}">
    <application android:label="{app_name}">
        <activity android:name=".MainActivity" android:label="{app_name}">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
        """)

    # Create a dummy MainActivity
    src_path = project_path / "src" / "main" / "java" / app_name.lower().replace(' ', '_').replace('-', '_')
    src_path.mkdir(parents=True, exist_ok=True)
    main_activity_path = src_path / "MainActivity.java"
    with open(main_activity_path, "w", encoding="utf-8") as f:
        f.write(f"""
package {app_name.lower().replace(' ', '_').replace('-', '_')};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.LinearLayout;
import android.graphics.Color;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        setContentView(layout);

        // Applying background color if specified
        String bgColor = "{parsed_instruction.get('entities', {}).get('color', '#FFFFFF')}"; // Default white
        if (!bgColor.equals("#FFFFFF")) {{
            try {{
                layout.setBackgroundColor(Color.parseColor(bgColor));
            }} catch (IllegalArgumentException e) {{
                // Handle invalid color format
                layout.setBackgroundColor(Color.WHITE);
            }}
        }}


        // Adding a button if specified
        Button myButton = new Button(this);
        myButton.setText("{parsed_instruction.get('entities', {}).get('button_text', 'Click Me')}");
        // Add onClick listener based on parsed_instruction['entities']['button_action'] if needed
        // For simplicity, we're just creating the button here.
        layout.addView(myButton);

    }}
}}
        """)

    print(f"Dummy Android project structure created at: {project_path}")
    return project_path

def cleanup_android_project_template():
    """Removes the dummy Android project template directory."""
    if ANDROID_PROJECT_TEMPLATE_DIR.exists():
        import shutil
        try:
            shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)
            print(f"Cleaned up dummy Android project template: {ANDROID_PROJECT_TEMPLATE_DIR}")
        except OSError as e:
            print(f"Error cleaning up {ANDROID_PROJECT_TEMPLATE_DIR}: {e}")

def cleanup_simulated_apk_output():
    """Removes the simulated APK output directory."""
    if SIMULATED_APK_OUTPUT_DIR.exists():
        import shutil
        try:
            shutil.rmtree(SIMULATED_APK_OUTPUT_DIR)
            print(f"Cleaned up simulated APK output: {SIMULATED_APK_OUTPUT_DIR}")
        except OSError as e:
            print(f"Error cleaning up {SIMULATED_APK_OUTPUT_DIR}: {e}")

def arabic_language_processor(instruction: str) -> dict:
    """
    Orchestrates the Arabic language processing and initial APK structure generation.
    This Lobe will:
    1. Load Arabic language knowledge.
    2. Parse an Arabic instruction.
    3. Generate a dummy Android project structure based on the parsed instruction.
    """
    print("\n--- Lobe 0_arabic_lobe: Processing Arabic Instruction ---")
    setup_directories()

    # Load Arabic knowledge (simulated)
    arabic_knowledge_file = KNOWLEDGE_BASE_DIR / "arabic_grammar_rules.json"
    # Create a dummy knowledge file if it doesn't exist for demonstration
    if not arabic_knowledge_file.exists():
        with open(arabic_knowledge_file, "w", encoding="utf-8") as f:
            json.dump({
                "keywords": {
                    "create_app": ["إنشاء تطبيق", "بناء تطبيق"],
                    "add_button": ["إضافة زر", "أضف زر"],
                    "change_color": ["تغيير اللون", "لون الشاشة"]
                },
                "entities": {
                    "app_name": ["اسم"],
                    "button_text": ["نص"],
                    "button_action": ["وظيفة"],
                    "color": ["إلى", "لون"]
                }
            }, f, ensure_ascii=False, indent=4)
        print(f"Created dummy Arabic knowledge file: {arabic_knowledge_file}")

    arabic_knowledge = load_arabic_knowledge(arabic_knowledge_file)

    # Parse the Arabic instruction
    parsed_instruction = parse_arabic_instruction(instruction, arabic_knowledge)

    # Generate initial APK structure based on parsed instruction
    app_name = parsed_instruction.get("entities", {}).get("app_name", "DefaultAppName")
    project_structure_path = generate_android_structure(app_name, parsed_instruction)

    print("\n--- Lobe 0_arabic_lobe: Finished ---")
    return {
        "parsed_instruction": parsed_instruction,
        "android_project_path": project_structure_path
    }

# --- Example Usage ---
if __name__ == "__main__":
    print("--- Starting Lobe 0: Arabic Lobe Demo ---")

    # Example Arabic instructions
    test_prompt_arabic_1 = "إنشاء تطبيق باسم 'تطبيق بسيط' وتغيير لون الشاشة إلى #F0F0F0"
    test_prompt_arabic_2 = "بناء تطبيق جديد باسم 'تطبيقي' وأضف زر بنص 'اضغط هنا' لوظيفة 'openSettings'"
    test_prompt_arabic_3 = "أنشئ تطبيق باسم 'تطبيقي الحلو' وقم بتغيير اللون إلى الأزرق" # Note: Color names might need further processing

    # Process the first prompt
    print(f"\n--- Processing Prompt 1: '{test_prompt_arabic_1}' ---")
    result_1 = arabic_language_processor(test_prompt_arabic_1)
    print(f"Result from Lobe 0 (Arabic Lobe) for prompt 1: {result_1}")

    # Process the second prompt
    print(f"\n--- Processing Prompt 2: '{test_prompt_arabic_2}' ---")
    result_2 = arabic_language_processor(test_prompt_arabic_2)
    print(f"Result from Lobe 0 (Arabic Lobe) for prompt 2: {result_2}")

    # Process the third prompt
    print(f"\n--- Processing Prompt 3: '{test_prompt_arabic_3}' ---")
    result_3 = arabic_language_processor(test_prompt_arabic_3)
    print(f"Result from Lobe 0 (Arabic Lobe) for prompt 3: {result_3}")


    # --- Demonstrating cleanup after the main process ---
    print("\n--- Final Cleanup of Dummy APK Output and Templates ---")
    cleanup_simulated_apk_output()
    cleanup_android_project_template()

    print("\n--- Lobe 0_arabic_lobe Module Demo Finished ---")