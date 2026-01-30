import os
import json
import shutil

# Assume these exist for demonstration purposes, in a real scenario they would be implemented
class ArabicParser:
    def parse_arabic_description(self, arabic_description: str) -> dict:
        """
        Parses natural language Arabic description into a structured format.
        This is a placeholder. A real implementation would involve advanced NLP techniques.
        """
        print(f"Parsing Arabic description: '{arabic_description}'")
        # Example: Simple keyword extraction for demonstration
        parsed_data = {
            "ui_elements": [],
            "actions": [],
            "app_name": "MyArabicApp"
        }
        if "input field" in arabic_description or "حقل ادخال" in arabic_description:
            parsed_data["ui_elements"].append({"type": "EditText", "label": "Message"})
        if "send button" in arabic_description or "زر الارسال" in arabic_description:
            parsed_data["ui_elements"].append({"type": "Button", "text": "Send", "action": "sendMessage"})
            parsed_data["actions"].append({"name": "sendMessage", "type": "send_message", "target": "backend"})
        if "title" in arabic_description:
            title_index = arabic_description.find("title") + len("title")
            title_end_index = arabic_description.find(".", title_index)
            if title_end_index == -1:
                title_end_index = len(arabic_description)
            parsed_data["app_name"] = arabic_description[title_index:title_end_index].strip()

        return parsed_data

class CodeGenerator:
    def generate_android_code(self, parsed_data: dict, project_root: str) -> str:
        """
        Generates Android (Java/Kotlin) code based on parsed data.
        This is a placeholder. A real implementation would create actual source files.
        """
        print(f"Generating Android code for '{parsed_data.get('app_name', 'UnnamedApp')}' in {project_root}")
        package_name = "com.example." + parsed_data.get("app_name", "myapp").lower().replace(" ", "")
        activity_name = parsed_data.get("app_name", "MainActivity").replace(" ", "")

        # Create dummy directories and files for demonstration
        os.makedirs(os.path.join(project_root, "app", "src", "main", "java", *package_name.split('.')), exist_ok=True)
        os.makedirs(os.path.join(project_root, "app", "src", "main", "res", "layout"), exist_ok=True)
        os.makedirs(os.path.join(project_root, "app", "src", "main", "res", "values"), exist_ok=True)

        activity_file_path = os.path.join(project_root, "app", "src", "main", "java", *package_name.split('.'), f"{activity_name}.java")
        layout_file_path = os.path.join(project_root, "app", "src", "main", "res", "layout", "activity_main.xml")
        manifest_file_path = os.path.join(project_root, "app", "src", "main", "AndroidManifest.xml")

        with open(activity_file_path, "w") as f:
            f.write(f"// Auto-generated Java code for {activity_name}\n")
            f.write(f"package {package_name};\n\n")
            f.write("import androidx.appcompat.app.AppCompatActivity;\nimport android.os.Bundle;\n\n")
            f.write(f"public class {activity_name} extends AppCompatActivity {{\n")
            f.write("    @Override\n    protected void onCreate(Bundle savedInstanceState) {\n        super.onCreate(savedInstanceState);\n        setContentView(R.layout.activity_main);\n")
            # Add UI element generation logic here based on parsed_data
            if "EditText" in str(parsed_data.get("ui_elements", [])):
                f.write("        // EditText for message input would be initialized here\n")
            if "Button" in str(parsed_data.get("ui_elements", [])):
                f.write("        // Button for sending message would be initialized and set listener here\n")
            f.write("    }\n}\n")

        with open(layout_file_path, "w") as f:
            f.write("<!-- Auto-generated layout XML -->\n")
            f.write("<androidx.constraintlayout.widget.ConstraintLayout xmlns:android=\"http://schemas.android.com/apk/res/android\" xmlns:app=\"http://schemas.android.com/apk/res-auto\" xmlns:tools=\"http://schemas.android.com/tools\" android:layout_width=\"match_parent\" android:layout_height=\"match_parent\" tools:context=\".MainActivity\">\n")
            # Add UI element layout here
            if "EditText" in str(parsed_data.get("ui_elements", [])):
                f.write("    <EditText\n        android:id=\"@+id/messageEditText\"\n        android:layout_width=\"0dp\"\n        android:layout_height=\"wrap_content\"\n        android:hint=\"Enter message\"\n        app:layout_constraintTop_toTopOf=\"parent\"\n        app:layout_constraintStart_toStartOf=\"parent\"\n        app:layout_constraintEnd_toEndOf=\"parent\"\n        android:layout_margin=\"16dp\"/>\n")
            if "Button" in str(parsed_data.get("ui_elements", [])):
                f.write("    <Button\n        android:id=\"@+id/sendButton\"\n        android:layout_width=\"wrap_content\"\n        android:layout_height=\"wrap_content\"\n        android:text=\"Send\"\n        app:layout_constraintTop_toBottomOf=\"@id/messageEditText\"\n        app:layout_constraintStart_toStartOf=\"parent\"\n        app:layout_constraintEnd_toEndOf=\"parent\"\n        android:layout_marginTop=\"16dp\"/>\n")
            f.write("</androidx.constraintlayout.widget.ConstraintLayout>\n")

        with open(manifest_file_path, "w") as f:
            f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
            f.write(f"<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\" package=\"{package_name}\">\n")
            f.write("    <application\n        android:allowBackup=\"true\"\n        android:icon=\"@mipmap/ic_launcher\"\n        android:label=\"@string/app_name\"\n        android:roundIcon=\"@mipmap/ic_launcher_round\"\n        android:supportsRtl=\"true\"\n        android:theme=\"@style/Theme.YourApp\">\n")
            f.write(f"        <activity android:name=\".{activity_name}\" android:exported=\"true\">\n")
            f.write("            <intent-filter>\n                <action android:name=\"android.intent.action.MAIN\" />\n                <category android:name=\"android.intent.category.LAUNCHER\" />\n            </intent-filter>\n        </activity>\n    </application>\n</manifest>\n")

        return project_root

