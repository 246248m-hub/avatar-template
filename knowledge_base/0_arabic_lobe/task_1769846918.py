import os
import json
import subprocess
import shutil
from typing import List, Dict, Any

class ArabicNLPProcessor:
    def __init__(self):
        # Placeholder for actual Arabic NLP libraries or models
        # In a real scenario, this would load models for tokenization,
        # morphological analysis, part-of-speech tagging, named entity recognition, etc.
        pass

    def preprocess_arabic_text(self, text: str) -> str:
        """
        Performs basic preprocessing for Arabic text.
        This could include normalization, removing diacritics, etc.
        """
        # Example: Simple normalization (replace common problematic characters)
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
        text = text.replace('ة', 'ه')
        text = ''.join(char for char in text if char.isprintable() or char in [' ', '\n'])
        return text

    def parse_arabic_intent(self, text: str) -> Dict[str, Any]:
        """
        Parses Arabic natural language text to extract intent and entities.
        This is a critical NLP function.
        """
        processed_text = self.preprocess_arabic_text(text)
        # In a real implementation, this would involve a sophisticated Arabic NLP pipeline.
        # For demonstration, we'll use a simplified rule-based approach or a mock.

        intent = "unknown"
        entities = {}

        if "إنشاء تطبيق" in processed_text or "صنع تطبيق" in processed_text:
            intent = "create_apk"
            # Extract app name, features, etc.
            if "تطبيق اسمه" in processed_text:
                try:
                    app_name_start = processed_text.index("تطبيق اسمه") + len("تطبيق اسمه")
                    app_name_end = processed_text.find("و", app_name_start) if "و" in processed_text[app_name_start:] else len(processed_text)
                    entities["app_name"] = processed_text[app_name_start:app_name_end].strip()
                except ValueError:
                    pass # App name not found in expected format

            if "له وظيفة" in processed_text:
                try:
                    feature_start = processed_text.index("له وظيفة") + len("له وظيفة")
                    feature_text = processed_text[feature_start:].strip()
                    # Simple feature extraction for demo
                    features = [f.strip() for f in feature_text.split("و") if f.strip()]
                    entities["features"] = features
                except ValueError:
                    pass # Features not found in expected format

        elif "تحديث التطبيق" in processed_text:
            intent = "update_apk"
            # Extract app name and update details
            if "التطبيق" in processed_text:
                try:
                    app_name_start = processed_text.index("التطبيق") + len("التطبيق")
                    app_name_end = processed_text.find("و", app_name_start) if "و" in processed_text[app_name_start:] else len(processed_text)
                    entities["app_name"] = processed_text[app_name_start:app_name_end].strip()
                except ValueError:
                    pass

        # Add more sophisticated parsing logic here, potentially using a NLU library
        # or a trained model for Arabic.

        return {"intent": intent, "entities": entities}

    def generate_arabic_response(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generates a natural language response in Arabic based on the analysis result.
        """
        intent = analysis_result.get("intent", "unknown")
        entities = analysis_result.get("entities", {})

        if intent == "create_apk":
            app_name = entities.get("app_name", "غير معروف")
            features = entities.get("features", [])
            if features:
                return f"سيتم إنشاء تطبيق باسم '{app_name}' مع الوظائف التالية: {', '.join(features)}. جاري العمل على ذلك."
            else:
                return f"سيتم إنشاء تطبيق باسم '{app_name}'. ما هي الوظائف التي ترغب في إضافتها؟"
        elif intent == "update_apk":
            app_name = entities.get("app_name", "غير معروف")
            return f"جارٍ تحديث التطبيق '{app_name}'. الرجاء توضيح التحديثات المطلوبة."
        elif intent == "unknown":
            return "لم أفهم طلبك. هل يمكنك إعادة صياغته باللغة العربية؟"
        else:
            return f"تم فهم الطلب بنية '{intent}' مع الكيانات: {entities}. جاري المعالجة."


class ArabicAPKGenerator:
    def __init__(self, nlp_processor: ArabicNLPProcessor, project_template_dir: str = "project_template"):
        self.nlp_processor = nlp_processor
        self.project_template_dir = project_template_dir
        self.temp_project_dir = None

    def _setup_project_environment(self, app_name: str, features: List[str] = None) -> str:
        """
        Sets up a temporary project directory based on a template.
        This would involve copying a base Android project and potentially
        modifying manifest files, strings, etc. based on app_name and features.
        """
        if not os.path.exists(self.project_template_dir):
            raise FileNotFoundError(f"Project template directory '{self.project_template_dir}' not found.")

        # Create a unique temporary directory for the project
        import uuid
        self.temp_project_dir = f"temp_apk_project_{app_name.replace(' ', '_')}_{uuid.uuid4().hex[:6]}"
        os.makedirs(self.temp_project_dir, exist_ok=True)

        # Copy the template to the temporary directory
        shutil.copytree(self.project_template_dir, self.temp_project_dir, dirs_exist_ok=True)

        # --- Placeholder for modifying project files ---
        # In a real scenario, you would:
        # 1. Modify AndroidManifest.xml (package name, app name resource)
        # 2. Modify res/values/strings.xml (app name, other strings)
        # 3. Potentially generate basic UI layouts (XML) based on 'features'
        # 4. Add necessary libraries or dependencies based on 'features'
        # For demonstration, we'll just return the path.
        print(f"Project environment set up at: {self.temp_project_dir}")
        return self.temp_project_dir

    def _generate_apk_code(self, project_dir: str, app_name: str, features: List[str] = None):
        """
        Generates or modifies Java/Kotlin code based on the extracted features.
        This is where Lobe 4 (Code Generation) would integrate heavily.
        """
        print(f"Generating code for app '{app_name}' with features: {features} in {project_dir}")
        # This is a placeholder for complex code generation logic.
        # It would involve parsing feature descriptions and generating
        # appropriate Java/Kotlin code, XML layouts, etc.

        # Example: Create a dummy main activity file if it doesn't exist
        main_activity_path = os.path.join(project_dir, "app", "src", "main", "java", "com", "example", "myapp", "MainActivity.java")
        os.makedirs(os.path.dirname(main_activity_path), exist_ok=True)

        if not os.path.exists(main_activity_path):
            with open(main_activity_path, "w", encoding="utf-8") as f:
                f.write("""
package com.example.myapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView textView = findViewById(R.id.textView);
        textView.setText("مرحباً بك في تطبيق """ + app_name + """!");
    }
}
""")
                print(f"Created dummy MainActivity.java")

        # Example: Create a dummy layout file if it doesn't exist
        layout_dir = os.path.join(project_dir, "app", "src", "main", "res", "layout")
        os.makedirs(layout_dir, exist_ok=True)
        activity_main_layout_path = os.path.join(layout_dir, "activity_main.xml")

        if not os.path.exists(activity_main_layout_path):
            with open(activity_main_layout_path, "w", encoding="utf-8") as f:
                f.write("""
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Loading..."
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
""")
                print(f"Created dummy activity_main.xml")


        # Add logic here to parse 'features' and generate corresponding Java/Kotlin code snippets
        # and update layout XML files. This would be a significant part of Lobe 4's role.

    def _build_apk(self, project_dir: str, app_name: str) -> str:
        """
        Compiles the Android project into an APK.
        This function would interface with Lobe 8 (APK Compiler).
        Assumes Gradle is set up in the project template.
        """
        print(f"Attempting to build APK for '{app_name}' from {project_dir}...")

        # Check if Gradle wrapper exists
        gradle_wrapper_path = os.path.join(project_dir, "gradlew")
        if not os.path.exists(gradle_wrapper_path):
            raise FileNotFoundError(f"Gradle wrapper (gradlew) not found in project directory: {project_dir}. "
                                    "Ensure your project template includes it.")

        # Construct the Gradle command
        # 'assembleDebug' builds a debug APK. 'assembleRelease' would build a release APK.
        gradle_command = [gradle_wrapper_path, "assembleDebug"]

        try:
            # Execute the Gradle command
            # We capture stdout and stderr to help with debugging build issues
            result = subprocess.run(gradle_command, cwd=project_dir, capture_output=True, text=True, check=True, encoding='utf-8')
            print("Gradle build output (stdout):\n", result.stdout)
            print("Gradle build output (stderr):\n", result.stderr)
            print("APK build completed successfully.")

            # Find the generated APK file
            # The path to the APK depends on the Gradle structure.
            # For a typical Android project, it's in app/build/outputs/apk/debug/
            apk_path_pattern = os.path.join(project_dir, "app", "build", "outputs", "apk", "debug", f"app-debug.apk")
            # In some setups, it might be named after the app if build.gradle configured it.
            # For simplicity, we assume the default 'app-debug.apk'.
            generated_apk_path = None
            for root, _, files in os.walk(os.path.join(project_dir, "app", "build", "outputs", "apk", "debug")):
                for file in files:
                    if file.endswith(".apk"):
                        generated_apk_path = os.path.join(root, file)
                        break
                if generated_apk_path:
                    break

            if not generated_apk_path:
                raise FileNotFoundError("Could not find the generated APK file after build.")

            return generated_apk_path

        except subprocess.CalledProcessError as e:
            print(f"Error during APK build: {e}")
            print("Gradle build error output (stdout):\n", e.stdout)
            print("Gradle build error output (stderr):\n", e.stderr)
            raise RuntimeError(f"APK build failed: {e.stderr}") from e
        except FileNotFoundError as e:
            print(f"Build environment error: {e}")
            raise RuntimeError(f"Build environment error: {e}") from e

    def cleanup_project_environment(self):
        """
        Removes the temporary project directory after APK generation.
        """
        if self.temp_project_dir and os.path.exists(self.temp_project_dir):
            try:
                shutil.rmtree(self.temp_project_dir)
                print(f"Temporary project directory '{self.temp_project_dir}' removed.")
                self.temp_project_dir = None
            except OSError as e:
                print(f"Error removing directory {self.temp_project_dir}: {e}")

    def generate_apk_from_arabic(self, arabic_prompt: str) -> str:
        """
        The main function to process an Arabic prompt and generate an APK.
        """
        print(f"\n--- Processing Arabic prompt: '{arabic_prompt}' ---")

        # 1. Parse Arabic NLP (Lobe 0)
        print("Step 1: Parsing Arabic NLP...")
        nlp_result = self.nlp_processor.parse_arabic_intent(arabic_prompt)
        print(f"NLP Analysis Result: {nlp_result}")

        intent = nlp_result.get("intent")
        entities = nlp_result.get("entities", {})

        if intent != "create_apk":
            response = self.nlp_processor.generate_arabic_response(nlp_result)
            print(f"Response: {response}")
            return f"Unsupported intent '{intent}'. Please request to create an APK."

        app_name = entities.get("app_name", "MyNewApp")
        features = entities.get("features", [])

        # Ensure app_name is safe for file system operations
        safe_app_name = "".join(c for c in app_name if c.isalnum() or c in (' ', '_')).rstrip()
        if not safe_app_name:
            safe_app_name = "DefaultApp"

        output_apk_path = None
        try:
            # 2. Setup Project Environment (Lobe 8 integration point)
            print("Step 2: Setting up project environment...")
            project_dir = self._setup_project_environment(safe_app_name, features)

            # 3. Generate Code (Lobe 4 integration point)
            print("Step 3: Generating code based on features...")
            self._generate_apk_code(project_dir, safe_app_name, features)

            # 4. Compile APK (Lobe 8 integration point)
            print("Step 4: Compiling APK...")
            output_apk_path = self._build_apk(project_dir, safe_app_name)
            print(f"Successfully generated APK: {output_apk_path}")

            # 5. Generate Confirmation Response (Lobe 0 integration point)
            confirmation_message = self.nlp_processor.generate_arabic_response({
                "intent": "create_apk",
                "entities": {"app_name": app_name, "features": features}
            })
            print(f"Confirmation: {confirmation_message}")

            return output_apk_path

        except FileNotFoundError as e:
            print(f"Error: {e}")
            return f"خطأ في إعداد بيئة المشروع: {e}"
        except RuntimeError as e:
            print(f"Error: {e}")
            return f"فشل بناء التطبيق: {e}"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return f"حدث خطأ غير متوقع: {e}"
        finally:
            # 6. Cleanup
            print("Step 5: Cleaning up project environment...")
            self.cleanup_project_environment()
            print("--- APK Generation Flow Finished ---")

if __name__ == '__main__':
    # --- Setup ---
    # Ensure a 'project_template' directory exists with a basic Android project structure.
    # For a real test, this would need a valid Android project.
    # For demonstration, we'll create a dummy structure if it doesn't exist.
    TEMPLATE_DIR = "project_template"
    if not os.path.exists(TEMPLATE_DIR):
        print(f"Creating dummy project template directory: {TEMPLATE_DIR}")
        os.makedirs(os.path.join(TEMPLATE_DIR, "app", "src", "main", "java", "com", "example", "myapp"), exist_ok=True)
        os.makedirs(os.path.join(TEMPLATE_DIR, "app", "src", "main", "res", "layout"), exist_ok=True)
        # Create dummy build.gradle files to satisfy potential checks
        with open(os.path.join(TEMPLATE_DIR, "build.gradle"), "w") as f:
            f.write("buildscript {}")
        with open(os.path.join(TEMPLATE_DIR, "app", "build.gradle"), "w") as f:
            f.write("plugins {\n    id 'com.android.application'\n}\nandroid {}")
        # Create a dummy gradlew and gradlew.bat for compatibility
        with open(os.path.join(TEMPLATE_DIR, "gradlew"), "w") as f:
            f.write("#!/bin/bash\necho 'Dummy gradlew'")
        with open(os.path.join(TEMPLATE_DIR, "gradlew.bat"), "w") as f:
            f.write("@echo off\necho Dummy gradlew.bat")

    print("\n--- Initializing Unified Mind Modules for Arabic APK Generation ---")
    arabic_nlp = ArabicNLPProcessor()
    apk_generator = ArabicAPKGenerator(nlp_processor=arabic_nlp, project_template_dir=TEMPLATE_DIR)
    print("--- Modules Initialized ---")

    # --- Test Cases ---
    test_prompts_arabic = [
        "أريد إنشاء تطبيق اسمه مكتشف الصور وله وظيفة عرض الصور من المعرض",
        "صمم لي تطبيق اسمه مدقق النصوص مع وظيفة التدقيق الإملائي",
        "قم بإنشاء تطبيق بسيط اسمه الآلة الحاسبة",
        "تحديث التطبيق الحاسبة", # This should trigger an unsupported intent for now
        "لا أريد إنشاء تطبيق" # This should trigger an unsupported intent
    ]

    generated_apk_paths = {}

    for i, prompt in enumerate(test_prompts_arabic):
        print(f"\n--- Test Case {i+1} ---")
        generated_path = apk_generator.generate_apk_from_arabic(prompt)
        generated_apk_paths[prompt] = generated_path
        print(f"Result for prompt '{prompt}': {generated_path}")
        print("--------------------")

    print("\n--- Unified Mind Arabic APK Generation Demo Finished ---")
    print("Generated APK paths:")
    for prompt, path in generated_apk_paths.items():
        print(f"- '{prompt}': {path}")

    # --- Final Cleanup ---
    print("\n--- Performing Unified Mind Cleanup ---")
    # In a real unified mind, this would involve more global cleanup.
    # For this module, the cleanup is primarily handled within the generator's finally block.
    # If there were any global resources managed here, they'd be released.
    print("--- Unified Mind Cleanup Complete ---")