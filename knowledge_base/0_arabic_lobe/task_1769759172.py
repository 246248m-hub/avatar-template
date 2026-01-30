import os
import re
import shutil

# Define a simple APK structure
APK_STRUCTURE = {
    "AndroidManifest.xml": {
        "template": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
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
    },
    "res/values/strings.xml": {
        "template": """<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""
    },
    "src/main/java/{package_path}/MainActivity.java": {
        "template": """package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }}
}}
"""
    },
    "src/main/res/layout/activity_main.xml": {
        "template": """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
    }
}

class ArabicAPKGenerator:
    def __init__(self, output_dir="generated_apk_project"):
        self.output_dir = output_dir
        self.package_name = "com.example.arabic_app"  # Default package name
        self.app_name = "ArabicApp"  # Default app name

    def set_package_name(self, package_name):
        self.package_name = package_name

    def set_app_name(self, app_name):
        self.app_name = app_name

    def _create_directory_structure(self):
        os.makedirs(os.path.join(self.output_dir, "res", "values"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "src", "main", "java", *self.package_name.split('.')), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "src", "main", "res", "layout"), exist_ok=True)

    def _generate_file_content(self, file_path, template_key):
        template = APK_STRUCTURE[template_key]["template"]
        package_path = ".".join(self.package_name.split('.'))
        if template_key == "src/main/java/{package_path}/MainActivity.java":
            java_package_path = os.path.join(*self.package_name.split('.'))
            return template.format(package_name=self.package_name, package_path=java_package_path)
        elif template_key == "res/values/strings.xml":
            return template.format(app_name=self.app_name)
        else:
            return template.format(package_name=self.package_name, app_name=self.app_name)

    def generate_apk_structure(self, arabic_nlp_description):
        """
        Generates a basic Android APK project structure from an Arabic NLP description.
        This is a simplified representation and would require a full NLP parser
        to extract meaningful information like app name, package name, etc.
        """
        print(f"--- Generating APK structure for: {arabic_nlp_description} ---")

        # Basic extraction of app name and package name from Arabic NLP description
        # This is a placeholder for a sophisticated Arabic NLP parser.
        # In a real scenario, this would involve understanding grammar, intent, and entities.

        # Example: If description contains "اسم التطبيق هو [اسم]" or "حزمة التطبيق هي [حزمة]"
        app_name_match = re.search(r"اسم التطبيق هو ([\w\s]+)", arabic_nlp_description)
        if app_name_match:
            self.set_app_name(app_name_match.group(1).strip())

        package_name_match = re.search(r"حزمة التطبيق هي ([\w\.]+)", arabic_nlp_description)
        if package_name_match:
            self.set_package_name(package_name_match.group(1).strip())
        else:
            # Fallback to default if not found, or attempt more complex parsing
            print(f"Warning: Could not extract package name from description. Using default: {self.package_name}")
            print(f"Warning: Could not extract app name from description. Using default: {self.app_name}")


        self._create_directory_structure()

        for file_path_template, content_info in APK_STRUCTURE.items():
            # Determine the actual file path based on the template
            if "{package_path}" in file_path_template:
                java_package_path = os.path.join(*self.package_name.split('.'))
                actual_file_path = file_path_template.format(package_path=java_package_path)
            else:
                actual_file_path = file_path_template

            full_output_path = os.path.join(self.output_dir, actual_file_path)
            file_content = self._generate_file_content(actual_file_path, file_path_template)

            with open(full_output_path, "w", encoding="utf-8") as f:
                f.write(file_content)
            print(f"Created: {full_output_path}")

        print(f"--- APK structure generated in: {self.output_dir} ---")
        return self.output_dir

    def cleanup_project(self):
        """Removes the generated project directory."""
        if os.path.exists(self.output_dir):
            print(f"\n--- Cleaning up generated project directory: {self.output_dir} ---")
            shutil.rmtree(self.output_dir)
            print("--- Cleanup complete ---")


if __name__ == '__main__':
    # Example Usage:
    generator = ArabicAPKGenerator()

    # Example Arabic NLP descriptions
    arabic_description_1 = "أنشئ تطبيق أندرويد باسم 'تطبيقي الأول' وحزمة التطبيق هي 'com.mycompany.firstapp'"
    arabic_description_2 = "أريد بناء مشروع APK جديد. اسم التطبيق هو 'تطبيق الترجمة' وحزمة التطبيق هي 'com.translate.arabic'"
    arabic_description_3 = "إنشاء مشروع بسيط اسمه 'HelloArabic' بحزمة 'com.hello.arabic'"


    print("\n--- Demo 1: Generating APK structure ---")
    try:
        project_path_1 = generator.generate_apk_structure(arabic_description_1)
        print(f"Project generated at: {project_path_1}")
    except Exception as e:
        print(f"Demo 1 failed: {e}")
    finally:
        generator.cleanup_project()


    print("\n--- Demo 2: Generating APK structure with different details ---")
    try:
        project_path_2 = generator.generate_apk_structure(arabic_description_2)
        print(f"Project generated at: {project_path_2}")
    except Exception as e:
        print(f"Demo 2 failed: {e}")
    finally:
        generator.cleanup_project()


    print("\n--- Demo 3: Generating APK structure with implicit package name extraction ---")
    try:
        project_path_3 = generator.generate_apk_structure(arabic_description_3)
        print(f"Project generated at: {project_path_3}")
    except Exception as e:
        print(f"Demo 3 failed: {e}")
    finally:
        generator.cleanup_project()

    print("\n--- ArabicAPKGenerator Module Demo Finished ---")