import requests, json, os, time, sys

def ask_gemini(prompt):
    api_key = os.getenv("GOOGLE_API_KEY")
    # نستخدم الرابط المستقر لضمان استمرارية العمل في غيابك
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    for i in range(3):
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=90)
            data = res.json()
            if res.status_code == 429:
                time.sleep(75); continue
            if "candidates" in data:
                text = data['candidates'][0]['content']['parts'][0]['text']
                return text.replace("```python", "").replace("```", "").strip()
        except:
            time.sleep(20)
    return None

# جمع سياق الخطأ والذاكرة
error_ctx = ""
if os.path.exists("error_log.txt"):
    with open("error_log.txt", "r") as f: error_ctx = f.read()[-500:]

last_mem = ""
if os.path.exists("knowledge_base"):
    files = sorted([f for f in os.listdir("knowledge_base")])
    if files:
        with open(os.path.join("knowledge_base", files[-1]), "r") as f:
            last_mem = f"// Context: {f.read()[-300:]}"

obj = os.getenv("OBJECTIVE")
prompt = f"Objective: {obj}\nErrors: {error_ctx}\nMemory: {last_mem}\nTask: Generate Python code. Respond ONLY with code."

code = ask_gemini(prompt)
if code and len(code) > 20:
    with open("current_thought.txt", "w") as f: f.write(code)
else:
    sys.exit(0)
