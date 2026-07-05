import json
import re
from datetime import datetime

log_file = "logs/app.log"
try:
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except Exception as e:
    print(f"Error reading log file: {e}")
    lines = []

print(f"Total lines in log: {len(lines)}")

# Simple parsing
llm_calls = []
tools = []
nodes = []
errors = []
evidence_count = []

for line in lines:
    if "LLM Execution Log" in line:
        llm_calls.append(line.strip())
    elif "Tool completed:" in line:
        tools.append(line.strip())
    elif "Node execution started:" in line or "finished in" in line or "completed in" in line:
        nodes.append(line.strip())
    elif "error" in line.lower() or "failed" in line.lower():
        errors.append(line.strip())
    elif "Evidence Collector yielded" in line or "Evidence Count:" in line:
        evidence_count.append(line.strip())

with open("perf_summary.txt", "w", encoding='utf-8') as f:
    f.write(f"LLM Calls: {len(llm_calls)}\n")
    for call in llm_calls[-50:]:
        f.write(call + "\n")
    f.write(f"\nTools: {len(tools)}\n")
    for t in tools[-50:]:
        f.write(t + "\n")
    f.write(f"\nNodes: {len(nodes)}\n")
    for n in nodes[-50:]:
        f.write(n + "\n")
    f.write(f"\nEvidence: {len(evidence_count)}\n")
    for e in evidence_count[-50:]:
        f.write(e + "\n")
    f.write(f"\nErrors: {len(errors)}\n")
    for e in errors[-50:]:
        f.write(e + "\n")
        
print("Wrote perf_summary.txt")
