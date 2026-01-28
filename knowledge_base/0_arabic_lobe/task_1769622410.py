import os
import subprocess
import shutil
from pathlib import Path

# Define constants for directory paths
BASE_DIR = Path(__file__).resolve().parent
APK_BUILD_DIR = BASE_DIR / "apk_build_artifacts"
JAVA_SOURCE_DIR = APK_BUILD_DIR / "java_src"
MANIFEST_DIR = APK_BUILD_DIR / "manifest"
RESOURCES_DIR = APK_BUILD_DIR / "res"
ASSETS_DIR = APK_BUILD_DIR / "assets"
SMALI_DIR = APK_BUILD_DIR / "smali"

# Ensure build directories are created
APK_BUILD_DIR.mkdir(exist_ok=True)
JAVA_SOURCE_DIR.mkdir(exist_ok=True)
MANIFEST_DIR.mkdir(exist_ok=True)
RESOURCES_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)
SMALI_DIR.mkdir(exist_ok=True)

class ArabicAPKBuilder:
    """
    A module designed to build APKs from natural language Arabic prompts,
    leveraging NLP Arabic understanding to generate Java code,
    Android Manifest, and resource files.
    """
    def __init__(self, language_model_path: str = None):
        """
        Initializes the ArabicAPKBuilder.

        Args:
            language_model_path (str, optional): Path to the language model
                                                 for Arabic text processing.
                                                 Defaults to None, implying an
                                                 internal or default model will be used.
        """
        self.language_model_path = language_model_path
        print("ArabicAPKBuilder initialized.")

    def parse_arabic_prompt(self, prompt: str) -> dict:
        """
        Parses an Arabic natural language prompt to extract intent, UI elements,
        and functionality requirements for an Android application.

        This method is a placeholder for advanced NLP Arabic processing.
        In a real implementation, this would involve tokenization,
        part-of-speech tagging, named entity recognition, and intent
        classification specifically for Arabic.

        Args:
            prompt (str): The Arabic natural language prompt describing the desired APK.

        Returns:
            dict: A structured representation of the prompt's requirements,
                  including inferred app name, activities, UI components,
                  and basic logic.
                  Example: {
                      "app_name": "تطبيق بسيط",
                      "activities": [
                          {
                              "name": "MainActivity",
                              "layout": "activity_main.xml",
                              "ui_elements": [
                                  {"type": "TextView", "id": "greeting_text", "text": "مرحبا بالعالم"},
                                  {"type": "Button", "id": "click_button", "text": "اضغط هنا"}
                              ],
                              "logic": "When click_button is clicked, change greeting_text to 'تم الضغط!'"
                          }
                      ]
                  }
        """
        print(f"Parsing Arabic prompt: '{prompt}'")
        # Placeholder for actual NLP Arabic parsing logic.
        # This would interact with a sophisticated Arabic NLP model.
        if "تطبيق لآلة حاسبة بسيطة" in prompt:
            return {
                "app_name": "آلة حاسبة بسيطة",
                "package_name": "com.example.simplecalculator",
                "activities": [
                    {
                        "name": "CalculatorActivity",
                        "layout": "activity_calculator.xml",
                        "ui_elements": [
                            {"type": "EditText", "id": "input_field", "hint": "أدخل الأرقام"},
                            {"type": "Button", "id": "btn_add", "text": "+"},
                            {"type": "Button", "id": "btn_subtract", "text": "-"},
                            {"type": "Button", "id": "btn_multiply", "text": "*"},
                            {"type": "Button", "id": "btn_divide", "text": "/"},
                            {"type": "Button", "id": "btn_equals", "text": "="},
                            {"type": "TextView", "id": "result_display", "text": "النتيجة: 0"}
                        ],
                        "logic": "Handle button clicks for operations and equals. Update input_field and result_display."
                    }
                ]
            }
        elif "تطبيق لعرض رسالة ترحيب" in prompt:
            return {
                "app_name": "تطبيق ترحيب",
                "package_name": "com.example.welcomeapp",
                "activities": [
                    {
                        "name": "WelcomeActivity",
                        "layout": "activity_welcome.xml",
                        "ui_elements": [
                            {"type": "TextView", "id": "welcome_message", "text": "أهلاً بك في تطبيق الترحيب!"}
                        ],
                        "logic": "Display the welcome message."
                    }
                ]
            }
        else:
            return {
                "app_name": "تطبيق افتراضي",
                "package_name": "com.example.defaultapp",
                "activities": [
                    {
                        "name": "MainActivity",
                        "layout": "activity_main.xml",
                        "ui_elements": [
                            {"type": "TextView", "id": "default_text", "text": "هذا تطبيق افتراضي"}
                        ],
                        "logic": "Display default text."
                    }
                ]
            }


    def generate_android_manifest(self, parsed_data: dict) -> Path:
        """
        Generates the AndroidManifest.xml file based on parsed application data.

        Args:
            parsed_data (dict): The structured data from parse_arabic_prompt.

        Returns:
            Path: The path to the generated AndroidManifest.xml file.
        """
        package_name = parsed_data.get("package_name", "com.example.generatedapp")
        app_name = parsed_data.get("app_name", "GeneratedApp")
        activities = parsed_data.get("activities", [])

        manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{app_name.replace(' ', '')}">
