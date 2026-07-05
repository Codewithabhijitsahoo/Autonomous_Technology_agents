import requests
import time
import json
from datetime import datetime

queries = [
    # Casual
    "Hello",
    "How are you?",
    "Tell me a joke",
    # Knowledge
    "What is Python?",
    "Explain Machine Learning.",
    "Difference between SQL and NoSQL.",
    # Medium
    "Latest AI models.",
    "Top AI startups this month.",
    "Recent Python releases.",
    # Deep
    "What are the latest AI models released in the past two weeks? Compare capabilities, context windows, pricing, benchmarks, market impact, enterprise adoption, GitHub activity, funding, competitors and future outlook."
]

url = "http://localhost:8000/api/chat"
headers = {"Content-Type": "application/json"}

results = []

print("Starting performance tests...")

for q in queries:
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Query: {q}")
    start = time.time()
    try:
        resp = requests.post(url, json={"query": q}, headers=headers)
        dur = time.time() - start
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"[{dur:.2f}s] Success. Response length: {len(data.get('response', ''))}")
            results.append({
                "query": q,
                "duration": dur,
                "status": "success",
                "length": len(data.get('response', ''))
            })
        else:
            print(f"[{dur:.2f}s] HTTP Error {resp.status_code}")
            results.append({
                "query": q,
                "duration": dur,
                "status": f"error_{resp.status_code}"
            })
    except Exception as e:
        dur = time.time() - start
        print(f"[{dur:.2f}s] Exception: {e}")
        results.append({
            "query": q,
            "duration": dur,
            "status": "exception"
        })

with open("perf_test_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nDone. Saved to perf_test_results.json")
