import os
import xml.etree.ElementTree as ET

# Assume these are defined elsewhere and accessible
KNOWLEDGE_BASE_DIR = "./knowledge_base"
ARABIC_LAYOUT_OUTPUT_DIR = "./arabic_layouts"

def setup_arabic_layout_generation_module():
    """
    Ensures the output directory for Arabic layouts exists.
    """
    if not os.path.exists(ARABIC_LAYOUT_OUTPUT_DIR):
        os.makedirs(ARABIC_LAYOUT_OUTPUT_DIR)
        print(f"Created directory for Arabic layouts: {ARABIC_LAYOUT_OUTPUT_DIR}")

def generate_arabic_layout(nl_description: str, output_filename: str):
    """
    Generates an Android XML layout file for an Arabic interface based on natural language description.
    This is a simplified representation. A real implementation would involve more sophisticated NLP
    to parse the description and map it to UI elements and their properties.

    Args:
        nl_description (str): Natural language description of the UI.
        output_filename (str): The name of the XML file to be generated.

    Returns:
        str: The absolute path to the generated XML file.
    """
    root = ET.Element("LinearLayout", xmlns_android="http://schemas.android.com/apk/res/android",
                      android_orientation="vertical", android_layout_width="match_parent",
                      android_layout_height="match_parent", android_layout_gravity="center")

    # Basic parsing of description to add elements (highly simplified)
    words = nl_description.lower().split()

    if "welcome" in words or "title" in words:
        title_text = "Welcome" if "welcome" in words else "App Title"
        title_view = ET.SubElement(root, "TextView", android_layout_width="wrap_content",
                                   android_layout_height="wrap_content",
                                   android_text=title_text,
                                   android_textSize="24sp",
                                   android_textStyle="bold",
                                   android_layout_gravity="center_horizontal",
                                   android_padding="16dp")

    if "button" in words:
        button_text = "Click Me"
        if "login" in words:
            button_text = "تسجيل الدخول" # Login in Arabic
        elif "submit" in words:
            button_text = "إرسال" # Submit in Arabic
        elif "next" in words:
            button_text = "التالي" # Next in Arabic

        button_view = ET.SubElement(root, "Button", android_layout_width="wrap_content",
                                    android_layout_height="wrap_content",
                                    android_text=button_text,
                                    android_layout_gravity="center_horizontal",
                                    android_layout_marginTop="20dp")

    if "input" in words or "text field" in words:
        hint_text = "Enter text"
        if "username" in words:
            hint_text = "اسم المستخدم" # Username in Arabic
        elif "password" in words:
            hint_text = "كلمة المرور" # Password in Arabic
        elif "email" in words:
            hint_text = "البريد الإلكتروني" # Email in Arabic

        input_view = ET.SubElement(root, "EditText", android_layout_width="match_parent",
                                   android_layout_height="wrap_content",
                                   android_hint=hint_text,
                                   android_layout_marginTop="16dp",
                                   android_padding="12dp",
                                   android_layout_marginStart="16dp",
                                   android_marginEnd="16dp",
                                   android_gravity="center_horizontal",
                                   android_inputType="text") # Default to text, could be parsed

    # Add a simple placeholder for an image if 'image' is mentioned
    if "image" in words:
        ET.SubElement(root, "ImageView", android_layout_width="200dp",
                      android_layout_height="200dp",
                      android_layout_gravity="center_horizontal",
                      android_layout_marginTop="20dp",
                      android_src="@drawable/placeholder_image") # Placeholder drawable

    tree = ET.ElementTree(root)
    output_path = os.path.join(ARABIC_LAYOUT_OUTPUT_DIR, f"{output_filename}.xml")
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"Generated Arabic layout XML: {output_path}")
    return os.path.abspath(output_path)

# --- Dummy Data for Demonstration ---
test_prompt_arabic_layout_1 = "Create a welcome screen with a title and a login button."
test_prompt_arabic_layout_2 = "A simple form with fields for username, password, and an email, followed by a submit button."
test_prompt_arabic_layout_3 = "A screen with an image and a next button."

def cleanup_dummy_files():
    """
    Removes dummy generated files.
    """
    if os.path.exists(ARABIC_LAYOUT_OUTPUT_DIR):
        for filename in os.listdir(ARABIC_LAYOUT_OUTPUT_DIR):
            file_path = os.path.join(ARABIC_LAYOUT_OUTPUT_DIR, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error removing file {file_path}: {e}")
        try:
            os.rmdir(ARABIC_LAYOUT_OUTPUT_DIR)
            print(f"Removed directory: {ARABIC_LAYOUT_OUTPUT_DIR}")
        except OSError as e:
            print(f"Error removing directory {ARABIC_LAYOUT_OUTPUT_DIR}: {e}")

# --- Arabic Layout Generation Lobe Demonstration ---
def arabic_layout_generation_lobe_demo():
    """
    Demonstrates the Arabic Layout Generation Lobe.
    """
    print("\n--- Initiating Arabic Layout Generation Lobe ---")
    setup_arabic_layout_generation_module()

    # Generate layouts based on Arabic natural language prompts
    layout_path_1 = generate_arabic_layout(test_prompt_arabic_layout_1, "welcome_screen_arabic")
    layout_path_2 = generate_arabic_layout(test_prompt_arabic_layout_2, "form_screen_arabic")
    layout_path_3 = generate_arabic_layout(test_prompt_arabic_layout_3, "image_screen_arabic")

    # This module's output (generated XML files) would be consumed by Lobe 4 (code_generation_lobe)
    # and potentially Lobe 8 (apk_compiler_lobe).
    print("\n--- Next logical step: Lobe 4_code_generation_lobe would consume these layouts ---")
    print(f"Generated Arabic Layouts: {[layout_path_1, layout_path_2, layout_path_3]}")

    # Clean up dummy files
    print("\n--- Cleaning up dummy files ---")
    cleanup_dummy_files()

    print("\n--- Arabic Layout Generation Lobe Demo Finished ---")

# Execute the demo
if __name__ == "__main__":
    arabic_layout_generation_lobe_demo()