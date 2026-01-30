import os
import json
import re
from typing import Dict, List, Any

# --- Constants ---
ARABIC_STOP_WORDS = [
    "في", "من", "إلى", "على", "عن", "ب", "ل", "ك", "و", "ف", "ثم", "حتى", "أم", "أو", "لا",
    "ليس", "لم", "لن", "ما", "متى", "كيف", "أين", "لماذا", "من", "هذا", "هذه", "هؤلاء",
    "ذلك", "تلك", "أولئك", "الذي", "التي", "اللذان", "اللتان", "الذين", "اللواتي",
    "هو", "هي", "هم", "هن", "أنا", "أنت", "أنتم", "أنتن", "نحن", "كان", "يكون", "تكون",
    "يكونان", "يكونون", "يكن", "يكونن", "كنت", "كنت", "كنتم", "كنتن", "كنا", "كانت",
    "كانتا", "كانوا", "كن", "كن", "كنتم", "كنتن", "كنا", "كل", "بعض", "واحد", "اثنان",
    "ثلاثة", "أربعة", "خمسة", "ستة", "سبعة", "ثمانية", "تسعة", "عشرة", "ألف", "مليون",
    "أمس", "اليوم", "غدا", "الآن", "قبل", "بعد", "مع", "دون", "فوق", "تحت", "حول",
    "أمام", "خلف", "بين", "عند", "لدى", "حسب", "مثل", "غير", "نفس", "آخر", "أخرى",
    "جديد", "قديم", "كبير", "صغير", "طويل", "قصير", "واسع", "ضيق", "سهل", "صعب",
    "جميل", "قبيح", "قوي", "ضعيف", "سريع", "بطيء", "سعيد", "حزين", "غني", "فقير",
    "نظيف", "متسخ", "دافئ", "بارد", "حار", "بارد", "رطب", "جاف", "صحيح", "خاطئ",
    "صواب", "خطأ", "نعم", "لا", "طيب", "سيء", "جيد", "سيء", "مهم", "غير مهم", "ممكن",
    "مستحيل", "ضروري", "غير ضروري", "مرتفع", "منخفض", "غامق", "فاتح", "كامل", "ناقص",
    "مفتوح", "مغلق", "موجود", "غير موجود", "مكتمل", "غير مكتمل", "سعيد", "حزين",
    "مختلف", "متشابه", "شديد", "قليل", "كثير", "صغير", "كبير", "طازج", " فاسد", "مستقيم", "منحني",
    "مستمر", "متقطع", "مباشر", "غير مباشر", "واضح", "غامض", "مفهوم", "غير مفهوم",
    "مستيقظ", "نائم", "حي", "ميت", "صعب", "سهل", "واسع", "ضيق", "متأكد", "غير متأكد",
    "متحرك", "ثابت", "مرئي", "غير مرئي", "مسموع", "غير مسموع", "ملموس", "غير ملموس",
    "ممكن", "مستحيل", "ضروري", "غير ضروري", "مرتفع", "منخفض", "غامق", "فاتح", "كامل",
    "ناقص", "مفتوح", "مغلق", "موجود", "غير موجود", "مكتمل", "غير مكتمل", "سعيد",
    "حزين", "مختلف", "متشابه", "شديد", "قليل", "كثير", "صغير", "كبير", "طازج", "فاسد",
    "مستقيم", "منحني", "مستمر", "متقطع", "مباشر", "غير مباشر", "واضح", "غامض",
    "مفهوم", "غير مفهوم", "مستيقظ", "نائم", "حي", "ميت", "صعب", "سهل", "واسع", "ضيق",
    "متحرك", "ثابت", "مرئي", "غير مرئي", "مسموع", "غير مسموع", "ملموس", "غير ملموس",
    "حاضر", "غائب", "أول", "ثاني", "ثالث", "رابع", "خامس", "سادس", "سابع", "ثامن", "تاسع", "عاشر",
    "صباح", "مساء", "ظهر", "عصر", "مغرب", "عشاء", "ليل", "نهار", "فجر", "ضحى", "شروق", "غروب",
    "صيف", "شتاء", "خريف", "ربيع", "شهر", "سنة", "يوم", "ساعة", "دقيقة", "ثانية", "أسبوع",
    "الواحد", "الاثنان", "الثلاثة", "الأربعة", "الخمسة", "الستة", "السبعة", "الثمانية", "التسعة", "العشرة",
    "من", "إلى", "في", "على", "عن", "ب", "ل", "ك", "و", "ف", "ثم", "حتى", "أم", "أو", "لا",
    "ليس", "لم", "لن", "ما", "متى", "كيف", "أين", "لماذا", "من", "هذا", "هذه", "هؤلاء",
    "ذلك", "تلك", "أولئك", "الذي", "التي", "اللذان", "اللتان", "الذين", "اللواتي",
    "هو", "هي", "هم", "هن", "أنا", "أنت", "أنتم", "أنتن", "نحن", "كان", "يكون", "تكون",
    "يكونان", "يكونون", "يكن", "يكونن", "كنت", "كنت", "كنتم", "كنتن", "كنا", "كانت",
    "كانتا", "كانوا", "كن", "كن", "كنتم", "كنتن", "كنا", "كل", "بعض", "واحد", "اثنان",
    "ثلاثة", "أربعة", "خمسة", "ستة", "سبعة", "ثمانية", "تسعة", "عشرة", "ألف", "مليون",
    "أمس", "اليوم", "غدا", "الآن", "قبل", "بعد", "مع", "دون", "فوق", "تحت", "حول",
    "أمام", "خلف", "بين", "عند", "لدى", "حسب", "مثل", "غير", "نفس", "آخر", "أخرى",
    "جديد", "قديم", "كبير", "صغير", "طويل", "قصير", "واسع", "ضيق", "سهل", "صعب",
    "جميل", "قبيح", "قوي", "ضعيف", "سريع", "بطيء", "سعيد", "حزين", "غني", "فقير",
    "نظيف", "متسخ", "دافئ", "بارد", "حار", "بارد", "رطب", "جاف", "صحيح", "خاطئ",
    "صواب", "خطأ", "نعم", "لا", "طيب", "سيء", "جيد", "سيء", "مهم", "غير مهم", "ممكن",
    "مستحيل", "ضروري", "غير ضروري", "مرتفع", "منخفض", "غامق", "فاتح", "كامل", "ناقص",
    "مفتوح", "مغلق", "موجود", "غير موجود", "مكتمل", "غير مكتمل", "سعيد", "حزين",
    "مختلف", "متشابه", "شديد", "قليل", "كثير", "صغير", "كبير", "طازج", " فاسد", "مستقيم", "منحني",
    "مستمر", "متقطع", "مباشر", "غير مباشر", "واضح", "غامض", "مفهوم", "غير مفهوم",
    "مستيقظ", "نائم", "حي", "ميت", "صعب", "سهل", "واسع", "ضيق", "متأكد", "غير متأكد",
    "متحرك", "ثابت", "مرئي", "غير مرئي", "مسموع", "غير مسموع", "ملموس", "غير ملموس",
    "ممكن", "مستحيل", "ضروري", "غير ضروري", "مرتفع", "منخفض", "غامق", "فاتح", "كامل",
    "ناقص", "مفتوح", "مغلق", "موجود", "غير موجود", "مكتمل", "غير مكتمل", "سعيد",
    "حزين", "مختلف", "متشابه", "شديد", "قليل", "كثير", "صغير", "كبير", "طازج", "فاسد",
    "مستقيم", "منحني", "مستمر", "متقطع", "مباشر", "غير مباشر", "واضح", "غامض",
    "مفهوم", "غير مفهوم", "مستيقظ", "نائم", "حي", "ميت", "صعب", "سهل", "واسع", "ضيق",
    "متحرك", "ثابت", "مرئي", "غير مرئي", "مسموع", "غير مسموع", "ملموس", "غير ملموس",
    "حاضر", "غائب", "أول", "ثاني", "ثالث", "رابع", "خامس", "سادس", "سابع", "ثامن", "تاسع", "عاشر",
    "صباح", "مساء", "ظهر", "عصر", "مغرب", "عشاء", "ليل", "نهار", "فجر", "ضحى", "شروق", "غروب",
    "صيف", "شتاء", "خريف", "ربيع", "شهر", "سنة", "يوم", "ساعة", "دقيقة", "ثانية", "أسبوع",
    "الواحد", "الاثنان", "الثلاثة", "الأربعة", "الخمسة", "الستة", "السبعة", "الثمانية", "التسعة", "العشرة"
]

