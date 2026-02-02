import os
import re
import shutil
from pathlib import Path

# Assume these are defined elsewhere and imported
# from lobe_0_language_lobe import LanguageLobe # For text generation
# from lobe_1_nlp_arabic_lobe import ArabicNLP # For Arabic parsing and understanding
# from lobe_4_code_generation_lobe import CodeGenerationLobe # For generating code from NLP
# from lobe_6_synthesis_lobe import SynthesisLobe # For combining components
# from lobe_8_apk_compiler_lobe import APKCompilerLobe # For compiling APKs
# from utils import KNOWLEDGE_BASE_DIR, ANDROID_PROJECT_TEMPLATE_DIR, PROJECT_OUTPUT_DIR, cleanup_dummy_files, cleanup_android_project_template # Utility functions

# --- Dummy Implementations for demonstration purposes ---
# In a real scenario, these would be actual imported modules.

class LanguageLobe:
    def generate_text(self, prompt: str) -> str:
        print(f"[LanguageLobe] Generating text for prompt: '{prompt}'")
        # Dummy text generation logic
        if "simple calculator" in prompt.lower():
            return """
            Create an Android application that functions as a simple calculator.
            It should support addition, subtraction, multiplication, and division.
            The user interface should have buttons for digits 0-9,
            operators (+, -, *, /), a clear button (C), and an equals button (=).
            The display should show the current input and the result.
            """
        elif "todo list" in prompt.lower():
            return """
            Develop an Android application for managing a to-do list.
            Users should be able to add new tasks, mark tasks as complete,
            and delete tasks. The list should be persistent.
            """
        else:
            return "Generate a basic Android app."

class ArabicNLP:
    def parse_arabic_description(self, description: str) -> dict:
        print(f"[ArabicNLP] Parsing Arabic description: '{description}'")
        # Dummy Arabic parsing logic
        app_definition = {
            "app_name": "GenericApp",
            "features": [],
            "language": "Arabic"
        }
        if "آلة حاسبة بسيطة" in description:
            app_definition["app_name"] = "SimpleCalculator"
            app_definition["features"].append("calculator")
        elif "قائمة مهام" in description:
            app_definition["app_name"] = "TodoList"
            app_definition["features"].append("todo_list")
        else:
            app_definition["app_name"] = "UnnamedArabicApp"
            app_definition["features"].append("basic_functionality")
        return app_definition

