import os
import shutil
import re

# Assume these constants are defined elsewhere
KNOWLEDGE_BASE_DIR = "./knowledge_base"
ANDROID_PROJECTS_DIR = "./android_projects"

def create_directory_if_not_exists(path):
    """Creates a directory if it doesn't already exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def clean_directory_contents(path):
    """Removes all files and subdirectories within a given directory."""
    if os.path.exists(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        print(f"Cleared contents of directory: {path}")

def extract_arabic_commands(text):
    """
    Extracts potential Arabic commands or intents from a given text.
    This is a simplified example and would need more sophisticated NLP for real-world use.
    """
    # This is a placeholder for actual Arabic NLP.
    # In a real scenario, this would involve tokenization,
    # morphological analysis, part-of-speech tagging, and intent recognition
    # for Arabic language.
    potential_commands = []
    # Simple keyword spotting for demonstration
    arabic_keywords = ["إنشاء", "تطبيق", "مشروع", "ملف", "قاعدة بيانات", "اسم"] # Create, application, project, file, database, name
    for keyword in arabic_keywords:
        if keyword in text:
            potential_commands.append(keyword)
    return list(set(potential_commands)) # Return unique commands

def process_arabic_instruction(instruction_text):
    """
    Parses an Arabic instruction to extract key parameters for APK generation.
    This function acts as a bridge between the Arabic NLP lobe and the code generation lobe.
    """
    extracted_commands = extract_arabic_commands(instruction_text)
    apk_parameters = {
        "app_name": None,
        "package_name": None,
        "project_type": None, # e.g., basic, with db, etc.
        "features": []
    }

    # Simplified parameter extraction based on keywords
    if "تطبيق" in extracted_commands or "مشروع" in extracted_commands:
        apk_parameters["project_type"] = "android_app"

    # Attempt to extract app name if present
    name_match = re.search(r"(اسم)?\s*التطبيق\s*هو\s*\"?(.*?)\"?", instruction_text)
    if name_match:
        apk_parameters["app_name"] = name_match.group(2).strip()
        # Generate a plausible package name if app name is found
        if apk_parameters["app_name"]:
            package_name_base = apk_parameters["app_name"].lower().replace(" ", "_")
            apk_parameters["package_name"] = f"com.example.{package_name_base}"

    # Add more sophisticated parsing for other parameters (e.g., database, specific UI elements)
    # based on Arabic keywords and grammatical structures.

    print(f"Parsed APK parameters from Arabic instruction: {apk_parameters}")
    return apk_parameters

def generate_android_project_structure(project_name, package_name):
    """
    Generates the basic directory structure for an Android project.
    This function is a precursor to actual code generation.
    """
    project_path = os.path.join(ANDROID_PROJECTS_DIR, project_name)
    create_directory_if_not_exists(project_path)

    app_module_path = os.path.join(project_path, "app")
    create_directory_if_not_exists(app_module_path)

    src_path = os.path.join(app_module_path, "src", "main")
    create_directory_if_not_exists(src_path)

    java_package_path = os.path.join(src_path, "java", *package_name.split('.'))
    create_directory_if_not_exists(java_package_path)

    resources_path = os.path.join(src_path, "res")
    create_directory_if_not_exists(resources_path)

    # Create basic placeholder files
    with open(os.path.join(project_path, "build.gradle"), "w") as f:
        f.write("// Top-level build file where you can add configuration options common to all sub-projects/modules.\n")
    with open(os.path.join(app_module_path, "build.gradle"), "w") as f:
        f.write(f"// Module-level build file for {project_name}\n")
    with open(os.path.join(src_path, "AndroidManifest.xml"), "w") as f:
        f.write(f"<manifest xmlns:android='http://schemas.android.com/apk/res/android' package='{package_name}'>\n    <application>\n    </application>\n</manifest>\n")

    print(f"Generated basic Android project structure at: {project_path}")
    return project_path

def create_dummy_android_project(app_name, package_name):
    """
    Creates a dummy Android project with basic structure.
    This is a placeholder for Lobe 4_code_generation_lobe's output.
    """
    print(f"\n--- Creating dummy Android project: '{app_name}' with package '{package_name}' ---")
    project_name = app_name.replace(" ", "_").lower()
    dummy_project_path = generate_android_project_structure(project_name, package_name)
    return dummy_project_path

def cleanup_dummy_files_and_dirs():
    """Cleans up dummy files and directories created during testing."""
    print("\n--- Cleaning up dummy files and directories ---")
    if os.path.exists(KNOWLEDGE_BASE_DIR):
        shutil.rmtree(KNOWLEDGE_BASE_DIR)
        print(f"Removed directory: {KNOWLEDGE_BASE_DIR}")
    if os.path.exists(ANDROID_PROJECTS_DIR):
        shutil.rmtree(ANDROID_PROJECTS_DIR)
        print(f"Removed directory: {ANDROID_PROJECTS_DIR}")
    print("Cleanup complete.")

if __name__ == '__main__':
    # --- Demo of Lobe 1_arabic_processing_lobe ---
    print("--- Arabic Processing Lobe Demo ---")
    arabic_instruction_1 = "أريد إنشاء تطبيق أندرويد جديد اسمه \"آلة حاسبة\"."
    apk_params_1 = process_arabic_instruction(arabic_instruction_1)

    arabic_instruction_2 = "أنشئ لي مشروع باسم \"مدير المهام\"."
    apk_params_2 = process_arabic_instruction(arabic_instruction_2)

    # --- Demo of integration with Lobe 4_code_generation_lobe (simulated) ---
    print("\n--- Simulating Lobe 4_code_generation_lobe interaction ---")

    # Scenario 1: Basic app
    app_name_1 = apk_params_1.get("app_name", "DefaultApp")
    package_name_1 = apk_params_1.get("package_name", "com.example.defaultapp")
    dummy_project_path_1 = create_dummy_android_project(app_name_1, package_name_1)

    # Scenario 2: Another app
    app_name_2 = apk_params_2.get("app_name", "TaskManager")
    package_name_2 = apk_params_2.get("package_name", "com.example.taskmanager")
    dummy_project_path_2 = create_dummy_android_project(app_name_2, package_name_2)

    print(f"\nDummy Android projects created at: {ANDROID_PROJECTS_DIR}")

    # --- Cleanup ---
    cleanup_dummy_files_and_dirs()
    print("\n--- Arabic Processing Lobe Demo Finished ---")