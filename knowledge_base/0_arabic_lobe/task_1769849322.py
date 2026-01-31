import os
import subprocess
import shutil
import re

# Assuming a structure where NLP logic resides in arabic_lobe and code generation in code_generation_lobe
# This module will orchestrate the process of translating Arabic NLP to code and then to an APK structure.

class ArabicToApkGenerator:
    def __init__(self, arabic_lobe_instance, code_generation_lobe_instance, apk_compiler_lobe_instance):
        self.arabic_lobe = arabic_lobe_instance
        self.code_generation_lobe = code_generation_lobe_instance
        self.apk_compiler_lobe = apk_compiler_lobe_instance
        self.project_dir_base = "generated_projects"
        self.apk_output_base = "generated_apks"

    def _create_project_directory(self, project_name):
        """Creates a unique directory for the Android project."""
        project_path = os.path.join(self.project_dir_base, project_name.replace(" ", "_").lower())
        os.makedirs(project_path, exist_ok=True)
        return project_path

    def _clean_up_project_directory(self, project_path):
        """Removes the project directory if it exists."""
        if os.path.exists(project_path):
            try:
                shutil.rmtree(project_path)
                print(f"Cleaned up project directory: {project_path}")
            except OSError as e:
                print(f"Error cleaning up project directory {project_path}: {e}")

    def _clean_up_apk_directory(self, apk_path):
        """Removes the APK and its associated build artifacts if they exist."""
        if os.path.exists(apk_path):
            try:
                os.remove(apk_path)
                print(f"Removed APK file: {apk_path}")
                # Optionally, remove the build directory as well
                build_dir = os.path.dirname(apk_path)
                if os.path.exists(build_dir):
                    shutil.rmtree(build_dir)
                    print(f"Cleaned up build directory: {build_dir}")
            except OSError as e:
                print(f"Error cleaning up APK file {apk_path}: {e}")

    def generate_apk_from_arabic(self, arabic_prompt, app_name="MyArabicApp"):
        """
        Orchestrates the process of generating an APK from an Arabic natural language prompt.

        Args:
            arabic_prompt (str): The natural language description of the desired Android application in Arabic.
            app_name (str): The desired name for the Android application.

        Returns:
            str: The path to the generated APK file, or None if generation failed.
        """
        print(f"\n--- Starting APK Generation for prompt: '{arabic_prompt}' ---")

        # Step 1: Process Arabic prompt using Arabic Lobe
        print("Step 1: Processing Arabic prompt...")
        nlp_output = self.arabic_lobe.parse_arabic_text(arabic_prompt)
        if not nlp_output:
            print("Error: Failed to parse Arabic prompt.")
            return None
        print("Arabic prompt parsed successfully.")

        # Step 2: Generate code from NLP output using Code Generation Lobe
        print("\nStep 2: Generating code from NLP output...")
        project_name = f"{app_name}_{os.urandom(4).hex()}" # Unique project name
        project_path = self._create_project_directory(project_name)
        generated_code_info = self.code_generation_lobe.generate_android_code(nlp_output, project_path)

        if not generated_code_info:
            print("Error: Failed to generate Android code.")
            self._clean_up_project_directory(project_path)
            return None
        print(f"Android code generated successfully in: {project_path}")
        # generated_code_info could be a dictionary containing paths to generated files like MainActivity.java, AndroidManifest.xml etc.

        # Step 3: Compile the generated code into an APK using APK Compiler Lobe
        print("\nStep 3: Compiling code into an APK...")
        apk_output_dir = os.path.join(self.apk_output_base, project_name)
        os.makedirs(apk_output_dir, exist_ok=True)
        output_apk_path = os.path.join(apk_output_dir, f"{app_name}.apk")

        # Ensure necessary build tools and SDK paths are configured within apk_compiler_lobe
        # For demonstration, assuming apk_compiler_lobe has a build_apk method
        apk_generated = self.apk_compiler_lobe.build_apk(project_path, output_apk_path)

        if not apk_generated:
            print("Error: Failed to compile APK.")
            self._clean_up_project_directory(project_path)
            self._clean_up_apk_directory(output_apk_path)
            return None
        print(f"APK generated successfully at: {output_apk_path}")

        # Clean up intermediate project files after successful APK generation
        print("\n--- Cleaning up intermediate project files ---")
        self._clean_up_project_directory(project_path)

        return output_apk_path