"""

        # Add app name string resource
        manifest_content += f"""
        <string name="app_name">{app_name}</string>
"""

        for activity in activities:
            activity_name = activity.get("name", "UnnamedActivity")
            manifest_content += f"""
        <activity android:name=".{activity_name}"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
"""
        manifest_content += """
    </application>

</manifest>
"""
        manifest_file = MANIFEST_DIR / "AndroidManifest.xml"
        with open(manifest_file, "w", encoding="utf-8") as f:
            f.write(manifest_content)
        print(f"Generated AndroidManifest.xml at: {manifest_file}")
        return manifest_file

    def generate_layout_file(self, activity_data: dict) -> Path:
        """
        Generates an Android layout XML file for a given activity.

        Args:
            activity_data (dict): Data for a single activity, including its UI elements.

        Returns:
            Path: The path to the generated layout XML file.
        """
        layout_name = activity_data.get("layout", "activity_default.xml")
        ui_elements = activity_data.get("ui_elements", [])
        activity_name = activity_data.get("name", "DefaultActivity")

        layout_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{activity_name}">
"""

        for i, element in enumerate(ui_elements):
            element_type = element.get("type", "TextView")
            element_id = element.get("id", f"element_{i}")
            text = element.get("text", "")
            hint = element.get("hint", "")

            layout_content += f"""
    <{element_type}
        android:id="@+id/{element_id}"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{text}"
        android:hint="{hint}"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent"
        tools:text="{text}" />
"""

        layout_content += """
</androidx.constraintlayout.widget.ConstraintLayout>
"""
        layout_file = RESOURCES_DIR / "layout" / layout_name
        layout_file.parent.mkdir(exist_ok=True)
        with open(layout_file, "w", encoding="utf-8") as f:
            f.write(layout_content)
        print(f"Generated layout file: {layout_file}")
        return layout_file

    def generate_java_activity(self, activity_data: dict, package_name: str) -> Path:
        """
        Generates a basic Java Activity file.

        Args:
            activity_data (dict): Data for a single activity.
            package_name (str): The package name for the Android application.

        Returns:
            Path: The path to the generated Java file.
        """
        activity_name = activity_data.get("name", "UnnamedActivity")
        layout_name = activity_data.get("layout", "activity_default")
        logic = activity_data.get("logic", "")

        java_content = f"""package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Button;
import android.widget.EditText; // Import for EditText

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{layout_name.replace('.xml', '')});

        // Initialize UI elements based on layout IDs
"""

        ui_elements = activity_data.get("ui_elements", [])
        for element in ui_elements:
            element_id = element.get("id", "")
            element_type = element.get("type", "TextView")
            if element_id:
                java_content += f"        {element_type} {element_id} = findViewById(R.id.{element_id});\n"

        java_content += "\n        // Basic logic implementation placeholder\n"
        if "آلة حاسبة بسيطة" in logic: # Specific logic for Calculator
            java_content += """
        EditText inputField = findViewById(R.id.input_field);
        TextView resultDisplay = findViewById(R.id.result_display);
        Button btnAdd = findViewById(R.id.btn_add);
        Button btnSubtract = findViewById(R.id.btn_subtract);
        Button btnMultiply = findViewById(R.id.btn_multiply);
        Button btnDivide = findViewById(R.id.btn_divide);
        Button btnEquals = findViewById(R.id.btn_equals);

        final String[] currentOperation = {""};
        final double[] operand1 = {0};

        View.OnClickListener numberButtonListener = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String buttonText = ((Button) v).getText().toString();
                inputField.setText(inputField.getText().toString() + buttonText);
            }
        };

        View.OnClickListener operationButtonListener = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    operand1[0] = Double.parseDouble(inputField.getText().toString());
                    currentOperation[0] = ((Button) v).getText().toString();
                    inputField.setText(""); // Clear input for next operand
                } catch (NumberFormatException e) {
                    resultDisplay.setText("خطأ في الإدخال");
                }
            }
        };

        btnAdd.setOnClickListener(operationButtonListener);
        btnSubtract.setOnClickListener(operationButtonListener);
        btnMultiply.setOnClickListener(operationButtonListener);
        btnDivide.setOnClickListener(operationButtonListener);

        btnEquals.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    double operand2 = Double.parseDouble(inputField.getText().toString());
                    double result = 0;

                    switch (currentOperation[0]) {
                        case "+":
                            result = operand1[0] + operand2;
                            break;
                        case "-":
                            result = operand1[0] - operand2;
                            break;
                        case "*":
                            result = operand1[0] * operand2;
                            break;
                        case "/":
                            if (operand2 == 0) {
                                resultDisplay.setText("لا يمكن القسمة على صفر");
                                return;
                            }
                            result = operand1[0] / operand2;
                            break;
                        default:
                            result = operand2; // If no operation was selected, just show the entered number
                            break;
                    }
                    resultDisplay.setText("النتيجة: " + result);
                    inputField.setText(""); // Clear input after calculation
                    currentOperation[0] = ""; // Reset operation
                    operand1[0] = 0; // Reset operand
                } catch (NumberFormatException e) {
                    resultDisplay.setText("خطأ في الإدخال");
                }
            }
        });

        // Assign listeners to number buttons (assuming buttons for 0-9)
        findViewById(R.id.btn_0).setOnClickListener(numberButtonListener);
        findViewById(R.id.btn_1).setOnClickListener(numberButtonListener);
        findViewById(R.id.btn_2).setOnClickListener(numberButtonListener);
        findViewById(R.id.btn_3).setOnClickListener(numberButtonListener);
        findViewById(R.id.btn_4).setOnClickListener(numberButtonListener);
        findViewById(R.id.btn_5).setOnClickListener(numberButtonListener);
        findViewById(R.id.btn_6).setOnClickListener(numberButtonListener);
        findViewById(R.id.btn_7).setOnClickListener(numberButtonListener);
        findViewById(R.id.btn_8).setOnClickListener(numberButtonListener);
        findViewById(R.id.btn_9).setOnClickListener(numberButtonListener);
        // Add listener for decimal point if needed
        // findViewById(R.id.btn_decimal).setOnClickListener(numberButtonListener);
"""
        elif "When click_button is clicked, change greeting_text to 'تم الضغط!'" in logic:
            java_content += """
        TextView greetingText = findViewById(R.id.greeting_text);
        Button clickButton = findViewById(R.id.click_button);

        clickButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                greetingText.setText("تم الضغط!");
            }
        });
"""
        else:
            java_content += f"""
        // Placeholder for logic: {logic}
        // This section would contain event listeners and method calls
        // to implement the described functionality.
"""

        java_content += """
    }
}
"""
        java_file_path = JAVA_SOURCE_DIR / package_name.replace('.', '/')
        java_file_path.mkdir(parents=True, exist_ok=True)
        java_file = java_file_path / f"{activity_name}.java"
        with open(java_file, "w", encoding="utf-8") as f:
            f.write(java_content)
        print(f"Generated Java activity file: {java_file}")
        return java_file

    def build_apk(self, parsed_data: dict) -> Path:
        """
        Builds the APK by compiling generated Java code and resources.
        This is a simplified representation of the build process, which would
        typically involve using Android SDK tools (javac, dx, aapt, apksigner).

        Args:
            parsed_data (dict): The structured data from parse_arabic_prompt.

        Returns:
            Path: The path to the generated APK file.
        """
        package_name = parsed_data.get("package_name", "com.example.generatedapp")
        app_name = parsed_data.get("app_name", "GeneratedApp").replace(' ', '').lower()
        apk_output_name = f"{app_name}.apk"
        apk_file_path = BASE_DIR / apk_output_name

        print("--- Starting APK Build Process ---")

        # 1. Generate AndroidManifest.xml
        manifest_file = self.generate_android_manifest(parsed_data)

        # 2. Generate Layout XML files
        for activity_data in parsed_data.get("activities", []):
            self.generate_layout_file(activity_data)

        # 3. Generate Java Activity files
        for activity_data in parsed_data.get("activities", []):
            self.generate_java_activity(activity_data, package_name)

        # --- Simplified build steps using external tools ---
        # In a real scenario, this would involve:
        # - Compiling Java source to .class files using javac
        # - Converting .class files to Dalvik Executable (.dex) using dx (or d8)
        # - Packaging resources and manifest using aapt
        # - Creating an unsigned APK
        # - Signing the APK with a debug or release key

        # For demonstration, we'll assume a simplified scenario where we
        # could potentially call external build tools if available.
        # Since we don't have a full Android SDK setup here, this is a mock.

        print("Mocking APK build process. In a real environment, this would invoke Android SDK tools.")
        print(f"Simulating creation of APK: {apk_file_path}")

        # Create a dummy APK file for demonstration purposes.
        # In a real scenario, you'd use `aapt` to package resources,
        # `javac` to compile Java, `d8` to create dex files, and then
        # zip them into an APK, followed by signing.
        try:
            # Attempt to create a dummy structure that resembles an APK's contents
            dummy_apk_contents_dir = APK_BUILD_DIR / "dummy_apk_structure"
            dummy_apk_contents_dir.mkdir(exist_ok=True)

            # Simulate classes.dex
            (dummy_apk_contents_dir / "classes.dex").touch()

            # Simulate resources.arsc (created by aapt)
            (dummy_apk_contents_dir / "resources.arsc").touch()

            # Simulate compiled layouts in res/layout
            res_layout_dir = dummy_apk_contents_dir / "res" / "layout"
            res_layout_dir.mkdir(parents=True, exist_ok=True)
            for layout_file in RESOURCES_DIR.glob("layout/*.xml"):
                shutil.copy(layout_file, res_layout_dir / layout_file.name)

            # Simulate AndroidManifest.xml
            shutil.copy(manifest_file, dummy_apk_contents_dir / "AndroidManifest.xml")

            # Create the dummy APK by zipping the contents
            # This requires the 'zip' command to be available.
            # Alternatively, use Python's zipfile module.
            with zipfile.ZipFile(apk_file_path, 'w') as zipf:
                for root, _, files in os.walk(dummy_apk_contents_dir):
                    for file in files:
                        abs_path = os.path.join(root, file)
                        arc_name = os.path.relpath(abs_path, dummy_apk_contents_dir)
                        zipf.write(abs_path, arcname=arc_name)

            print(f"Successfully created a dummy APK file at: {apk_file_path}")
            # Clean up dummy structure
            shutil.rmtree(dummy_apk_contents_dir)

        except FileNotFoundError:
            print("Warning: 'zip' command not found. Cannot create dummy APK. Continuing without APK generation.")
            # Create an empty placeholder file if zip is not available.
            apk_file_path.touch()
            print(f"Created an empty placeholder APK file at: {apk_file_path}")
        except Exception as e:
            print(f"An error occurred during dummy APK creation: {e}")
            apk_file_path.touch()
            print(f"Created an empty placeholder APK file at: {apk_file_path}")


        print("--- APK Build Process Mock Finished ---")
        return apk_file_path

    def generate_apk_from_prompt(self, prompt: str) -> Path:
        """
        Orchestrates the process of parsing an Arabic prompt and building an APK.

        Args:
            prompt (str): The Arabic natural language prompt.

        Returns:
            Path: The path to the generated APK file.
        """
        print(f"\n--- Generating APK from prompt: '{prompt}' ---")
        parsed_data = self.parse_arabic_prompt(prompt)
        apk_path = self.build_apk(parsed_data)
        print(f"--- APK Generation Complete: {apk_path} ---")
        return apk_path

