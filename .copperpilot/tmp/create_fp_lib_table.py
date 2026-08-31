import os, glob

# Scan all directories in GNSS_LIBRARY containing .kicad_mod files
mod_dirs = set()
for root, dirs, files in os.walk('GNSS_LIBRARY'):
    for f in files:
        if f.endswith('.kicad_mod'):
            mod_dirs.add(root.replace('\\', '/'))

print(f"Found {len(mod_dirs)} directories containing .kicad_mod:")
for d in sorted(mod_dirs):
    print("  ", d)

# Generate fp-lib-table
entries = []
# Standard footprint library names from schematic
# 1) Specific library folders
for d in sorted(mod_dirs):
    # Extract clean library nickname
    parts = d.split('/')
    if parts[-1] == 'footprints.pretty' or parts[-1] == 'KiCad':
        nick = parts[-2] if parts[-1] == 'footprints.pretty' else parts[-3] if len(parts) > 2 else parts[-1]
    else:
        nick = parts[-1]
    
    # Also handle specific prefixes like 1056, BLM21PG221SN1D, etc.
    entries.append(f'  (lib (name "{nick}")(type "KiCad")(uri "${{KIPRJMOD}}/{d}")(options "")(descr ""))')

# Add common aliases used in schematics:
aliases = {
    "GNSS": "GNSS_LIBRARY",
    "GNSS_Library": "GNSS_LIBRARY",
    "gnss1_Library": "GNSS_LIBRARY",
    "1056": "GNSS_LIBRARY/1056",
    "5033981892": "GNSS_LIBRARY/5033981892",
    "ASPIAIG-F5030-2R2M-T": "GNSS_LIBRARY/ASPIAIG-F5030-2R2M-T",
    "BLM21PG221SN1D": "GNSS_LIBRARY/BLM21PG221SN1D",
    "C0402C104K4RAC": "GNSS_LIBRARY/C0402C104K4RAC",
    "DP83825IRMQR": "GNSS_LIBRARY/DP83825IRMQR",
    "ECS-250-12-33-AGN-TR": "GNSS_LIBRARY/ECS-250-12-33-AGN-TR",
    "ESP32-C3-MINI-1-N4": "GNSS_LIBRARY/ESP32-C3-MINI-1-N4",
    "GRM033R71C103KE14D": "GNSS_LIBRARY/GRM033R71C103KE14D",
    "ICM-42688-P": "GNSS_LIBRARY/ICM-42688-P",
    "IR3883MTRPBF": "GNSS_LIBRARY/IR3883MTRPBF",
    "LD39200PU33R": "GNSS_LIBRARY/LD39200PU33R",
    "LQG15HS47NJ02D": "GNSS_LIBRARY/LQG15HS47NJ02D",
    "LT3045EDD_PBF": "GNSS_LIBRARY/LT3045EDD#PBF",
    "LT6000IDCB_TRMPBF": "GNSS_LIBRARY/LT6000IDCB#TRMPBF",
    "MMBT3904LT1G": "GNSS_LIBRARY/MMBT3904LT1G",
    "PESD0402-140": "GNSS_LIBRARY/PESD0402-140",
    "SMA-J-P-X-RA-TH1": "GNSS_LIBRARY/SAMTEC_SMA-J-P-X-RA-TH1",
    "TL3301EF100QG": "GNSS_LIBRARY/TL3301EF100QG",
    "TPS22946YZPR": "GNSS_LIBRARY/TPS22946YZPR",
    "WE-CBF_0603": "GNSS_LIBRARY/WE-CBF_0603",
}

for nick, relpath in aliases.items():
    entries.append(f'  (lib (name "{nick}")(type "KiCad")(uri "${{KIPRJMOD}}/{relpath}")(options "")(descr ""))')

# De-duplicate entries by name
unique_entries = {}
for e in entries:
    name_m = os.path.basename(e.split('"')[1])
    # key by lib name
    lib_name = e.split('"')[1]
    unique_entries[lib_name] = e

fp_lib_content = "(fp_lib_table\n  (version 7)\n" + "\n".join(unique_entries.values()) + "\n)\n"

with open('fp-lib-table', 'w', encoding='utf-8') as f:
    f.write(fp_lib_content)

print(f"\nCreated fp-lib-table with {len(unique_entries)} library entries.")
