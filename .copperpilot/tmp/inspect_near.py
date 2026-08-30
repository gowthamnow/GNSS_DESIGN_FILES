def inspect_near(fname, target_x, target_y, radius=5.0):
    print(f"\n================ Inspecting {fname} near ({target_x}, {target_y}) ================")
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check all sexpr elements
    # lines with (at x y ...) or (pts (xy x y) ...)
    import re
    # find all (symbol ... (at x y ...))
    for m in re.finditer(r'\((symbol|wire|junction|no_connect|global_label|label|hierarchical_label|power_port|text)\b[^\)]*?\((?:at|pts)\s+([\s\S]*?)\)', content):
        elem_type = m.group(1)
        raw_pts = m.group(2)
        # extract xy
        pts = re.findall(r'\(xy\s+([\d\.-]+)\s+([\d\.-]+)\)', raw_pts)
        if not pts:
            # try (at x y ...)
            at_m = re.search(r'([\d\.-]+)\s+([\d\.-]+)', raw_pts)
            if at_m:
                pts = [(at_m.group(1), at_m.group(2))]
        for px, py in pts:
            px, py = float(px), float(py)
            if abs(px - target_x) <= radius and abs(py - target_y) <= radius:
                # get snippet
                start = max(0, m.start() - 50)
                end = min(len(content), m.end() + 50)
                print(f"Matched {elem_type} at ({px}, {py}):\n{content[m.start():m.end()]}\n")

inspect_near('Controller.kicad_sch', 264.16, 142.24, radius=3.0)
inspect_near('USB_HUB_sch.kicad_sch', 168.91, 63.5, radius=3.0)
