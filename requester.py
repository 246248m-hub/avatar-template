import requests, json, os, time

def ask_gemini(prompt):
    api_key = os.getenv("GOOGLE_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json", "User-Agent": "Phoenix-Architect/2.0"}
    for i in range(5):
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=60)
            data = res.json()
            if "candidates" in data:
                return data['candidates'][0]['content']['parts'][0]['text'].replace("```python", "").replace("```", "").strip()
            time.sleep(40 * (i+1))
        except:
            time.sleep(20)
    return None

# جلب سياق الأخطاء للإصلاح الذاتي
error_context = ""
if os.path.exists("error_log.txt"):
    with open("error_log.txt", "r") as f:
        error_context = f"\n⚠️ LAST FAILURE ERROR: {f.read()[-600:]}\nPlease fix this in the next iteration."

# جلب سياق الذاكرة من الفصوص
context = ""
if os.path.exists("knowledge_base"):
    for lobe in sorted(os.listdir("knowledge_base")):
        lobe_path = os.path.join("knowledge_base", lobe)
        if os.path.isdir(lobe_path):
            files = sorted([f for f in os.listdir(lobe_path) if f.startswith("task_")])
            if files:
                with open(os.path.join(lobe_path, files[-1]), "r") as c:
                    context += f"// Context from {lobe}: {c.read()[-400:]}\n"

obj = os.getenv("OBJECTIVE")
prompt = f"Grand Objective: {obj}. {error_context}\nBrain Context:\n{context}\nTask: Write the next self-contained Python script. Respond ONLY with raw code."

code = ask_gemini(prompt)
if code:
    with open("current_task.py", "w") as f: f.write(code)
    print("✅ Evolutionary Step Generated!")
else:
    exit(1)