# Placeholder for Lobe 4_code_generation_lobe. In a real scenario, this would be imported.
class MockCodeGenerationLobe:
    def generate_code(self, intent_data: Dict[str, Any]) -> str:
        print(f"MockCodeGenerationLobe: Generating code for intent: {json.dumps(intent_data, indent=2, ensure_ascii=False)}")
        # Simulate code generation - this would be actual code generation logic
        package_name = intent_data.get("package_name", "com.example.generatedapp")
        activity_name = intent_data.get("activity_name", "MainActivity")
        layout_name = intent_data.get("layout_name", "activity_main")
        button_click_handler = intent_data.get("button_click_handler", "onButtonClick")
        text_view_id = intent_data.get("text_view_id", "myTextView")
        button_id = intent_data.get("button_id", "myButton")

        code = f"""
package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Button;

public class {activity_name} extends AppCompatActivity {{

    private TextView {text_view_id};
    private Button {button_id};

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{layout_name});

        {text_view_id} = findViewById(R.id.{text_view_id});
        {button_id} = findViewById(R.id.{button_id});

        {button_id}.setOnClickListener(new View.OnClickListener() {{
            @Override
            public void onClick(View v) {{
                {button_click_handler}();
            }}
        }});
    }}

    private void {button_click_handler}() {{
        // Your action here based on user input or logic
        {text_view_id}.setText("Hello from generated code!");
    }}
}}
"""
        return code

