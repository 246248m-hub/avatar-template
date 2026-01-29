import os
import json
import zipfile
import subprocess
from pathlib import Path

# Assume these are defined in other lobes or configuration files
KNOWLEDGE_BASE_DIR = Path("knowledge_base")
PROJECT_TEMPLATE_DIR = Path("project_templates/android")
OUTPUT_DIR = Path("generated_apks")
GRADLE_WRAPPER_PATH = "gradlew" # Relative path to the gradlew script

class ArabicParser:
    def __init__(self, knowledge_base_path: Path):
        self.knowledge_base_path = knowledge_base_path
        self.intent_map = self._load_intent_map()

    def _load_intent_map(self):
        try:
            with open(self.knowledge_base_path / "arabic_intents.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Intent map not found at {self.knowledge_base_path / 'arabic_intents.json'}")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.knowledge_base_path / 'arabic_intents.json'}")
            return {}

    def parse_arabic_command(self, command: str) -> dict:
        """
        Parses an Arabic command to identify its intent and entities.
        This is a simplified example. A real implementation would use
        more sophisticated NLP techniques (e.g., NLTK, spaCy with Arabic models).
        """
        for intent, patterns in self.intent_map.items():
            for pattern in patterns.get("keywords", []):
                if pattern.lower() in command.lower():
                    entities = self._extract_entities(command, intent)
                    return {"intent": intent, "entities": entities}
        return {"intent": "unknown", "entities": {}}

    def _extract_entities(self, command: str, intent: str) -> dict:
        """
        Extracts entities based on the identified intent.
        This is a placeholder and would need specific logic for each intent.
        """
        entities = {}
        if intent == "create_calculator_app":
            # Example: Extract app name if provided
            import re
            match = re.search(r"إنشاء تطبيق حاسبة باسم (.*)", command, re.IGNORECASE)
            if match:
                entities["app_name"] = match.group(1).strip()
        return entities

class ApkBuilder:
    def __init__(self, project_template_path: Path, output_dir: Path):
        self.project_template_path = project_template_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_apk(self, app_name: str, android_manifest_content: str, java_code: str, layout_xml: str) -> Path:
        """
        Builds an Android APK from provided components.
        This method orchestrates the process of setting up a project,
        writing necessary files, and invoking Gradle to build the APK.
        """
        project_root = self.output_dir / f"{app_name}_project"
        project_root.mkdir(parents=True, exist_ok=True)

        # 1. Copy project template
        import shutil
        shutil.copytree(self.project_template_path, project_root, dirs_exist_ok=True)

        # 2. Write AndroidManifest.xml
        manifest_dir = project_root / "app" / "src" / "main"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        with open(manifest_dir / "AndroidManifest.xml", "w", encoding="utf-8") as f:
            f.write(android_manifest_content)

        # 3. Write Java code
        java_dir = manifest_dir / "java" / "com" / "example" / "myapp" # Example package
        java_dir.mkdir(parents=True, exist_ok=True)
        with open(java_dir / f"{app_name.capitalize()}.java", "w", encoding="utf-8") as f:
            f.write(java_code)

        # 4. Write layout XML
        layout_dir = project_root / "app" / "src" / "main" / "res" / "layout"
        layout_dir.mkdir(parents=True, exist_ok=True)
        with open(layout_dir / "activity_main.xml", "w", encoding="utf-8") as f:
            f.write(layout_xml)

        # 5. Update build.gradle (simplified: assumes basic structure)
        # In a real scenario, you'd parse and modify build.gradle more robustly.
        # For this demo, we assume the template is sufficient or you'd update
        # things like applicationId.

        # 6. Invoke Gradle to build the APK
        print(f"Invoking Gradle to build APK for '{app_name}'...")
        try:
            # Ensure gradlew is executable
            gradlew_path = project_root / GRADLE_WRAPPER_PATH
            if not gradlew_path.exists():
                raise FileNotFoundError(f"Gradle wrapper script not found at {gradlew_path}")
            gradlew_path.chmod(gradlew_path.stat().st_mode | 0o111) # Make executable

            # Execute Gradle command
            # Use a shell=True for simplicity, but be cautious in production
            result = subprocess.run(
                [f"./{GRADLE_WRAPPER_PATH}", "assembleDebug"],
                cwd=project_root,
                capture_output=True,
                text=True,
                check=True
            )
            print("Gradle build output:")
            print(result.stdout)

            # Find the generated APK
            apk_path = None
            for root, _, files in os.walk(project_root / "app" / "build" / "outputs" / "apk" / "debug"):
                for file in files:
                    if file.endswith(".apk"):
                        apk_path = Path(root) / file
                        break
                if apk_path:
                    break

            if apk_path:
                final_apk_path = self.output_dir / f"{app_name}.apk"
                shutil.move(apk_path, final_apk_path)
                print(f"APK successfully generated: {final_apk_path}")
                return final_apk_path
            else:
                raise RuntimeError("Could not find generated APK file.")

        except subprocess.CalledProcessError as e:
            print(f"Gradle build failed: {e}")
            print("Gradle stderr:")
            print(e.stderr)
            raise RuntimeError(f"APK build process failed: {e.stderr}") from e
        except Exception as e:
            print(f"An error occurred during APK building: {e}")
            raise RuntimeError(f"APK build process encountered an unexpected error: {e}") from e

