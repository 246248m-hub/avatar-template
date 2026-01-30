import os
import re

class ArabicSyntaxAnalyzer:
    """
    Analyzes Arabic text to identify grammatical structures relevant to APK generation.
    This is a simplified model for demonstration. A real implementation would involve
    complex NLP techniques.
    """

    def __init__(self):
        # Placeholder for a more sophisticated Arabic grammar model.
        # This could include POS tagging, dependency parsing, named entity recognition, etc.
        self.grammar_rules = {
            "action_verb": ["افتح", "أنشئ", "اعرض", "سجل", "ابحث", "أرسل", "تصفح", "قم بتشغيل", "احفظ", "حذف"],
            "noun_phrase": ["الشاشة", "صفحة", "البيانات", "ملف", "قائمة", "النص", "الصورة", "الزر", "المستخدم", "الإعدادات", "النتائج"],
            "preposition": ["في", "على", "إلى", "من", "مع", "بواسطة"],
            "adjective": ["جديد", "رئيسي", "تفصيلي", "متقدم", "بسيط", "شامل"],
            "identifier_pattern": r"([اسم|معرف|معرف_لـ])\s*:\s*['\"]?([\w\s]+)['\"]?",
            "attribute_pattern": r"([خاصية|سمة])\s*:\s*['\"]?([\w\s]+)['\"]?",
            "element_type_pattern": r"(نوع)\s*:\s*['\"]?([\w]+)['\"]?"
        }

    def analyze(self, text):
        """
        Analyzes Arabic text and extracts potential APK components.
        Returns a dictionary of identified components.
        """
        components = {
            "actions": [],
            "targets": [],
            "screens": [],
            "data_entities": [],
            "attributes": [],
            "element_types": [],
            "identifiers": []
        }

        words = re.findall(r'\b\w+\b', text.lower(), re.UNICODE)

        for i, word in enumerate(words):
            if word in self.grammar_rules["action_verb"]:
                components["actions"].append(word)

            if word in self.grammar_rules["noun_phrase"]:
                # Simple heuristic: If a noun phrase follows an action verb, it's likely a target.
                if i > 0 and words[i-1] in self.grammar_rules["action_verb"]:
                    components["targets"].append(word)
                if "شاشة" in word or "صفحة" in word:
                    components["screens"].append(word)
                components["data_entities"].append(word)

            if word in self.grammar_rules["adjective"]:
                # Simple heuristic: If an adjective precedes a noun phrase, it describes it.
                if i < len(words) - 1 and words[i+1] in self.grammar_rules["noun_phrase"]:
                    components["attributes"].append(f"{word} {words[i+1]}")

        # Analyze for specific patterns
        for match in re.finditer(self.grammar_rules["identifier_pattern"], text, re.UNICODE):
            components["identifiers"].append(match.group(2).strip())

        for match in re.finditer(self.grammar_rules["attribute_pattern"], text, re.UNICODE):
            components["attributes"].append(match.group(2).strip())

        for match in re.finditer(self.grammar_rules["element_type_pattern"], text, re.UNICODE):
            components["element_types"].append(match.group(2).strip())

        return components

