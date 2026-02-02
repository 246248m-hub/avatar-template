import os
import subprocess
from typing import List, Dict, Any

# Assume these helper functions and classes are defined elsewhere and imported
# from utils import get_file_content, create_file, execute_command, cleanup_directory
# from models import AndroidManifest, JavaFile, XmlLayout, ResourceFile

# Mock implementations for demonstration purposes
class MockManifest:
    def __init__(self):
        self.package_name = "com.example.app"
        self.version_code = 1
        self.version_name = "1.0"
        self.activities = []
        self.permissions = []

    def add_activity(self, name: str, intent_filters: List[Dict[str, Any]] = None):
        self.activities.append({"name": name, "intent_filters": intent_filters or []})

    def to_xml(self) -> str:
        activity_declarations = ""
        for activity in self.activities:
            activity_declarations += f"""
            <activity android:name=".{activity['name']}">
                {"".join([f'<intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter>' if 'MAIN' in f.get('action', '') else '' for f in activity['intent_filters']])}
            </activity>
            """
        return f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{self.package_name}"
    android:versionCode="{self.version_code}"
    android:versionName="{self.version_name}">
    {activity_declarations}
</manifest>
"""

class MockJavaFile:
    def __init__(self, class_name: str, package_name: str):
        self.class_name = class_name
        self.package_name = package_name
        self.imports = []
        self.methods = []
        self.fields = []

    def add_import(self, import_statement: str):
        self.imports.append(import_statement)

    def add_method(self, method_signature: str, method_body: str):
        self.methods.append({"signature": method_signature, "body": method_body})

    def add_field(self, field_declaration: str):
        self.fields.append(field_declaration)

    def to_java(self) -> str:
        imports_str = "\n".join(self.imports)
        fields_str = "\n".join(self.fields)
        methods_str = "\n".join([f"{sig} {{\n{body}\n}}" for sig, body in self.methods])
        return f"""package {self.package_name};

{imports_str}