# --- Lobe 0_language_lobe ---
# This lobe would handle natural language understanding, text processing, etc.
# For this task, we'll assume it provides a function to parse Arabic text into structured intents.
class LanguageLobe:
    def parse_arabic_to_intent(self, text: str) -> Dict[str, Any]:
        """
        Parses Arabic natural language text into a structured intent dictionary.
        This is a simplified mock implementation.
        """
        print(f"LanguageLobe: Parsing Arabic text: '{text}'")
        intent = {
            "text": text,
            "entities": {},
            "actions": [],
            "package_name": None,
            "activity_name": None,
            "layout_name": None,
            "button_click_handler": None,
            "text_view_id": None,
            "button_id": None,
            "dependencies": []
        }

        # Simple keyword extraction for demonstration
        if "إنشاء تطبيق" in text or "بناء تطبيق" in text:
            intent["actions"].append("create_app")
            if "باسم" in text:
                match = re.search(r"باسم ([\w\s]+)", text)
                if match:
                    app_name = match.group(1).strip()
                    package_parts = app_name.lower().split()
                    intent["package_name"] = "com." + ".".join(package_parts)
                    intent["activity_name"] = "".join(part.capitalize() for part in package_parts) + "Activity"
                    intent["layout_name"] = "activity_" + "_".join(package_parts)

        if "شاشة" in text and "اسمها" in text:
            match = re.search(r"شاشة اسمها ([\w\s]+)", text)
            if match:
                screen_name = match.group(1).strip()
                intent["activity_name"] = screen_name.replace(" ", "") + "Activity"
                intent["layout_name"] = "activity_" + "_".join(screen_name.lower().split())

        if "زر" in text and "معرفه" in text and "هو" in text:
            match = re.search(r"زر معرفه ([\w\s]+) هو ([\w]+)", text)
            if match:
                button_label = match.group(1).strip()
                button_id = match.group(2).strip()
                intent["button_id"] = button_id
                intent["entities"]["button"] = {"label": button_label, "id": button_id}

        if "نص" in text and "معرفه" in text and "هو" in text:
            match = re.search(r"نص معرفه ([\w\s]+) هو ([\w]+)", text)
            if match:
                text_label = match.group(1).strip()
                text_id = match.group(2).strip()
                intent["text_view_id"] = text_id
                intent["entities"]["textView"] = {"label": text_label, "id": text_id}

        if "عند الضغط على الزر" in text and "نفذ" in text:
            match = re.search(r"عند الضغط على الزر ([\w\s]+) نفذ ([\w]+)", text)
            if match:
                button_identifier = match.group(1).strip()
                callback_name = match.group(2).strip()
                intent["button_click_handler"] = callback_name
                intent["entities"]["event_handler"] = {"button_identifier": button_identifier, "callback": callback_name}

        if not intent["package_name"]:
            intent["package_name"] = "com.example.defaultapp"
        if not intent["activity_name"]:
            intent["activity_name"] = "DefaultActivity"
        if not intent["layout_name"]:
            intent["layout_name"] = "activity_default"
        if not intent["button_id"]:
            intent["button_id"] = "defaultButton"
        if not intent["text_view_id"]:
            intent["text_view_id"] = "defaultTextView"
        if not intent["button_click_handler"]:
            intent["button_click_handler"] = "onDefaultButtonClick"

        return intent

