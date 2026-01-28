import os
import shutil
import subprocess
from pathlib import Path

# --- Configuration ---
KNOWLEDGE_BASE_DIR = Path("knowledge_base")
ARABIC_GRAMMAR_DIR = KNOWLEDGE_BASE_DIR / "arabic_grammar"
ARABIC_LEXICON_DIR = KNOWLEDGE_BASE_DIR / "arabic_lexicon"
APK_TEMPLATES_DIR = KNOWLEDGE_BASE_DIR / "apk_templates"

# --- Helper Functions ---

def ensure_directory_exists(dir_path: Path):
    """Ensures a directory exists, creating it if it doesn't."""
    dir_path.mkdir(parents=True, exist_ok=True)

def load_text_from_file(file_path: Path) -> str:
    """Loads text content from a given file."""
    if not file_path.exists():
        return ""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def save_text_to_file(file_path: Path, content: str):
    """Saves text content to a given file."""
    ensure_directory_exists(file_path.parent)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def get_all_files_in_directory(dir_path: Path, extension: str = None) -> list[Path]:
    """Gets all files in a directory, optionally filtered by extension."""
    if not dir_path.exists():
        return []
    files = list(dir_path.iterdir())
    if extension:
        files = [f for f in files if f.is_file() and f.suffix == extension]
    return sorted(files)

# --- Lobe 0: Arabic NLP Core ---

class ArabicNlpCore:
    """
    Core functionalities for Arabic Natural Language Processing,
    including parsing and generation.
    """
    def __init__(self, grammar_dir: Path, lexicon_dir: Path):
        self.grammar_dir = grammar_dir
        self.lexicon_dir = lexicon_dir
        self.grammar_rules = self._load_grammar()
        self.lexicon = self._load_lexicon()

    def _load_grammar(self) -> dict:
        """Loads Arabic grammar rules from files."""
        grammar_data = {}
        for rule_file in get_all_files_in_directory(self.grammar_dir, ".rul"):
            rule_name = rule_file.stem
            grammar_data[rule_name] = load_text_from_file(rule_file)
        return grammar_data

    def _load_lexicon(self) -> dict:
        """Loads Arabic lexicon entries from files."""
        lexicon_data = {}
        for word_file in get_all_files_in_directory(self.lexicon_dir, ".lex"):
            word = word_file.stem
            lexicon_data[word] = load_text_from_file(word_file)
        return lexicon_data

    def parse_arabic_text(self, text: str) -> dict:
        """
        Parses Arabic text into a structured representation.
        This is a placeholder for a complex NLP parsing algorithm.
        It will attempt to match words to lexicon and apply grammar rules.
        """
        parsed_structure = {"tokens": [], "structure": None, "errors": []}
        words = text.split()  # Simple tokenization

        for i, word in enumerate(words):
            token_info = {"word": word, "lemma": None, "pos": None, "meaning": None}
            if word in self.lexicon:
                token_info["meaning"] = self.lexicon[word]
                # Simplified POS tagging based on lexicon entry structure
                if "noun" in self.lexicon[word].lower():
                    token_info["pos"] = "NOUN"
                elif "verb" in self.lexicon[word].lower():
                    token_info["pos"] = "VERB"
                elif "adjective" in self.lexicon[word].lower():
                    token_info["pos"] = "ADJ"
                else:
                    token_info["pos"] = "UNKNOWN"
            else:
                token_info["pos"] = "UNKNOWN"
                parsed_structure["errors"].append(f"Unknown word: {word}")
            parsed_structure["tokens"].append(token_info)

        # Placeholder for grammar-based structure analysis
        # In a real system, this would involve more sophisticated parsing
        # using self.grammar_rules to build a parse tree or similar.
        if len(parsed_structure["tokens"]) > 0:
            # Basic sentence structure attempt
            sentence_structure = []
            for token in parsed_structure["tokens"]:
                if token["pos"] in ["NOUN", "VERB", "ADJ"]:
                    sentence_structure.append(token["pos"])
            if sentence_structure:
                parsed_structure["structure"] = " ".join(sentence_structure)
        else:
            parsed_structure["structure"] = "EMPTY"

        return parsed_structure

    def generate_arabic_text(self, parsed_data: dict) -> str:
        """
        Generates Arabic text from a structured representation.
        This is a placeholder for a complex NLP generation algorithm.
        """
        generated_words = []
        if "tokens" in parsed_data:
            for token_info in parsed_data["tokens"]:
                word = token_info.get("word")
                if word:
                    generated_words.append(word)
                elif token_info.get("lemma"):
                    # Attempt to find a word for the lemma if no specific word is given
                    # This is a very simplified lookup
                    found_word = None
                    for lexicon_word, meaning in self.lexicon.items():
                        if token_info["lemma"] in lexicon_word and token_info["pos"] in meaning:
                            found_word = lexicon_word
                            break
                    if found_word:
                        generated_words.append(found_word)
                    else:
                        generated_words.append("[UNK]") # Unknown placeholder
                else:
                    generated_words.append("[UNK]")
        elif "structure" in parsed_data:
            # Attempt to generate based on structure, very rudimentary
            structure_parts = parsed_data["structure"].split()
            for part in structure_parts:
                found_word = None
                for lexicon_word, meaning in self.lexicon.items():
                    if part.upper() in meaning.upper():
                        found_word = lexicon_word
                        break
                if found_word:
                    generated_words.append(found_word)
                else:
                    generated_words.append("[UNK]")

        return " ".join(generated_words)

