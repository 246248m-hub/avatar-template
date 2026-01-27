import os
import re
from typing import List, Dict, Any

# Assume existence of these modules/functions from other lobes
# from lobe_0_language_lobe import LanguageLobe
# from lobe_3_arabic_parser_lobe import ArabicParserLobe
# from lobe_8_apk_compiler_lobe import APKCompilerLobe
# from lobe_11_resource_manager_lobe import ResourceManagerLobe

# Mock implementations for demonstration purposes
class LanguageLobe:
    def generate_text(self, prompt: str) -> str:
        print(f"Mock LanguageLobe generating text for: '{prompt}'")
        if "basic Android activity" in prompt:
            return """
            A simple Android Activity.
            It should have a TextView that displays "Hello, World!".
            The layout should be a ConstraintLayout.
            """
        elif "Button with click listener" in prompt:
            return """
            A Button that, when clicked, changes the text of a TextView.
            The TextView should initially say "Initial Text".
            When clicked, the Button changes it to "Button Clicked!".
            """
        else:
            return f"Mock generated text for: {prompt}"

class ArabicParserLobe:
    def parse_nlp_request(self, arabic_prompt: str) -> Dict[str, Any]:
        print(f"Mock ArabicParserLobe parsing: '{arabic_prompt}'")
        # Simple mock parsing: extract keywords and intent
        keywords = re.findall(r'\b\w+\b', arabic_prompt.lower())
        intent = "unknown"
        if "إنشاء" in arabic_prompt and "نشاط" in arabic_prompt:
            intent = "create_activity"
        elif "زر" in arabic_prompt and "استماع" in arabic_prompt:
            intent = "add_button_listener"
        elif "عرض" in arabic_prompt and "نص" in arabic_prompt:
            intent = "display_text"

        return {
            "original_prompt": arabic_prompt,
            "parsed_keywords": keywords,
            "detected_intent": intent,
            "parameters": {}
        }

class APKCompilerLobe:
    def compile_apk(self, project_path: str) -> str:
        print(f"Mock APKCompilerLobe compiling APK for: {project_path}")
        # Simulate compilation success
        return f"{project_path}/app-release.apk"

class ResourceManagerLobe:
    def get_resource_path(self, resource_name: str) -> str:
        print(f"Mock ResourceManagerLobe getting path for: {resource_name}")
        # Simulate returning a path
        return f"./resources/{resource_name}"