# Example Usage (for testing this module in isolation)
if __name__ == "__main__":
    import zipfile # Import zipfile here for the dummy APK creation

    # Clean up previous artifacts if they exist
    if APK_BUILD_DIR.exists():
        shutil.rmtree(APK_BUILD_DIR)
    APK_BUILD_DIR.mkdir()

    if (BASE_DIR / "simple_calculator.apk").exists():
        (BASE_DIR / "simple_calculator.apk").unlink()
    if (BASE_DIR / "welcome_app.apk").exists():
        (BASE_DIR / "welcome_app.apk").unlink()


    builder = ArabicAPKBuilder()

    # Example 1: Simple Calculator
    calculator_prompt = "أنشئ تطبيق آلة حاسبة بسيطة تدعم الجمع والطرح والضرب والقسمة."
    calculator_apk_path = builder.generate_apk_from_prompt(calculator_prompt)
    print(f"Calculator APK generated at: {calculator_apk_path}")

    # Example 2: Welcome App
    welcome_prompt = "أنشئ تطبيق لعرض رسالة ترحيب باسم 'أهلاً بك في تطبيق الترحيب!'"
    welcome_apk_path = builder.generate_apk_from_prompt(welcome_prompt)
    print(f"Welcome App APK generated at: {welcome_apk_path}")

    # Example 3: Default App
    default_prompt = "تطبيق افتراضي."
    default_apk_path = builder.generate_apk_from_prompt(default_prompt)
    print(f"Default App APK generated at: {default_apk_path}")

    print("\n--- ArabicAPKBuilder Demo Finished ---")

    # Clean up dummy directories created by the builder
    if APK_BUILD_DIR.exists():
        print(f"Cleaning up APK build artifacts in: {APK_BUILD_DIR}")
        shutil.rmtree(APK_BUILD_DIR)