# --- Mock Lobe Instances for Demonstration ---
# In a real scenario, these would be actual instances of your Lobe classes.

class MockArabicLobe:
    def parse_arabic_text(self, text):
        print(f"MockArabicLobe: Parsing '{text}'")
        # Simulate parsing Arabic text into a structured format
        # For example, returning a dictionary describing UI elements and logic
        if "زر" in text and "نص" in text:
            return {
                "ui_elements": [
                    {"type": "Button", "text": "اضغط هنا", "action": "showMessage"},
                    {"type": "TextView", "text": "مرحبا بالعالم"}
                ],
                "logic": {
                    "showMessage": "print('Button pressed!')"
                }
            }
        elif "صورة" in text:
            return {
                "ui_elements": [
                    {"type": "ImageView", "source": "sample_image.png"}
                ]
            }
        return None

class MockCodeGenerationLobe:
    def generate_android_code(self, nlp_output, project_path):
        print(f"MockCodeGenerationLobe: Generating code in {project_path} from NLP output.")
        # Simulate creating basic Android project files (e.g., Java, XML)
        os.makedirs(os.path.join(project_path, "app", "src", "main", "java", "com", "example", "myarabicapp"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "app", "src", "main", "res", "layout"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "app", "src", "main", "res", "drawable"), exist_ok=True) # For images

        # Create a dummy AndroidManifest.xml
        manifest_content = """
        <manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.myarabicapp">
            <application android:allowBackup="true" android:icon="@mipmap/ic_launcher" android:label="@string/app_name" android:roundIcon="@mipmap/ic_launcher_round" android:supportsRtl="true" android:theme="@style/AppTheme">
                <activity android:name=".MainActivity">
                    <intent-filter>
                        <action android:name="android.intent.action.MAIN"/>
                        <category android:name="android.intent.category.LAUNCHER"/>
                    </intent-filter>
                </activity>
            </application>
        </manifest>
        """
        with open(os.path.join(project_path, "app", "src", "main", "AndroidManifest.xml"), "w", encoding="utf-8") as f:
            f.write(manifest_content)

        # Create a dummy strings.xml
        strings_content = """
        <resources>
            <string name="app_name">MyArabicApp</string>
        </resources>
        """
        with open(os.path.join(project_path, "app", "src", "main", "res", "values", "strings.xml"), "w", encoding="utf-8") as f:
            f.write(strings_content)

        # Create a dummy MainActivity.java
        main_activity_content = """
        package com.example.myarabicapp;

        import androidx.appcompat.app.AppCompatActivity;
        import android.os.Bundle;
        import android.widget.TextView;
        import android.widget.Button;
        import android.widget.Toast;
        import android.widget.ImageView;
        import android.graphics.drawable.Drawable;

        public class MainActivity extends AppCompatActivity {

            @Override
            protected void onCreate(Bundle savedInstanceState) {
                super.onCreate(savedInstanceState);
                setContentView(R.layout.activity_main);

        """
        if "ui_elements" in nlp_output:
            layout_elements = []
            for element in nlp_output["ui_elements"]:
                if element["type"] == "Button":
                    button_id = f"button_{element['text'].replace(' ', '_').lower()}"
                    layout_elements.append(f'        Button {button_id} = findViewById(R.id.{button_id});\n')
                    if "action" in element:
                        # Simulate handling actions
                        if element["action"] == "showMessage":
                            main_activity_content += f'        {button_id}.setOnClickListener(v -> {{ Toast.makeText(this, "تم الضغط على الزر!", Toast.LENGTH_SHORT).show(); }});\n'
                        else:
                             main_activity_content += f'        {button_id}.setOnClickListener(v -> {{ /* TODO: Implement action: {element["action"]} */ }});\n'
                elif element["type"] == "TextView":
                    tv_id = f"textView_{element['text'][:10].replace(' ', '_').lower()}" # Shorten ID for simplicity
                    layout_elements.append(f'        TextView {tv_id} = findViewById(R.id.{tv_id});\n')
                    main_activity_content += f'        {tv_id}.setText("{element["text"]}");\n'
                elif element["type"] == "ImageView":
                    img_id = f"imageView_{os.urandom(4).hex()}"
                    layout_elements.append(f'        ImageView {img_id} = findViewById(R.id.{img_id});\n')
                    if "source" in element and element["source"]:
                        # Simulate setting image source, assuming it's in drawables
                        image_name = os.path.splitext(element["source"])[0]
                        main_activity_content += f'        try {{ Drawable d = getResources().getDrawable(R.drawable.{image_name}); {img_id}.setImageDrawable(d); }} catch (Exception e) {{ e.printStackTrace(); }}\n'


            if layout_elements:
                main_activity_content += "".join(layout_elements)

        main_activity_content += """
            }
        }
        """
        with open(os.path.join(project_path, "app", "src", "main", "java", "com", "example", "myarabicapp", "MainActivity.java"), "w", encoding="utf-8") as f:
            f.write(main_activity_content)

        # Create a dummy activity_main.xml
        layout_content = """
        <?xml version="1.0" encoding="utf-8"?>
        <androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
            xmlns:app="http://schemas.android.com/apk/res-auto"
            xmlns:tools="http://schemas.android.com/tools"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            tools:context=".MainActivity">
        """
        if "ui_elements" in nlp_output:
            top_margin = 16
            for i, element in enumerate(nlp_output["ui_elements"]):
                element_type = element["type"]
                element_text = element.get("text", "Element")
                element_id_base = element_text.replace(' ', '_').lower()
                element_id = f"{element_type.lower()}_{element_id_base[:10]}" if element_type in ["Button", "TextView"] else f"imageView_{os.urandom(4).hex()}" # Unique ID

                if element_type == "Button":
                    layout_content += f"""
            <Button
                android:id="@+id/{element_id}"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="{element_text}"
                app:layout_constraintTop_toTopOf="parent"
                app:layout_constraintStart_toStartOf="parent"
                app:layout_constraintEnd_toEndOf="parent"
                app:layout_constraintHorizontal_bias="0.5"
                android:layout_marginTop="{top_margin}dp"
                app:layout_constraintTop_toBottomOf="parent"
                app:layout_constraintVertical_bias="0.0"/>
                    """
                    top_margin += 60 # Approximate spacing for buttons
                elif element_type == "TextView":
                    layout_content += f"""
            <TextView
                android:id="@+id/{element_id}"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="{element_text}"
                app:layout_constraintTop_toTopOf="parent"
                app:layout_constraintStart_toStartOf="parent"
                app:layout_constraintEnd_toEndOf="parent"
                app:layout_constraintHorizontal_bias="0.5"
                android:layout_marginTop="{top_margin}dp"
                app:layout_constraintTop_toBottomOf="parent"
                app:layout_constraintVertical_bias="0.0"/>
                    """
                    top_margin += 50 # Approximate spacing for text views
                elif element_type == "ImageView":
                    layout_content += f"""
            <ImageView
                android:id="@+id/{element_id}"
                android:layout_width="200dp"
                android:layout_height="200dp"
                android:contentDescription="@string/app_name"
                app:layout_constraintTop_toTopOf="parent"
                app:layout_constraintStart_toStartOf="parent"
                app:layout_constraintEnd_toEndOf="parent"
                app:layout_constraintHorizontal_bias="0.5"
                android:layout_marginTop="{top_margin}dp"
                app:layout_constraintTop_toBottomOf="parent"
                app:layout_constraintVertical_bias="0.0"/>
                    """
                    top_margin += 210 # Approximate spacing for image views

        layout_content += """
        </androidx.constraintlayout.widget.ConstraintLayout>
        """
        with open(os.path.join(project_path, "app", "src", "main", "res", "layout", "activity_main.xml"), "w", encoding="utf-8") as f:
            f.write(layout_content)

        # Create a dummy sample_image.png if the prompt requested it
        if any(e.get("type") == "ImageView" and e.get("source") == "sample_image.png" for e in nlp_output.get("ui_elements", [])):
            # Create a simple placeholder image file
            with open(os.path.join(project_path, "app", "src", "main", "res", "drawable", "sample_image.png"), "wb") as f:
                f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\xfc\xff\xff?\x03\x00\x08\xfb\x02\xfe\xa7\xcd\x89\xe3\x00\x00\x00\x00IEND\xaeB`\x82')


        return {"project_path": project_path, "generated_files": ["MainActivity.java", "AndroidManifest.xml", "activity_main.xml"]}

class MockApkCompilerLobe:
    def build_apk(self, project_path, output_apk_path):
        print(f"MockApkCompilerLobe: Compiling project at {project_path} to {output_apk_path}.")
        # Simulate APK compilation. In a real scenario, this would involve calling
        # Android SDK build tools (e.g., Gradle).
        # For this mock, we'll just create a dummy APK file.
        try:
            # Create the output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_apk_path), exist_ok=True)
            with open(output_apk_path, "w") as f:
                f.write("This is a dummy APK file.")
            print("Mock APK compilation successful.")
            return True
        except Exception as e:
            print(f"Mock APK compilation failed: {e}")
            return False

if __name__ == '__main__':
    # --- Example Usage ---

    # Instantiate mock lobes
    mock_arabic_lobe = MockArabicLobe()
    mock_code_generation_lobe = MockCodeGenerationLobe()
    mock_apk_compiler_lobe = MockApkCompilerLobe()

    # Instantiate the main generator
    apk_generator = ArabicToApkGenerator(
        arabic_lobe_instance=mock_arabic_lobe,
        code_generation_lobe_instance=mock_code_generation_lobe,
        apk_compiler_lobe_instance=mock_apk_compiler_lobe
    )

    # Define an Arabic prompt
    # "أنشئ تطبيقًا يحتوي على زر يقول 'اضغط هنا' يعرض رسالة، وشاشة نصية تقول 'مرحبا بالعالم'."
    arabic_prompt_1 = "أنشئ تطبيقًا يحتوي على زر يقول 'اضغط هنا' يعرض رسالة، وشاشة نصية تقول 'مرحبا بالعالم'."
    generated_apk_1 = apk_generator.generate_apk_from_arabic(arabic_prompt_1, app_name="HelloArabicApp")
    if generated_apk_1:
        print(f"\nSuccessfully generated APK: {generated_apk_1}")
    else:
        print("\nAPK generation failed for prompt 1.")

    print("\n" + "="*50 + "\n")

    # Another example with an image
    # "أريد تطبيقًا يعرض صورة."
    arabic_prompt_2 = "أريد تطبيقًا يعرض صورة باسم sample_image.png."
    generated_apk_2 = apk_generator.generate_apk_from_arabic(arabic_prompt_2, app_name="ImageApp")
    if generated_apk_2:
        print(f"\nSuccessfully generated APK: {generated_apk_2}")
    else:
        print("\nAPK generation failed for prompt 2.")

    # Cleanup any remaining generated directories if the script is run directly
    print("\n--- Final Cleanup of base directories ---")
    if os.path.exists("generated_projects"):
        try:
            shutil.rmtree("generated_projects")
            print("Removed base directory: generated_projects")
        except OSError as e:
            print(f"Error removing base directory generated_projects: {e}")
    if os.path.exists("generated_apks"):
        try:
            shutil.rmtree("generated_apks")
            print("Removed base directory: generated_apks")
        except OSError as e:
            print(f"Error removing base directory generated_apks: {e}")