# --- Mock Data and Functions (for demonstration purposes) ---
# In a real system, these would be generated by other lobes.

def mock_generate_android_manifest(app_name: str) -> str:
    return f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.myapp">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".{app_name.capitalize()}">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""

def mock_generate_java_code(app_name: str) -> str:
    # Simplified calculator logic
    return f"""
package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class {app_name.capitalize()} extends AppCompatActivity {{

    private TextView textViewResult;
    private String currentInput = "";
    private String operator = "";
    private double operand1 = 0;
    private boolean expectingNewOperand = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assuming layout is activity_main.xml

        textViewResult = findViewById(R.id.textViewResult);
        Button btnClear = findViewById(R.id.btnClear);
        Button btnDivide = findViewById(R.id.btnDivide);
        Button btnMultiply = findViewById(R.id.btnMultiply);
        Button btnSubtract = findViewById(R.id.btnSubtract);
        Button btnAdd = findViewById(R.id.btnAdd);
        Button btnEquals = findViewById(R.id.btnEquals);
        Button btnDecimal = findViewById(R.id.btnDecimal);
        Button btn0 = findViewById(R.id.btn0);
        Button btn1 = findViewById(R.id.btn1);
        Button btn2 = findViewById(R.id.btn2);
        Button btn3 = findViewById(R.id.btn3);
        Button btn4 = findViewById(R.id.btn4);
        Button btn5 = findViewById(R.id.btn5);
        Button btn6 = findViewById(R.id.btn6);
        Button btn7 = findViewById(R.id.btn7);
        Button btn8 = findViewById(R.id.btn8);
        Button btn9 = findViewById(R.id.btn9);

        View.OnClickListener numberClickListener = v -> {{
            Button button = (Button) v;
            String digit = button.getText().toString();
            if (expectingNewOperand) {{
                currentInput = digit;
                expectingNewOperand = false;
            }} else {{
                currentInput = currentInput + digit;
            }}
            textViewResult.setText(currentInput);
        }};

        View.OnClickListener operatorClickListener = v -> {{
            Button button = (Button) v;
            String op = button.getText().toString();
            if (!currentInput.isEmpty()) {{
                if (operator.isEmpty()) {{
                    operand1 = Double.parseDouble(currentInput);
                }} else {{
                    calculate();
                }}
                operator = op;
                expectingNewOperand = true;
            }}
        }};

        btn0.setOnClickListener(numberClickListener);
        btn1.setOnClickListener(numberClickListener);
        btn2.setOnClickListener(numberClickListener);
        btn3.setOnClickListener(numberClickListener);
        btn4.setOnClickListener(numberClickListener);
        btn5.setOnClickListener(numberClickListener);
        btn6.setOnClickListener(numberClickListener);
        btn7.setOnClickListener(numberClickListener);
        btn8.setOnClickListener(numberClickListener);
        btn9.setOnClickListener(numberClickListener);
        btnDecimal.setOnClickListener(numberClickListener); // Handle decimal point logic

        btnAdd.setOnClickListener(operatorClickListener);
        btnSubtract.setOnClickListener(operatorClickListener);
        btnMultiply.setOnClickListener(operatorClickListener);
        btnDivide.setOnClickListener(operatorClickListener);

        btnEquals.setOnClickListener(v -> {{
            if (!operator.isEmpty() && !currentInput.isEmpty()) {{
                calculate();
                operator = "";
                expectingNewOperand = true; // Ready for a new calculation
            }}
        }});

        btnClear.setOnClickListener(v -> {{
            currentInput = "";
            operator = "";
            operand1 = 0;
            expectingNewOperand = false;
            textViewResult.setText("0");
        }});
    }}

    private void calculate() {{
        double operand2 = Double.parseDouble(currentInput);
        double result = 0;

        switch (operator) {{
            case "+":
                result = operand1 + operand2;
                break;
            case "-":
                result = operand1 - operand2;
                break;
            case "*":
                result = operand1 * operand2;
                break;
            case "/":
                if (operand2 != 0) {{
                    result = operand1 / operand2;
                }} else {{
                    textViewResult.setText("Error"); // Division by zero
                    return;
                }}
                break;
        }}

        operand1 = result;
        currentInput = String.valueOf(result);
        textViewResult.setText(currentInput);
    }}
}}
"""