# --- Lobe 1: APK Structure Definition ---

class ApkStructureManager:
    """
    Manages the definition and templating of APK structures.
    """
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.apk_templates = self._load_apk_templates()

    def _load_apk_templates(self) -> dict:
        """Loads APK structural templates from files."""
        templates = {}
        for template_file in get_all_files_in_directory(self.templates_dir, ".tpl"):
            template_name = template_file.stem
            templates[template_name] = load_text_from_file(template_file)
        return templates

    def get_apk_template(self, template_name: str) -> str:
        """Retrieves a specific APK template."""
        return self.apk_templates.get(template_name, "")

    def generate_apk_manifest(self, app_name: str, permissions: list[str], activities: list[dict]) -> str:
        """
        Generates a basic AndroidManifest.xml content.
        This is a simplified representation.
        """
        manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.{app_name.lower().replace(' ', '')}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
"""
        for perm in permissions:
            manifest_content += f"        <uses-permission android:name=\"{perm}\" />\n"

        for activity in activities:
            manifest_content += f"""
        <activity android:name=".{activity.get('name', 'MainActivity')}"
                  android:exported="{activity.get('exported', 'true')}">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
"""
        manifest_content += """
    </application>
</manifest>
"""
        return manifest_content

    def generate_build_gradle(self, app_name: str, min_sdk: int = 21, target_sdk: int = 33, compile_sdk: int = 33) -> str:
        """
        Generates a basic app-level build.gradle content.
        """
        gradle_content = f"""
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    namespace 'com.example.{app_name.lower().replace(' ', '')}'
    compileSdk {compile_sdk}

    defaultConfig {{
        applicationId "com.example.{app_name.lower().replace(' ', '')}"
        minSdk {min_sdk}
        targetSdk {target_sdk}
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
    kotlinOptions {{
        jvmTarget = '1.8'
    }}
}}

