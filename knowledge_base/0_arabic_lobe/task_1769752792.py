import os
import shutil
import subprocess
from pathlib import Path

# Assume a rudimentary knowledge base for demonstration purposes
KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
if not KNOWLEDGE_BASE_DIR.exists():
    KNOWLEDGE_BASE_DIR.mkdir()
    (KNOWLEDGE_BASE_DIR / "arabic_grammar.json").write_text("{}")
    (KNOWLEDGE_BASE_DIR / "arabic_syntax.json").write_text("{}")
    (KNOWLEDGE_BASE_DIR / "apk_structure.json").write_text("{}")

# Mock components for demonstration
class ArabicParser:
    def parse(self, text: str) -> dict:
        print(f"Parsing Arabic text: '{text}'")
        # In a real scenario, this would involve sophisticated NLP techniques
        # For demonstration, we'll return a simplified structure
        if "create an app" in text.lower():
            return {"intent": "create_app", "details": {"app_name": "MyNewApp"}}
        elif "add a button" in text.lower():
            return {"intent": "add_component", "details": {"component_type": "button", "text": "Click Me"}}
        return {"intent": "unknown", "details": {}}

class ArabicCodeGenerator:
    def generate_android_manifest(self, app_name: str) -> str:
        print(f"Generating AndroidManifest.xml for '{app_name}'")
        return f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.{app_name.lower()}">
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
</manifest>"""

    def generate_activity_layout(self, component_data: dict) -> str:
        print(f"Generating layout for component: {component_data}")
        layout_content = '<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto" xmlns:tools="http://schemas.android.com/tools" android:layout_width="match_parent" android:layout_height="match_parent" android:orientation="vertical" tools:context=".MainActivity">\n'
        if component_data.get("component_type") == "button":
            button_text = component_data.get("text", "Button")
            layout_content += f'    <Button\n'
            layout_content += f'        android:id="@+id/myButton"\n'
            layout_content += f'        android:layout_width="wrap_content"\n'
            layout_content += f'        android:layout_height="wrap_content"\n'
            layout_content += f'        android:text="{button_text}" />\n'
        layout_content += '</LinearLayout>'
        return layout_content

    def generate_main_activity_java(self, app_name: str) -> str:
        print(f"Generating MainActivity.java for '{app_name}'")
        return f"""package com.example.{app_name.lower()};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // TODO: Add component logic here based on parsed input
    }}
}}
"""

class ProjectBuilder:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.package_name = ""
        self.app_name = ""

    def create_project_structure(self, app_name: str):
        self.app_name = app_name
        self.package_name = f"com.example.{app_name.lower()}"
        self.root_dir.mkdir(parents=True, exist_ok=True)

        # Android project structure mimicry
        (self.root_dir / "app").mkdir(exist_ok=True)
        (self.root_dir / "app" / "src").mkdir(exist_ok=True)
        (self.root_dir / "app" / "src" / "main").mkdir(exist_ok=True)
        (self.root_dir / "app" / "src" / "main" / "java").mkdir(parents=True, exist_ok=True)
        (self.root_dir / "app" / "src" / "main" / "java" / self.package_name.replace('.', os.sep)).mkdir(parents=True, exist_ok=True)
        (self.root_dir / "app" / "src" / "main" / "res").mkdir(exist_ok=True)
        (self.root_dir / "app" / "src" / "main" / "res" / "layout").mkdir(exist_ok=True)
        (self.root_dir / "app" / "src" / "main" / "res" / "values").mkdir(exist_ok=True)

        # Create initial placeholder files
        (self.root_dir / "app" / "src" / "main" / "AndroidManifest.xml").touch()
        (self.root_dir / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml").touch()
        (self.root_dir / "app" / "src" / "main" / "java" / self.package_name.replace('.', os.sep) / "MainActivity.java").touch()
        (self.root_dir / "app" / "src" / "main" / "res" / "values" / "strings.xml").write_text(f'<resources><string name="app_name">{app_name}</string></resources>')

        print(f"Created project structure for '{app_name}' at {self.root_dir}")

    def add_component_to_project(self, component_data: dict, code_generator: ArabicCodeGenerator):
        layout_file_path = self.root_dir / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml"
        activity_file_path = self.root_dir / "app" / "src" / "main" / "java" / self.package_name.replace('.', os.sep) / "MainActivity.java"

        # For simplicity, we'll overwrite the layout and modify the activity if needed.
        # A real implementation would parse the existing layout and activity and inject.
        new_layout_content = code_generator.generate_layout_for_component(component_data)
        layout_file_path.write_text(new_layout_content)
        print(f"Updated layout file: {layout_file_path}")

        # In a real scenario, you would parse MainActivity.java and inject necessary code
        # For this demo, we'll assume MainActivity.java is generated with placeholders for components.
        # A more robust approach would be to add logic to the onCreate method to find and interact with components.

    def write_manifest(self, manifest_content: str):
        manifest_file_path = self.root_dir / "app" / "src" / "main" / "AndroidManifest.xml"
        manifest_file_path.write_text(manifest_content)
        print(f"Wrote AndroidManifest.xml to {manifest_file_path}")

    def write_activity(self, activity_content: str):
        activity_file_path = self.root_dir / "app" / "src" / "main" / "java" / self.package_name.replace('.', os.sep) / "MainActivity.java"
        activity_file_path.write_text(activity_content)
        print(f"Wrote MainActivity.java to {activity_file_path}")

    def cleanup(self):
        if self.root_dir.exists():
            print(f"Cleaning up project directory: {self.root_dir}")
            shutil.rmtree(self.root_dir)

class ArabicAPKCompiler:
    def __init__(self, project_root: Path, android_sdk_path: str):
        self.project_root = project_root
        self.android_sdk_path = android_sdk_path
        self.build_tools_path = Path(android_sdk_path) / "build-tools"
        self.platforms_path = Path(android_sdk_path) / "platforms"
        self.apksigner_path = Path(android_sdk_path) / "build-tools" / self._get_latest_build_tools() / "apksigner"
        self.aapt_path = Path(android_sdk_path) / "build-tools" / self._get_latest_build_tools() / "aapt"
        self.dx_path = Path(android_sdk_path) / "build-tools" / self._get_latest_build_tools() / "dx" # Older SDKs might use this for dexing. Newer ones use D8.

        # Find D8 if available (preferred for modern Android development)
        d8_path_candidates = list(Path(android_sdk_path).rglob("d8"))
        self.d8_path = d8_path_candidates[0] if d8_path_candidates else None

        self.platform_tools_path = Path(android_sdk_path) / "platform-tools"
        self.adb_path = self.platform_tools_path / "adb"


    def _get_latest_build_tools(self) -> str:
        if not self.build_tools_path.exists():
            raise FileNotFoundError(f"Build tools directory not found: {self.build_tools_path}")
        build_tool_versions = sorted(os.listdir(self.build_tools_path), reverse=True)
        if not build_tool_versions:
            raise FileNotFoundError(f"No build tools found in: {self.build_tools_path}")
        return build_tool_versions[0]

    def _run_command(self, command: list, cwd: Path = None, env: dict = None):
        print(f"Executing: {' '.join(command)}")
        try:
            result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=True, env=env)
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
            print("STDOUT:", e.stdout)
            print("STDERR:", e.stderr)
            raise

    def compile_apk(self, app_name: str, output_dir: Path) -> Path:
        # This is a simplified flow. A real Android build process involves Gradle,
        # which handles much more complexity. This mimics some steps for demonstration.

        # 1. Identify Java and Javac
        java_home = os.environ.get("JAVA_HOME")
        if not java_home:
            raise EnvironmentError("JAVA_HOME environment variable not set. Cannot compile.")
        java_cmd = Path(java_home) / "bin" / "java"
        javac_cmd = Path(java_home) / "bin" / "javac"

        # 2. Compile Java source files
        app_package_path = self.project_root / "app" / "src" / "main" / "java" / f"com.example.{app_name.lower()}"
        main_activity_java = app_package_path / "MainActivity.java"
        classes_dir = self.project_root / "classes"
        classes_dir.mkdir(exist_ok=True)

        # Need to find Android SDK jars for compilation. This is highly dependent on SDK structure.
        # A common location for platform jars is under SDK/platforms/android-<version>/android.jar
        android_jar_version = "android-30" # Example, should be dynamically found
        android_jar = self.platforms_path / android_jar_version / "android.jar"
        if not android_jar.exists():
            print(f"Warning: {android_jar} not found. Compilation might fail or require manual path configuration.")
            # Fallback or error out if critical
            raise FileNotFoundError(f"Android platform jar not found: {android_jar}")


        javac_command = [
            str(javac_cmd),
            f"-bootclasspath={android_jar}",
            f"-d={classes_dir}",
            str(main_activity_java)
        ]
        self._run_command(javac_command)

        # 3. Dexing (converting .class files to .dex)
        dex_file = self.project_root / "classes.dex"
        if self.d8_path and self.d8_path.exists():
            # Using D8 (preferred)
            d8_command = [
                str(java_cmd),
                "-jar",
                str(self.d8_path),
                str(classes_dir),
                "--output",
                str(self.project_root)
            ]
            self._run_command(d8_command)
        elif self.dx_path and self.dx_path.exists():
            # Using dx (older)
            dx_command = [
                str(self.dx_path),
                "--dex",
                f"--output={dex_file}",
                str(classes_dir)
            ]
            self._run_command(dx_command)
        else:
            raise FileNotFoundError("D8 or dx tool not found. Cannot dex classes.")


        # 4. Creating an unsigned APK
        apk_output_dir = output_dir / "unsigned_apks"
        apk_output_dir.mkdir(parents=True, exist_ok=True)
        unsigned_apk_path = apk_output_dir / f"{app_name}-unsigned.apk"

        # This step is usually handled by aapt or aapt2 to create the APK structure
        # For simplicity, we'll assume a basic structure can be created.
        # Aapt2 is the modern tool.
        aapt2_path = self.build_tools_path / self._get_latest_build_tools() / "aapt2"
        if not aapt2_path.exists():
             aapt2_path = self.build_tools_path / self._get_latest_build_tools() / "aapt" # Fallback to aapt if aapt2 not found
             if not aapt2_path.exists():
                 raise FileNotFoundError("aapt2 or aapt tool not found. Cannot create APK structure.")

        # Clean up old intermediate files if they exist
        for ext in [".apk", ".zip", ".res", ".res.apk"]:
            if (self.project_root / f"app-{ext}").exists():
                (self.project_root / f"app-{ext}").unlink()
            if (self.project_root / f"{app_name}.apk").exists():
                (self.project_root / f"{app_name}.apk").unlink()

        # Use aapt/aapt2 to package resources and create an intermediate APK.
        # This command is a simplified representation. The actual command sequence for
        # packaging resources and creating an intermediate APK is more involved.
        # A common approach involves `aapt2 link` and `aapt2 compile` followed by `aapt2 process`.
        # For this demo, we'll simulate the creation of an intermediate file.

        # A more realistic approach using AAPT2:
        # 1. Compile resources: aapt2 compile -o app.flt app/src/main/res
        # 2. Link resources: aapt2 link app.flt -o app.apk --manifest app/src/main/AndroidManifest.xml
        # This requires a more elaborate resource compilation process which we are skipping for this example.

        # For a simpler demonstration, we will use `zip` to create an APK structure
        # and then use apksigner. This is NOT how Android build tools work internally
        # but serves to demonstrate the signing step.

        # Create a dummy APK structure
        apk_contents_dir = self.project_root / "apk_contents"
        apk_contents_dir.mkdir(exist_ok=True)

        # Copy AndroidManifest.xml
        shutil.copy(self.project_root / "app" / "src" / "main" / "AndroidManifest.xml", apk_contents_dir / "AndroidManifest.xml")

        # Copy resources (simplified)
        res_dir = apk_contents_dir / "res"
        res_dir.mkdir(exist_ok=True)
        if (self.project_root / "app" / "src" / "main" / "res" / "layout").exists():
            shutil.copytree(self.project_root / "app" / "src" / "main" / "res" / "layout", res_dir / "layout", dirs_exist_ok=True)
        if (self.project_root / "app" / "src" / "main" / "res" / "values").exists():
            shutil.copytree(self.project_root / "app" / "src" / "main" / "res" / "values", res_dir / "values", dirs_exist_ok=True)

        # Copy dex file
        shutil.copy(dex_file, apk_contents_dir / "classes.dex")

        # Create META-INF directory for signature
        (apk_contents_dir / "META-INF").mkdir(exist_ok=True)
        (apk_contents_dir / "META-INF" / "MANIFEST.MF").touch() # Dummy manifest file

        # Create the unsigned APK by zipping the contents
        # Note: This does NOT create a valid APK structure as Android expects.
        # A real APK is a ZIP file with specific directory structures and headers.
        # This is a very crude simulation.
        apk_zip_command = ["zip", "-r", str(unsigned_apk_path), ".", "-C", str(apk_contents_dir)]
        self._run_command(apk_zip_command, cwd=apk_contents_dir)

        print(f"Created unsigned APK at: {unsigned_apk_path}")

        # 5. Sign the APK
        # For signing, we need a keystore. For demonstration, we'll use a dummy one
        # or assume one exists. A real build process uses a debug keystore or a release keystore.
        # We'll create a dummy keystore for this example if it doesn't exist.
        dummy_keystore_path = self.project_root / "dummy.keystore"
        if not dummy_keystore_path.exists():
            print("Creating a dummy keystore for signing...")
            keytool_cmd = [
                str(Path(java_home) / "bin" / "keytool"),
                "-genkey", "-v", "-keystore", str(dummy_keystore_path),
                "-alias", "myalias", "-keyalg", "RSA", "-keysize", "2048",
                "-validity", "10000", "-storepass", "password", "-keypass", "password",
                "-dname", "CN=Android Debug,O=Android,C=US"
            ]
            self._run_command(keytool_cmd)

        signed_apk_path = output_dir / f"{app_name}-signed.apk"
        apksigner_command = [
            str(self.apksigner_path),
            "sign",
            "--ks", str(dummy_keystore_path),
            "--ks-pass", "pass:password",
            "--out", str(signed_apk_path),
            str(unsigned_apk_path)
        ]
        self._run_command(apksigner_command)

        print(f"Signed APK created at: {signed_apk_path}")

        # Clean up intermediate files
        if classes_dir.exists():
            shutil.rmtree(classes_dir)
        if dex_file.exists():
            dex_file.unlink()
        if apk_contents_dir.exists():
            shutil.rmtree(apk_contents_dir)
        if unsigned_apk_path.exists():
            unsigned_apk_path.unlink() # Remove unsigned version after successful signing

        return signed_apk_path

class ArabicNLPProcessor:
    def __init__(self):
        self.parser = ArabicParser()
        self.code_generator = ArabicCodeGenerator()
        self.project_builder = None
        self.apk_compiler = None

    def set_android_sdk_path(self, sdk_path: str):
        self.apk_compiler = ArabicAPKCompiler(Path("./temp_project"), sdk_path)
        print(f"Android SDK path set to: {sdk_path}")

    def process_natural_language_request(self, nl_request: str, project_root: Path, output_dir: Path):
        parsed_data = self.parser.parse(nl_request)
        intent = parsed_data.get("intent")
        details = parsed_data.get("details", {})

        if intent == "create_app":
            app_name = details.get("app_name", "MyArabicApp")
            print(f"Creating new app: {app_name}")
            self.project_builder = ProjectBuilder(project_root / app_name)
            self.project_builder.create_project_structure(app_name)

            # Generate initial manifest
            manifest_content = self.code_generator.generate_android_manifest(app_name)
            self.project_builder.write_manifest(manifest_content)

            # Generate initial activity and layout
            activity_content = self.code_generator.generate_main_activity_java(app_name)
            self.project_builder.write_activity(activity_content)

            return {"status": "success", "message": f"App '{app_name}' created. Project structure generated."}

        elif intent == "add_component" and self.project_builder:
            print(f"Adding component: {details.get('component_type')}")
            # In a real scenario, you'd parse the existing layout and activity
            # and inject the new component's definition and logic.
            # For this demo, we'll assume a single main layout that gets updated.
            layout_content = self.code_generator.generate_activity_layout(details)
            self.project_builder.root_dir.joinpath("app", "src", "main", "res", "layout", "activity_main.xml").write_text(layout_content)
            print(f"Added component '{details.get('component_type')}' to layout.")
            return {"status": "success", "message": f"Component '{details.get('component_type')}' added."}

        elif intent == "build_apk" and self.project_builder and self.apk_compiler:
            print("Initiating APK build process...")
            app_name = self.project_builder.app_name
            signed_apk_path = self.apk_compiler.compile_apk(app_name, output_dir)
            return {"status": "success", "message": f"APK built successfully at {signed_apk_path}"}

        else:
            return {"status": "error", "message": f"Unsupported intent '{intent}' or missing context."}

    def cleanup_project(self):
        if self.project_builder:
            self.project_builder.cleanup()
            self.project_builder = None
        if self.apk_compiler and Path("./temp_project").exists():
            shutil.rmtree("./temp_project")
            print("Cleaned up temporary project directory.")


# --- Demo Usage ---
if __name__ == "__main__":
    # Ensure you have an Android SDK installed and JAVA_HOME set.
    # Replace with your actual Android SDK path.
    ANDROID_SDK_ROOT = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
    if not ANDROID_SDK_ROOT:
        print("Please set the ANDROID_HOME or ANDROID_SDK_ROOT environment variable.")
        print("Example: export ANDROID_HOME=/Users/youruser/Library/Android/sdk")
        exit(1)

    output_directory = Path("./build_output")
    output_directory.mkdir(exist_ok=True)

    processor = ArabicNLPProcessor()
    processor.set_android_sdk_path(ANDROID_SDK_ROOT)

    # 1. Create a new app
    request1 = "أنشئ تطبيقًا جديدًا اسمه 'ألف باء'" # Create a new app named 'Alif Ba'
    result1 = processor.process_natural_language_request(request1, Path("./temp_project"), output_directory)
    print(f"Result 1: {result1}")

    # 2. Add a component to the existing app
    if processor.project_builder:
        request2 = "أضف زرًا مع النص 'اضغط هنا'" # Add a button with text 'Click Here'
        result2 = processor.process_natural_language_request(request2, Path("./temp_project"), output_directory)
        print(f"Result 2: {result2}")

    # 3. Build the APK
    if processor.project_builder and processor.apk_compiler:
        request3 = "قم ببناء ملف APK للتطبيق الحالي" # Build the APK for the current app
        result3 = processor.process_natural_language_request(request3, Path("./temp_project"), output_directory)
        print(f"Result 3: {result3}")
    else:
        print("Cannot build APK: Project builder or APK compiler not initialized.")


    # Clean up
    processor.cleanup_project()
    print("\n--- ArabicNLPProcessor Module Demo Finished ---")