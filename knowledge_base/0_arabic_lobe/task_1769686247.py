import os
import re
import subprocess
import shutil
from pathlib import Path

# Assume existence of utility functions for project setup and cleanup
# For demonstration, we'll define simple mock versions.

def create_dummy_project(base_dir: Path, project_name: str) -> Path:
    """Creates a dummy Android project structure."""
    project_root = base_dir / project_name
    src_dir = project_root / "app" / "src" / "main" / "java" / "com" / "example" / project_name.lower().replace(" ", "")
    res_dir = project_root / "app" / "src" / "main" / "res"
    manifest_dir = project_root / "app" / "src" / "main"

    project_root.mkdir(parents=True, exist_ok=True)
    src_dir.mkdir(parents=True, exist_ok=True)
    res_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)

    # Create a minimal AndroidManifest.xml
    manifest_content = """
    <manifest xmlns:android="http://schemas.android.com/apk/res/android"
        package="com.example.myapp">
        <application android:allowBackup="true"
            android:icon="@mipmap/ic_launcher"
            android:label="@string/app_name"
            android:roundIcon="@mipmap/ic_launcher_round"
            android:supportsRtl="true"
            android:theme="@style/AppTheme">
            <activity android:name=".MainActivity">
                <intent-filter>
                    <action android:name="android.intent.action.MAIN" />
                    <category android:name="android.intent.category.LAUNCHER" />
                </intent-filter>
            </activity>
        </application>
    </manifest>
    """
    (manifest_dir / "AndroidManifest.xml").write_text(manifest_content)

    # Create a minimal MainActivity.java
    activity_content = """
    package com.example.myapp;

    import androidx.appcompat.app.AppCompatActivity;
    import android.os.Bundle;

    public class MainActivity extends AppCompatActivity {
        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_main);
        }
    }
    """
    (src_dir / "MainActivity.java").write_text(activity_content)

    # Create a minimal activity_main.xml
    layout_content = """
    <?xml version="1.0" encoding="utf-8"?>
    <androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
        xmlns:app="http://schemas.android.com/apk/res-auto"
        xmlns:tools="http://schemas.android.com/tools"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        tools:context=".MainActivity">

        <TextView
            android:id="@+id/greetingTextView"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Hello World!"
            app:layout_constraintBottom_toBottomOf="parent"
            app:layout_constraintLeft_toLeftOf="parent"
            app:layout_constraintRight_toRightOf="parent"
            app:layout_constraintTop_toTopOf="parent" />

    </androidx.constraintlayout.widget.ConstraintLayout>
    """
    (res_dir / "layout" / "activity_main.xml").write_text(layout_content)


    return project_root

def build_apk(project_path: Path) -> None:
    """Simulates building an APK from an Android project."""
    print(f"Simulating APK build for project at: {project_path}")
    # In a real scenario, this would involve calling Gradle or Android SDK tools.
    # For this example, we'll just create a dummy APK file.
    apk_path = project_path.parent / f"{project_path.name}.apk"
    with open(apk_path, "w") as f:
        f.write("This is a dummy APK file.")
    print(f"Dummy APK created at: {apk_path}")

# --- Lobe 4: Arabic NLP Integration Module ---

