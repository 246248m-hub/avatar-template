import os
import shutil
import subprocess
from pathlib import Path

KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
ANDROID_PROJECT_TEMPLATE_DIR = Path("./android_project_template")
OUTPUT_APKS_DIR = Path("./output_apks")
ARABIC_NLP_REQUEST_DIR = Path("./arabic_nlp_requests")

def setup_directories():
    """Ensures necessary directories exist for the Arabic NLP and APK compilation."""
    KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)
    ARABIC_NLP_REQUEST_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_APKS_DIR.mkdir(parents=True, exist_ok=True)

def create_dummy_arabic_request_file(filename, content):
    """Creates a dummy file for an Arabic NLP request."""
    filepath = ARABIC_NLP_REQUEST_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath

def process_arabic_nlp_request(request_file_path, knowledge_base_dir):
    """
    Simulates processing an Arabic NLP request.
    In a real scenario, this would involve complex NLP tasks like:
    - Tokenization and Lemmatization of Arabic text.
    - Understanding user intent (e.g., "create an app that shows a button and prints 'Hello'").
    - Extracting key entities (e.g., button text, action).
    - Generating a structured representation of the desired APK functionality.
    """
    print(f"Simulating Arabic NLP processing for: {request_file_path}")
    print(f"Using knowledge base from: {knowledge_base_dir}")

    # Simulate extracting information from the Arabic request
    with open(request_file_path, "r", encoding="utf-8") as f:
        arabic_instruction = f.read()

    # Placeholder for actual NLP logic
    # This would involve libraries like `camel_tools`, `nltk` with Arabic models, etc.
    # For demonstration, we'll just extract keywords and assume a simple structure.
    generated_code_structure = {}
    if "button" in arabic_instruction.lower() and "print" in arabic_instruction.lower():
        generated_code_structure["ui_elements"] = [{"type": "Button", "text": "Click Me"}]
        generated_code_structure["actions"] = [{"element": "Button", "event": "onClick", "action": "print", "message": "Hello World"}]
    elif "text view" in arabic_instruction.lower():
        generated_code_structure["ui_elements"] = [{"type": "TextView", "text": "Welcome"}]
    else:
        generated_code_structure["ui_elements"] = []
        generated_code_structure["actions"] = []

    print(f"NLP parsed instruction: '{arabic_instruction}'")
    print(f"Generated intermediate structure: {generated_code_structure}")

    # This structure would then be passed to Lobe 4_code_generation_lobe
    return generated_code_structure

def cleanup_dummy_files(dirs_to_clean=None):
    """Cleans up dummy files and directories created during the demo."""
    if dirs_to_clean is None:
        dirs_to_clean = [ARABIC_NLP_REQUEST_DIR]
    for d in dirs_to_clean:
        if d.exists():
            shutil.rmtree(d)
            print(f"Removed dummy directory: {d}")

