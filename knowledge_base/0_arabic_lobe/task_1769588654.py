import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Assuming necessary imports from other lobes are handled by the environment
# For demonstration purposes, we'll simulate them if they don't exist.

try:
    from lobe_0_arabic_lobe import parse_arabic_to_intermediate, generate_apk_structure_from_intermediate
except ImportError:
    print("Simulating lobe_0_arabic_lobe for demonstration.")
    def parse_arabic_to_intermediate(prompt: str) -> Dict[str, Any]:
        """
        Simulates parsing an Arabic prompt into an intermediate representation
        suitable for APK generation.
        """
        print(f"Simulating parse_arabic_to_intermediate for prompt: '{prompt}'")
        # A simplified intermediate representation
        return {
            "app_name": f"GeneratedApp_{prompt[:5]}",
            "package_name": f"com.example.{prompt.lower().replace(' ', '_')}",
            "version_name": "1.0",
            "version_code": 1,
            "features": {
                "main_activity": {
                    "layout": "activity_main.xml",
                    "buttons": [
                        {"id": "button_greet", "text": "Greet User", "action": "show_greeting"}
                    ],
                    "text_views": [
                        {"id": "text_welcome", "text": "Welcome to the app!"}
                    ]
                }
            },
            "permissions": ["INTERNET"]
        }

    def generate_apk_structure_from_intermediate(intermediate_repr: Dict[str, Any], output_dir: Path) -> Path:
        """
        Simulates generating a basic APK structure (manifest, layout files)
        from an intermediate representation.
        """
        print(f"Simulating generate_apk_structure_from_intermediate for app: {intermediate_repr.get('app_name')}")
        app_dir = output_dir / intermediate_repr["package_name"].replace('.', os.sep)
        app_dir.mkdir(parents=True, exist_ok=True)

        # Generate AndroidManifest.xml
        manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{intermediate_repr['package_name']}">

    <uses-sdk android:minSdkVersion="21" android:targetSdkVersion="33"/>
    """
        if "INTERNET" in intermediate_repr.get("permissions", []):
            manifest_content += '    <uses-permission android:name="android.permission.INTERNET"/>\n'

        manifest_content += f"""
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="{intermediate_repr.get('app_name', 'MyApplication')}"
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
        manifest_path = app_dir / "AndroidManifest.xml"
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)

        # Generate layout file (simplified)
        layout_dir = app_dir / "res" / "layout"
        layout_dir.mkdir(parents=True, exist_ok=True)
        layout_filename = intermediate_repr["features"]["main_activity"]["layout"]
        layout_path = layout_dir / layout_filename

        layout_content = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/text_welcome"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{intermediate_repr['features']['main_activity']['text_views'][0]['text']}"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent"/>

    <Button
        android:id="@+id/button_greet"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{intermediate_repr['features']['main_activity']['buttons'][0]['text']}"
        app:layout_constraintTop_toBottomOf="@+id/text_welcome"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="20dp"/>
</androidx.constraintlayout.widget.ConstraintLayout>
"""
        with open(layout_path, "w", encoding="utf-8") as f:
            f.write(layout_content)

        # Simulate creation of basic launcher icon directories
        icon_dir = app_dir / "res" / "mipmap-xhdpi"
        icon_dir.mkdir(parents=True, exist_ok=True)
        (icon_dir / "ic_launcher.png").touch()
        (icon_dir / "ic_launcher_round.png").touch()

        return app_dir


# Global directory for generated APK structures
GENERATED_APKS_DIR = Path("./generated_apk_structures")
GENERATED_APKS_DIR.mkdir(parents=True, exist_ok=True)

def build_initial_apk_structure(arabic_prompt: str) -> Optional[Path]:
    """
    Parses an Arabic prompt and generates the initial Android project structure
    (manifest, resource files) for an APK.

    Args:
        arabic_prompt: The natural language prompt in Arabic describing the desired APK.

    Returns:
        The path to the root directory of the generated APK project structure,
        or None if parsing or generation fails.
    """
    print(f"\n--- Initiating Lobe 4: Code Generation Lobe (APK Structure) ---")
    print(f"Processing Arabic prompt: '{arabic_prompt}'")

    # Step 1: Parse Arabic prompt into an intermediate representation
    # This simulates the role of Lobe 0 (arabic_lobe) in understanding the prompt
    # and translating it into a structured format.
    intermediate_representation = parse_arabic_to_intermediate(arabic_prompt)

    if not intermediate_representation:
        print("Error: Failed to parse Arabic prompt into intermediate representation.")
        return None

    print(f"Successfully parsed prompt. Intermediate representation generated.")
    # Optionally, print or log the intermediate representation for debugging
    # print(f"Intermediate Representation: {json.dumps(intermediate_representation, indent=2)}")

    # Step 2: Generate the basic APK project structure from the intermediate representation
    # This is the core of the "code generation" for the APK's foundational files.
    # It simulates the process that would eventually lead to compilation.
    try:
        apk_project_root = generate_apk_structure_from_intermediate(
            intermediate_representation,
            GENERATED_APKS_DIR
        )
        print(f"Successfully generated initial APK project structure at: {apk_project_root}")
        return apk_project_root
    except Exception as e:
        print(f"Error generating APK project structure: {e}")
        return None

def cleanup_generated_apk_structures():
    """
    Removes the directory containing generated APK structures.
    """
    print("\n--- Cleaning up generated APK structures ---")
    if GENERATED_APKS_DIR.exists():
        import shutil
        try:
            shutil.rmtree(GENERATED_APKS_DIR)
            print(f"Removed directory: {GENERATED_APKS_DIR}")
        except OSError as e:
            print(f"Error removing directory {GENERATED_APKS_DIR}: {e}")
    else:
        print(f"Directory {GENERATED_APKS_DIR} does not exist, no cleanup needed.")

if __name__ == "__main__":
    # Example Usage of Lobe 4_code_generation_lobe
    arabic_input_prompt = "تطبيق بسيط يعرض رسالة ترحيب وزر لقول مرحبًا" # "A simple app that displays a welcome message and a button to say hello"

    generated_structure_path = build_initial_apk_structure(arabic_input_prompt)

    if generated_structure_path:
        print("\n--- Lobe 4: Code Generation Lobe (APK Structure) Demo Finished Successfully ---")
        print(f"Generated APK structure is located at: {generated_structure_path}")

        # Simulate next steps in the pipeline (e.g., Lobe 6_synthesis_lobe and Lobe 8_apk_compiler_lobe)
        print("\n--- Initiating next step: Lobe 6_synthesis_lobe (Simulated) ---")
        print("Simulating synthesis of logic and resources into a compilable unit.")
        # In a real scenario, this would involve Lobe 6 taking the structure and adding code.

        print("\n--- Initiating next step: Lobe 8_apk_compiler_lobe (Simulated) ---")
        print("Simulating the compilation of the APK project structure into a final APK.")
        # In a real scenario, this would involve Lobe 8 invoking build tools.
        print("Mocking debug.keystore setup...")
        mock_keystore_dir = generated_structure_path / ".android"
        mock_keystore_dir.mkdir(parents=True, exist_ok=True)
        debug_keystore_path = mock_keystore_dir / "debug.keystore"
        debug_keystore_path.touch()
        print("Mock debug.keystore created.")
        # End of simulated Lobe 8


    else:
        print("\n--- Lobe 4: Code Generation Lobe (APK Structure) Demo Failed ---")

    # Cleanup
    cleanup_generated_apk_structures()

    # Verify cleanup
    if not GENERATED_APKS_DIR.exists():
        print("Cleanup successful.")
    else:
        print("Cleanup failed.")