public class {self.class_name} {{
    {fields_str}
    {methods_str}
}}
"""

class MockXmlLayout:
    def __init__(self, root_element: str = "LinearLayout", layout_width: str = "match_parent", layout_height: str = "match_parent"):
        self.root_element = root_element
        self.attributes = {
            "xmlns:android": "http://schemas.android.com/apk/res/android",
            "android:layout_width": layout_width,
            "android:layout_height": layout_height,
            "android:orientation": "vertical"
        }
        self.children = []

    def add_child(self, child_element: Any):
        self.children.append(child_element)

    def to_xml(self) -> str:
        children_str = "\n".join([child.to_xml() if hasattr(child, 'to_xml') else str(child) for child in self.children])
        attributes_str = " ".join([f'{k}="{v}"' for k, v in self.attributes.items()])
        return f"<{self.root_element} {attributes_str}>\n{children_str}\n</{self.root_element}>"

class MockTextView(MockXmlLayout):
    def __init__(self, text: str, id: str = None, layout_width: str = "wrap_content", layout_height: str = "wrap_content", text_size: str = "16sp", gravity: str = "center"):
        super().__init__(root_element="TextView", layout_width=layout_width, layout_height=layout_height)
        self.attributes["android:text"] = f"@{id}" if id else text
        if id:
            self.attributes["android:id"] = f"@+id/{id}"
        if text_size:
            self.attributes["android:textSize"] = text_size
        if gravity:
            self.attributes["android:gravity"] = gravity

class MockButton(MockXmlLayout):
    def __init__(self, text: str, id: str = None, layout_width: str = "wrap_content", layout_height: str = "wrap_content"):
        super().__init__(root_element="Button", layout_width=layout_width, layout_height=layout_height)
        self.attributes["android:text"] = f"@{id}" if id else text
        if id:
            self.attributes["android:id"] = f"@+id/{id}"

class MockEditText(MockXmlLayout):
    def __init__(self, id: str, hint: str, layout_width: str = "match_parent", layout_height: str = "wrap_content"):
        super().__init__(root_element="EditText", layout_width=layout_width, layout_height=layout_height)
        self.attributes["android:id"] = f"@+id/{id}"
        self.attributes["android:hint"] = hint
        self.attributes["android:inputType"] = "text"

def create_file(filepath: str, content: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def execute_command(command: List[str], cwd: str = None):
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=True)
        print(f"Command executed successfully: {' '.join(command)}")
        print(f"Stdout:\n{result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(command)}")
        print(f"Stderr:\n{e.stderr}")
        return None
    except FileNotFoundError:
        print(f"Error: Command not found. Is '{command[0]}' in your PATH?")
        return None

def cleanup_directory(directory_path: str):
    if os.path.exists(directory_path):
        import shutil
        shutil.rmtree(directory_path)
        print(f"Cleaned up directory: {directory_path}")

def get_file_content(filepath: str) -> str:
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# Assume a base project structure exists or is created by a previous lobe.
# For this demo, we'll simulate a minimal structure.

class ArabicAPKGenerator:
    def __init__(self, project_root: str = "./android_project_demo"):
        self.project_root = project_root
        self.src_dir = os.path.join(project_root, "app", "src", "main")
        self.manifest_path = os.path.join(self.src_dir, "AndroidManifest.xml")
        self.res_dir = os.path.join(self.src_dir, "res")
        self.layout_dir = os.path.join(self.res_dir, "layout")
        self.values_dir = os.path.join(self.res_dir, "values")
        self.java_dir = os.path.join(self.src_dir, "java", "com", "example", "app")
        self.package_name = "com.example.app"
        self.main_activity_name = "MainActivity"

    def setup_project_structure(self):
        """Creates a basic Android project directory structure."""
        cleanup_directory(self.project_root)
        os.makedirs(self.java_dir, exist_ok=True)
        os.makedirs(self.layout_dir, exist_ok=True)
        os.makedirs(self.values_dir, exist_ok=True)

        # Create a placeholder strings.xml
        strings_content = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Arabic App</string>
</resources>
"""
        create_file(os.path.join(self.values_dir, "strings.xml"), strings_content)

    def generate_manifest(self, activities_info: List[Dict[str, Any]]):
        """Generates AndroidManifest.xml."""
        manifest = MockManifest()
        manifest.package_name = self.package_name
        # Add main activity
        manifest.add_activity(self.main_activity_name, [{"action": "android.intent.action.MAIN", "category": "android.intent.category.LAUNCHER"}])
        # Add other activities if specified
        for activity_info in activities_info:
            manifest.add_activity(activity_info['name'], activity_info.get('intent_filters', []))

        create_file(self.manifest_path, manifest.to_xml())
        print(f"Generated {self.manifest_path}")

    def generate_main_activity(self, layout_name: str):
        """Generates the main Java activity file."""
        activity_content = MockJavaFile(class_name=self.main_activity_name, package_name=self.package_name)
        activity_content.add_import("android.os.Bundle")
        activity_content.add_import("androidx.appcompat.app.AppCompatActivity")
        activity_content.add_method("onCreate", f"""
super.onCreate(savedInstanceState);
setContentView(R.layout.{layout_name});
        """)
        create_file(os.path.join(self.java_dir, f"{self.main_activity_name}.java"), activity_content.to_java())
        print(f"Generated {self.main_activity_name}.java")

    def generate_layout(self, layout_name: str, ui_elements: List[Dict[str, Any]]):
        """Generates an XML layout file with specified UI elements."""
        root_layout = MockXmlLayout()
        root_layout.attributes["android:orientation"] = "vertical"
        root_layout.attributes["android:padding"] = "16dp"

        for element_info in ui_elements:
            element_type = element_info.get("type")
            if element_type == "TextView":
                tv = MockTextView(
                    text=element_info.get("text", ""),
                    id=element_info.get("id"),
                    layout_width=element_info.get("layout_width", "wrap_content"),
                    layout_height=element_info.get("layout_height", "wrap_content"),
                    text_size=element_info.get("text_size", "16sp"),
                    gravity=element_info.get("gravity", "center")
                )
                root_layout.add_child(tv)
            elif element_type == "EditText":
                et = MockEditText(
                    id=element_info["id"],
                    hint=element_info.get("hint", ""),
                    layout_width=element_info.get("layout_width", "match_parent"),
                    layout_height=element_info.get("layout_height", "wrap_content")
                )
                root_layout.add_child(et)
            elif element_type == "Button":
                btn = MockButton(
                    text=element_info.get("text", ""),
                    id=element_info.get("id"),
                    layout_width=element_info.get("layout_width", "wrap_content"),
                    layout_height=element_info.get("layout_height", "wrap_content")
                )
                root_layout.add_child(btn)
            else:
                print(f"Warning: Unsupported UI element type '{element_type}'")

        create_file(os.path.join(self.layout_dir, f"{layout_name}.xml"), root_layout.to_xml())
        print(f"Generated layout: {layout_name}.xml")

    def build_apk(self) -> str | None:
        """Builds the APK using Gradle.
        Assumes Gradle is installed and in the PATH.
        """
        print("Attempting to build APK using Gradle...")
        # Use a wrapper script if available, otherwise assume gradle command is in PATH
        gradle_command = ["./gradlew", "assembleDebug"] # Assumes gradlew is in project_root
        if not os.path.exists(os.path.join(self.project_root, "gradlew")):
            gradle_command = ["gradle", "assembleDebug"]
            print("gradlew script not found, attempting to use 'gradle' command.")

        result = execute_command(gradle_command, cwd=self.project_root)

        if result is None:
            print("Gradle build failed.")
            return None

        # Try to find the generated APK
        # Common paths: app/build/outputs/apk/debug/app-debug.apk
        apk_path = os.path.join(self.project_root, "app", "build", "outputs", "apk", "debug", "app-debug.apk")
        if os.path.exists(apk_path):
            print(f"Successfully generated APK at: {apk_path}")
            return apk_path
        else:
            print("Could not find generated APK at expected location.")
            # Attempt to parse build output for APK location, or return None
            return None

    def generate_apk_from_arabic(self, arabic_command: str) -> str | None:
        """
        Parses an Arabic command and generates a corresponding Android APK.
        This is a simplified parser and generator.
        """
        print(f"\n--- Processing Arabic Command: '{arabic_command}' ---")
        self.setup_project_structure()

        # --- Simplified Arabic Command Parsing ---
        # This needs to be significantly more sophisticated for real-world use.
        # We'll look for keywords to determine the app's functionality and UI.

        app_title = "تطبيق بسيط"
        main_activity_layout_name = "activity_main"
        ui_elements = []
        activities_to_declare = []

        if "احسب مساحة المستطيل" in arabic_command or "حساب مساحة المستطيل" in arabic_command:
            app_title = "حاسبة مساحة المستطيل"
            main_activity_layout_name = "activity_rectangle_area"

            # UI for rectangle area calculation
            ui_elements.extend([
                {"type": "TextView", "text": "أدخل الطول:", "id": "label_length", "gravity": "left", "layout_width": "match_parent"},
                {"type": "EditText", "id": "edit_text_length", "hint": "الطول", "layout_width": "match_parent"},
                {"type": "TextView", "text": "أدخل العرض:", "id": "label_width", "gravity": "left", "layout_width": "match_parent"},
                {"type": "EditText", "id": "edit_text_width", "hint": "العرض", "layout_width": "match_parent"},
                {"type": "Button", "text": "احسب", "id": "button_calculate", "layout_width": "wrap_content", "gravity": "center_horizontal"},
                {"type": "TextView", "text": "المساحة:", "id": "label_area", "gravity": "left", "layout_width": "match_parent"},
                {"type": "TextView", "text": "", "id": "text_view_area", "gravity": "center", "text_size": "20sp", "layout_width": "match_parent"}
            ])

            # Generate a corresponding Java activity that handles the calculation
            main_activity_java = MockJavaFile(class_name=self.main_activity_name, package_name=self.package_name)
            main_activity_java.add_import("android.os.Bundle")
            main_activity_java.add_import("androidx.appcompat.app.AppCompatActivity")
            main_activity_java.add_import("android.widget.EditText")
            main_activity_java.add_import("android.widget.TextView")
            main_activity_java.add_import("android.widget.Button")
            main_activity_java.add_import("android.view.View")
            main_activity_java.add_import("android.text.TextUtils")
            main_activity_java.add_field("EditText editTextLength;")
            main_activity_java.add_field("EditText editTextWidth;")
            main_activity_java.add_field("TextView textViewArea;")
            main_activity_java.add_field("Button buttonCalculate;")

            calculate_logic = """
            String lengthStr = editTextLength.getText().toString();
            String widthStr = editTextWidth.getText().toString();

            if (TextUtils.isEmpty(lengthStr) || TextUtils.isEmpty(widthStr)) {
                textViewArea.setText("الرجاء إدخال الطول والعرض.");
                return;
            }

            try {
                double length = Double.parseDouble(lengthStr);
                double width = Double.parseDouble(widthStr);
                double area = length * width;
                textViewArea.setText(String.format("المساحة: %.2f", area));
            } catch (NumberFormatException e) {
                textViewArea.setText("إدخال غير صالح. الرجاء إدخال أرقام.");
            }
            """
            main_activity_java.add_method("onCreate", f"""
super.onCreate(savedInstanceState);
setContentView(R.layout.{main_activity_layout_name});

editTextLength = findViewById(R.id.edit_text_length);
editTextWidth = findViewById(R.id.edit_text_width);
textViewArea = findViewById(R.id.text_view_area);
buttonCalculate = findViewById(R.id.button_calculate);

buttonCalculate.setOnClickListener(new View.OnClickListener() {{
    @Override
    public void onClick(View v) {{
        {calculate_logic}
    }}
}});
            """)
            create_file(os.path.join(self.java_dir, f"{self.main_activity_name}.java"), main_activity_java.to_java())
            print(f"Generated Java for rectangle area calculation.")

        elif "عرض رسالة ترحيب" in arabic_command:
            app_title = "رسالة ترحيب"
            main_activity_layout_name = "activity_welcome"

            ui_elements.extend([
                {"type": "TextView", "text": "أهلاً بك في تطبيقنا!", "id": "welcome_message", "layout_width": "match_parent", "gravity": "center", "text_size": "24sp"}
            ])
            # Basic welcome activity
            self.generate_main_activity(main_activity_layout_name)

        else:
            # Default basic app
            app_title = "تطبيق افتراضي"
            ui_elements.extend([
                {"type": "TextView", "text": "تم إنشاء التطبيق", "id": "default_text", "layout_width": "match_parent", "gravity": "center"}
            ])
            self.generate_main_activity(main_activity_layout_name)


        # Update strings.xml
        strings_content = f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{app_title}</string>
    <string name="welcome_message">أهلاً بك في تطبيقنا!</string>
    <string name="label_length">الطول:</string>
    <string name="label_width">العرض:</string>
    <string name="button_calculate">احسب</string>
    <string name="label_area">المساحة:</string>
