import os
import shutil
from pathlib import Path

# Assume these are defined in other lobes or globally
KNOWLEDGE_BASE_DIR = "./knowledge_base"
GENERATED_CODE_DIR = "./generated_code"
ANDROID_PROJECT_TEMPLATES = "./android_templates"

class ArabicNLPProcessor:
    """
    A class to handle Arabic Natural Language Processing tasks,
    specifically focusing on parsing and generating text related to
    Android project structures and APK compilation.
    """
    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = Path(knowledge_base_path)
        os.makedirs(self.knowledge_base_path, exist_ok=True)
        self.current_prompt = ""
        self.processed_data = {}

    def load_knowledge(self, file_name: str) -> str:
        """Loads text content from a file in the knowledge base."""
        file_path = self.knowledge_base_path / file_name
        if not file_path.exists():
            raise FileNotFoundError(f"Knowledge file not found: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def parse_arabic_prompt(self, prompt_text: str) -> dict:
        """
        Parses Arabic natural language prompts related to Android project
        structure and APK compilation. This is a placeholder for more
        sophisticated NLP parsing.
        """
        self.current_prompt = prompt_text
        # In a real scenario, this would involve tokenization,
        # part-of-speech tagging, named entity recognition,
        # and intent classification specific to Android development
        # in Arabic.
        parsed_info = {
            "intent": "unknown",
            "components": [],
            "project_name": "my_app",
            "package_name": "com.example.myapp",
            "activity_names": [],
            "layout_names": [],
            "dependencies": []
        }

        # Simple keyword-based parsing for demonstration
        if "إنشاء مشروع أندرويد" in prompt_text or "create android project" in prompt_text:
            parsed_info["intent"] = "create_project"
            if "اسم المشروع" in prompt_text:
                parts = prompt_text.split("اسم المشروع")
                if len(parts) > 1:
                    parsed_info["project_name"] = parts[1].strip().split(" ")[0]
            if "اسم الحزمة" in prompt_text:
                parts = prompt_text.split("اسم الحزمة")
                if len(parts) > 1:
                    parsed_info["package_name"] = parts[1].strip().split(" ")[0]
            if "أنشطة" in prompt_text:
                parts = prompt_text.split("أنشطة")
                if len(parts) > 1:
                    activities_str = parts[1].split(" ")[0]
                    parsed_info["activity_names"] = [a.strip() for a in activities_str.split(',') if a.strip()]

        elif "تجميع APK" in prompt_text or "compile APK" in prompt_text:
            parsed_info["intent"] = "compile_apk"
            if "ملف المشروع" in prompt_text:
                parts = prompt_text.split("ملف المشروع")
                if len(parts) > 1:
                    parsed_info["project_path"] = parts[1].strip().split(" ")[0]

        self.processed_data[prompt_text] = parsed_info
        return parsed_info

    def generate_arabic_text(self, parsed_data: dict) -> str:
        """
        Generates Arabic natural language text based on parsed data,
        such as confirmations of actions or descriptions of generated code.
        This is a placeholder for more sophisticated NLG.
        """
        intent = parsed_data.get("intent", "unknown")
        project_name = parsed_data.get("project_name", "المشروع")
        package_name = parsed_data.get("package_name", "com.example.app")
        activity_names = parsed_data.get("activity_names", [])

        if intent == "create_project":
            response = f"تم إنشاء مشروع أندرويد جديد باسم '{project_name}' وحزمة '{package_name}'."
            if activity_names:
                response += f" تم تحديد الأنشطة التالية: {', '.join(activity_names)}."
            return response
        elif intent == "compile_apk":
            project_path = parsed_data.get("project_path", "المسار المحدد")
            return f"تم بدء عملية تجميع APK للمشروع الموجود في المسار: '{project_path}'. سيتم إعلامك عند الانتهاء."
        else:
            return "تم فهم طلبك. جاري المعالجة."

    def process_and_generate(self, prompt_text: str) -> tuple[dict, str]:
        """
        Orchestrates parsing and generation for a given Arabic prompt.
        Returns the parsed data and the generated Arabic text.
        """
        parsed_info = self.parse_arabic_prompt(prompt_text)
        generated_text = self.generate_arabic_text(parsed_info)
        return parsed_info, generated_text

class APKStructureBuilder:
    """
    Builds the basic Android project structure based on parsed requirements.
    This module focuses on creating directories and essential files.
    """
    def __init__(self, template_dir: str, output_dir: str):
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.template_dir, exist_ok=True) # Ensure template dir exists

    def _create_android_directory_structure(self, project_path: Path, package_name: str, activity_names: list):
        """Creates the standard Android project directory hierarchy."""
        # Basic structure
        (project_path / "app" / "src" / "main" / "java" / package_name.replace('.', '/')).mkdir(parents=True, exist_ok=True)
        (project_path / "app" / "src" / "main" / "res" / "layout").mkdir(parents=True, exist_ok=True)
        (project_path / "app" / "src" / "main" / "res" / "drawable").mkdir(parents=True, exist_ok=True)
        (project_path / "app" / "src" / "main" / "res" / "mipmap").mkdir(parents=True, exist_ok=True)
        (project_path / "app" / "src" / "main" / "res" / "values").mkdir(parents=True, exist_ok=True)

        # Create MainActivity or default if none specified
        main_activity_java_path = project_path / "app" / "src" / "main" / "java" / package_name.replace('.', '/') / "MainActivity.java"
        if "MainActivity" not in activity_names and not activity_names:
            with open(main_activity_java_path, "w", encoding="utf-8") as f:
                f.write(f"""package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }}
}}
""")
        # Create layout for MainActivity
        main_layout_xml_path = project_path / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml"
        if not main_layout_xml_path.exists():
            with open(main_layout_xml_path, "w", encoding="utf-8") as f:
                f.write(f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{package_name.split('.')[-1]}.MainActivity">

    <!-- Your layout content here -->

</androidx.constraintlayout.widget.ConstraintLayout>
""")

        # Create specified activities and layouts
        for activity_name in activity_names:
            activity_java_path = project_path / "app" / "src" / "main" / "java" / package_name.replace('.', '/') / f"{activity_name}.java"
            layout_xml_path = project_path / "app" / "src" / "main" / "res" / "layout" / f"activity_{activity_name.lower()}.xml"

            if not activity_java_path.exists():
                with open(activity_java_path, "w", encoding="utf-8") as f:
                    f.write(f"""package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class {activity_name} extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{f"activity_{activity_name.lower()}"});
    }}
}}
""")
            if not layout_xml_path.exists():
                with open(layout_xml_path, "w", encoding="utf-8") as f:
                    f.write(f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{package_name.split('.')[-1]}.{activity_name}">

    <!-- Layout for {activity_name} -->

</androidx.constraintlayout.widget.ConstraintLayout>
""")

        # Create strings.xml
        strings_xml_path = project_path / "app" / "src" / "main" / "res" / "values" / "strings.xml"
        if not strings_xml_path.exists():
            with open(strings_xml_path, "w", encoding="utf-8") as f:
                f.write(f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{project_path.name}</string>
</resources>
""")

        # Create AndroidManifest.xml
        manifest_xml_path = project_path / "app" / "src" / "main" / "AndroidManifest.xml"
        if not manifest_xml_path.exists():
            manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{project_path.name}">

        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
"""
            for activity_name in activity_names:
                manifest_content += f"""
        <activity android:name=".{activity_name}" />
"""
            manifest_content += """
    </application>

</manifest>
"""
            with open(manifest_xml_path, "w", encoding="utf-8") as f:
                f.write(manifest_content)

        # Create build.gradle (app level) - basic structure
        build_gradle_app_path = project_path / "app" / "build.gradle"
        if not build_gradle_app_path.exists():
            with open(build_gradle_app_path, "w", encoding="utf-8") as f:
                f.write(f"""plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android' // Assuming Kotlin might be used later
}}

android {{
    namespace '{package_name}'
    compileSdk 33 // Example SDK version

    defaultConfig {{
        applicationId "{package_name}"
        minSdk 21 // Example min SDK version
        targetSdk 33
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }}

    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }}
    }}
    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }}
    // For Kotlin
    // kotlinOptions {{
    //     jvmTarget = '1.8'
    // }}
}}

dependencies {{
    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
""")

        # Create build.gradle (project level) - basic structure
        build_gradle_project_path = project_path / "build.gradle"
        if not build_gradle_project_path.exists():
            with open(build_gradle_project_path, "w", encoding="utf-8") as f:
                f.write(f"""// Top-level build file where you can add configuration options common to all sub-projects/modules.
buildscript {{
    repositories {{
        google()
        mavenCentral()
    }}
    dependencies {{
        classpath "com.android.tools.build:gradle:7.4.2" // Example Gradle plugin version
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:1.8.0" // Example Kotlin plugin version
    }}
}}

allprojects {{
    repositories {{
        google()
        mavenCentral()
    }}
}}

task clean(type: Delete) {{
    delete rootProject.buildDir
}}
""")

    def build_project_structure(self, project_name: str, package_name: str, activity_names: list) -> Path:
        """
        Generates the directory structure and essential files for an Android project.
        """
        generated_project_path = self.output_dir / project_name
        if generated_project_path.exists():
            print(f"Project directory '{generated_project_path}' already exists. Skipping creation.")
            return generated_project_path

        print(f"Creating Android project structure for '{project_name}' at '{generated_project_path}'...")
        generated_project_path.mkdir(parents=True, exist_ok=True)

        # Copying basic template files if they exist in the template directory
        # For now, we'll generate them directly. In a real scenario, these would be
        # more sophisticated templates.
        self._create_android_directory_structure(generated_project_path, package_name, activity_names)

        return generated_project_path

# --- Demonstration / Integration ---

def demo_apk_structure_builder():
    """
    Demonstrates the functionality of the ArabicNLPProcessor and APKStructureBuilder.
    """
    print("\n--- Arabic NLP and APK Structure Builder Module Demonstration ---")

    # Initialize NLP processor
    arabic_nlp = ArabicNLPProcessor(knowledge_base_path=KNOWLEDGE_BASE_DIR)

    # Initialize APK structure builder
    apk_builder = APKStructureBuilder(
        template_dir=ANDROID_PROJECT_TEMPLATES,
        output_dir=GENERATED_CODE_DIR
    )

    # --- Scenario 1: Create a simple project ---
    prompt_1 = "أريد إنشاء مشروع أندرويد جديد باسم 'MyFirstApp' واسم الحزمة 'com.example.myfirstapp'"
    print(f"\nProcessing prompt: '{prompt_1}'")
    parsed_data_1, generated_text_1 = arabic_nlp.process_and_generate(prompt_1)
    print(f"NLP Output: {generated_text_1}")
    print(f"Parsed Data: {parsed_data_1}")

    project_path_1 = apk_builder.build_project_structure(
        project_name=parsed_data_1["project_name"],
        package_name=parsed_data_1["package_name"],
        activity_names=[]
    )
    print(f"Successfully prepared Android project structure. Project path: {project_path_1}")

    # --- Scenario 2: Create a project with activities ---
    prompt_2 = "قم بإنشاء مشروع أندرويد جديد باسم 'MultiActivityApp' واسم الحزمة 'com.example.multiapp' مع أنشطة 'SecondActivity', 'ThirdActivity'"
    print(f"\nProcessing prompt: '{prompt_2}'")
    parsed_data_2, generated_text_2 = arabic_nlp.process_and_generate(prompt_2)
    print(f"NLP Output: {generated_text_2}")
    print(f"Parsed Data: {parsed_data_2}")

    project_path_2 = apk_builder.build_project_structure(
        project_name=parsed_data_2["project_name"],
        package_name=parsed_data_2["package_name"],
        activity_names=parsed_data_2["activity_names"]
    )
    print(f"Successfully prepared Android project structure. Project path: {project_path_2}")

    # --- Scenario 3: Prompt to compile APK (simulated by NLP) ---
    prompt_3 = "ابدأ في تجميع APK للمشروع الموجود في المسار: './generated_code/MyFirstApp'"
    print(f"\nProcessing prompt: '{prompt_3}'")
    parsed_data_3, generated_text_3 = arabic_nlp.process_and_generate(prompt_3)
    print(f"NLP Output: {generated_text_3}")
    print(f"Parsed Data: {parsed_data_3}")

    print("\n--- Arabic NLP and APK Structure Builder Module Demo Finished ---")

    # Clean up generated directories for demonstration
    print("\n--- Cleaning up generated directories ---")
    if os.path.exists(GENERATED_CODE_DIR):
        shutil.rmtree(GENERATED_CODE_DIR)
        print(f"Removed directory: {GENERATED_CODE_DIR}")
    if os.path.exists(KNOWLEDGE_BASE_DIR):
        # You might want to keep knowledge base or clean it selectively
        pass
    if os.path.exists(ANDROID_PROJECT_TEMPLATES):
        # You might want to keep templates or clean them selectively
        pass

if __name__ == "__main__":
    # Create dummy directories for demonstration if they don't exist
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    os.makedirs(GENERATED_CODE_DIR, exist_ok=True)
    os.makedirs(ANDROID_PROJECT_TEMPLATES, exist_ok=True)

    demo_apk_structure_builder()

    print("\n--- Initiating next step: Lobe 4_code_generation_lobe ---")