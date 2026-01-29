import os
import shutil
import subprocess
import json
from pathlib import Path
from typing import Dict, Any

# --- Configuration ---
PROJECT_TEMPLATE_DIR = Path("./project_templates/android_basic")
OUTPUT_DIR = Path("./generated_apks")

# --- Helper Functions ---
def load_language_model(model_name: str = "gpt-3.5-turbo"):
    """
    Loads a language model. In a real scenario, this would involve
    instantiating an API client or loading a local model.
    For this example, we'll simulate it.
    """
    print(f"Simulating loading language model: {model_name}")
    class MockLanguageModel:
        def generate(self, prompt: str, context: Dict[str, Any] = None) -> str:
            print(f"Simulating LLM generation for prompt: {prompt[:50]}...")
            # In a real LLM, this would be the core generation logic.
            # For Arabic, we'd expect it to generate code or descriptions.
            if "generate Arabic Android UI component code" in prompt:
                return "// Simulated Arabic UI code for a Button\nButton arabicButton = new Button(this);\narabicButton.setText(\"زر\");\narabicButton.setId(View.generateViewId());\nlayout.addView(arabicButton);"
            elif "generate manifest entry for Arabic language" in prompt:
                return "<application android:supportsRtl=\"true\"> ... </application>"
            elif "extract package name and main activity from Arabic prompt" in prompt:
                return json.dumps({"package_name": "com.example.arabicapp", "main_activity": "MainActivity"})
            else:
                return "// Simulated generic code\npublic class MainActivity extends AppCompatActivity { ... }"
    return MockLanguageModel()

def create_android_project(project_name: str, template_dir: Path, output_dir: Path) -> Path:
    """
    Creates a new Android project from a template.
    """
    print(f"Creating Android project '{project_name}' from template '{template_dir}' in '{output_dir}'")
    project_path = output_dir / project_name
    if project_path.exists():
        shutil.rmtree(project_path)
    shutil.copytree(template_dir, project_path)
    return project_path

def modify_project_files(project_path: Path, modifications: Dict[str, str]):
    """
    Applies modifications to project files.
    This is a simplified version; real modifications would be more complex.
    """
    print(f"Applying modifications to project at '{project_path}'")
    for file_path_rel, content in modifications.items():
        file_path = project_path / file_path_rel
        if file_path.is_file():
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(f"\n// Custom modification:\n{content}")
            print(f"  - Modified: {file_path_rel}")
        else:
            print(f"  - Warning: File not found for modification: {file_path_rel}")

def compile_apk(project_path: Path, output_apk_path: Path) -> bool:
    """
    Compiles the Android project into an APK.
    This requires Android SDK and Gradle to be set up.
    """
    print(f"Attempting to compile APK for project at '{project_path}'")
    try:
        # Assuming the project is set up for Gradle
        # This command might vary depending on the project structure and SDK setup
        # For a simple project, './gradlew assembleDebug' might work from the project root
        # We'll simulate success here.
        print("Simulating APK compilation. This requires Android SDK and Gradle.")
        # In a real scenario:
        # original_dir = os.getcwd()
        # os.chdir(project_path)
        # subprocess.run(["./gradlew", "assembleDebug"], check=True, capture_output=True, text=True)
        # os.chdir(original_dir)
        # Find the generated APK (usually in app/build/outputs/apk/debug/app-debug.apk)
        # shutil.copy(project_path / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk", output_apk_path)
        print(f"Simulated successful compilation. APK would be generated at: {output_apk_path}")
        # Create a dummy APK file for demonstration
        with open(output_apk_path, "w", encoding="utf-8") as f:
            f.write("// Dummy APK file")
        return True
    except subprocess.CalledProcessError as e:
        print(f"APK compilation failed: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during compilation: {e}")
        return False

# --- Lobe Definition ---