class CodeGenerationLobe:
    def generate_android_code(self, app_definition: dict) -> dict:
        print(f"[CodeGenerationLobe] Generating Android code for: {app_definition}")
        generated_code = {
            "java": "",
            "xml": ""
        }
        app_name = app_definition.get("app_name", "DefaultApp")
        features = app_definition.get("features", [])

        if "calculator" in features:
            generated_code["java"] = f"""
package com.example.{app_name.lower()};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {{
    TextView textViewResult;
    String currentInput = "";
    String operator = "";
    double operand1 = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{app_name.lower()}_activity); // Assuming layout file name matches app_name

        textViewResult = findViewById(R.id.textViewResult);
        // Initialize buttons and set listeners (omitted for brevity)
    }}

    public void onDigitClick(View v) {{
        currentInput += ((Button)v).getText().toString();
        textViewResult.setText(currentInput);
    }}

    public void onOperatorClick(View v) {{
        if (operator.isEmpty()) {{
            operand1 = Double.parseDouble(currentInput);
            operator = ((Button)v).getText().toString();
            currentInput = "";
        }} else {{
            // Handle chaining operations
            onEqualsClick(v);
            operator = ((Button)v).getText().toString();
        }}
    }}

    public void onEqualsClick(View v) {{
        if (!operator.isEmpty() && !currentInput.isEmpty()) {{
            double operand2 = Double.parseDouble(currentInput);
            double result = 0;
            switch (operator) {{
                case "+": result = operand1 + operand2; break;
                case "-": result = operand1 - operand2; break;
                case "*": result = operand1 * operand2; break;
                case "/":
                    if (operand2 != 0) {{
                        result = operand1 / operand2;
                    }} else {{
                        textViewResult.setText("Error");
                        return;
                    }}
                    break;
            }}
            textViewResult.setText(String.valueOf(result));
            operand1 = result;
            currentInput = "";
            operator = "";
        }}
    }}

    public void onClearClick(View v) {{
        currentInput = "";
        operator = "";
        operand1 = 0;
        textViewResult.setText("");
    }}
}}
"""
            generated_code["xml"] = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{app_name}Activity">

    <TextView
        android:id="@+id/textViewResult"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:textAlignment="center"
        android:textSize="36sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        android:layout_marginTop="32dp"/>

    <!-- Button definitions for digits, operators, C, = would go here -->
    <!-- Example for digit 7 -->
    <Button
        android:id="@+id/button7"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="7"
        android:onClick="onDigitClick"
        app:layout_constraintTop_toBottomOf="@id/textViewResult"
        app:layout_constraintStart_toStartOf="parent"
        android:layout_marginTop="16dp"
        android:layout_marginStart="16dp"/>

    <!-- ... other buttons ... -->

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        elif "todo_list" in features:
            generated_code["java"] = f"""
package com.example.{app_name.lower()};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ListView;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {{
    EditText taskEditText;
    ListView taskListView;
    List<String> taskList;
    ArrayAdapter<String> taskAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{app_name.lower()}_activity); // Assuming layout file name matches app_name

        taskEditText = findViewById(R.id.taskEditText);
        taskListView = findViewById(R.id.taskListView);

        taskList = new ArrayList<>();
        taskAdapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, taskList);
        taskListView.setAdapter(taskAdapter);

        // Load tasks from persistence (omitted for brevity)
    }}

    public void onAddTaskClick(View v) {{
        String task = taskEditText.getText().toString().trim();
        if (!task.isEmpty()) {{
            taskList.add(task);
            taskAdapter.notifyDataSetChanged();
            taskEditText.setText("");
            // Save tasks to persistence (omitted for brevity)
        }}
    }}

    // Methods for marking as complete and deleting would be added here
    // Example:
    public void onDeleteTaskClick(View v) {{
        // Logic to delete selected task
    }}

    public void onMarkCompleteClick(View v) {{
        // Logic to mark selected task as complete
    }}
}}
"""
            generated_code["xml"] = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{app_name}Activity">

    <EditText
        android:id="@+id/taskEditText"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:hint="Enter a new task"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toStartOf="@+id/addTaskButton"
        android:layout_marginTop="16dp"
        android:layout_marginStart="16dp"
        android:layout_marginEnd="8dp"/>

    <Button
        android:id="@+id/addTaskButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Add"
        android:onClick="onAddTaskClick"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="16dp"
        android:layout_marginEnd="16dp"/>

    <ListView
        android:id="@+id/taskListView"
        android:layout_width="0dp"
        android:layout_height="0dp"
        app:layout_constraintTop_toBottomOf="@id/taskEditText"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent"
        android:layout_marginTop="16dp"
        android:layout_marginStart="16dp"
        android:layout_marginEnd="16dp"
        android:layout_marginBottom="16dp"/>

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        else:
            # Default basic app structure
            generated_code["java"] = f"""
package com.example.{app_name.lower()};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{app_name.lower()}_activity); // Assuming layout file name matches app_name
    }}
}}
"""
            generated_code["xml"] = f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{app_name}Activity">

    <!-- Basic layout content -->
