# Check IR3883 calculations:
# Vout = Vref * (1 + Rtop/Rbot)
# IR3883 Vref = 0.5V (typical) or 0.6V? Let's check datasheet.
# In schematic:
# R11 (Rtop) = 16.5K, R12 (Rbot) = 2.94K
# If Vref = 0.5V: Vout = 0.5 * (1 + 16.5 / 2.94) = 0.5 * (1 + 5.612) = 0.5 * 6.612 = 3.306V! (Matches 3.3V!)
# R13 (PGOOD pullup) = 49.9K to +3.3V
# C18 (BOOT cap) = 0.1uF between SW and BOOT
# L1 = 2.2uH (ASPIAIG-F5030-2R2M-T)
# Output caps: C15 (22uF), C16 (22uF)
# Input caps: C19 (22uF), C20 (22uF), C21 (0.1uF)

# Check LT3045 calculations:
# Vout = Rset * 100uA
# In schematic: R14 = 33.2K, C24 = 0.47uF (SET capacitor)
# Vout = 33.2k * 100uA = 3.32V! (Matches 3.3V for +3V3_GNSS!)
# Input caps: C25 = 4.7uF
# Output caps: C26 = 10uF

# Check ADP150-3.3:
# Fixed 3.3V LDO
# Input caps: C23 = 10uF
# Output caps: C22 = 10uF

print("Calculated Vout for IR3883: 3.306V")
print("Calculated Vout for LT3045: 3.32V")
