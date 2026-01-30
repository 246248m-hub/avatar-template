import os
import json
import shutil
from collections import defaultdict

# Assume these are defined elsewhere or will be dynamically generated
# For this module, we'll simulate their presence
KNOWLEDGE_BASE_DIR = "knowledge_base"
OUTPUT_DIR = "generated_apks"
LANGUAGE_CODE = "ar"

class ArabicParser:
    """
    Parses Arabic natural language input to extract structured information
    relevant for APK generation. This is a simplified representation.
    """
    def __init__(self, knowledge_base_path):
        self.knowledge_base_path = knowledge_base_path
        self.intent_entities_map = {} # Simulate loading from KB
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        # In a real system, this would load structured data from Arabic NLP models
        # and define mappings between Arabic phrases and intents/entities.
        # For demonstration, we'll use a dummy map.
        self.intent_entities_map = {
            "إنشاء تطبيق": {"intent": "create_app", "entities": ["app_name", "features"]},
            "إضافة زر": {"intent": "add_ui_element", "entities": ["element_type", "text", "action"]},
            "عرض نص": {"intent": "display_text", "entities": ["text_content"]},
            "تغيير لون الخلفية": {"intent": "change_background", "entities": ["color"]},
            "الذهاب إلى شاشة": {"intent": "navigate", "entities": ["screen_name"]},
        }
        print(f"ArabicParser initialized with knowledge from: {self.knowledge_base_path}")

    def parse_arabic_input(self, arabic_text):
        """
        Parses Arabic text to identify intents and entities.
        This is a highly simplified simulation.
        """
        parsed_data = {"intent": "unknown", "entities": {}}
        for phrase, mapping in self.intent_entities_map.items():
            if phrase in arabic_text:
                parsed_data["intent"] = mapping["intent"]
                # Basic entity extraction simulation
                for entity in mapping["entities"]:
                    if entity == "app_name":
                        # Find text after "تطبيق"
                        parts = arabic_text.split(phrase)
                        if len(parts) > 1:
                            potential_name = parts[1].strip()
                            if potential_name:
                                parsed_data["entities"][entity] = potential_name
                    elif entity == "text_content":
                        # Find text after "عرض"
                        parts = arabic_text.split("عرض ")
                        if len(parts) > 1:
                            potential_text = parts[1].strip()
                            if potential_text:
                                parsed_data["entities"][entity] = potential_text
                    elif entity == "element_type":
                        # Simple keyword spotting for element type
                        if "زر" in arabic_text:
                            parsed_data["entities"][entity] = "button"
                        elif "تسمية" in arabic_text:
                            parsed_data["entities"][entity] = "label"
                    elif entity == "color":
                        # Simple keyword spotting for color
                        if "أزرق" in arabic_text:
                            parsed_data["entities"][entity] = "blue"
                        elif "أخضر" in arabic_text:
                            parsed_data["entities"][entity] = "green"
                        elif "أحمر" in arabic_text:
                            parsed_data["entities"][entity] = "red"
                    elif entity == "screen_name":
                        # Find text after "شاشة"
                        parts = arabic_text.split("شاشة ")
                        if len(parts) > 1:
                            potential_screen = parts[1].strip()
                            if potential_screen:
                                parsed_data["entities"][entity] = potential_screen
                    # Add more entity extraction logic here
                break # Assume first matching phrase is sufficient for this demo
        return parsed_data

class ArabicAPKGenerator:
    """
    Generates basic APK project structure and placeholder code based on
    parsed Arabic natural language input.
    """
    def __init__(self, output_root_dir, language_code="ar"):
        self.output_root_dir = output_root_dir
        self.language_code = language_code
        os.makedirs(self.output_root_dir, exist_ok=True)

    def _create_project_structure(self, app_name):
        """Creates a basic Android project directory structure."""
        app_dir_name = app_name.replace(" ", "_").lower()
        project_path = os.path.join(self.output_root_dir, app_dir_name)
        src_path = os.path.join(project_path, "app", "src", "main")
        java_path = os.path.join(src_path, "java")
        res_path = os.path.join(src_path, "res")
        layout_path = os.path.join(res_path, "layout")
        values_path = os.path.join(res_path, "values")

        os.makedirs(java_path, exist_ok=True)
        os.makedirs(layout_path, exist_ok=True)
        os.makedirs(values_path, exist_ok=True)

        print(f"Created project structure for '{app_name}' at: {project_path}")
        return project_path, java_path, layout_path, values_path

    def _generate_main_activity(self, java_path, app_name, parsed_commands):
        """Generates a placeholder MainActivity.java file."""
        package_name = "com.example." + app_name.replace(" ", "").lower()
        activity_file_path = os.path.join(java_path, package_name.replace(".", os.sep), "MainActivity.java")
        os.makedirs(os.path.dirname(activity_file_path), exist_ok=True)

        java_code = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView; // Example import