</androidx.constraintlayout.widget.ConstraintLayout>
"""
        return generated_code

class SynthesisLobe:
    def construct_android_project(self, app_name: str, java_code: str, xml_layout: str) -> str:
        print(f"[SynthesisLobe] Constructing Android project for: {app_name}")
        project_dir_name = f"{app_name.replace(' ', '')}Project"
        project_path = Path(PROJECT_OUTPUT_DIR) / project_dir_name
        template_path = Path(ANDROID_PROJECT_TEMPLATE_DIR)

        if not template_path.exists():
            print(f"Error: Android project template not found at {template_path}")
            return ""

        try:
            shutil.copytree(template_path, project_path)
            print(f"Copied project template to: {project_path}")

            # Create necessary directories if they don't exist
            java_src_dir = project_path / "app" / "src" / "main" / "java" / "com" / "example" / app_name.lower()
            res_layout_dir = project_path / "app" / "src" / "main" / "res" / "layout"

            java_src_dir.mkdir(parents=True, exist_ok=True)
            res_layout_dir.mkdir(parents=True, exist_ok=True)

            # Write Java code
            main_activity_path = java_src_dir / "MainActivity.java"
            with open(main_activity_path, "w", encoding="utf-8") as f:
                f.write(java_code)
            print(f"Wrote MainActivity.java to: {main_activity_path}")

            # Write XML layout
            layout_file_name = f"{app_name.lower()}_activity.xml"
            layout_path = res_layout_dir / layout_file_name
            with open(layout_path, "w", encoding="utf-8") as f:
                f.write(xml_layout)
            print(f"Wrote {layout_file_name} to: {layout_path}")

            # Update AndroidManifest.xml (basic placeholder, more sophisticated merging might be needed)
            manifest_path = project_path / "app" / "src" / "main" / "AndroidManifest.xml"
            if manifest_path.exists():
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest_content = f.read()

                # Injecting activity declaration if not present (simple regex, can be fragile)
                activity_declaration = f"""
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
"""
                if f'<activity android:name=".MainActivity">' not in manifest_content:
                    manifest_content = manifest_content.replace("</application>", activity_declaration + "    </application>")
                    with open(manifest_path, "w", encoding="utf-8") as f:
                        f.write(manifest_content)
                    print(f"Updated AndroidManifest.xml with MainActivity.")
            else:
                print(f"Warning: AndroidManifest.xml not found at {manifest_path}")


            return str(project_path)

        except Exception as e:
            print(f"Error constructing Android project: {e}")
            return ""

class APKCompilerLobe:
    def compile_apk(self, project_path: str, app_name: str) -> str:
        print(f"[APKCompilerLobe] Compiling APK for project at: {project_path}")
        # This is a placeholder. In a real scenario, this would invoke Android SDK tools
        # like Gradle or `aapt` and `dx`/`d8` to build the APK.
        # For demonstration, we'll just create a dummy APK file path.

        if not Path(project_path).exists():
            print(f"Error: Project path '{project_path}' does not exist.")
            return ""

        # Simulate build process
        print("Simulating Android build process...")
        # In a real scenario, you'd run Gradle commands like:
        # subprocess.run(["./gradlew", "assembleRelease"], cwd=project_path)
        # Or use specific Android build tools.

        # For this demo, assume success and create a dummy APK path.
        # The actual APK would be in project_path/app/build/outputs/apk/release/
        apk_output_dir = Path(project_path) / "app" / "build" / "outputs" / "apk" / "release"
        apk_output_dir.mkdir(parents=True, exist_ok=True)
        generated_apk_path = apk_output_dir / f"{app_name.lower()}-release.apk"

        # Create a dummy APK file to simulate its existence
        try:
            with open(generated_apk_path, "w") as f:
                f.write("This is a dummy APK file.\n")
            print(f"Dummy APK file created at: {generated_apk_path}")
            return str(generated_apk_path)
        except Exception as e:
            print(f"Error creating dummy APK file: {e}")
            return ""


# --- End Dummy Implementations ---

# --- Lobe 3_arabic_nlp_module ---
# This lobe is responsible for understanding natural language Arabic
# and converting it into a structured, actionable format for subsequent lobes.

class ArabicNLPLobe:
    def __init__(self):
        self.arabic_parser = ArabicNLP()
        self.language_generator = LanguageLobe() # Used for generating structured descriptions if needed
        self.last_thought = "Initialized ArabicNLP Lobe."

    def process_arabic_request(self, arabic_prompt: str) -> dict:
        """
        Processes a natural language Arabic prompt to extract application requirements.

        Args:
            arabic_prompt: The natural language Arabic description of the desired app.

        Returns:
            A dictionary containing the structured app definition, or an error message.
            Example: {"app_name": "MyAwesomeApp", "features": ["login", "dashboard"], "language": "Arabic"}
        """
        print(f"\n--- Lobe 3_arabic_nlp_module Processing ---")
        print(f"Received Arabic prompt: '{arabic_prompt}'")

        try:
            # Use the ArabicNLP to parse the description
            app_definition = self.arabic_parser.parse_arabic_description(arabic_prompt)

            if not app_definition or not app_definition.get("app_name"):
                self.last_thought = "Failed to parse Arabic prompt or extract app name."
                print("Error: Could not extract a valid app definition from the Arabic prompt.")
                # Fallback: try to generate a generic app name and description
                generic_description_prompt = "Generate a description for a simple Android app in Arabic."
                generated_description = self.language_generator.generate_text(generic_description_prompt)
                app_definition = self.arabic_parser.parse_arabic_description(generated_description)
                if not app_definition or not app_definition.get("app_name"):
                    app_definition = {"app_name": "GenericArabicApp", "features": ["basic"], "language": "Arabic"}


            self.last_thought = f"Successfully parsed Arabic prompt. App definition: {app_definition}"
            print(f"Structured App Definition: {app_definition}")
            return app_definition

        except Exception as e:
            self.last_thought = f"An error occurred during Arabic NLP processing: {e}"
            print(f"Error processing Arabic prompt: {e}")
            return {"error": str(e)}

    def get_last_thought(self):
        return self.last_thought

# --- Lobe 4_code_generation_module ---
# This lobe takes the structured app definition and generates the necessary
# Java/Kotlin code and XML layouts for an Android application.

class CodeGenerationLobe:
    def __init__(self):
        self.code_generator = CodeGenerationLobe() # Instantiating the dummy class
        self.last_thought = "Initialized Code Generation Lobe."

    def generate_android_components(self, app_definition: dict) -> dict:
        """
        Generates Android Java code and XML layout files based on the app definition.

        Args:
            app_definition: A dictionary containing the structured app requirements.

        Returns:
            A dictionary with keys 'java' and 'xml' containing the generated code strings.
        """
        print(f"\n--- Lobe 4_code_generation_module Processing ---")
        print(f"Generating code for app definition: {app_definition}")

        try:
            generated_code = self.code_generator.generate_android_code(app_definition)
            self.last_thought = f"Successfully generated Android code components. Java code length: {len(generated_code.get('java', ''))}, XML code length: {len(generated_code.get('xml', ''))}"
            print("Generated Java Code Snippet:\n", generated_code['java'][:200] + "...")
            print("Generated XML Code Snippet:\n", generated_code['xml'][:200] + "...")
            return generated_code
        except Exception as e:
            self.last_thought = f"An error occurred during code generation: {e}"
            print(f"Error generating Android code: {e}")
            return {"error": str(e)}

    def get_last_thought(self):
        return self.last_thought

# --- Lobe 6_synthesis_module ---
# This lobe orchestrates the assembly of the generated code into a
# complete Android project structure, preparing it for compilation.

class SynthesisLobe:
    def __init__(self):
        self.project_constructor = SynthesisLobe() # Instantiating the dummy class
        self.last_thought = "Initialized Synthesis Lobe."

    def construct_project(self, app_definition: dict, generated_code: dict) -> str:
        """
        Constructs a full Android project structure from the generated code components.

        Args:
            app_definition: The structured app definition.
            generated_code: A dictionary containing 'java' and 'xml' code strings.

        Returns:
            The path to the constructed Android project directory, or an empty string on failure.
        """
        print(f"\n--- Lobe 6_synthesis_module Processing ---")
        app_name = app_definition.get("app_name", "UnnamedApp")
        java_code = generated_code.get("java", "")
        xml_layout = generated_code.get("xml", "")

        if not java_code or not xml_layout:
            self.last_thought = "Missing generated Java code or XML layout for project construction."
            print("Error: Cannot construct project without Java code and XML layout.")
            return ""

        print(f"Constructing Android project for '{app_name}'...")

        try:
            project_path = self.project_constructor.construct_android_project(app_name, java_code, xml_layout)
            if project_path:
                self.last_thought = f"Successfully constructed Android project at: {project_path}"
                print(f"Android project constructed at: {project_path}")
            else:
                self.last_thought = "Failed to construct Android project."
                print("Failed to construct Android project.")
            return project_path
        except Exception as e:
            self.last_thought = f"An error occurred during project synthesis: {e}"
            print(f"Error constructing Android project: {e}")
            return ""

    def get_last_thought(self):
        return self.last_thought

# --- Lobe 8_apk_compiler_module ---
# This lobe takes a constructed Android project and compiles it into a
# functional APK file.

class APKCompilerLobe:
    def __init__(self):
        self.compiler = APKCompilerLobe() # Instantiating the dummy class
        self.last_thought = "Initialized APK Compiler Lobe."

    def build_apk(self, project_path: str, app_name: str) -> str:
        """
        Compiles an Android project into an APK file.

        Args:
            project_path: The path to the Android project directory.
            app_name: The name of the application.

        Returns:
            The path to the generated APK file, or an empty string on failure.
        """
        print(f"\n--- Lobe 8_apk_compiler_module Processing ---")
        print(f"Attempting to compile APK for project at '{project_path}'...")

        if not project_path or not Path(project_path).exists():
            self.last_thought = "Invalid project path provided for APK compilation."
            print(f"Error: Project path '{project_path}' is invalid or does not exist.")
            return ""

        try:
            generated_apk_path = self.compiler.compile_apk(project_path, app_name)
            if generated_apk_path:
                self.last_thought = f"Successfully compiled APK at: {generated_apk_path}"
                print(f"Successfully generated APK at: {generated_apk_path}")
            else:
                self.last_thought = "APK compilation process failed."
                print("\nAPK generation process failed.")
            return generated_apk_path
        except Exception as e:
            self.last_thought = f"An error occurred during APK compilation: {e}"
            print(f"Error during APK compilation: {e}")
            return ""

    def get_last_thought(self):
        return self.last_thought

# --- Main Orchestration Example ---
# This demonstrates how the lobes would interact in a simplified flow.
# In a full implementation, a higher-level orchestrator (e.g., SynthesisLobe or a dedicated OrchestratorLobe)
# would manage the sequence and data flow between all lobes.

# Define dummy directories for demonstration purposes
KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
ANDROID_PROJECT_TEMPLATE_DIR = Path("./android_template")
PROJECT_OUTPUT_DIR = Path("./generated_projects")

# Create dummy directories and template if they don't exist
KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)
ANDROID_PROJECT_TEMPLATE_DIR.mkdir(exist_ok=True)
PROJECT_OUTPUT_DIR.mkdir(exist_ok=True)

# Create a dummy Android project template structure
(ANDROID_PROJECT_TEMPLATE_DIR / "app").mkdir(parents=True, exist_ok=True)
(ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src").mkdir(parents=True, exist_ok=True)
(ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main").mkdir(parents=True, exist_ok=True)
(ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "java" / "com" / "example" / "genericapp").mkdir(parents=True, exist_ok=True)
(ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "res" / "layout").mkdir(parents=True, exist_ok=True)

# Create dummy essential files within the template
with open(ANDROID_PROJECT_TEMPLATE_DIR / "settings.gradle", "w") as f:
    f.write("// dummy settings.gradle\n")
with open(ANDROID_PROJECT_TEMPLATE_DIR / "build.gradle", "w") as f:
    f.write("// dummy build.gradle\n")
with open(ANDROID_PROJECT_TEMPLATE_DIR / "app" / "build.gradle", "w") as f:
    f.write("// dummy app/build.gradle\n")
with open(ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "AndroidManifest.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.genericapp">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.GenericApp">
        <!-- MainActivity will be injected here -->
    </application>
</manifest>
""")