class ArabicCodeGenerator:
    """
    Lobe 4: Code Generation Lobe
    Generates Android code (Java/Kotlin and XML) from a structured representation
    derived from Arabic NLP requests.
    """
    def __init__(self, android_template_dir, output_dir):
        self.android_template_dir = Path(android_template_dir)
        self.output_dir = Path(output_dir)
        self.project_root = None

    def setup_project_environment(self, project_name="MyArabicApp"):
        """Sets up a temporary Android project directory for code generation."""
        if not self.android_template_dir.exists():
            raise FileNotFoundError(f"Android project template not found at: {self.android_template_dir}")

        self.project_root = self.output_dir / project_name
        if self.project_root.exists():
            shutil.rmtree(self.project_root)
        shutil.copytree(self.android_template_dir, self.project_root)
        print(f"Copied Android project template to: {self.project_root}")

    def generate_java_code(self, intermediate_structure):
        """Generates Java code for the main activity based on the structure."""
        activity_file = self.project_root / "app" / "src" / "main" / "java" / "com" / "example" / "myarabicapp" / "MainActivity.java"
        if not activity_file.exists():
            raise FileNotFoundError(f"MainActivity template not found at: {activity_file}")

        with open(activity_file, "r", encoding="utf-8") as f:
            activity_content = f.read()

        # Simulate code injection based on the intermediate structure
        ui_elements = intermediate_structure.get("ui_elements", [])
        actions = intermediate_structure.get("actions", [])

        layout_binding_code = ""
        click_listener_code = ""
        import_statements = set()

        # Add imports for UI elements and listeners
        if any(e["type"] == "Button" for e in ui_elements):
            import_statements.add("import android.widget.Button;")
            import_statements.add("import android.view.View;")

        for element in ui_elements:
            element_type = element.get("type")
            element_text = element.get("text", "")
            if element_type == "Button":
                layout_binding_code += f"        Button {element_type.lower()}_{element_text.lower().replace(' ', '_')} = findViewById(R.id.{element_type.lower()}_{element_text.lower().replace(' ', '_')});\n"
                for action in actions:
                    if action.get("element") == "Button" and action.get("action") == "print":
                        listener_id = f"{element_type.lower()}_{element_text.lower().replace(' ', '_')}_listener"
                        click_listener_code += f"        {element_type.lower()}_{element_text.lower().replace(' ', '_')}.setOnClickListener(new View.OnClickListener() {{\n"
                        click_listener_code += f"            @Override\n"
                        click_listener_code += f"            public void onClick(View v) {{\n"
                        click_listener_code += f"                Log.d(\"ArabicApp\", \"{action.get('message', 'Button clicked!')}\");\n"
                        click_listener_code += f"            }}\n"
                        click_listener_code += f"        }}); \n"
                        import_statements.add("import android.util.Log;")

        # Inject UI element binding and click listeners into the onCreate method
        onCreate_method_start = "protected void onCreate(Bundle savedInstanceState) {"
        onCreate_method_end = "}"
        
        if onCreate_method_start in activity_content:
            parts = activity_content.split(onCreate_method_start, 1)
            header = parts[0]
            rest = parts[1]
            
            onCreate_body_parts = rest.split(onCreate_method_end, 1)
            onCreate_body = onCreate_body_parts[0]
            footer = onCreate_method_end + onCreate_body_parts[1]

            # Add imports
            import_block = "\n".join(sorted(list(import_statements)))
            activity_content = header.replace("// Additional imports", import_block) + onCreate_method_start + onCreate_body.replace("super.onCreate(savedInstanceState);", f"super.onCreate(savedInstanceState);\n        setContentView(R.layout.activity_main);\n") + layout_binding_code + click_listener_code + footer
        else:
            print("Warning: Could not find onCreate method to inject code.")


        with open(activity_file, "w", encoding="utf-8") as f:
            f.write(activity_content)
        print(f"Generated Java code for MainActivity: {activity_file}")

    def generate_xml_layout(self, intermediate_structure):
        """Generates XML layout for the main activity."""
        layout_file = self.project_root / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml"
        if not layout_file.exists():
            print(f"Warning: activity_main.xml template not found at: {layout_file}. Creating a basic one.")
            layout_file.parent.mkdir(parents=True, exist_ok=True)
            with open(layout_file, "w", encoding="utf-8") as f:
                f.write('<?xml version="1.0" encoding="utf-8"?>\n')
                f.write('<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto" xmlns:tools="http://schemas.android.com/tools" android:layout_width="match_parent" android:layout_height="match_parent" tools:context=".MainActivity">\n')
                f.write('</androidx.constraintlayout.widget.ConstraintLayout>')
        
        with open(layout_file, "r", encoding="utf-8") as f:
            layout_content = f.read()

        # Simulate adding UI elements to the layout
        ui_elements = intermediate_structure.get("ui_elements", [])
        
        xml_elements_to_add = []
        # Assuming a basic ConstraintLayout structure for simplicity
        layout_end_tag_index = layout_content.rfind("</androidx.constraintlayout.widget.ConstraintLayout>")
        if layout_end_tag_index == -1:
             layout_end_tag_index = layout_content.rfind("</ConstraintLayout>") # Fallback

        if layout_end_tag_index == -1:
            print("Error: Could not find the end of the ConstraintLayout tag in the XML.")
            return

        insert_point = layout_end_tag_index
        
        element_id_counter = 0
        for element in ui_elements:
            element_type = element.get("type")
            element_text = element.get("text", "")
            
            if element_type == "Button":
                unique_id = f"button_{element_id_counter}"
                xml_elements_to_add.append(
                    f'    <Button\n'
                    f'        android:id="@+id/{unique_id}"\n'
                    f'        android:layout_width="wrap_content"\n'
                    f'        android:layout_height="wrap_content"\n'
                    f'        android:text="{element_text}"\n'
                    f'        app:layout_constraintBottom_toBottomOf="parent"\n'
                    f'        app:layout_constraintTop_toTopOf="parent"\n'
                    f'        app:layout_constraintStart_toStartOf="parent"\n'
                    f'        app:layout_constraintEnd_toEndOf="parent"\n'
                    f'    />'
                )
                element_id_counter += 1
            elif element_type == "TextView":
                unique_id = f"textview_{element_id_counter}"
                xml_elements_to_add.append(
                    f'    <TextView\n'
                    f'        android:id="@+id/{unique_id}"\n'
                    f'        android:layout_width="wrap_content"\n'
                    f'        android:layout_height="wrap_content"\n'
                    f'        android:text="{element_text}"\n'
                    f'        app:layout_constraintBottom_toBottomOf="parent"\n'
                    f'        app:layout_constraintTop_toTopOf="parent"\n'
                    f'        app:layout_constraintStart_toStartOf="parent"\n'
                    f'        app:layout_constraintEnd_toEndOf="parent"\n'
                    f'    />'
                )
                element_id_counter += 1
        
        if xml_elements_to_add:
            new_layout_content = layout_content[:insert_point] + "\n" + "\n".join(xml_elements_to_add) + "\n" + layout_content[insert_point:]
            with open(layout_file, "w", encoding="utf-8") as f:
                f.write(new_layout_content)
            print(f"Generated XML layout: {layout_file}")
        else:
            print("No UI elements to add to the layout.")

    def build_apk(self, project_name="MyArabicApp"):
        """
        Simulates the APK compilation process.
        In a real scenario, this would involve calling Gradle commands.
        """
        print(f"\n--- Simulating APK Compilation for {project_name} ---")
        # This is a highly simplified simulation. A real build would involve:
        # 1. Navigating to the project root.
        # 2. Executing `./gradlew assembleDebug` or `./gradlew build`.
        # 3. Handling build errors and capturing the APK path.

        if not self.project_root or not self.project_root.exists():
            raise FileNotFoundError("Project environment not set up. Call setup_project_environment first.")

        # Simulate creating a dummy APK file
        dummy_apk_path = self.output_dir / f"{project_name.lower()}-debug.apk"
        try:
            with open(dummy_apk_path, "w") as f:
                f.write("This is a dummy APK file.")
            print(f"Simulated APK created at: {dummy_apk_path}")
            return dummy_apk_path
        except Exception as e:
            print(f"Error simulating APK creation: {e}")
            return None

