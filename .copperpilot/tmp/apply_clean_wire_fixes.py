import os
import re
import uuid

sch_path = os.path.abspath("ZED_Z9P.kicad_sch")
with open(sch_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update wire 39626359-22a8-4c9f-b3be-c40d12e8b284:
text = re.sub(r'\(wire\s+\(pts\s+\(xy\s+218\.44\s+82\.55\)\s+\(xy\s+218\.44\s+49\.53\)\)\s+\(stroke[^)]+\)\s+\(uuid\s+"39626359-22a8-4c9f-b3be-c40d12e8b284"\)\)',
              r'(wire (pts (xy 218.44 82.55) (xy 218.44 44.45)) (stroke (width 0) (type default)) (uuid "39626359-22a8-4c9f-b3be-c40d12e8b284"))', text)

# 2. Update wire 41fc751a-7b3b-4899-ad43-d8c760447fa0:
text = re.sub(r'\(wire\s+\(pts\s+\(xy\s+218\.44\s+49\.53\)\s+\(xy\s+236\.22\s+49\.53\)\)\s+\(stroke[^)]+\)\s+\(uuid\s+"41fc751a-7b3b-4899-ad43-d8c760447fa0"\)\)',
              r'(wire (pts (xy 218.44 44.45) (xy 236.22 44.45)) (stroke (width 0) (type default)) (uuid "41fc751a-7b3b-4899-ad43-d8c760447fa0"))', text)

# 3. Remove wire c568ae98-7ca8-4720-94e4-7497675f68b3 (the short from ANT_SHORT_N to R81/R82 tap):
text = re.sub(r'\(wire\s+\(pts\s+\(xy\s+217\.17\s+76\.2\)\s+\(xy\s+222\.25\s+76\.2\)\)\s+\(stroke[^)]+\)\s+\(uuid\s+"c568ae98-7ca8-4720-94e4-7497675f68b3"\)\)\n?', '', text)

# 4. Update wire d140eeb2-43bb-40cf-a734-d102e3a73c1c to connect U14.OC (217.17, 85.09) to ANT_SHORT_N (217.17, 96.52):
text = re.sub(r'\(wire\s+\(pts\s+\(xy\s+217\.17\s+76\.2\)\s+\(xy\s+217\.17\s+96\.52\)\)\s+\(stroke[^)]+\)\s+\(uuid\s+"d140eeb2-43bb-40cf-a734-d102e3a73c1c"\)\)',
              r'(wire (pts (xy 217.17 85.09) (xy 217.17 96.52)) (stroke (width 0) (type default)) (uuid "d140eeb2-43bb-40cf-a734-d102e3a73c1c"))', text)

# 5. Connect U13.6 V+ (250.19, 76.2) to +3V3_GNSS
# Add wire from (250.19, 76.2) to (247.65, 74.93) [which is R84.1 +3V3_GNSS tap] or (250.19, 76.2) -> (250.19, 74.93) -> (247.65, 74.93)
wire_u13_vcc1 = f'  (wire (pts (xy 250.19 76.2) (xy 250.19 74.93)) (stroke (width 0) (type default)) (uuid "{uuid.uuid4()}"))\n'
wire_u13_vcc2 = f'  (wire (pts (xy 250.19 74.93) (xy 247.65 74.93)) (stroke (width 0) (type default)) (uuid "{uuid.uuid4()}"))\n'
junction_u13_vcc = f'  (junction (at 247.65 74.93) (diameter 0) (color 0 0 0 0) (uuid "{uuid.uuid4()}"))\n'

idx = text.rfind(')')
text = text[:idx] + wire_u13_vcc1 + wire_u13_vcc2 + junction_u13_vcc + text[idx:]

with open(sch_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Applied all wire and connectivity fixes cleanly!")