class APKBuilder:
    def build_apk(self, project_root: str, app_name: str) -> str:
        """
        Builds an APK from the generated Android project.
        This is a placeholder. A real implementation would use Android SDK tools.
        """
        print(f"Building APK for '{app_name}' from project at {project_root}")
        apk_path = os.path.join(project_root, "app", "build", "outputs", "apk", "debug", f"{app_name.lower().replace(' ', '')}-debug.apk")
        os.makedirs(os.path.dirname(apk_path), exist_ok=True)
        with open(apk_path, "w") as f:
            f.write(f"// Dummy APK file for {app_name}\n")
            f.write("This is a placeholder for an actual APK file.\n")
        print(f"Dummy APK created at: {apk_path}")
        return apk_path

class ArabicAPKGenerator:
    def __init__(self):
        self.arabic_parser = ArabicParser()
        self.code_generator = CodeGenerator()
        self.apk_builder = APKBuilder()
        self.generated_apks_dir = "generated_apks"
        os.makedirs(self.generated_apks_dir, exist_ok=True)

    def generate_apk(self, arabic_description: str) -> tuple[str, str]:
        """
        Generates an APK from a natural language Arabic description.
        """
        print(f"\n--- Generating APK for Arabic Description: '{arabic_description}' ---")

        # Step 1: Parse the Arabic description
        parsed_data = self.arabic_parser.parse_arabic_description(arabic_description)
        app_name = parsed_data.get("app_name", "GeneratedApp")
        print(f"Parsed Data: {json.dumps(parsed_data, indent=2)}")

        # Step 2: Generate Android project code
        # Create a temporary project directory for code generation
        temp_project_root = os.path.join(self.generated_apks_dir, f"{app_name.lower().replace(' ', '')}_project")
        if os.path.exists(temp_project_root):
            shutil.rmtree(temp_project_root)
        os.makedirs(temp_project_root, exist_ok=True)

        generated_project_root = self.code_generator.generate_android_code(parsed_data, temp_project_root)
        print(f"Android project generated at: {generated_project_root}")

        # Step 3: Build the APK
        apk_output_path = self.apk_builder.build_apk(generated_project_root, app_name)
        print(f"APK generated successfully at: {apk_output_path}")

        return generated_project_root, apk_output_path

    def cleanup_generated_apks(self):
        """
        Cleans up the directory containing generated APKs and projects.
        """
        print(f"\n--- Cleaning up generated APKs directory: {self.generated_apks_dir} ---")
        if os.path.exists(self.generated_apks_dir):
            shutil.rmtree(self.generated_apks_dir)
            print("Generated APKs directory removed.")
        else:
            print("Generated APKs directory does not exist.")

if __name__ == '__main__':
    arabic_generator = ArabicAPKGenerator()

    # Example 1: Simple app with input and send button
    arabic_description_1 = "صمم لي تطبيق عنوانه 'رسالة ترحيب' يحتوي على حقل ادخال للرسالة وزر للارسال."
    project_root_1, apk_path_1 = arabic_generator.generate_apk(arabic_description_1)

    # Example 2: Another app description
    arabic_description_2 = "تطبيق بسيط بعنوان 'الآلة الحاسبة' مع حقل ادخال للأرقام وزر للجمع."
    # Note: The current parser is very basic and might not fully interpret 'addition button' or 'calculator' accurately.
    # This highlights the need for more sophisticated NLP in ArabicParser.
    project_root_2, apk_path_2 = arabic_generator.generate_apk(arabic_description_2)

    # Clean up the generated files after demonstrations
    arabic_generator.cleanup_generated_apks()

    print("\n--- Arabic APK Generation Module Demo Finished ---")