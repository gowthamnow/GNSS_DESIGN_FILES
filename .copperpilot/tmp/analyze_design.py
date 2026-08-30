import os
import re
import sys

def parse_erc():
    with open('.copperpilot/tmp/review-erc.rpt', 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    print("=== ERC REPORT SUMMARY ===")
    violations = re.findall(r'\[([^\]]+)\]:\s*([^\n]+)', text)
    v_counts = {}
    for v_type, v_msg in violations:
        v_counts[v_type] = v_counts.get(v_type, 0) + 1
    for k, v in sorted(v_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {k}: {v}")

    # Let's inspect some specific violations
    print("\n--- SAMPLE ERC VIOLATIONS (top 30 non-endpoint-off-grid) ---")
    count = 0
    for v_type, v_msg in violations:
        if "endpoint_off_grid" in v_type or "off_grid" in v_type:
            continue
        print(f"[{v_type}] {v_msg}")
        count += 1
        if count >= 30:
            break

def parse_drc():
    if not os.path.exists('.copperpilot/tmp/review-drc.rpt'):
        print("No DRC report found.")
        return
    with open('.copperpilot/tmp/review-drc.rpt', 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    print("\n=== DRC REPORT SUMMARY ===")
    violations = re.findall(r'\[([^\]]+)\]:\s*([^\n]+)', text)
    v_counts = {}
    for v_type, v_msg in violations:
        v_counts[v_type] = v_counts.get(v_type, 0) + 1
    for k, v in sorted(v_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {k}: {v}")

if __name__ == '__main__':
    parse_erc()
    parse_drc()