class ArabicNLPProcessor:
    """
    Processes Arabic natural language input to extract intent, entities,
    and generate code snippets or configurations.
    """
    def __init__(self):
        # Placeholder for Arabic NLP models and libraries
        # In a real implementation, this would load NLTK, spaCy with Arabic models,
        # or custom-trained models.
        self.arabic_tokenizer = None
        self.arabic_intent_recognizer = None
        self.arabic_entity_extractor = None
        print("ArabicNLPProcessor initialized (placeholders for models).")

    def preprocess_arabic_text(self, text: str) -> str:
        """
        Performs basic preprocessing for Arabic text.
        Removes diacritics, normalizes characters, etc.
        """
        # Remove diacritics
        text = re.sub(r'[\u064B-\u0652]', '', text)
        # Normalize variations of alif, ya, ta marbuta
        text = re.sub(r'أ|إ|آ', 'ا', text)
        text = re.sub(r'ى', 'ي', text)
        text = re.sub(r'ة', 'ه', text)
        # Remove punctuation and extra whitespace
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def parse_arabic_command(self, command: str) -> dict:
        """
        Parses an Arabic command to identify intent and extract relevant entities.
        This is a simplified example. A real implementation would use ML models.
        """
        processed_command = self.preprocess_arabic_text(command)
        print(f"Processed Arabic command: '{processed_command}'")

        intent = "unknown"
        entities = {}

        # Simple keyword-based intent and entity recognition
        if "إنشاء شاشة" in processed_command or "إنشاء واجهة" in processed_command:
            intent = "create_screen"
            match = re.search(r'(?:شاشة|واجهة)\s+([\w\s]+)', processed_command)
            if match:
                entities['screen_name'] = match.group(1).strip().replace(" ", "_")
        elif "عرض رسالة" in processed_command:
            intent = "display_message"
            match = re.search(r'عرض\s+رسالة\s+"([^"]+)"', processed_command)
            if match:
                entities['message_text'] = match.group(1)
        elif "زر" in processed_command and "انقر" in processed_command:
            intent = "button_click_action"
            button_name_match = re.search(r'الزر\s+([\w\s]+?)\s+عند\s+النقر', processed_command)
            if button_name_match:
                entities['button_name'] = button_name_match.group(1).strip().replace(" ", "_")
            action_match = re.search(r'عند\s+النقر\s+:\s*(.+)', processed_command)
            if action_match:
                entities['action'] = action_match.group(1).strip()
        elif "عنوان التطبيق" in processed_command:
            intent = "set_app_title"
            match = re.search(r'عنوان\s+التطبيق\s+هو\s+"([^"]+)"', processed_command)
            if match:
                entities['title'] = match.group(1)


        return {"intent": intent, "entities": entities}

    def generate_android_config(self, parsed_command: dict) -> dict:
        """
        Generates Android-specific configurations based on parsed Arabic commands.
        Returns a dictionary representing the configuration changes.
        """
        config = {}
        intent = parsed_command.get("intent")
        entities = parsed_command.get("entities", {})

        if intent == "create_screen":
            screen_name = entities.get("screen_name", "NewScreen")
            config['create_activity'] = screen_name
            config['layout_name'] = f"activity_{screen_name.lower()}"
            config['layout_content'] = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{screen_name}">

    <TextView
        android:id="@+id/welcomeTextView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Welcome to {screen_name}"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        elif intent == "display_message":
            message_text = entities.get("message_text", "Hello from Arabic NLP!")
            # This would typically translate to adding a Toast or Snackbar in the UI.
            # For now, we'll represent it as a UI element to be added.
            config['add_ui_element'] = {
                "type": "TextView",
                "id": "dynamicMessageTextView",
                "text": message_text,
                "constraints": "app:layout_constraintTop_toBottomOf=\"@id/some_other_view\", app:layout_constraintStart_toStartOf=\"parent\"" # Example constraints
            }
        elif intent == "button_click_action":
            button_name = entities.get("button_name", "actionButton")
            action = entities.get("action", "do_nothing")
            config['add_button'] = {
                "id": f"btn_{button_name}",
                "text": button_name.replace("_", " ").title(),
                "onClick_action": action
            }
        elif intent == "set_app_title":
            title = entities.get("title", "My App")
            config['app_title'] = title
            # This would involve modifying strings.xml and potentially res/values/strings.xml

        return config

    def generate_java_code_snippet(self, android_config: dict, activity_name: str = "MainActivity") -> str:
        """
        Generates Java code snippets for Android activities based on configurations.
        """
        code_snippets = []
        layout_name = android_config.get('layout_name')
        add_ui_element = android_config.get('add_ui_element')
        add_button = android_config.get('add_button')
        app_title = android_config.get('app_title')

        if app_title:
            # This would ideally modify strings.xml and access it.
            # For simplicity, we'll assume it's handled elsewhere for now or
            # add a placeholder comment.
            code_snippets.append(f"// TODO: Set app title to '{app_title}' in strings.xml")

        if add_button:
            btn_id = add_button['id']
            btn_text = add_button['text']
            onclick_action = add_button['onClick_action']
            code_snippets.append(f"""
// Add a button to your layout (e.g., activity_main.xml)
// <Button android:id="@+id/{btn_id}" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="{btn_text}"/>

// In {activity_name}.java:
Button {btn_id} = findViewById(R.id.{btn_id});
{btn_id}.setOnClickListener(new View.OnClickListener() {{
    @Override
    public void onClick(View v) {{
        // Handle '{onclick_action}' action
        Log.d("ArabicNLP", "Button {btn_id} clicked, performing action: {onclick_action}");
        // Example: startActivity(new Intent(this, TargetActivity.class));
        // Example: Toast.makeText(this, "Action: {onclick_action}", Toast.LENGTH_SHORT).show();
    }}
}});
""")

        if add_ui_element:
            element_id = add_ui_element['id']
            element_text = add_ui_element['text']
            code_snippets.append(f"""
// Add this TextView to your layout (e.g., activity_main.xml) with appropriate constraints
// <TextView android:id="@+id/{element_id}" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="{element_text}"/>

// In {activity_name}.java:
TextView {element_id} = findViewById(R.id.{element_id});
if ({element_id} != null) {{
    {element_id}.setText("{element_text}");
}}
""")

        # If a new activity needs to be created, generate its basic structure
        if android_config.get('create_activity'):
            new_activity_name = android_config['create_activity']
            new_layout_name = android_config.get('layout_name', f'activity_{new_activity_name.lower()}')
            code_snippets.append(f"""
// Create a new Activity: {new_activity_name}.java
// Package: com.example.myapp (adjust as needed)
// Layout: res/layout/{new_layout_name}.xml

package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView; // Example import

public class {new_activity_name} extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{new_layout_name});

        // Example: Find and set text on a TextView if it exists
        TextView welcomeTextView = findViewById(R.id.welcomeTextView);
        if (welcomeTextView != null) {{
            // welcomeTextView.setText("Content for {new_activity_name}");
        }}
    }}
}}
""")
            # Also add to AndroidManifest.xml (placeholder for now)
            code_snippets.append(f"// TODO: Register '{new_activity_name}' Activity in AndroidManifest.xml")


        return "\n".join(code_snippets)

    def process_arabic_intent_for_apk(self, arabic_prompt: str, project_path: Path, main_activity_name: str = "MainActivity") -> str:
        """
        Orchestrates the process from Arabic natural language prompt to Android code generation.
        """
        print(f"\n--- Processing Arabic prompt for APK: '{arabic_prompt}' ---")
        parsed_command = self.parse_arabic_command(arabic_prompt)
        print(f"Parsed command: {parsed_command}")

        android_config = self.generate_android_config(parsed_command)
        print(f"Generated Android config: {android_config}")

        generated_code = self.generate_java_code_snippet(android_config, activity_name=main_activity_name)
        print(f"Generated Java code snippet:\n{generated_code}")

        # This is where Lobe 4 would interact with Lobe 6 (Synthesis) and Lobe 8 (APK Compiler)
        # For demonstration, we'll just print.
        print("\n--- Integration Points ---")
        print(f"Lobe 4: Ready to pass android_config: {android_config} to Lobe 6 for synthesis.")
        print(f"Lobe 4: Ready to pass generated_code: '{generated_code}' to Lobe 8 for compilation/integration.")

        # Simulate writing to files for context
        if android_config.get('create_activity'):
            activity_name = android_config['create_activity']
            layout_name = android_config['layout_name']
            src_dir = project_path / "app" / "src" / "main" / "java" / "com" / "example" / "myapp".replace(" ", "")
            res_layout_dir = project_path / "app" / "src" / "main" / "res" / "layout"

            src_dir.mkdir(parents=True, exist_ok=True)
            res_layout_dir.mkdir(parents=True, exist_ok=True)

            # Write new activity file
            activity_file_content = f"""
package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView; // Example import

public class {activity_name} extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{layout_name});

        TextView welcomeTextView = findViewById(R.id.welcomeTextView);
        if (welcomeTextView != null) {{
            welcomeTextView.setText("Welcome to {activity_name}");
        }}
    }}
}}
"""
            (src_dir / f"{activity_name}.java").write_text(activity_file_content)
            print(f"Simulated creation of: {src_dir / f'{activity_name}.java'}")

            # Write new layout file
            layout_file_content = android_config.get('layout_content', f"<!-- Default layout for {activity_name} -->")
            (res_layout_dir / f"{layout_name}.xml").write_text(layout_file_content)
            print(f"Simulated creation of: {res_layout_dir / f'{layout_name}.xml'}")

            # Update AndroidManifest.xml (simplified)
            manifest_path = project_path / "app" / "src" / "main" / "AndroidManifest.xml"
            manifest_content = manifest_path.read_text()
            if f"<{activity_name}" not in manifest_content:
                activity_declaration = f"""
        <activity android:name=".{activity_name}" />
"""
                manifest_content = manifest_content.replace("</application>", f"{activity_declaration}\n    </application>")
                manifest_path.write_text(manifest_content)
                print(f"Simulated update of: {manifest_path}")


        return generated_code # Return the generated code for potential further processing