class ArabicAPKStructureGenerator:
    """
    Generates a basic APK project structure based on analyzed Arabic components.
    This is a simplified representation. A real APK generator would need
    to map these components to actual code constructs (Activities, Layouts, etc.).
    """

    def __init__(self, base_path="./apk_projects"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def generate_structure(self, project_name, components):
        """
        Creates a directory structure for the APK project.
        """
        project_root = os.path.join(self.base_path, project_name.replace(" ", "_"))
        os.makedirs(project_root, exist_ok=True)

        # Create basic directories
        os.makedirs(os.path.join(project_root, "app"), exist_ok=True)
        os.makedirs(os.path.join(project_root, "app", "src"), exist_ok=True)
        os.makedirs(os.path.join(project_root, "app", "src", "main"), exist_ok=True)
        os.makedirs(os.path.join(project_root, "app", "src", "main", "java"), exist_ok=True)
        os.makedirs(os.path.join(project_root, "app", "src", "main", "res"), exist_ok=True)
        os.makedirs(os.path.join(project_root, "app", "src", "main", "res", "layout"), exist_ok=True)
        os.makedirs(os.path.join(project_root, "app", "src", "main", "res", "values"), exist_ok=True)

        # Placeholder for manifest file
        with open(os.path.join(project_root, "app", "src", "main", "AndroidManifest.xml"), "w", encoding="utf-8") as f:
            f.write(f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.{project_name.lower().replace(' ', '')}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{project_name.replace(' ', '')}">

        <!-- Main Activity -->
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <!-- Dynamically added activities/screens based on components -->
""")
            for screen in components.get("screens", []):
                activity_name = "".join(word.capitalize() for word in screen.split()) + "Activity"
                f.write(f'        <activity android:name=".{activity_name}" />\n')
            f.write("    </application>\n")
            f.write("</manifest>\n")

        # Placeholder for strings.xml
        with open(os.path.join(project_root, "app", "src", "main", "res", "values", "strings.xml"), "w", encoding="utf-8") as f:
            f.write(f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{project_name}</string>
    <!-- Dynamically added strings -->
""")
            for screen in components.get("screens", []):
                f.write(f'    <string name="{screen.lower().replace(" ", "_")}"> {screen} </string>\n')
            for identifier in components.get("identifiers", []):
                f.write(f'    <string name="{identifier.lower().replace(" ", "_")}"> {identifier} </string>\n')
            f.write("</resources>\n")

        # Placeholder for MainActivity.java
        main_activity_name = "MainActivity"
        java_package = f"com.example.{project_name.lower().replace(' ', '')}"
        os.makedirs(os.path.join(project_root, "app", "src", "main", "java", *java_package.split('.')))

        with open(os.path.join(project_root, "app", "src", "main", "java", *java_package.split('.'), f"{main_activity_name}.java"), "w", encoding="utf-8") as f:
            f.write(f"""package {java_package};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.content.Intent;
import android.view.View;
import android.widget.Button;

public class {main_activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Assumes a default activity_main.xml

        // Dynamically add buttons for navigation to other screens
""")
            for screen in components.get("screens", []):
                screen_variable_name = "".join(word.capitalize() for word in screen.split())
                button_id_name = f"btn_{screen.lower().replace(' ', '_')}"
                f.write(f"""
        Button {button_id_name} = findViewById(R.id.{button_id_name});
        if ({button_id_name} != null) {{
            {button_id_name}.setText("{screen}"); // Set button text
            {button_id_name}.setOnClickListener(new View.OnClickListener() {{
                @Override
                public void onClick(View v) {{
                    Intent intent = new Intent(MainActivity.this, {screen_variable_name}Activity.class);
                    startActivity(intent);
                }}
            }});
        }}
""")
            f.write("""
    }
}
""")

        # Placeholder for activity_main.xml
        with open(os.path.join(project_root, "app", "src", "main", "res", "layout", "activity_main.xml"), "w", encoding="utf-8") as f:
            f.write(f"""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp"
    tools:context=".{main_activity_name}">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/app_name"
        android:textSize="24sp"
        android:layout_gravity="center_horizontal"
        android:layout_marginBottom="24dp"/>

""")
            for screen in components.get("screens", []):
                button_id_name = f"btn_{screen.lower().replace(' ', '_')}"
                f.write(f'    <Button\n        android:id="@+id/{button_id_name}"\n        android:layout_width="match_parent"\n        android:layout_height="wrap_content"\n        android:text="{screen}"\n        android:layout_marginBottom="12dp"/>\n')
            f.write("""
</LinearLayout>
""")

        # Create placeholder activities for other screens
        for screen in components.get("screens", []):
            activity_name = "".join(word.capitalize() for word in screen.split()) + "Activity"
            layout_name = f"activity_{screen.lower().replace(' ', '_')}"
            with open(os.path.join(project_root, "app", "src", "main", "java", *java_package.split('.'), f"{activity_name}.java"), "w", encoding="utf-8") as f:
                f.write(f"""package {java_package};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class {activity_name} extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{layout_name}); // Assuming a layout for this screen
        setTitle("{screen}"); // Set the title of the activity
    }}
}}
""")
            # Create placeholder layout file for the new activity
            with open(os.path.join(project_root, "app", "src", "main", "res", "layout", f"{layout_name}.xml"), "w", encoding="utf-8") as f:
                f.write(f"""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp"
    tools:context=".{activity_name}">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/{screen.lower().replace(' ', '_')}"
        android:textSize="20sp"
        android:layout_gravity="center_horizontal"
        android:layout_marginBottom="16dp"/>

    <!-- Content for the {screen} screen will go here -->

</LinearLayout>
""")

        return {"project_root": project_root}

# --- Demo Usage ---

if __name__ == "__main__":
    print("--- Arabic Syntax Analyzer and APK Structure Generator Module Demo ---")

    analyzer = ArabicSyntaxAnalyzer()
    generator = ArabicAPKStructureGenerator()

    # Test Case 1: Simple app with navigation
    prompt_1 = "أنشئ تطبيق بسيط يعرض شاشة رئيسية وشاشة تفاصيل المستخدم.  اسم التطبيق: دليلي."
    print(f"\nAnalyzing prompt: '{prompt_1}'")
    components_1 = analyzer.analyze(prompt_1)
    print(f"Analyzed components: {components_1}")
    apk_info_1 = generator.generate_structure("دليلي", components_1)
    if apk_info_1:
        print(f"Generated APK structure for 'دليلي' at: {apk_info_1['project_root']}")
    else:
        print("Failed to generate APK structure for 'دليلي'.")

    # Test Case 2: App with data fetching and search
    prompt_2 = "أريد تطبيقًا لعرض قائمة بالمنتجات. يجب أن يحتوي على شاشة بحث عن المنتجات. اسم التطبيق: متجري."
    print(f"\nAnalyzing prompt: '{prompt_2}'")
    components_2 = analyzer.analyze(prompt_2)
    print(f"Analyzed components: {components_2}")
    apk_info_2 = generator.generate_structure("متجري", components_2)
    if apk_info_2:
        print(f"Generated APK structure for 'متجري' at: {apk_info_2['project_root']}")
    else:
        print("Failed to generate APK structure for 'متجري'.")

    # Test Case 3: More complex structure with specific identifiers and attributes
    prompt_3 = "قم ببناء تطبيق لإدارة المهام. يجب أن يتضمن شاشة المهام، وشاشة إضافة مهمة جديدة.  اسم التطبيق: منظّم أعمال.  مهمة لها اسم: 'قراءة الكتاب'، خاصية: 'عاجلة'."
    print(f"\nAnalyzing prompt: '{prompt_3}'")
    components_3 = analyzer.analyze(prompt_3)
    print(f"Analyzed components: {components_3}")
    apk_info_3 = generator.generate_structure("منظّم أعمال", components_3)
    if apk_info_3:
        print(f"Generated APK structure for 'منظّم أعمال' at: {apk_info_3['project_root']}")
    else:
        print("Failed to generate APK structure for 'منظّم أعمال'.")

    print("\n--- Arabic Syntax Analyzer and APK Structure Generator Module Demo Finished ---")