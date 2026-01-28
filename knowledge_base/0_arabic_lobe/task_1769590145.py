import os
import json
from pathlib import Path
from typing import List, Dict, Any

# Define a consistent directory for knowledge base files
KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)

# --- Lobe 0: Language Lobe (Conceptual - focusing on Arabic interpretation) ---
class ArabicParser:
    """
    Conceptual Arabic parser to extract intent and entities from natural language prompts.
    In a real scenario, this would involve sophisticated NLP libraries.
    For this example, we'll use simple keyword matching.
    """
    def __init__(self):
        pass

    def parse(self, prompt: str) -> Dict[str, Any]:
        intent = "unknown"
        entities = {}

        prompt_lower = prompt.lower()

        if "تطبيق يعرض رسالة ترحيبية" in prompt_lower or "app displays welcome message" in prompt_lower:
            intent = "display_welcome_message"
            # Extract message content if specified, otherwise use a default
            message_start = prompt_lower.find("رسالة")
            if message_start != -1:
                message_content = prompt[message_start + len("رسالة") + 1:].strip()
                # Simple heuristic to find the actual message, can be improved
                if "هي" in message_content:
                    entities["message"] = message_content.split("هي", 1)[1].strip().rstrip('.')
                else:
                    entities["message"] = "Welcome!" # Default if not explicitly specified
            else:
                entities["message"] = "Welcome!"

        elif "زر يفتح صفحة" in prompt_lower or "button opens page" in prompt_lower:
            intent = "button_opens_page"
            page_name_match = prompt_lower.split("صفحة", 1)
            if len(page_name_match) > 1:
                entities["page_name"] = page_name_match[1].strip().rstrip('.')
            else:
                entities["page_name"] = "Details" # Default page name

        elif "قائمة" in prompt_lower or "list" in prompt_lower:
            intent = "create_list"
            # Further parsing for list items could be added here

        return {"intent": intent, "entities": entities}

# --- Lobe 1: Knowledge Base Lobe (Conceptual) ---
class KnowledgeBase:
    """
    Manages structured data and templates for code generation.
    """
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(exist_ok=True)

    def save_template(self, name: str, content: str):
        template_path = self.base_dir / f"{name}.tmpl"
        template_path.write_text(content)
        print(f"Saved template: {template_path}")

    def load_template(self, name: str) -> str:
        template_path = self.base_dir / f"{name}.tmpl"
        if template_path.exists():
            return template_path.read_text()
        else:
            raise FileNotFoundError(f"Template '{name}' not found in {self.base_dir}")

    def save_config(self, name: str, config_data: Dict[str, Any]):
        config_path = self.base_dir / f"{name}.config"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)
        print(f"Saved config: {config_path}")

    def load_config(self, name: str) -> Dict[str, Any]:
        config_path = self.base_dir / f"{name}.config"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {} # Return empty dict if config doesn't exist

