import requests, json, base64, os, time, random

api_key = os.getenv("GOOGLE_API_KEY")
obj = os.getenv("OBJECTIVE")

# قراءة آخر جزء من الذاكرة لتوفير السياق
context = ""
if os.path.exists("knowledge_base"):
    files = sorted([f for f in os.listdir("knowledge_base") if f.startswith("task_")])
    for f in files[-3:]:
        with open(f"knowledge_base/{f}", "r") as c:
            context += c.read()[-1000:]

# الرابط الذهبي الخاص بك
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"

payload = {
    "contents": [{
        "parts": [{"text": f"You are an AI Architect. Objective: {obj}. Context: {context}. Write ONLY raw Python code. No markdown."}]
    }]
}

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G960F)"
}

for i in range(1, 6):
    print(f"🤖 Attempt {i}...")
    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        if "candidates" in data:
            code = data['candidates'][0]['content']['parts'][0]['text']
            clean_code = code.replace("```python", "").replace("```", "").strip()
            with open("current_task.py", "w") as f:
                f.write(clean_code)
            print("✅ Success!")
            exit(0)
        elif "error" in data and data["error"]["code"] == 429:
            wait = i * 40 # انتظار تصاعدي
            print(f"⚠️ Quota Hit. Sleeping {wait}s...")
            time.sleep(wait)
        else:
            print(f"❌ Error: {data}")
            time.sleep(10)
    except Exception as e:
        print(f"⚠️ Connection error: {e}")
        time.sleep(20)
exit(1)