def mock_generate_layout_xml(app_name: str) -> str:
    return f"""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{app_name.capitalize()}">

    <TextView
        android:id="@+id/textViewResult"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginStart="16dp"
        android:layout_marginTop="16dp"
        android:layout_marginEnd="16dp"
        android:text="0"
        android:textSize="48sp"
        android:gravity="end"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <Button
        android:id="@+id/btnClear"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="C"
        android:textSize="24sp"
        app:layout_constraintBaseline_toBaselineOf="@+id/btnDivide"
        app:layout_constraintEnd_toStartOf="@+id/btnDivide"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toStartOf="parent" />

    <Button
        android:id="@+id/btnDivide"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="/"
        android:textSize="24sp"
        app:layout_constraintBaseline_toBaselineOf="@+id/btnMultiply"
        app:layout_constraintEnd_toStartOf="@+id/btnMultiply"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toEndOf="@+id/btnClear" />

    <Button
        android:id="@+id/btnMultiply"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="*"
        android:textSize="24sp"
        app:layout_constraintBaseline_toBaselineOf="@+id/btnSubtract"
        app:layout_constraintEnd_toStartOf="@+id/btnSubtract"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toEndOf="@+id/btnDivide" />

    <Button
        android:id="@+id/btnSubtract"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="-"
        android:textSize="24sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toEndOf="@+id/btnMultiply"
        app:layout_constraintTop_toBottomOf="@+id/textViewResult"
        app:layout_constraintVertical_bias="0.1" />

    <Button
        android:id="@+id/btn7"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="7"
        android:textSize="24sp"
        app:layout_constraintBaseline_toBaselineOf="@+id/btn8"
        app:layout_constraintEnd_toStartOf="@+id/btn8"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toStartOf="parent" />

    <Button
        android:id="@+id/btn8"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="8"
        android:textSize="24sp"
        app:layout_constraintBaseline_toBaselineOf="@+id/btn9"
        app:layout_constraintEnd_toStartOf="@+id/btn9"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toEndOf="@+id/btn7" />

    <Button
        android:id="@+id/btn9"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="9"
        android:textSize="24sp"
        app:layout_constraintBaseline_toBaselineOf="@+id/btnAdd"
        app:layout_constraintEnd_toStartOf="@+id/btnAdd"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toEndOf="@+id/btn8" />

    <Button
        android:id="@+id/btnAdd"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="+"
        android:textSize="24sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toEndOf="@+id/btn9"
        app:layout_constraintTop_toBottomOf="@+id/btnSubtract"
        app:layout_constraintVertical_bias="0.0" />

    <Button
        android:id="@+id/btn4"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="4"
        android:textSize="24sp"
        app:layout_constraintBaseline_toBaselineOf="@+id/btn5"
        app:layout_constraintEnd_toStartOf="@+id/btn5"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toStartOf="parent" />

    <Button
        android:id="@+id/btn5"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="5"
        android:textSize="24sp"
        app:layout_constraintBaseline_toBaselineOf="@+id/btn6"
        app:layout_constraintEnd_toStartOf="@+id/btn6"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toEndOf="@+id/btn4" />

    <Button
        android:id="@+id/btn6"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="6"
        android:textSize="24sp"
        app:layout_constraintBaseline_toBaselineOf="@+id/btnEquals"
        app:layout_constraintEnd_toStartOf="@+id/btnEquals"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toEndOf="@+id/btn5" />

    <Button
        android:id="@+id/btnEquals"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="="
        android:textSize="24sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toEndOf="@+id/btn6"
        app:layout_constraintTop_toBottomOf="@+id/btnAdd"
        app:layout_constraintVertical_bias="0.0" />

    <Button
        android:id="@+id/btn1"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="1"
        android:textSize="24sp"
        app:layout_constraintBaseline_toBaselineOf="@+id/btn2"
        app:layout_constraintEnd_toStartOf="@+id/btn2"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toStartOf="parent" />

    <Button
        android:id="@+id/btn2"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="2"
        android:textSize="24sp"
        app:layout_constraintBaseline_toBaselineOf="@+id/btn3"
        app:layout_constraintEnd_toStartOf="@+id/btn3"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toEndOf="@+id/btn1" />

    <Button
        android:id="@+id/btn3"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="3"
        android:textSize="24sp"
        app:layout_constraintBaseline_toBaselineOf="@+id/btnDecimal"
        app:layout_constraintEnd_toStartOf="@+id/btnDecimal"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toEndOf="@+id/btn2" />

    <Button
        android:id="@+id/btnDecimal"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="."
        android:textSize="24sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toEndOf="@+id/btn3"
        app:layout_constraintTop_toBottomOf="@+id/btnEquals"
        app:layout_constraintVertical_bias="0.0" />

    <Button
        android:id="@+id/btn0"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="0"
        android:textSize="24sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.5"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/btn1" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""

# --- Lobe 7_apk_assembly_lobe ---
class ApkAssemblyLobe:
    def __init__(self, arabic_parser: ArabicParser, apk_builder: ApkBuilder):
        self.arabic_parser = arabic_parser
        self.apk_builder = apk_builder

    def process_arabic_command_for_apk(self, command: str) -> str:
        """
        Processes an Arabic command to generate an APK.
        This function orchestrates the parsing and building process.
        """
        print(f"\n--- Processing command for APK generation: '{command}' ---")
        parsed_command = self.arabic_parser.parse_arabic_command(command)

        if parsed_command["intent"] == "create_calculator_app":
            app_name = parsed_command.get("entities", {}).get("app_name", "MyCalculator")
            print(f"Intent recognized: Create Calculator App. App Name: {app_name}")

            # Mock generation of necessary Android components.
            # In a real scenario, these would be generated by other lobes based on entities.
            android_manifest = mock_generate_android_manifest(app_name)
            java_code = mock_generate_java_code(app_name)
            layout_xml = mock_generate_layout_xml(app_name)

            try:
                generated_apk_path = self.apk_builder.build_apk(
                    app_name=app_name,
                    android_manifest_content=android_manifest,
                    java_code=java_code,
                    layout_xml=layout_xml
                )
                print(f"APK generation successful. Path: {generated_apk_path}")
                return str(generated_apk_path)
            except RuntimeError as e:
                print(f"APK generation failed: {e}")
                return "APK generation failed."
        else:
            print(f"Unknown intent or insufficient information: {parsed_command['intent']}")
            return "Failed: Unknown intent."

# --- Main Execution / Demo ---
if __name__ == "__main__":
    # Setup paths
    KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    PROJECT_TEMPLATE_DIR.mkdir(exist_ok=True)

    # Create dummy intent map file for demonstration
    dummy_intent_map = {
        "create_calculator_app": {
            "keywords": ["إنشاء تطبيق حاسبة", "اصنع آلة حاسبة", "تطبيق حاسبة"],
            "slots": {"app_name": {"type": "string", "description": "اسم التطبيق"}}
        },
        "create_notes_app": {
            "keywords": ["إنشاء تطبيق ملاحظات", "اصنع تطبيق ملاحظات"],
            "slots": {}
        }
    }
    with open(KNOWLEDGE_BASE_DIR / "arabic_intents.json", "w", encoding="utf-8") as f:
        json.dump(dummy_intent_map, f, ensure_ascii=False, indent=4)

    # Create a dummy project template directory structure (minimal required for build)
    # In a real scenario, this would be a full Android project template.
    (PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "res" / "layout").mkdir(parents=True, exist_ok=True)
    (PROJECT_TEMPLATE_DIR / "app" / "src" / "main" / "java" / "com" / "example" / "myapp").mkdir(parents=True, exist_ok=True)
    (PROJECT_TEMPLATE_DIR / "gradle").mkdir(parents=True, exist_ok=True)
    (PROJECT_TEMPLATE_DIR / "gradlew").touch() # Placeholder for gradlew
    (PROJECT_TEMPLATE_DIR / "settings.gradle").touch()
    (PROJECT_TEMPLATE_DIR / "build.gradle").touch()
    (PROJECT_TEMPLATE_DIR / "app" / "build.gradle").touch()


    # Initialize Lobes
    arabic_parser_lobe = ArabicParser(knowledge_base_path=KNOWLEDGE_BASE_DIR)
    apk_builder_lobe = ApkBuilder(project_template_path=PROJECT_TEMPLATE_DIR, output_dir=OUTPUT_DIR)
    apk_assembly_lobe = ApkAssemblyLobe(arabic_parser=arabic_parser_lobe, apk_builder=apk_builder_lobe)

    # --- Demo ---
    print("--- ApkAssemblyLobe Demo ---")

    # Test Case 1: Create Calculator App
    command1 = "إنشاء تطبيق حاسبة باسم MyAwesomeCalculator"
    generated_apk_path_calc = apk_assembly_lobe.process_arabic_command_for_apk(command1)
    if "APK generation successful" in generated_apk_path_calc:
        print(f"Demo 1: APK generation successful. APK located at: {generated_apk_path_calc}")
    else:
        print("Demo 1: APK generation failed.")

    # Test Case 2: Create Calculator App with default name
    command2 = "اصنع لي آلة حاسبة"
    generated_apk_path_calc_default = apk_assembly_lobe.process_arabic_command_for_apk(command2)
    if "APK generation successful" in generated_apk_path_calc_default:
        print(f"Demo 2: APK generation successful. APK located at: {generated_apk_path_calc_default}")
    else:
        print("Demo 2: APK generation failed.")

    # Test Case 3: Unsupported command
    command3 = "اصنع تطبيق ملاحظات"
    result_unsupported = apk_assembly_lobe.process_arabic_command_for_apk(command3)
    if "Failed: Unknown intent." in result_unsupported:
        print(f"Demo 3: Correctly handled unsupported command.")
    else:
        print(f"Demo 3: Failed to handle unsupported command correctly. Result: {result_unsupported}")


    print("\n--- ApkAssemblyLobe Demo Finished ---")

    # Clean up dummy files and directories
    print("\n--- Cleaning up dummy files and directories ---")
    if KNOWLEDGE_BASE_DIR.exists():
        import shutil
        shutil.rmtree(KNOWLEDGE_BASE_DIR)
    if PROJECT_TEMPLATE_DIR.exists():
        import shutil
        shutil.rmtree(PROJECT_TEMPLATE_DIR)
    # Keep generated APKs for inspection
    # if OUTPUT_DIR.exists():
    #     import shutil
    #     shutil.rmtree(OUTPUT_DIR)