def cleanup_android_project_artifacts(dirs_to_clean=None):
    """Cleans up dummy Android project directories and output APKs."""
    if dirs_to_clean is None:
        dirs_to_clean = [ANDROID_PROJECT_TEMPLATE_DIR, OUTPUT_APKS_DIR]
    for d in dirs_to_clean:
        if d.exists():
            shutil.rmtree(d)
            print(f"Removed dummy Android project directory: {d}")


def main_execution_flow():
    """
    Orchestrates the Arabic NLP processing and APK generation.
    This function simulates the interaction between Lobes 0, 4, and 8.
    """
    setup_directories()

    # --- Simulate Lobe 0_arabic_lobe ---
    print("\n--- Simulating Lobe 0: Arabic NLP Processing ---")
    arabic_request_content = "قم بإنشاء تطبيق يعرض زرًا ويطبع رسالة 'مرحبا بالعالم' عند الضغط عليه."
    request_file = create_dummy_arabic_request_file("app_creation_request.txt", arabic_request_content)

    # This is where Lobe 0 would call its Arabic processing function
    # For demonstration, we call it directly:
    intermediate_structure = process_arabic_nlp_request(request_file, KNOWLEDGE_BASE_DIR)

    print("\n--- Lobe 0 Finished ---")
    cleanup_dummy_files(dirs_to_clean=[ARABIC_NLP_REQUEST_DIR]) # Clean up request file

    # --- Simulate Lobe 4_code_generation_lobe ---
    print("\n--- Initiating Lobe 4: Code Generation ---")
    # Assume a basic Android project template exists for demonstration
    # In a real scenario, this would be pre-configured or fetched.
    if not ANDROID_PROJECT_TEMPLATE_DIR.exists():
        print(f"Creating dummy Android project template at: {ANDROID_PROJECT_TEMPLATE_DIR}")
        ANDROID_PROJECT_TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
        (ANDROID_PROJECT_TEMPLATE_DIR / "app").mkdir(parents=True, exist_ok=True)
        (ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "java" / "com" / "example" / "myarabicapp").mkdir(parents=True, exist_ok=True)
        (ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "res" / "layout").mkdir(parents=True, exist_ok=True)

        # Dummy MainActivity.java template
        with open(ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "java" / "com" / "example" / "myarabicapp" / "MainActivity.java", "w", encoding="utf-8") as f:
            f.write("""package com.example.myarabicapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button; // Placeholder for import
import android.view.View; // Placeholder for import
import android.util.Log; // Placeholder for import

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // setContentView will be injected here
        // UI element binding will be injected here
        // Click listeners will be injected here
    }
}
""")
        # Dummy activity_main.xml template
        with open(ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml", "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write('<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto" xmlns:tools="http://schemas.android.com/tools" android:layout_width="match_parent" android:layout_height="match_parent" tools:context=".MainActivity">\n')
            f.write('</androidx.constraintlayout.widget.ConstraintLayout>')

    code_generator = ArabicCodeGenerator(ANDROID_PROJECT_TEMPLATE_DIR, OUTPUT_APKS_DIR)
    project_name = "ArabicGeneratedApp"
    code_generator.setup_project_environment(project_name=project_name)
    code_generator.generate_java_code(intermediate_structure)
    code_generator.generate_xml_layout(intermediate_structure)

    print("\n--- Lobe 4 Finished ---")

    # --- Simulate Lobe 8_apk_compiler_lobe ---
    print("\n--- Initiating Lobe 8: APK Compiler ---")
    # This lobe would trigger the build process.
    # For demonstration, we call the `build_apk` method of the code generator.
    generated_apk_path = code_generator.build_apk(project_name=project_name)

    if generated_apk_path:
        print(f"APK compilation simulated successfully. Output: {generated_apk_path}")
    else:
        print("APK compilation simulation failed.")

    print("\n--- Lobe 8 Finished ---")

    print("\n--- Grand Objective Simulation Flow Finished ---")
    # Final cleanup of all generated artifacts
    cleanup_android_project_artifacts(dirs_to_clean=[ANDROID_PROJECT_TEMPLATE_DIR, OUTPUT_APKS_DIR])


if __name__ == "__main__":
    main_execution_flow()