def cleanup_android_project_template():
    """Cleans up dummy project files and directories."""
    print("\n--- Cleaning up dummy project template ---")
    if ANDROID_PROJECT_TEMPLATE_DIR.exists():
        try:
            # Remove specific dummy files first to avoid issues during recursive deletion
            settings_gradle = ANDROID_PROJECT_TEMPLATE_DIR / "settings.gradle"
            if settings_gradle.exists(): settings_gradle.unlink()
            build_gradle = ANDROID_PROJECT_TEMPLATE_DIR / "build.gradle"
            if build_gradle.exists(): build_gradle.unlink()
            app_build_gradle = ANDROID_PROJECT_TEMPLATE_DIR / "app" / "build.gradle"
            if app_build_gradle.exists(): app_build_gradle.unlink()
            manifest_xml = ANDROID_PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "AndroidManifest.xml"
            if manifest_xml.exists(): manifest_xml.unlink()

            shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)
            print(f"Removed dummy template directory: {ANDROID_PROJECT_TEMPLATE_DIR}")
        except Exception as e:
            print(f"Error during template cleanup: {e}")

def cleanup_generated_projects():
    """Cleans up generated project directories."""
    print("\n--- Cleaning up generated projects ---")
    if PROJECT_OUTPUT_DIR.exists():
        try:
            shutil.rmtree(PROJECT_OUTPUT_DIR)
            print(f"Removed generated projects directory: {PROJECT_OUTPUT_DIR}")
        except Exception as e:
            print(f"Error during generated projects cleanup: {e}")


