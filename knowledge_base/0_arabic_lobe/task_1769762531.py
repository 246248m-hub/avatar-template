import os
import re
import shutil

# Assume a dummy directory structure for APK compilation
DUMMY_PROJECT_ROOT = "dummy_apk_project"
DUMMY_MANIFEST_PATH = os.path.join(DUMMY_PROJECT_ROOT, "AndroidManifest.xml")
DUMMY_JAVA_SRC_DIR = os.path.join(DUMMY_PROJECT_ROOT, "app", "src", "main", "java")
DUMMY_RES_DIR = os.path.join(DUMMY_PROJECT_ROOT, "app", "src", "main", "res")

class ArabicNLPModule:
    """
    A module to process Arabic natural language queries, extract intents and entities,
    and prepare them for code generation.
    """
    def __init__(self):
        self.intent_keywords = {
            "create_activity": ["أنشئ", "اكتب", "صمم"],
            "set_text": ["اجعل النص", "ضع النص", "غيّر النص"],
            "add_button": ["أضف زر", "أنشئ زر"]
        }
        self.entity_patterns = {
            "activity_name": r"نشاط ([\w]+)",
            "text_content": r"النص هو \"(.*?)\"",
            "button_text": r"نص الزر هو \"(.*?)\""
        }

    def extract_intent_and_entities(self, query: str) -> dict:
        """
        Extracts the primary intent and associated entities from an Arabic query.

        Args:
            query: The Arabic natural language query.

        Returns:
            A dictionary containing the identified intent and entities.
            Example: {'intent': 'create_activity', 'entities': {'activity_name': 'MyActivity'}}
        """
        query_lower = query.lower()
        identified_intent = None
        extracted_entities = {}

        # Intent extraction
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    identified_intent = intent
                    break
            if identified_intent:
                break

        if not identified_intent:
            return {"intent": "unknown", "entities": {}}

        # Entity extraction based on identified intent
        if identified_intent == "create_activity":
            match = re.search(self.entity_patterns["activity_name"], query_lower)
            if match:
                extracted_entities["activity_name"] = match.group(1).capitalize() # Capitalize for class names
        elif identified_intent == "set_text":
            match = re.search(self.entity_patterns["text_content"], query_lower)
            if match:
                extracted_entities["text_content"] = match.group(1)
        elif identified_intent == "add_button":
            match = re.search(self.entity_patterns["button_text"], query_lower)
            if match:
                extracted_entities["button_text"] = match.group(1)

        return {"intent": identified_intent, "entities": extracted_entities}

class APKCompilerModule:
    """
    Simulates the compilation of an Android project into an APK.
    This module focuses on creating a basic project structure and a dummy manifest.
    """
    def __init__(self):
        self.project_root = DUMMY_PROJECT_ROOT
        self.manifest_path = DUMMY_MANIFEST_PATH
        self.java_src_dir = DUMMY_JAVA_SRC_DIR
        self.res_dir = DUMMY_RES_DIR

    def _create_dummy_project_structure(self):
        """Creates a basic directory structure for an Android project."""
        if os.path.exists(self.project_root):
            shutil.rmtree(self.project_root) # Clean up previous runs

        os.makedirs(os.path.join(self.project_root, "app", "src", "main", "java"), exist_ok=True)
        os.makedirs(os.path.join(self.project_root, "app", "src", "main", "res"), exist_ok=True)
        os.makedirs(os.path.join(self.project_root, "app", "build"), exist_ok=True)
        print(f"Created dummy project structure at: {self.project_root}")

    def _create_dummy_manifest(self, package_name="com.example.myapplication"):
        """Creates a placeholder AndroidManifest.xml."""
        manifest_content = f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <!-- Activities will be added here by the code generation module -->
    </application>
</manifest>
"""
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)
        print(f"Created dummy AndroidManifest.xml at: {self.manifest_path}")

    def compile_apk(self, project_config: dict) -> str:
        """
        Simulates the APK compilation process.
        In a real scenario, this would involve using Android SDK tools (aapt, dx, apksigner, etc.).
        Here, we just create the project structure and a dummy manifest.

        Args:
            project_config: A dictionary containing information about the project,
                            e.g., package name.

        Returns:
            A string indicating the success or failure of the simulated compilation,
            and the path to the dummy project.
        """
        package_name = project_config.get("package_name", "com.example.generatedapp")

        try:
            self._create_dummy_project_structure()
            self._create_dummy_manifest(package_name=package_name)
            print(f"\n--- Simulated APK compilation for package '{package_name}' successful. ---")
            return f"Simulated APK compilation successful. Project located at: {self.project_root}"
        except Exception as e:
            print(f"Simulated APK compilation failed: {e}")
            return f"Simulated APK compilation failed: {e}"

    def cleanup(self):
        """Cleans up the dummy project directory."""
        if os.path.exists(self.project_root):
            print(f"\n--- Cleaning up dummy project directory: {self.project_root} ---")
            shutil.rmtree(self.project_root)
            print("Dummy project directory removed.")

# --- Example Usage ---
if __name__ == "__main__":
    arabic_nlp = ArabicNLPModule()
    apk_compiler = APKCompilerModule()

    print("--- Testing Arabic NLP Module ---")
    queries = [
        "أنشئ نشاط MyNewActivity",
        "اجعل النص هو \"مرحباً بالعالم!\"",
        "أضف زر بنص \"اضغط هنا\"",
        "اكتب كلاس بسيط" # Intent not directly supported by current entity patterns
    ]

    for query in queries:
        intent_entities = arabic_nlp.extract_intent_and_entities(query)
        print(f"Query: '{query}' -> {intent_entities}")

    print("\n--- Testing APK Compiler Module ---")
    # Simulate compilation based on extracted intents (this would be driven by Lobe 4)
    dummy_project_config = {"package_name": "com.generated.arabicapp"}
    compile_result = apk_compiler.compile_apk(dummy_project_config)
    print(compile_result)

    # In a real system, Lobe 4 would generate Java/Kotlin files and potentially XML resources
    # based on the intent_entities and then pass the project structure to this module.

    # Clean up
    apk_compiler.cleanup()

    print("\n--- Arabic NLP and APK Compiler Module Demo Finished ---")