import android.graphics.Color; // Example import

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // --- Dynamic UI Elements based on Arabic commands ---
"""
        # Simulate adding UI elements based on parsed commands
        ui_element_id_counter = 1
        for command in parsed_commands:
            intent = command.get("intent")
            entities = command.get("entities", {})

            if intent == "display_text":
                text_content = entities.get("text_content", "Hello World!")
                element_id = f"textView_{ui_element_id_counter}"
                java_code += f"""
        TextView tv{ui_element_id_counter} = new TextView(this);
        tv{ui_element_id_counter}.setId(View.generateViewId()); // Generate dynamic ID
        tv{ui_element_id_counter}.setText("{text_content}");
        // Add layout parameters to position this dynamically added TextView
        // This requires more sophisticated layout management
        // For demo, assume it's added to a LinearLayout or ConstraintLayout
        // addView(tv{ui_element_id_counter}); // Placeholder for adding to layout
        System.out.println("Added TextView with text: {text_content}");
"""
                ui_element_id_counter += 1

            elif intent == "change_background":
                color_name = entities.get("color", "white")
                color_hex = "#FFFFFF" # Default
                if color_name == "blue":
                    color_hex = "#0000FF"
                elif color_name == "green":
                    color_hex = "#00FF00"
                elif color_name == "red":
                    color_hex = "#FF0000"

                java_code += f"""
        // Setting background color requires access to the root view or a specific layout element
        // For demo purposes, we'll just print the intent
        System.out.println("Requested background color change to: {color_name}");
        // Example: getWindow().getDecorView().setBackgroundColor(Color.parseColor("{color_hex}"));
"""
            elif intent == "add_ui_element" and entities.get("element_type") == "button":
                button_text = entities.get("text", "Click Me")
                action = entities.get("action", "none")
                element_id = f"button_{ui_element_id_counter}"
                java_code += f"""
        // Button generation logic would go here.
        // This would involve creating a Button object, setting its text,
        // and potentially attaching an OnClickListener for the action.
        System.out.println("Requested to add a button with text: '{button_text}' and action: '{action}'");
"""
                ui_element_id_counter += 1
            # Add logic for other intents like navigation, adding different UI elements etc.

        java_code += f"""
        // --- End of Dynamic UI Elements ---
    }}
}}
"""
        with open(activity_file_path, "w", encoding="utf-8") as f:
            f.write(java_code)
        print(f"Generated {activity_file_path}")
        return activity_file_path

    def _generate_layout_xml(self, layout_path, app_name, parsed_commands):
        """Generates a placeholder activity_main.xml file."""
        layout_file_path = os.path.join(layout_path, "activity_main.xml")

        xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{app_name.replace(' ', '').lower()}.MainActivity">

    <TextView
        android:id="@+id/textView_welcome"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Welcome to {app_name}"
        android:textSize="24sp"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent" />

    <!-- Dynamic UI elements would be added here or handled programmatically -->
"""
        # Simulate adding elements to XML if they are not handled purely in Java
        # For simplicity, we'll focus on programmatic addition in Java for this demo
        # If the intent was to create static XML, this section would be more complex.

        xml_content += """
</androidx.constraintlayout.widget.ConstraintLayout>
"""
        with open(layout_file_path, "w", encoding="utf-8") as f:
            f.write(xml_content)
        print(f"Generated {layout_file_path}")
        return layout_file_path

    def _generate_strings_xml(self, values_path, app_name):
        """Generates a placeholder strings.xml file."""
        strings_file_path = os.path.join(values_path, "strings.xml")
        xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{app_name}</string>
    <string name="welcome_message">Welcome to {app_name}</string>
