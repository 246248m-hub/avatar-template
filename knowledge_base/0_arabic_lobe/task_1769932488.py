import os
import shutil
import re

# Define paths relative to the current script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARABIC_KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, "arabic_knowledge_base")
GENERATED_LAYOUTS_DIR = os.path.join(BASE_DIR, "generated_layouts")
GENERATED_CODE_DIR = os.path.join(BASE_DIR, "generated_code")
ANDROID_PROJECT_TEMPLATE_DIR = os.path.join(BASE_DIR, "android_project_template")

class ArabicLayoutGenerator:
    """
    This lobe is responsible for generating Android XML layouts based on Arabic natural language descriptions.
    It will parse the description, identify UI elements and their properties, and construct the corresponding XML.
    """
    def __init__(self):
        self.element_mapping = {
            "زر": "Button",
            "نص": "TextView",
            "صورة": "ImageView",
            "حقل إدخال": "EditText",
            "قائمة": "ListView",
            "شبكة": "GridView",
            "مفتاح تبديل": "Switch",
            "شريط تمرير": "SeekBar",
            "شريط تقدم": "ProgressBar",
            "راديو": "RadioButton",
            "مربع اختيار": "CheckBox",
            "رأس": "Header",
            "أسفل": "Footer"
        }
        self.attribute_mapping = {
            "عرض": "android:layout_width",
            "ارتفاع": "android:layout_height",
            "ملء": "match_parent",
            "اعتمادا على المحتوى": "wrap_content",
            "نص": "android:text",
            "لون النص": "android:textColor",
            "حجم النص": "android:textSize",
            "معرف": "android:id",
            "هامش علوي": "android:marginTop",
            "هامش سفلي": "android:marginBottom",
            "هامش أيسر": "android:marginLeft",
            "هامش أيمن": "android:marginRight",
            "وسادة علوية": "android:paddingTop",
            "وسادة سفلية": "android:paddingBottom",
            "وسادة يسرى": "android:paddingLeft",
            "وسادة يمنى": "android:paddingRight",
            "محاذاة": "android:gravity",
            "مركز": "center",
            "يمين": "right",
            "وسط": "center_horizontal",
            "أسفل": "bottom",
            "تكبير": "scaleType",
            "احتواء": "fitCenter",
            "صورة": "android:src",
            "تلميح": "android:hint",
            "نص قابل للتحرير": "android:editable",
            "عرض دائما": "android:alwaysDrawnWithCache",
            "قابلة للتحديد": "android:focusable",
            "قابلة للنقر": "android:clickable"
        }
        self.valid_attributes = set(self.attribute_mapping.values())

    def parse_arabic_description(self, description: str) -> list:
        """
        Parses an Arabic description to extract UI elements and their properties.
        This is a simplified parser and can be significantly enhanced.
        """
        elements = []
        # Split description into potential element definitions
        potential_elements = re.split(r'\s*و\s*', description)

        for item in potential_elements:
            item = item.strip()
            if not item:
                continue

            element_type = None
            properties = {}

            # Attempt to identify element type
            for ar, en in self.element_mapping.items():
                if item.startswith(ar):
                    element_type = en
                    item = item[len(ar):].strip()
                    break

            if not element_type:
                continue # Skip if no known element type is found

            # Parse properties
            # This is a very basic regex for property extraction, needs improvement
            # e.g., "زر بنص 'حفظ' وبعرض ملء وبارتفاع اعتمادا على المحتوى"
            property_matches = re.findall(r'بـ(?:ـ(?:ـ ([\w\s]+))?)? \'([\w\s]+)\'|بـ([\w\s]+) ([\w\s]+)', item)

            for match in property_matches:
                if match[0] or match[1]: # Matched pattern like "بـ[property_name] '[property_value]'"
                    prop_name_ar = match[0].strip() if match[0] else match[1].strip()
                    prop_value_ar = match[2].strip() if match[2] else match[3].strip()
                elif match[2] or match[3]: # Matched pattern like "بـ[property_name] [property_value]"
                    prop_name_ar = match[2].strip()
                    prop_value_ar = match[3].strip()
                else:
                    continue

                if prop_name_ar in self.attribute_mapping:
                    attr_name_en = self.attribute_mapping[prop_name_ar]
                    prop_value_en = self.attribute_mapping.get(prop_value_ar, prop_value_ar)
                    properties[attr_name_en] = prop_value_en
                elif prop_name_ar.startswith("معرف"): # Special handling for ID
                    id_value = prop_value_ar.replace("'", "").strip()
                    if not id_value.startswith("@+id/"):
                        id_value = f"@+id/{id_value.lower().replace(' ', '_')}"
                    properties["android:id"] = id_value


            elements.append({"type": element_type, "properties": properties})

        return elements

    def generate_layout_xml(self, elements: list) -> str:
        """
        Generates Android XML layout string from parsed UI elements.
        """
        if not elements:
            return "<LinearLayout xmlns:android=\"http://schemas.android.com/apk/res/android\"\n    android:layout_width=\"match_parent\"\n    android:layout_height=\"match_parent\"\n    android:orientation=\"vertical\">\n    <!-- No elements defined -->\n</LinearLayout>"

        xml_lines = [
            "<LinearLayout xmlns:android=\"http://schemas.android.com/apk/res/android\"",
            "    android:layout_width=\"match_parent\"",
            "    android:layout_height=\"match_parent\"",
            "    android:orientation=\"vertical\">"
        ]

        for element in elements:
            element_type = element["type"]
            properties = element["properties"]

            # Start the element tag
            xml_lines.append(f"    <{element_type}")

            # Add properties
            for attr, value in properties.items():
                # Ensure value is properly quoted if it's a string and not a special attribute
                if isinstance(value, str) and not value.startswith("@") and not value in ["match_parent", "wrap_content", "center", "right", "center_horizontal", "bottom", "fitCenter"]:
                    if not (value.startswith("'") and value.endswith("'")):
                        value = f"'{value}'"
                xml_lines.append(f"        {attr}=\"{value}\"")

            # Close the element tag
            xml_lines.append("    />") # Assuming self-closing tags for simplicity

        xml_lines.append("</LinearLayout>")
        return "\n".join(xml_lines)

    def create_layout_file(self, filename: str, xml_content: str):
        """
        Saves the generated XML content to a file in the generated layouts directory.
        """
        if not os.path.exists(GENERATED_LAYOUTS_DIR):
            os.makedirs(GENERATED_LAYOUTS_DIR)
        filepath = os.path.join(GENERATED_LAYOUTS_DIR, f"{filename}.xml")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xml_content)
        print(f"Generated layout file: {filepath}")

    def process_arabic_prompt(self, prompt: str, layout_name: str = "generated_layout"):
        """
        Processes an Arabic natural language prompt to generate an Android layout file.
        """
        print(f"\n--- Processing Arabic prompt for layout: '{prompt}' ---")
        parsed_elements = self.parse_arabic_description(prompt)
        if not parsed_elements:
            print("No UI elements could be parsed from the prompt.")
            return None
        layout_xml = self.generate_layout_xml(parsed_elements)
        self.create_layout_file(layout_name, layout_xml)
        return layout_xml

