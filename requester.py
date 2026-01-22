import requests, json, os, time

def ask_gemini(prompt):
    api_key = os.getenv("GOOGLE_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    for i in range(5):
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=90)
            data = res.json()
            if "candidates" in data:
                raw_text = data['candidates'][0]['content']['parts'][0]['text']
                # تنظيف الكود من علامات الماركداون والزوائد
                clean_code = raw_text.replace("```python", "").replace("```", "").strip()
                return clean_code
            print(f"Attempt {i+1} failed: {data}")
            time.sleep(30)
        except Exception as e:
            print(f"Network error: {e}")
            time.sleep(20)
    return None

error_context = ""
if os.path.exists("error_log.txt"):
    with open("error_log.txt", "r") as f: error_context = f.read()[-800:]

memory = ""
if os.path.exists("knowledge_base"):
    for lobe in sorted(os.listdir("knowledge_base")):
        path = os.path.join("knowledge_base", lobe)
        if os.path.isdir(path):
            files = sorted([f for f in os.listdir(path) if f.startswith("task_")])
            if files:
                with open(os.path.join(path, files[-1]), "r") as c:
                    memory += f"// Memory from {lobe}: {c.read()[-250:]}\n"

obj = os.getenv("OBJECTIVE")
prompt = f"Objective: {obj}\nErrors: {error_context}\nMemory: {memory}\nTask: Generate next Python code. If env error, start with 'YML_REPAIR:' + executor.yml. Respond ONLY with raw code."

code = ask_gemini(prompt)
if code and len(code) > 20:
    with open("current_thought.txt", "w") as f: f.write(code)
else:
    exit(1)