</resources>
"""
        create_file(os.path.join(self.values_dir, "strings.xml"), strings_content)
        print(f"Updated strings.xml with app title: {app_title}")

        # Generate manifest
        self.generate_manifest(activities_to_declare)

        # Generate layout
        self.generate_layout(main_activity_layout_name, ui_elements)

        # Generate main activity (if not generated by specific logic)
        if not os.path.exists(os.path.join(self.java_dir, f"{self.main_activity_name}.java")):
             self.generate_main_activity(main_activity_layout_name)


        # Build APK
        return self.build_apk()

def demo_arabic_generator():
    """Demonstrates the Arabic APK Generator."""
    print("\n--- Arabic APK Generator Module Demo ---")

    # Initialize the generator
    generator = ArabicAPKGenerator()

    # Example 1: Simple greeting app
    arabic_command_1 = "إنشاء تطبيق يعرض رسالة ترحيب بسيطة"
    apk_path_1 = generator.generate_apk_from_arabic(arabic_command_1)
    if apk_path_1:
        print(f"Generated APK for command 1: {apk_path_1}")
    else:
        print("APK generation failed for command 1.")

    # Example 2: Rectangle area calculator
    arabic_command_2 = "بناء تطبيق يحسب مساحة المستطيل من الطول والعرض المدخلين"
    apk_path_2 = generator.generate_apk_from_arabic(arabic_command_2)
    if apk_path_2:
        print(f"Generated APK for command 2: {apk_path_2}")
    else:
        print("APK generation failed for command 2.")

    # Example 3: Another rectangle area calc command variation
    arabic_command_3 = "تطبيقاً يحسب مساحة المستطيل"
    apk_path_3 = generator.generate_apk_from_arabic(arabic_command_3)
    if apk_path_3:
        print(f"Generated APK for command 3: {apk_path_3}")
    else:
        print("APK generation failed for command 3.")

    print("\n--- All Example Demos Finished ---")

    # Clean up the dummy project
    print("\n--- Cleaning up demo project ---")
    cleanup_directory(generator.project_root)

    print("\n--- Arabic APK Generator Module Demo Finished ---")

if __name__ == "__main__":
    demo_arabic_generator()