def setup_arabic_layout_generation_module():
    """
    Initializes and demonstrates the ArabicLayoutGenerator.
    """
    print("\n--- Arabic Layout Generation Module Setup ---")
    arabic_generator = ArabicLayoutGenerator()

    # Example 1: Simple button
    prompt1 = "زر بنص 'حفظ'"
    arabic_generator.process_arabic_prompt(prompt1, "simple_button_layout")

    # Example 2: Text view with properties
    prompt2 = "نص بنص 'مرحبا بالعالم' وبحجم نص 24sp وبمعرف نص_ترحيب"
    arabic_generator.process_arabic_prompt(prompt2, "text_view_layout")

    # Example 3: Image view with dimensions and source
    prompt3 = "صورة بصورة '@drawable/my_image' وبعرض ملء وبارتفاع اعتمادا على المحتوى"
    arabic_generator.process_arabic_prompt(prompt3, "image_view_layout")

    # Example 4: Edit text with hint and ID
    prompt4 = "حقل إدخال بتلميح 'أدخل اسمك هنا' وبمعرف حقل_الاسم"
    arabic_generator.process_arabic_prompt(prompt4, "edit_text_layout")

    # Example 5: Combination of elements
    prompt5 = "نص بنص 'عنوان التطبيق' وبعرض ملء وبارتفاع اعتمادا على المحتوى ومعرف عنوان_رئيسي و زر بنص 'تسجيل الدخول' وبعرض ملء وبارتفاع اعتمادا على المحتوى ومعرف زر_دخول"
    arabic_generator.process_arabic_prompt(prompt5, "combined_layout")

    print("\n--- Arabic Layout Generation Module Demo Finished ---")

# Example of how this module would be called
if __name__ == "__main__":
    # This section is for demonstration purposes.
    # In a real execution flow, these would be orchestrated by other lobes.

    # Clean up previous runs if necessary
    if os.path.exists(GENERATED_LAYOUTS_DIR):
        shutil.rmtree(GENERATED_LAYOUTS_DIR)
        print(f"Removed existing directory: {GENERATED_LAYOUTS_DIR}")

    setup_arabic_layout_generation_module()

    # This module's output (generated XML files) would be consumed by Lobe 4 (code_generation_lobe)
    # and potentially Lobe 8 (apk_compiler_lobe).
    print("\n--- Next logical step: Lobe 4_code_generation_lobe would consume these layouts ---")