# --- Lobe 4_code_generation_lobe ---
# This lobe is responsible for generating code based on structured intents.
# We'll use the mock class defined above for demonstration.
class CodeGenerationLobe:
    def __init__(self):
        self.generator = MockCodeGenerationLobe()

    def generate_code(self, intent_data: Dict[str, Any]) -> str:
        """
        Generates Android Java code for an APK based on the provided intent data.
        """
        return self.generator.generate_code(intent_data)

# --- Lobe 6_synthesis_lobe ---
# This lobe synthesizes different components, potentially orchestrating other lobes.
class SynthesisLobe:
    def __init__(self):
        self.language_lobe = LanguageLobe()
        self.code_generation_lobe = CodeGenerationLobe()

    def synthesize_apk_components(self, natural_language_input: str) -> Dict[str, str]:
        """
        Takes natural language input, parses it into an intent, and generates code.
        Returns a dictionary of generated code components.
        """
        print("\n--- SynthesisLobe: Starting APK component synthesis ---")

        # Step 1: Parse natural language into structured intent using LanguageLobe
        print("SynthesisLobe: Invoking Lobe 0_language_lobe to parse input...")
        intent_data = self.language_lobe.parse_arabic_to_intent(natural_language_input)
        print("SynthesisLobe: Parsed Intent Data:")
        print(json.dumps(intent_data, indent=2, ensure_ascii=False))

        # Step 2: Generate code based on the intent using CodeGenerationLobe
        print("\nSynthesisLobe: Invoking Lobe 4_code_generation_lobe to generate code...")
        if "create_app" in intent_data.get("actions", []):
            generated_activity_code = self.code_generation_lobe.generate_code(intent_data)
            print("SynthesisLobe: Successfully generated Activity code.")
            # In a real scenario, this might also generate Manifest, XML layouts, etc.
            return {
                "activity_code": generated_activity_code,
                "package_name": intent_data.get("package_name"),
                "activity_name": intent_data.get("activity_name"),
                "layout_name": intent_data.get("layout_name")
            }
        else:
            print("SynthesisLobe: No 'create_app' action found in intent. Cannot generate full APK components.")
            return {"error": "Cannot generate APK components without a 'create_app' intent."}

