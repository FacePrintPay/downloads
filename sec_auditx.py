import json
import subprocess
from datetime import datetime

def scan_and_flag_deprecations():
    timestamp = datetime.utcnow().isoformat() + "Z"
    print(f"🔍 Running AutoDepAgent @ {timestamp}")

    # Run npm outdated and audit
    subprocess.run(["npm", "outdated"], check=False)
    subprocess.run(["npm", "audit"], check=False)

    print("📦 Checking for deprecated packages...")
    output = subprocess.check_output(["npm", "ls", "--json", "--depth=1"]).decode("utf-8")
    data = json.loads(output)

    flagged = []

    for pkg, info in data.get("dependencies", {}).items():
        if "deprecated" in info:
            flagged.append((pkg, info["version"], info.get("deprecated", "No reason provided")))

    if flagged:
        print("\n🚨 Deprecated packages found:")
        for name, ver, reason in flagged:
            print(f"  - {name}@{ver}: {reason}")
    else:
        print("✅ No deprecated packages detected.")

if __name__ == "__main__":
    scan_and_flag_deprecations()