# --- DEMO SECTION ---
if __name__ == "__main__":
    DEMO_PROJECT_BASE_DIR = Path("./dummy_projects")
    DEMO_PROJECT_BASE_DIR.mkdir(exist_ok=True)

    # Mock setup for Lobe 0, 1, 2, 3 to provide context
    print("\n--- Mocking Lobe 0-3 Context ---")
    mock_prompt_arabic = "إنشاء شاشة جديدة اسمها شاشة الترحيب"
    print(f"Mock Arabic Prompt: '{mock_prompt_arabic}'")
    print("--- Mocking Complete ---\n")

    # Initialize Lobe 4
    arabic_nlp_processor = ArabicNLPProcessor()

    # Create a dummy Android project
    project_name = "MyArabicApp"
    print(f"--- Creating dummy project: {project_name} ---")
    dummy_project_root = create_dummy_project(DEMO_PROJECT_BASE_DIR, project_name)
    print(f"Dummy project created at: {dummy_project_root}\n")

    # Process the Arabic prompt using Lobe 4
    generated_code_snippet = arabic_nlp_processor.process_arabic_intent_for_apk(
        arabic_prompt=mock_prompt_arabic,
        project_path=dummy_project_root,
        main_activity_name="MainActivity"
    )

    print(f"\n--- Lobe 4: Arabic NLP Integration Module Demo Finished ---")
    print(f"Generated code for prompt '{mock_prompt_arabic}':\n{generated_code_snippet}")

    # Simulate interaction with other lobes
    print("\n--- Simulating Lobe 6 (Synthesis) Interaction ---")
    print("Lobe 4 passing generated code to Lobe 6 for further synthesis.")
    # In a real scenario, Lobe 6 would take the generated_code and android_config
    # and integrate them more deeply, perhaps by modifying existing Java files or
    # generating Gradle configurations.
    print("--- Lobe 6 Interaction Simulated ---\n")

    print("--- Simulating Lobe 8 (APK Compiler) Interaction ---")
    print("Lobe 4 passing project path to Lobe 8 for potential APK build.")
    # Lobe 8 would take the project path and potentially the synthesized code
    # and initiate the build process.
    build_apk(dummy_project_root)
    print("--- Lobe 8 Interaction Simulated ---\n")


    # Clean up dummy project
    print("\n--- Cleaning up dummy project ---")
    if DEMO_PROJECT_BASE_DIR.exists():
        print(f"Removing dummy project directory: {DEMO_PROJECT_BASE_DIR}")
        shutil.rmtree(DEMO_PROJECT_BASE_DIR)

    print("\n--- Lobe 4: Arabic NLP Integration Module Demo Finished ---")