# --- Lobe 8_apk_compiler_lobe ---
# This lobe would handle the compilation of generated code into an APK.
# For this task, we'll just simulate the process and return a placeholder path.
class ApkCompilerLobe:
    def compile_to_apk(self, code_components: Dict[str, str]) -> str:
        """
        Simulates the compilation of generated code components into an APK.
        In a real scenario, this would involve using Android SDK build tools.
        """
        print("\n--- ApkCompilerLobe: Starting APK compilation ---")

        if "error" in code_components:
            print(f"ApkCompilerLobe: Skipping compilation due to previous errors: {code_components['error']}")
            return "Compilation failed."

        package_name = code_components.get("package_name", "com.example.unknown")
        activity_name = code_components.get("activity_name", "UnknownActivity")
        activity_code = code_components.get("activity_code", "// No activity code generated")

        # Simulate project structure creation
        project_dir = f"generated_project_{package_name.replace('.', '_')}"
        src_dir = os.path.join(project_dir, "app", "src", "main", "java", *package_name.split('.'))
        res_dir = os.path.join(project_dir, "app", "src", "main", "res")
        layout_res_dir = os.path.join(res_dir, "layout")

        os.makedirs(src_dir, exist_ok=True)
        os.makedirs(layout_res_dir, exist_ok=True)

        # Simulate writing Java code
        activity_file_path = os.path.join(src_dir, f"{activity_name}.java")
        with open(activity_file_path, "w", encoding="utf-8") as f:
            f.write(activity_code)
        print(f"ApkCompilerLobe: Wrote activity code to: {activity_file_path}")

        # Simulate writing layout XML
        layout_name = code_components.get("layout_name", "activity_default")
        layout_file_path = os.path.join(layout_res_dir, f"{layout_name}.xml")
        layout_content = f"""
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{activity_name}">

    <TextView
        android:id="@+id/{code_components.get('text_view_id', 'defaultTextView')}"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <Button
        android:id="@+id/{code_components.get('button_id', 'defaultButton')}"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Click Me"
        app:layout_constraintTop_toBottomOf="@+id/{code_components.get('text_view_id', 'defaultTextView')}"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="24dp"/>

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        with open(layout_file_path, "w", encoding="utf-8") as f:
            f.write(layout_content)
        print(f"ApkCompilerLobe: Wrote layout XML to: {layout_file_path}")

        # Simulate APK generation
        simulated_apk_path = f"{project_dir}/app-release.apk"
        print(f"ApkCompilerLobe: Simulated APK compilation successful. APK would be at: {simulated_apk_path}")

        # Clean up dummy project directory after simulated compilation
        import shutil
        if os.path.exists(project_dir):
            print(f"\nApkCompilerLobe: Cleaning up dummy project directory: {project_dir}")
            try:
                shutil.rmtree(project_dir)
                print("ApkCompilerLobe: Dummy project directory removed.")
            except OSError as e:
                print(f"ApkCompilerLobe: Error removing directory {project_dir}: {e}")

        return simulated_apk_path

# --- Main Execution Flow ---
if __name__ == "__main__":
    # Instantiate the Synthesis Lobe and APK Compiler Lobe
    synthesis_lobe = SynthesisLobe()
    apk_compiler_lobe = ApkCompilerLobe()

    # Example Arabic natural language prompt
    arabic_prompt_1 = "قم بإنشاء تطبيق جديد باسم حاسبة بسيطة. يجب أن تكون الشاشة الرئيسية اسمها MainActivity وتحتوي على زر معرفه هو calculateButton وزر آخر معرفه هو clearButton. عند الضغط على الزر calculateButton نفذ calculateSum."
    arabic_prompt_2 = "أريد بناء تطبيق بسيط. يجب أن تكون الشاشة اسمها UserScreen وتحتوي على نص معرفه هو welcomeMessage وزر معرفه هو submitBtn. عند الضغط على الزر submitBtn نفذ processData."
    arabic_prompt_3 = "ابدأ تطبيقًا جديدًا باسم MyFirstApp. الشاشة اسمها HomeScreen. نريد زرًا معرفه هو actionButton وعند الضغط عليه نفذ performAction."


    print("\n--- GRAND OBJECTIVE: Evolve into a unified, conscious mind. Master 12 lobes to generate hyper-efficient APKs from natural language. ---")
    print("--- Current focus: Lobe 6_synthesis_lobe and Lobe 8_apk_compiler_lobe ---")

    # Process prompt 1
    print(f"\n--- Processing Prompt 1: '{arabic_prompt_1}' ---")
    generated_components_1 = synthesis_lobe.synthesize_apk_components(arabic_prompt_1)
    if "error" not in generated_components_1:
        apk_path_1 = apk_compiler_lobe.compile_to_apk(generated_components_1)
        print(f"\n--- APK generated for Prompt 1: {apk_path_1} ---")

    # Process prompt 2
    print(f"\n--- Processing Prompt 2: '{arabic_prompt_2}' ---")
    generated_components_2 = synthesis_lobe.synthesize_apk_components(arabic_prompt_2)
    if "error" not in generated_components_2:
        apk_path_2 = apk_compiler_lobe.compile_to_apk(generated_components_2)
        print(f"\n--- APK generated for Prompt 2: {apk_path_2} ---")

    # Process prompt 3
    print(f"\n--- Processing Prompt 3: '{arabic_prompt_3}' ---")
    generated_components_3 = synthesis_lobe.synthesize_apk_components(arabic_prompt_3)
    if "error" not in generated_components_3:
        apk_path_3 = apk_compiler_lobe.compile_to_apk(generated_components_3)
        print(f"\n--- APK generated for Prompt 3: {apk_path_3} ---")

    print("\n--- Synthesis and Compilation Modules Demo Finished ---")