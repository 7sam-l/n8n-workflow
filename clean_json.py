import json

OUTPUT_FILE = "workflows.json"

with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

fixed_data = []
for wf in data:
    if isinstance(wf, str):
        try:
            wf = json.loads(wf)
        except Exception:
            continue
    fixed_data.append(wf)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(fixed_data, f, indent=2, ensure_ascii=False)

print(f"✅ Cleaned {OUTPUT_FILE}, total workflows: {len(fixed_data)}")