class CodeGeneratorLobe:
    def __init__(self):
        self.language_lobe = LanguageLobe()
        self.arabic_parser_lobe = ArabicParserLobe()
        self.resource_manager = ResourceManagerLobe()
        self.code_templates = {
            "activity_template": """
package com.example.unifiedmindapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{layout_name});

        TextView textView = findViewById(R.id.textView);
        textView.setText("{initial_text}");
    }}
}}
            """,
            "layout_template": """
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{activity_name}">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{initial_text}"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    {button_element}

</androidx.constraintlayout.widget.ConstraintLayout>
            """,
            "button_element_template": """
    <Button
        android:id="@+id/button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Click Me"
        app:layout_constraintTop_toBottomOf="@+id/textView"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="20dp" />
            """,
            "button_listener_code": """
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

// ... inside onCreate method of {activity_name} ...
Button button = findViewById(R.id.button);
TextView textView = findViewById(R.id.textView);
button.setOnClickListener(new View.OnClickListener() {{
    @Override
    public void onClick(View v) {{
        textView.setText("Button Clicked!");
    }}
}});
            """
        }

    def generate_android_module(self, arabic_prompt: str, project_root: str) -> str:
        """
        Parses an Arabic prompt and generates a corresponding Android module (Activity, layout, etc.).

        Args:
            arabic_prompt: The natural language instruction in Arabic.
            project_root: The root directory of the Android project.

        Returns:
            The path to the generated module file or an error message.
        """
        parsed_data = self.arabic_parser_lobe.parse_nlp_request(arabic_prompt)
        intent = parsed_data.get("detected_intent")

        if intent == "create_activity":
            return self._generate_activity(parsed_data, project_root)
        elif intent == "add_button_listener":
            return self._add_button_listener(parsed_data, project_root)
        elif intent == "display_text":
            return self._generate_text_display_element(parsed_data, project_root)
        else:
            return f"Error: Unrecognized intent '{intent}' from prompt: {arabic_prompt}"

    def _generate_activity(self, parsed_data: Dict[str, Any], project_root: str) -> str:
        """Generates a basic Android Activity and its layout."""
        activity_name = "MainActivity" # Default, can be made dynamic
        layout_name = "activity_main" # Default
        initial_text = "Hello, World!" # Default

        # Further parsing or defaulting for parameters could go here
        # For now, we use the default values for simplicity

        activity_code = self.code_templates["activity_template"].format(
            activity_name=activity_name,
            layout_name=layout_name,
            initial_text=initial_text
        )

        layout_code = self.code_templates["layout_template"].format(
            activity_name=activity_name,
            initial_text=initial_text,
            button_element="" # No button by default for basic activity
        )

        java_dir = os.path.join(project_root, "app", "src", "main", "java", "com", "example", "unifiedmindapp")
        res_dir = os.path.join(project_root, "app", "src", "main", "res")
        layout_dir = os.path.join(res_dir, "layout")

        os.makedirs(java_dir, exist_ok=True)
        os.makedirs(layout_dir, exist_ok=True)

        activity_file_path = os.path.join(java_dir, f"{activity_name}.java")
        with open(activity_file_path, "w", encoding="utf-8") as f:
            f.write(activity_code)

        layout_file_path = os.path.join(layout_dir, f"{layout_name}.xml")
        with open(layout_file_path, "w", encoding="utf-8") as f:
            f.write(layout_code)

        return f"Generated Activity: {activity_file_path} and Layout: {layout_file_path}"

    def _add_button_listener(self, parsed_data: Dict[str, Any], project_root: str) -> str:
        """Adds a button and its click listener to an existing activity."""
        activity_name = "MainActivity" # Assumes we are modifying MainActivity for now
        layout_name = "activity_main" # Assumes we are modifying activity_main.xml

        button_xml = self.code_templates["button_element_template"]
        button_listener_java = self.code_templates["button_listener_code"].format(activity_name=activity_name)

        layout_file_path = os.path.join(project_root, "app", "src", "main", "res", "layout", f"{layout_name}.xml")
        java_file_path = os.path.join(project_root, "app", "src", "main", "java", "com", "example", "unifiedmindapp", f"{activity_name}.java")

        # --- Modify Layout XML ---
        with open(layout_file_path, "r", encoding="utf-8") as f:
            layout_content = f.read()

        # Find the closing tag of the root ConstraintLayout and insert the button before it
        layout_parts = layout_content.rsplit("</androidx.constraintlayout.widget.ConstraintLayout>", 1)
        if len(layout_parts) == 2:
            modified_layout_content = layout_parts[0] + button_xml + "\n    </androidx.constraintlayout.widget.ConstraintLayout>"
            with open(layout_file_path, "w", encoding="utf-8") as f:
                f.write(modified_layout_content)
            layout_modification_status = f"Modified layout: {layout_file_path}"
        else:
            layout_modification_status = f"Error modifying layout: {layout_file_path} (unexpected format)"

        # --- Modify Java Activity ---
        with open(java_file_path, "r", encoding="utf-8") as f:
            java_content = f.read()

        # Find the end of the onCreate method and insert the button listener code
        onCreate_end_marker = "}"
        # Find the last closing brace of onCreate. This is a simplified approach.
        # A more robust approach would involve proper Java parsing.
        onCreate_index = java_content.find("protected void onCreate(Bundle savedInstanceState) {")
        if onCreate_index != -1:
            # Find the last closing brace after the onCreate start
            search_start_index = onCreate_index + len("protected void onCreate(Bundle savedInstanceState) {")
            last_brace_index = -1
            brace_count = 0
            for i in range(search_start_index, len(java_content)):
                if java_content[i] == '{':
                    brace_count += 1
                elif java_content[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        last_brace_index = i
                        break

            if last_brace_index != -1:
                # Insert before the last brace of onCreate
                modified_java_content = java_content[:last_brace_index] + button_listener_java + "\n" + java_content[last_brace_index:]
                with open(java_file_path, "w", encoding="utf-8") as f:
                    f.write(modified_java_content)
                java_modification_status = f"Modified Java activity: {java_file_path}"
            else:
                java_modification_status = f"Error modifying Java activity: {java_file_path} (could not find end of onCreate)"
        else:
            java_modification_status = f"Error modifying Java activity: {java_file_path} (onCreate method not found)"

        return f"{layout_modification_status}\n{java_modification_status}"


    def _generate_text_display_element(self, parsed_data: Dict[str, Any], project_root: str) -> str:
        """
        Generates a TextView element and potentially updates an activity to display text.
        This is a more complex scenario, requiring modification of existing layouts/activities.
        For this example, we'll assume it modifies an existing layout and activity.
        """
        # This function is a placeholder for more advanced text manipulation.
        # In a real scenario, it would:
        # 1. Detect which layout/activity to modify based on context.
        # 2. Extract desired text and potentially its ID.
        # 3. Add a TextView to the layout or modify an existing one.
        # 4. Update the Activity Java code to set the text if needed.
        print("Executing _generate_text_display_element (Placeholder).")
        return "Text display element generation logic not fully implemented in this mock."


# DEMO USAGE SECTION - This part should not be in the final exported code,
# but is included here to show how the module would be used and tested.
if __name__ == "__main__":
    # Create a dummy project root for demonstration
    DEMO_PROJECT_ROOT = "./temp_android_project"
    os.makedirs(os.path.join(DEMO_PROJECT_ROOT, "app", "src", "main", "java", "com", "example", "unifiedmindapp"), exist_ok=True)
    os.makedirs(os.path.join(DEMO_PROJECT_ROOT, "app", "src", "main", "res", "layout"), exist_ok=True)

    code_generator = CodeGeneratorLobe()

    print("--- Testing Lobe 4: Code Generation (Arabic NLP to Android Code) ---")

    # Test Case 1: Create a basic activity
    arabic_prompt_1 = "أنشئ لي نشاط أندرويد بسيط يعرض \"مرحباً بالعالم\"."
    print(f"\nProcessing Arabic Prompt 1: '{arabic_prompt_1}'")
    result_1 = code_generator.generate_android_module(arabic_prompt_1, DEMO_PROJECT_ROOT)
    print(f"Result 1: {result_1}")

    # Test Case 2: Add a button with a click listener
    arabic_prompt_2 = "أضف زر إلى النشاط الحالي وأضف له مستمع نقرات ليغير النص."
    print(f"\nProcessing Arabic Prompt 2: '{arabic_prompt_2}'")
    result_2 = code_generator.generate_android_module(arabic_prompt_2, DEMO_PROJECT_ROOT)
    print(f"Result 2: {result_2}")

    # Test Case 3: Placeholder for text display
    arabic_prompt_3 = "أريد عرض رسالة \"تم التحديث\" في نص."
    print(f"\nProcessing Arabic Prompt 3: '{arabic_prompt_3}'")
    result_3 = code_generator.generate_android_module(arabic_prompt_3, DEMO_PROJECT_ROOT)
    print(f"Result 3: {result_3}")

    # Clean up dummy directory
    import shutil
    try:
        shutil.rmtree(DEMO_PROJECT_ROOT)
        print(f"\nCleaned up dummy project directory: {DEMO_PROJECT_ROOT}")
    except OSError as e:
        print(f"Error removing directory {DEMO_PROJECT_ROOT}: {e}")

    print("\n--- Lobe 4 Code Generation Demo Finished ---")