if __name__ == "__main__":
    # Initialize the lobes
    arabic_nlp_lobe = ArabicNLPLobe()
    code_generation_lobe = CodeGenerationLobe()
    synthesis_lobe = SynthesisLobe()
    apk_compiler_lobe = APKCompilerLobe()

    # Example Arabic prompt for a calculator app
    arabic_prompt_calculator = "أريد تطبيق آلة حاسبة بسيطة."
    # Example Arabic prompt for a todo list app
    arabic_prompt_todo = "أريد تطبيق قائمة مهام."

    # --- Processing a Calculator App Request ---
    print("\n--- DEMO: Building a Calculator App from Arabic ---")
    app_definition_calc = arabic_nlp_lobe.process_arabic_request(arabic_prompt_calculator)

    if "error" not in app_definition_calc:
        generated_code_calc = code_generation_lobe.generate_android_components(app_definition_calc)
        if "error" not in generated_code_calc:
            project_path_calc = synthesis_lobe.construct_project(app_definition_calc, generated_code_calc)
            if project_path_calc:
                generated_apk_path_calc = apk_compiler_lobe.build_apk(project_path_calc, app_definition_calc.get("app_name", "CalculatorApp"))
                if generated_apk_path_calc:
                    print(f"\nCalculator App APK generated successfully at: {generated_apk_path_calc}")
                else:
                    print("\nFailed to generate Calculator App APK.")
            else:
                print("\nFailed to construct Calculator App project.")
        else:
            print("\nFailed to generate code for Calculator App.")
    else:
        print("\nFailed to process Arabic request for Calculator App.")

    # --- Processing a To-Do List App Request ---
    print("\n\n--- DEMO: Building a To-Do List App from Arabic ---")
    app_definition_todo = arabic_nlp_lobe.process_arabic_request(arabic_prompt_todo)

    if "error" not in app_definition_todo:
        generated_code_todo = code_generation_lobe.generate_android_components(app_definition_todo)
        if "error" not in generated_code_todo:
            project_path_todo = synthesis_lobe.construct_project(app_definition_todo, generated_code_todo)
            if project_path_todo:
                generated_apk_path_todo = apk_compiler_lobe.build_apk(project_path_todo, app_definition_todo.get("app_name", "TodoListApp"))
                if generated_apk_path_todo:
                    print(f"\nTo-Do List App APK generated successfully at: {generated_apk_path_todo}")
                else:
                    print("\nFailed to generate To-Do List App APK.")
            else:
                print("\nFailed to construct To-Do List App project.")
        else:
            print("\nFailed to generate code for To-Do List App.")
    else:
        print("\nFailed to process Arabic request for To-Do List App.")

    # --- Clean up dummy files and directories ---
    cleanup_android_project_template()
    cleanup_generated_projects()

    print("\n--- Grand Objective Demo Finished ---")