</resources>
"""
        with open(strings_file_path, "w", encoding="utf-8") as f:
            f.write(xml_content)
        print(f"Generated {strings_file_path}")
        return strings_file_path

    def generate_apk_module(self, arabic_commands_list):
        """
        Generates a basic APK project structure and placeholder code
        from a list of parsed Arabic commands.
        """
        if not arabic_commands_list:
            print("No Arabic commands provided for APK generation.")
            return

        # Assume the first command is to create the app to get the app name
        app_name = "MyArabicApp" # Default if no 'create_app' intent found
        parsed_commands = []

        for cmd_data in arabic_commands_list:
            if cmd_data.get("intent") == "create_app":
                app_name = cmd_data.get("entities", {}).get("app_name", app_name)
            parsed_commands.append(cmd_data)

        project_path, java_path, layout_path, values_path = self._create_project_structure(app_name)
        self._generate_main_activity(java_path, app_name, parsed_commands)
        self._generate_layout_xml(layout_path, app_name, parsed_commands)
        self._generate_strings_xml(values_path, app_name)

        print(f"\n--- Basic APK module structure for '{app_name}' generated at: {project_path} ---")
        print("Note: This is a simplified generation. Real APKs require more detailed code and resource definitions.")
        return project_path

class ArabicNLPModule:
    """
    Orchestrates Arabic NLP parsing and APK generation.
    This module acts as an intermediary, taking natural language input,
    parsing it, and then instructing the APK generator.
    """
    def __init__(self, knowledge_base_dir, output_dir):
        self.parser = ArabicParser(knowledge_base_dir)
        self.generator = ArabicAPKGenerator(output_dir, language_code=LANGUAGE_CODE)
        self.knowledge_base_dir = knowledge_base_dir
        self.output_dir = output_dir

    def process_arabic_instruction(self, arabic_text):
        """
        Parses a single Arabic instruction and generates the corresponding APK module.
        """
        print(f"\n--- Processing Arabic Instruction: '{arabic_text}' ---")
        parsed_data = self.parser.parse_arabic_input(arabic_text)
        print(f"Parsed data: {parsed_data}")

        # In a real system, we would aggregate commands if they are related to the same app.
        # For this demo, each instruction might trigger a separate (though basic) generation.
        # A more robust system would group commands into a single app definition.

        generated_project_path = self.generator.generate_apk_module([parsed_data])
        return generated_project_path, parsed_data

    def process_arabic_sequence(self, arabic_texts):
        """
        Processes a sequence of Arabic instructions, potentially building a more complex app.
        This is a simplified aggregation.
        """
        print("\n--- Processing Sequence of Arabic Instructions ---")
        all_parsed_data = []
        app_name = "MyUnifiedApp"
        for text in arabic_texts:
            parsed_data = self.parser.parse_arabic_input(text)
            if parsed_data.get("intent") == "create_app":
                app_name = parsed_data.get("entities", {}).get("app_name", app_name)
            all_parsed_data.append(parsed_data)

        if not all_parsed_data:
            print("No Arabic instructions to process.")
            return None

        print(f"Aggregated parsed data for app '{app_name}': {all_parsed_data}")
        generated_project_path = self.generator.generate_apk_module(all_parsed_data)
        return generated_project_path

def demonstrate_arabic_nlp_and_apk_generator():
    """
    Demonstrates the Arabic NLP and APK Generator module.
    """
    print("\n--- Initiating Arabic NLP and APK Generator Module Demo ---")

    # Create dummy knowledge base directory if it doesn't exist
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    # Create dummy knowledge file (optional for this demo, parser uses hardcoded map)
    with open(os.path.join(KNOWLEDGE_BASE_DIR, "arabic_nlp_config.json"), "w", encoding="utf-8") as f:
        json.dump({"description": "Dummy config for Arabic NLP"}, f)

    arabic_nlp_module = ArabicNLPModule(KNOWLEDGE_BASE_DIR, OUTPUT_DIR)

    # --- Test Case 1: Create a simple app ---
    instruction1 = "أريد إنشاء تطبيق اسمه 'مساعدي العربي'"
    generated_path1, parsed1 = arabic_nlp_module.process_arabic_instruction(instruction1)
    print(f"Generated for instruction 1: {generated_path1}, Parsed: {parsed1}")

    # --- Test Case 2: Add a text view to an existing or new app context ---
    # In a real scenario, we'd need to maintain app context.
    # For this demo, we'll process it as if it's for a new app or an implicit one.
    instruction2 = "اعرض النص 'أهلاً بك في عالم الذكاء الاصطناعي'"
    generated_path2, parsed2 = arabic_nlp_module.process_arabic_instruction(instruction2)
    print(f"Generated for instruction 2: {generated_path2}, Parsed: {parsed2}")

    # --- Test Case 3: Combine multiple commands into a single app generation ---
    arabic_sequence = [
        "قم ببناء تطبيق باسم 'تطبيق التحكم'",
        "أضف زر بعنوان 'تشغيل'",
        "غير لون الخلفية إلى الأزرق",
        "اعرض النص 'تم التنفيذ بنجاح'"
    ]
    generated_path_seq = arabic_nlp_module.process_arabic_sequence(arabic_sequence)
    print(f"Generated for sequence: {generated_path_seq}")

    # --- Test Case 4: More complex interaction ---
    complex_sequence = [
        "إنشاء تطبيق اسمه 'تطبيق الاستكشاف'",
        "اعرض النص 'ابدأ رحلتك'",
        "أضف زر بعنوان 'التالي' مع إجراء 'الانتقال إلى الشاشة الثانية'",
        "اذهب إلى شاشة 'الشاشة الثانية'"
    ]
    generated_path_complex = arabic_nlp_module.process_arabic_sequence(complex_sequence)
    print(f"Generated for complex sequence: {generated_path_complex}")


    # --- Cleanup ---
    print("\n--- Cleaning up generated APK directories ---")
    if os.path.exists(OUTPUT_DIR):
        try:
            shutil.rmtree(OUTPUT_DIR)
            print(f"Removed output directory: {OUTPUT_DIR}")
        except OSError as e:
            print(f"Error removing directory {OUTPUT_DIR}: {e}")

    # Clean up dummy knowledge base dir if empty
    if os.path.exists(KNOWLEDGE_BASE_DIR) and not os.listdir(KNOWLEDGE_BASE_DIR):
        os.rmdir(KNOWLEDGE_BASE_DIR)
        print(f"Removed empty knowledge base directory: {KNOWLEDGE_BASE_DIR}")

    print("\n--- Arabic NLP and APK Generator Module Demo Finished ---")

if __name__ == "__main__":
    demonstrate_arabic_nlp_and_apk_generator()