class ArabicApkGenerator:
    def __init__(self):
        self.llm = load_language_model()
        self.project_root: Path | None = None
        self.generated_apk_path: Path | None = None

    def extract_project_info(self, natural_language_prompt: str) -> Dict[str, str]:
        """
        Uses the LLM to extract project details like package name and main activity
        from an Arabic natural language prompt.
        """
        print(f"Extracting project info from Arabic prompt: '{natural_language_prompt}'")
        extraction_prompt = f"""
        Based on the following Arabic natural language description of an Android app,
        extract the desired package name and the name of the main activity.
        Return the result as a JSON object with keys 'package_name' and 'main_activity'.

        Arabic Prompt: "{natural_language_prompt}"
        """
        try:
            json_output = self.llm.generate(extraction_prompt)
            project_info = json.loads(json_output)
            print(f"Extracted project info: {project_info}")
            return project_info
        except Exception as e:
            print(f"Error extracting project info: {e}")
            # Fallback for demonstration
            return {"package_name": "com.arabic.example", "main_activity": "ArabicMainActivity"}

    def generate_arabic_ui_code(self, component_description: str) -> str:
        """
        Generates Android UI code (e.g., XML or Java/Kotlin) for Arabic components
        based on a description.
        """
        print(f"Generating Arabic UI code for: '{component_description}'")
        generation_prompt = f"""
        Generate Android UI code (Java/Kotlin) for the following Arabic UI component description.
        Ensure the code is syntactically correct for an Android Activity.

        Description: "{component_description}"
        """
        try:
            code = self.llm.generate(generation_prompt)
            print("Generated UI code snippet.")
            return code
        except Exception as e:
            print(f"Error generating UI code: {e}")
            return "// Error generating UI code"

    def generate_manifest_entry(self, language_support_desc: str) -> str:
        """
        Generates necessary AndroidManifest.xml entries for Arabic language support.
        """
        print(f"Generating manifest entry for: '{language_support_desc}'")
        generation_prompt = f"""
        Generate AndroidManifest.xml snippet to ensure proper Arabic language support (RTL, etc.).

        Description: "{language_support_desc}"
        """
        try:
            manifest_snippet = self.llm.generate(generation_prompt)
            print("Generated manifest snippet.")
            return manifest_snippet
        except Exception as e:
            print(f"Error generating manifest entry: {e}")
            return "<!-- Error generating manifest entry -->"

    def create_apk(self, natural_language_prompt: str) -> Path | None:
        """
        Orchestrates the creation of an Android APK from a natural language prompt.
        """
        print("\n--- Initiating Arabic APK Generation ---")

        # 1. Extract Project Information
        project_info = self.extract_project_info(natural_language_prompt)
        package_name = project_info.get("package_name", "com.arabic.generated")
        main_activity_name = project_info.get("main_activity", "MainActivity")
        project_name = f"{package_name.split('.')[-1]}_app" # Simple project name from package

        # 2. Create Android Project from Template
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.project_root = create_android_project(project_name, PROJECT_TEMPLATE_DIR, OUTPUT_DIR)
        print(f"Project created at: {self.project_root}")

        # 3. Generate and Integrate Arabic Specific Code/Configurations
        modifications = {}

        # Simulate generating and adding UI code
        ui_code_description = "A simple button with the text 'اضغط هنا'"
        arabic_ui_code = self.generate_arabic_ui_code(ui_code_description)
        # In a real scenario, this code would be inserted into the appropriate Java/Kotlin file
        # For demonstration, we'll add it as a comment in a dummy modification
        modifications["app/src/main/java/com/example/android_basic/MainActivity.java"] = f"""
        // Added Arabic UI component
        {arabic_ui_code}
        """

        # Simulate generating and adding manifest entry
        manifest_entry_description = "Enable Right-to-Left (RTL) support and Arabic resources"
        manifest_snippet = self.generate_manifest_entry(manifest_entry_description)
        # In a real scenario, this would be merged into the AndroidManifest.xml
        modifications["app/src/main/AndroidManifest.xml"] = f"""
        {manifest_snippet}
        """

        # Apply modifications (simplified)
        modify_project_files(self.project_root, modifications)

        # 4. Compile APK
        self.generated_apk_path = OUTPUT_DIR / f"{project_name}.apk"
        if compile_apk(self.project_root, self.generated_apk_path):
            print(f"\nSuccessfully generated APK: {self.generated_apk_path}")
            return self.generated_apk_path
        else:
            print("\nAPK generation failed.")
            return None

    def cleanup_generated_projects(self):
        """
        Cleans up the generated project directory.
        """
        if self.project_root and self.project_root.exists():
            print(f"Cleaning up generated project directory: {self.project_root}")
            shutil.rmtree(self.project_root)
            self.project_root = None
        if self.generated_apk_path and self.generated_apk_path.exists():
            print(f"Cleaning up generated APK: {self.generated_apk_path}")
            self.generated_apk_path.unlink()
            self.generated_apk_path = None

# --- Demo Usage ---
if __name__ == "__main__":
    # Ensure the project template directory exists for the demo
    if not PROJECT_TEMPLATE_DIR.exists():
        print(f"Error: Project template directory '{PROJECT_TEMPLATE_DIR}' not found.")
        print("Please create a directory './project_templates/android_basic' with a basic Android project structure.")
    else:
        generator = ArabicApkGenerator()

        # Example Arabic prompt
        arabic_prompt_example = "إنشاء تطبيق أندرويد بسيط يعرض 'أهلاً بالعالم' بزر للتفاعل."

        try:
            generated_apk = generator.create_apk(arabic_prompt_example)
            if generated_apk:
                print(f"\nAPK generation process completed successfully. APK saved at: {generated_apk}")
            else:
                print("\nAPK generation process encountered errors.")
        except Exception as e:
            print(f"\nAn error occurred during the APK generation demo: {e}")
        finally:
            # Clean up generated projects after the demo
            generator.cleanup_generated_projects()

        print("\n--- Arabic APK Generator Module Demo Finished ---")