# --- Lobe 4: Code Generation Lobe ---
class CodeGenerator:
    """
    Generates Android code snippets based on parsed intent and knowledge base.
    """
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
        self.kb.save_template("activity_layout", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="16dp"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/welcomeText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{{message}}"
        android:textSize="24sp"
        android:textStyle="bold" />

</LinearLayout>""")

        self.kb.save_template("activity_java", """package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView welcomeText = findViewById(R.id.welcomeText);
        welcomeText.setText("{{message}}");
    }
}""")

        self.kb.save_template("button_layout", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="16dp"
    tools:context=".MainActivity">

    <Button
        android:id="@+id/myButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Go to {{page_name}}" />

</LinearLayout>""")

        self.kb.save_template("button_activity_java", """package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assumes layout file is named activity_main.xml

        Button myButton = findViewById(R.id.myButton);
        myButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, {{page_name_class}}.class);
                startActivity(intent);
            }
        });
    }
}""")
        self.kb.save_template("detail_activity_java", """package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class {{page_name_class}} extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detail); // Assumes layout file is named activity_detail.xml
    }
}""")

        self.kb.save_template("detail_layout", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="16dp"
    tools:context=".{{page_name_class}}">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Details for {{page_name}}"
        android:textSize="20sp" />

</LinearLayout>""")


    def generate_activity_code(self, app_config: Dict[str, Any]) -> Dict[str, str]:
        """
        Generates main activity code based on the app configuration.
        """
        generated_code = {}
        intent = app_config.get("intent")
        entities = app_config.get("entities", {})

        if intent == "display_welcome_message":
            layout_template = self.kb.load_template("activity_layout")
            activity_template = self.kb.load_template("activity_java")

            generated_code["activity_layout.xml"] = layout_template.replace("{{message}}", entities.get("message", "Hello!"))
            generated_code["MainActivity.java"] = activity_template.replace("{{message}}", entities.get("message", "Hello!"))
        elif intent == "button_opens_page":
            layout_template = self.kb.load_template("button_layout")
            activity_template = self.kb.load_template("button_activity_java")

            page_name = entities.get("page_name", "Details")
            page_name_class = "".join(word.capitalize() for word in page_name.split()) # e.g., "Details"

            generated_code["activity_main.xml"] = layout_template.replace("{{page_name}}", page_name)
            generated_code["MainActivity.java"] = activity_template.replace("{{page_name}}", page_name).replace("{{page_name_class}}", page_name_class)

            # Generate the detail activity if it's a new page being referenced
            if page_name_class not in ["MainActivity", "SplashActivity"]: # Avoid overwriting common names
                detail_layout_template = self.kb.load_template("detail_layout")
                detail_activity_template = self.kb.load_template("detail_activity_java")

                generated_code[f"activity_{page_name.lower()}.xml"] = detail_layout_template.replace("{{page_name}}", page_name).replace("{{page_name_class}}", page_name_class)
                generated_code[f"{page_name_class}.java"] = detail_activity_template.replace("{{page_name}}", page_name).replace("{{page_name_class}}", page_name_class)

        else:
            print(f"Warning: No specific code generation logic for intent '{intent}'")
            # Fallback to a basic template if needed
            basic_layout_template = "<TextView android:layout_width='match_parent' android:layout_height='match_parent' android:gravity='center' android:text='App running!' />"
            basic_activity_template = """package com.example.myapp;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
public class MainActivity extends AppCompatActivity {
    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}"""
            generated_code["activity_main.xml"] = basic_layout_template
            generated_code["MainActivity.java"] = basic_activity_template

        return generated_code

    def generate_manifest_entry(self, activity_name: str, is_launcher: bool = False) -> str:
        """
        Generates an AndroidManifest.xml entry for an activity.
        """
        intent_filter = ""
        if is_launcher:
            intent_filter = """
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>"""

        return f"""
        <activity android:name=".{activity_name}"
            android:exported="true">{intent_filter}</activity>"""

# --- Lobe 5: Project Structure Lobe (Conceptual) ---
class ProjectStructure:
    """
    Manages the creation and organization of Android project files.
    """
    def __init__(self, project_name: str = "MyApp", base_dir: Path = Path(".")) -> None:
        self.project_name = project_name
        self.root_dir = base_dir / project_name
        self.src_dir = self.root_dir / "app" / "src" / "main"
        self.res_dir = self.src_dir / "res"
        self.layout_dir = self.res_dir / "layout"
        self.manifest_path = self.src_dir / "AndroidManifest.xml"
        self.java_dir = self.src_dir / "java" / "com" / "example" / "myapp" # Default package

        self._create_directories()

    def _create_directories(self) -> None:
        self.root_dir.mkdir(exist_ok=True)
        self.java_dir.mkdir(parents=True, exist_ok=True)
        self.layout_dir.mkdir(parents=True, exist_ok=True)
        self.res_dir.mkdir(parents=True, exist_ok=True) # Ensure res dir exists

    def write_file(self, path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        print(f"Wrote file: {path}")

    def get_manifest_path(self) -> Path:
        return self.manifest_path

    def get_java_dir(self) -> Path:
        return self.java_dir

    def get_layout_dir(self) -> Path:
        return self.layout_dir

    def get_root_dir(self) -> Path:
        return self.root_dir

# --- Lobe 0_arabic_lobe (Integration Point) ---
def build_apk_from_arabic(arabic_prompt: str, project_name: str = "MyArabicApp") -> None:
    """
    Orchestrates the process of building an APK from an Arabic natural language prompt.
    """
    print(f"\n--- Processing Arabic Prompt: '{arabic_prompt}' ---")

    # 1. Parse the Arabic prompt
    parser = ArabicParser()
    parsed_data = parser.parse(arabic_prompt)
    app_config = parsed_data
    print(f"Parsed data: {app_config}")

    if app_config["intent"] == "unknown":
        print("Could not determine intent from prompt. Cannot proceed.")
        return

    # 2. Initialize Knowledge Base and Code Generator
    kb = KnowledgeBase(KNOWLEDGE_BASE_DIR)
    code_gen = CodeGenerator(kb)

    # 3. Set up Project Structure
    project_struct = ProjectStructure(project_name=project_name)
    manifest_path = project_struct.get_manifest_path()
    java_dir = project_struct.get_java_dir()
    layout_dir = project_struct.get_layout_dir()

    # 4. Generate Code
    generated_files = code_gen.generate_activity_code(app_config)

    # 5. Write Generated Code to Project Structure
    app_activities = []
    is_launcher_activity_set = False

    for filename, content in generated_files.items():
        if filename.endswith(".xml"):
            file_path = layout_dir / filename
            project_struct.write_file(file_path, content)
        elif filename.endswith(".java"):
            activity_name = filename.replace(".java", "")
            file_path = java_dir / filename
            project_struct.write_file(file_path, content)
            app_activities.append(activity_name)
            if not is_launcher_activity_set and "MainActivity" in activity_name:
                is_launcher_activity_set = True # Assume MainActivity is launcher by default


    # 6. Generate AndroidManifest.xml
    manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    package="com.example.myapp">
"""
    for activity in app_activities:
        is_launcher = (activity == "MainActivity" and is_launcher_activity_set)
        manifest_content += code_gen.generate_manifest_entry(activity, is_launcher=is_launcher)

    # Add other essential manifest elements if needed (e.g., application tag)
    manifest_content += """
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.MyArabicApp"
        tools:targetApi="31">
        <!-- Activities will be added here -->
    </application>
</manifest>
"""
    project_struct.write_file(manifest_path, manifest_content)

    print(f"\n--- APK Structure Generation Complete for '{project_name}' ---")
    print(f"Project root: {project_struct.get_root_dir()}")
    print(f"Activities generated: {app_activities}")
    print("\nNext steps: Compile the APK using Lobe 8_apk_compiler_lobe.")

# --- Dummy/Mock functions for other lobes (to satisfy dependencies) ---
# In a real system, these would be actual implementations from other lobes.

class MockAPKCompiler:
    def __init__(self):
        print("MockAPKCompiler initialized.")
        self.message = "Mocking debug.keystore" # Simulate a message that Lobe 8 might check

    def compile_apk(self, project_path: Path, output_dir: Path) -> Path:
        print(f"Mock: Compiling APK for project at {project_path}")
        output_dir.mkdir(exist_ok=True)
        mock_apk_path = output_dir / f"{project_path.name}.apk"
        mock_apk_path.write_text("This is a mock APK file.")
        print(f"Mock: APK generated at {mock_apk_path}")
        return mock_apk_path

class MockSynthesisLobe:
    def __init__(self):
        print("MockSynthesisLobe initialized.")

    def synthesize_code(self, parsed_data: Dict[str, Any]) -> Dict[str, str]:
        print("Mock: Synthesizing code...")
        # In a real scenario, this would delegate to CodeGenerator
        kb = KnowledgeBase(KNOWLEDGE_BASE_DIR)
        code_gen = CodeGenerator(kb)
        return code_gen.generate_activity_code(parsed_data)

# --- Example Usage ---
if __name__ == "__main__":
    # Ensure the knowledge base directory exists
    KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)

    # --- Demo of Lobe 0_arabic_lobe ---
    print("\n--- Initiating Lobe 0_arabic_lobe Demo ---")

    # Example 1: Display a welcome message
    arabic_prompt_1 = "أريد تطبيق يعرض رسالة ترحيبية على شاشته الرئيسية باسم 'أهلاً بك في تطبيقي'."
    build_apk_from_arabic(arabic_prompt_1, project_name="WelcomeApp")

    # Example 2: Button to open a details page
    arabic_prompt_2 = "بناء تطبيق فيه زر يفتح صفحة تفاصيل المنتج."
    build_apk_from_arabic(arabic_prompt_2, project_name="ProductApp")

    # Example 3: Simple welcome message (default)
    arabic_prompt_3 = "إنشاء تطبيق يعرض رسالة ترحيب."
    build_apk_from_arabic(arabic_prompt_3, project_name="SimpleWelcomeApp")

    # Example 4: Button to a specific page
    arabic_prompt_4 = "أريد زر لفتح صفحة الإعدادات."
    build_apk_from_arabic(arabic_prompt_4, project_name="SettingsApp")


    # --- Mocking the flow for other lobes ---
    print("\n--- Simulating interaction with other lobes ---")

    # Simulate Lobe 6 (Synthesis) calling Lobe 4 (Code Generation)
    mock_synth = MockSynthesisLobe()
    mock_parser = ArabicParser()
    mock_parsed_data = mock_parser.parse("أريد تطبيق يظهر رسالة 'Hello World'")
    synthesized_code = mock_synth.synthesize_code(mock_parsed_data)
    print(f"Mock Synthesis returned code snippets: {list(synthesized_code.keys())}")

    # Simulate Lobe 8 (APK Compiler)
    mock_compiler = MockAPKCompiler()
    project_path_for_compilation = Path("./WelcomeApp") # Assuming WelcomeApp was created
    output_directory = Path("./apks")
    if project_path_for_compilation.exists():
        compiled_apk = mock_compiler.compile_apk(project_path_for_compilation, output_directory)
        print(f"Mock compilation result: {compiled_apk}")
    else:
        print("Mock compilation skipped: Project directory not found.")

    # Clean up dummy project directories if needed for repeated runs
    import shutil
    for proj_name in ["WelcomeApp", "ProductApp", "SimpleWelcomeApp", "SettingsApp"]:
        proj_path = Path(proj_name)
        if proj_path.exists() and proj_path.is_dir():
            print(f"Cleaning up project directory: {proj_path}")
            shutil.rmtree(proj_path)

    if output_directory.exists() and output_directory.is_dir():
        print(f"Cleaning up output directory: {output_directory}")
        shutil.rmtree(output_directory)

    print("\n--- Arabic Lobe Demo Finished ---")
    print("\n--- Initiating next step: Lobe 4_code_generation_lobe ---")