dependencies {{

    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
        return gradle_content

# --- Lobe 2: Natural Language to APK Logic Mapper ---

class ArabicApkMapper:
    """
    Maps Arabic natural language descriptions to APK components and configurations.
    """
    def __init__(self, nlp_core: ArabicNlpCore, apk_manager: ApkStructureManager):
        self.nlp_core = nlp_core
        self.apk_manager = apk_manager
        self.knowledge_base_dir = KNOWLEDGE_BASE_DIR
        self.generated_apk_dir = Path("generated_apks")
        self.generated_apk_dir.mkdir(parents=True, exist_ok=True)

    def process_natural_language_request(self, nl_request: str, app_name: str) -> Path:
        """
        Processes a natural language request to generate an APK structure.

        Args:
            nl_request: The natural language description of the desired APK.
            app_name: The desired name for the application.

        Returns:
            The path to the generated APK project directory.
        """
        print(f"\n--- Processing Natural Language Request for '{app_name}' ---")
        parsed_request = self.nlp_core.parse_arabic_text(nl_request)
        print(f"Parsed request: {parsed_request}")

        # --- Mapping NLP output to APK components ---
        app_permissions = []
        app_activities = []
        template_choice = "basic_app" # Default template

        if "tokens" in parsed_request:
            for token_info in parsed_request["tokens"]:
                word = token_info["word"]
                pos = token_info["pos"]
                meaning = token_info["meaning"]

                # Example mapping logic:
                if pos == "NOUN" and "إنترنت" in meaning:
                    app_permissions.append("android.permission.INTERNET")
                if pos == "NOUN" and "موقع" in meaning:
                    app_permissions.append("android.permission.ACCESS_FINE_LOCATION")
                if pos == "VERB" and "عرض" in meaning:
                    # If "display" verb, assume it needs an activity
                    activity_name = "DisplayActivity" # Default for this verb
                    if "الشاشة" in nl_request: # More specific instruction
                        activity_name = "MainScreenActivity"
                    app_activities.append({"name": activity_name, "exported": "true"})
                if pos == "NOUN" and "واجهة" in meaning:
                     # Could map to a UI template or specific activity
                     pass
                if pos == "NOUN" and "قائمة" in meaning:
                    # Could map to a specific UI element or screen
                    pass
                if "تسجيل الدخول" in nl_request: # Keyword matching for specific features
                    app_activities.append({"name": "LoginActivity", "exported": "true"})
                    app_permissions.append("android.permission.ACCESS_NETWORK_STATE") # Often needed for login

            # If no activities were explicitly defined, add a default launcher activity
            if not app_activities:
                app_activities.append({"name": "MainActivity", "exported": "true"})

        # --- Create Project Structure ---
        project_dir = self.generated_apk_dir / app_name.replace(" ", "_")
        project_dir.mkdir(parents=True, exist_ok=True)

        # Create manifest
        manifest_content = self.apk_manager.generate_apk_manifest(app_name, app_permissions, app_activities)
        manifest_dir = project_dir / "app" / "src" / "main"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        save_text_to_file(manifest_dir / "AndroidManifest.xml", manifest_content)

        # Create build.gradle
        gradle_content = self.apk_manager.generate_build_gradle(app_name)
        save_text_to_file(project_dir / "build.gradle", gradle_content)
        # Also need to handle the app-level build.gradle if structure is more complex
        # For simplicity, this example creates a root build.gradle.
        # A more robust solution would create app/build.gradle and settings.gradle.

        # Placeholder for other files (res/values/strings.xml, res/layout/activity_main.xml, etc.)
        # These would be generated based on more detailed NLP instructions or templates.

        print(f"Generated APK project structure at: {project_dir}")
        return project_dir

# --- DEMO ---

def setup_mock_knowledge_base():
    """Sets up a mock knowledge base for demonstration."""
    print("--- Setting up Mock Knowledge Base ---")
    ensure_directory_exists(KNOWLEDGE_BASE_DIR)
    ensure_directory_exists(ARABIC_GRAMMAR_DIR)
    ensure_directory_exists(ARABIC_LEXICON_DIR)
    ensure_directory_exists(APK_TEMPLATES_DIR)

    # Mock Arabic Grammar Rules
    save_text_to_file(ARABIC_GRAMMAR_DIR / "sentence_structure.rul",
                      "VERB NOUN ADJECTIVE | NOUN VERB")
    save_text_to_file(ARABIC_GRAMMAR_DIR / "noun_phrase.rul",
                      "ARTICLE NOUN | ADJECTIVE NOUN")

    # Mock Arabic Lexicon Entries
    save_text_to_file(ARABIC_LEXICON_DIR / "تطبيق.lex",
                      "NOUN | software, application")
    save_text_to_file(ARABIC_LEXICON_DIR / "إنترنت.lex",
                      "NOUN | internet, network access")
    save_text_to_file(ARABIC_LEXICON_DIR / "عرض.lex",
                      "VERB | display, show")
    save_text_to_file(ARABIC_LEXICON_DIR / "مستخدم.lex",
                      "NOUN | user")
    save_text_to_file(ARABIC_LEXICON_DIR / "جديد.lex",
                      "ADJECTIVE | new")
    save_text_to_file(ARABIC_LEXICON_DIR / "الشاشة.lex",
                      "NOUN | screen, display")
    save_text_to_file(ARABIC_LEXICON_DIR / "موقع.lex",
                      "NOUN | location, site")
    save_text_to_file(ARABIC_LEXICON_DIR / "تسجيل.lex",
                      "NOUN | registration, login")
    save_text_to_file(ARABIC_LEXICON_DIR / "الدخول.lex",
                      "NOUN | entry, access (login)")


    # Mock APK Templates (minimal for demo)
    save_text_to_file(APK_TEMPLATES_DIR / "basic_app.tpl",
                      "This is a placeholder for a basic APK template.")

    print("Mock knowledge base setup complete.")

def cleanup_mock_knowledge_base():
    """Cleans up the mock knowledge base."""
    print("\n--- Cleaning up Mock Knowledge Base ---")
    if KNOWLEDGE_BASE_DIR.exists():
        shutil.rmtree(KNOWLEDGE_BASE_DIR)
    if Path("generated_apks").exists():
        shutil.rmtree(Path("generated_apks"))
    print("Mock knowledge base cleanup complete.")

def arabic_nlp_and_apk_module_demo():
    """Demonstrates the Arabic NLP and APK Generation module."""
    setup_mock_knowledge_base()

    # Initialize modules
    arabic_nlp = ArabicNlpCore(ARABIC_GRAMMAR_DIR, ARABIC_LEXICON_DIR)
    apk_manager = ApkStructureManager(APK_TEMPLATES_DIR)
    apk_mapper = ArabicApkMapper(arabic_nlp, apk_manager)

    # --- Test Case 1: Simple App with Internet Permission ---
    nl_request_1 = "إنشاء تطبيق بسيط يتصل بالإنترنت."
    app_name_1 = "InternetApp"
    apk_path_1 = apk_mapper.process_natural_language_request(nl_request_1, app_name_1)
    print(f"\nGenerated APK project for '{app_name_1}' at: {apk_path_1}")

    # --- Test Case 2: App with Location and Display Activity ---
    nl_request_2 = "أريد تطبيق يعرض الموقع للمستخدم."
    app_name_2 = "LocationDisplayApp"
    apk_path_2 = apk_mapper.process_natural_language_request(nl_request_2, app_name_2)
    print(f"\nGenerated APK project for '{app_name_2}' at: {apk_path_2}")

    # --- Test Case 3: App with Login functionality ---
    nl_request_3 = "بناء تطبيق لتسجيل الدخول."
    app_name_3 = "LoginApp"
    apk_path_3 = apk_mapper.process_natural_language_request(nl_request_3, app_name_3)
    print(f"\nGenerated APK project for '{app_name_3}' at: {apk_path_3}")

    cleanup_mock_knowledge_base()
    print("\n--- Arabic NLP and APK Generation Module Demo Finished ---")

if __name__ == "__main__":
    # This module's primary task is to define the functional Python code.
    # The demo execution will be handled by the orchestrator based on this definition.
    # However, for self-contained testing and clarity, a demo execution block is included.
    print("--- Defining Arabic NLP and APK Generation Module ---")
    # In a real system, this code would be imported and called.
    # For this submission, we are providing the raw code.
    pass # The actual execution will be managed externally.