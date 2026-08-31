# KiCad 8.0 Design Review & Verification Report

**Date:** March 2025  
**Toolchain:** KiCad 8.0 CLI (`kicad-cli` 8.0.0)  
**Project:** GNSS Receiver & Multi-Interface Controller Board  
**Target Module:** u-blox ZED-F9P-05B High-Precision GNSS Module with Active Antenna Supervisor

---

## Executive Summary

A comprehensive post-correction design review was performed using KiCad 8.0 on all schematic sheets (`GNSS.kicad_sch`, `ZED_Z9P.kicad_sch`, `Controller.kicad_sch`, `Ethernet.kicad_sch`, `USB_HUB_sch.kicad_sch`, `Power_sch.kicad_sch`, `Arduino.kicad_sch`, `ESP.kicad_sch`, `IMU.kicad_sch`).

Several critical issues from the initial review were successfully resolved by the user, including the global ground short to `USB_SCL`, the disconnected USB hub power rail, STM32 `VSSA` analog ground connection, DP83825 thermal ground pad, and the Ethernet crystal capacitor value.

However, an exhaustive deep-dive analysis of the **Antenna Subsystem (`ZED_Z9P.kicad_sch`)** revealed **three critical hardware bugs** that will completely disable active antenna power delivery, break open-circuit detection, and subject digital pins to invalid intermediate voltages. Additional major issues remain in the **Power UVLO divider**, **Arduino SWD conflict**, and **MCU clock damping**.

---

## 1. Verified User Corrections (Done Well)

| Item | Subsystem | Status | Description |
|---|---|---|---|
| **C1** | Global Ground | **RESOLVED** | Ground net is now a proper 257-node `GND` network; `USB_SCL` is isolated to a 4-node I2C bus (`IC1.24`, `IC3.59`, `R8.1`, `R87.2`). |
| **C2** | `USB_HUB_sch` | **RESOLVED** | Net `+3.3V_HUB` is now powered through ferrite bead `FL10.2` and feeds all `IC1` VDD33/VDDA33 power pins and decoupling capacitors. |
| **C3** | `Controller_sch` | **RESOLVED** | STM32H563 `IC3` Pin 19 (`VSSA`) and Pin 20 (`VREF-`) are now tied directly to the system `GND` plane. |
| **C4** | `Ethernet_sch` | **RESOLVED** | Ethernet crystal capacitor `C27` was corrected from `27uF` to `27pF`. |
| **C5** | `Ethernet_sch` | **RESOLVED** | `ETH_REFCLK` is now isolated between PHY `U4.2` and MCU `IC3.24`; RJ45 LED loading removed. |
| **C6** | `Ethernet_sch` | **RESOLVED** | DP83825 `U4` thermal pad pins 25–30 (`EXP`) are tied to `GND`. |
| **C8** | `Controller_sch` | **RESOLVED** | STM32 GPIO contention eliminated: `ETH_RST_N` is driven solely by `IC3.38` (`PE7`). |
| **M3** | `ESP_sch` | **RESOLVED** | 1 µF capacitor `C81` added to `ESP_EN` to ensure reliable power-on RC reset timing. |
| **M5** | `ZED_Z9P_sch` | **RESOLVED** | Net `/ZED_Z9P/ANT_OFF` is now properly connected to `IC2.5` (`ANT_OFF_`), `Q1.5`, and `Q2.1`. |

---

## 2. In-Depth Antenna & RF Front-End Analysis (`ZED_Z9P.kicad_sch`)

The active antenna supervisor circuit was analyzed against the u-blox ZED-F9P Integration Manual (UBX-18010802), Texas Instruments TPS22946 datasheet, Linear Technology LT6000 datasheet, and Vishay Si1016CX dual MOSFET datasheet.

### Critical Findings in Antenna Circuitry

```
[VCC_RF (3.3V)] ---> [U14 TPS22946 Load Switch] ---> (VOUT)
                                                           |
                      [Q1 SI1016CX Dual FET] <-------------+ (Connected to Pin 4: WRONG PIN!)
                           (Symbol Pinout Scrambled: Physical Gate Pin 6 Floating!)
                                   | (DEAD PATH - NO POWER OUTPUT)
                                   v
                             [R32 (10Ω)] ---> [L3 (47nH)] ---> [RF_IN / J4 SMA]
                                   |
                +------------------+------------------+
                |                                     |
       [U13 LT6000 (-IN)]                    [U13 LT6000 (+IN)]
        (V = 3.15V @ 15mA)                    (V = 1.65V from R81/R82 Divider)
                |                                     |
                +---------> [U13 Output] <------------+
                            (V_out = 0V ALWAYS: Antenna Open Detect Permanently Stuck LOW)
```

### Detailed Antenna Fault Breakdown:

#### 1. CRITICAL: `Q1` (Si1016CX) Dual MOSFET Symbol Pin Mismatch Disconnects Active Antenna Power
- **Root Cause**: The library symbol `GNSS_LIBRARY/LIB_SI1016CX-T1-GE3/SI1016CX-T1-GE3/KiCad/SI1016CX-T1-GE3.kicad_sym` defines:
  - Symbol Pin 4 = `S2`, Pin 5 = `G2`, Pin 6 = `D1`.
- **Physical Part Pinout** (Vishay Si1016CX SC-89-6 / SOT-563 package):
  - Pin 1 = `S1` (N-MOSFET Source)
  - Pin 2 = `G1` (N-MOSFET Gate)
  - Pin 3 = `D2` (P-MOSFET Drain)
  - **Pin 4 = `D1` (N-MOSFET Drain)**
  - **Pin 5 = `S2` (P-MOSFET Source)**
  - **Pin 6 = `G2` (P-MOSFET Gate)**
- **Hardware Failure**:
  - `U14.VOUT` (3.3V) connects to **Pin 4** (the internal Drain of the unused N-channel FET, whose Source is floating).
  - Net `ANT_OFF` connects to **Pin 5** (the Source of the P-channel FET).
  - Physical **Pin 6** (the actual Gate of the P-channel FET) is completely **unconnected / floating**.
  - **Result**: The P-channel MOSFET can never turn on. **0V** is delivered to the active antenna on `J4`.
- **Fix**: Update the library symbol pinout to match the Vishay datasheet: Pin 4 = D1, Pin 5 = S2, Pin 6 = G2; rewire `U14.VOUT` to Pin 5 (`S2`), `ANT_OFF` to Pin 6 (`G2`), and `R32` to Pin 3 (`D2`).

#### 2. CRITICAL: `U13` (LT6000) Antenna Detect Comparator Reference Threshold is Mathematically Impossible
- **Root Cause**: Resistors $R81 = 10\text{ k}\Omega$ and $R82 = 10\text{ k}\Omega$ divide the supply voltage down to $V_{+IN} = 1.65\text{V}$.
  - The inverting input `U13.2` (`-IN`) measures the voltage after current sense resistor $R32 = 10\,\Omega$.
  - When an active antenna is drawing nominal current ($15\text{ mA}$):
    $$V_{-IN} = 3.3\text{V} - (0.015\text{ A} \times 10\,\Omega) = 3.15\text{V}$$
  - Since $V_{+IN} (1.65\text{V}) < V_{-IN} (3.15\text{V})$, the comparator output `U13.4` (`OUT` -> `ANT_DETECT`) is **LOW (0V)**.
  - To trip the comparator HIGH ($V_{+IN} > V_{-IN}$), the antenna current must exceed:
    $$I_{\text{trip}} = \frac{3.3\text{V} - 1.65\text{V}}{10\,\Omega} = 165\text{ mA}$$
    This exceeds the TPS22946 max current limit ($155\text{ mA}$) and is $10\times$ higher than any standard GNSS active antenna.
- **Hardware Failure**: The receiver will permanently report **"Antenna Open / Not Connected"** under all operating conditions.
- **Fix**: Re-dimension the high-side voltage divider to create a $30\text{–}50\text{ mV}$ drop below supply: set $R81 = 100\,\Omega$ (or $1\text{ k}\Omega$) and $R82 = 10\text{ k}\Omega$ (or $68\text{ k}\Omega$).

#### 3. CRITICAL: `ANT_SHORT_N` Pin (IC2 Pin 6) Biased into Indeterminate CMOS Logic State
- **Root Cause**: `IC2.6` (`ANT_SHORT_N`) is an active-low CMOS digital input on the ZED-F9P. It is hardwired to `/ZED_Z9P/ANT_SHORT_N` at the center tap of the $10\text{k}\Omega / 10\text{k}\Omega$ divider, holding it at $1.65\text{V}$.
- **Hardware Failure**: For 3.3V CMOS logic ($V_{IL} \le 0.66\text{V}$, $V_{IH} \ge 2.31\text{V}$), $1.65\text{V}$ is in the forbidden linear transition zone, causing shoot-through current in the input buffer and erratic false-positive short-circuit alarms.
- **Fix**: Disconnect `IC2.6` from the analog comparator threshold divider; connect `IC2.6` to `ANT_FAULT` (from `U14.OC`) with a 10 kΩ pull-up to `RF_VCC`.

---

## 3. Prioritized Actionable Fix List Across All Sheets

### Critical Severity (Must Fix Before PCB Fabrication)

| Ref | Sheet | Issue Description | Corrective Action |
|---|---|---|---|
| **C-A1** | `ZED_Z9P` | **`Q1` Si1016CX Symbol Pin Scrambling**: Pins 4, 5, 6 in symbol library do not match physical SOT-563 package, leaving P-FET gate floating and antenna unpowered. | Correct symbol pins: Pin 4 = D1, Pin 5 = S2, Pin 6 = G2. Wire `U14.VOUT` -> Pin 5, `ANT_OFF` -> Pin 6, `R32` -> Pin 3. |
| **C-A2** | `ZED_Z9P` | **`U13` LT6000 Open-Circuit Threshold Broken ($V_{\text{ref}} = 1.65\text{V}$)**: Requires 165 mA current draw to trigger open-circuit detect. | Change $R81 = 100\,\Omega$ and $R82 = 10\text{ k}\Omega$ to set $V_{+IN} \approx 3.27\text{V}$ (detects $I > 3\text{ mA}$). |
| **C-A3** | `ZED_Z9P` | **`ANT_SHORT_N` (Pin 6) Biased to 1.65V**: Undefined CMOS digital voltage causes false short detections. | Disconnect `IC2.6` from divider; tie to `U14.OC` (`ANT_FAULT`) or pull-up to `RF_VCC`. |

### Major Severity (Significant Functional & Debugging Risks)

| Ref | Sheet | Issue Description | Corrective Action |
|---|---|---|---|
| **M1** | `Arduino` | **Arduino D2/D3 Hardwired to STM32 SWD Lines**: `A1` pins 17 (`D2`) and 18 (`D3`) connect to `SWCLK`/`SWDIO`, causing attached Arduino shields to crash JTAG/SWD debugging. | Disconnect `A1` 17/18 from SWD; reassign to spare GPIOs (`PA0`, `PA8`, `PC6`, `PD2`). |
| **M2** | `Power_sch` | **Buck Regulator UVLO Divider Shorted**: Both pins of `R46` connect to 5V; `U7.EN` is tied to 5V; `R47` drains power to GND without setting UVLO. | Connect 5V -> `R46.1`; `R46.2` to `U7.5` (`EN`) and `R47.2`; `R47.1` to GND (sets 3.9V UVLO threshold). |
| **M3** | `Controller` | **Excessive Series Resistor & Shunt Cap on 24 MHz TCXO (`R22` = 470 Ω, `C66` = 15 pF)**: `U8` active CMOS clock output is excessively loaded and filtered before reaching `IC3.12` (`OSC_IN`). | Replace `R22` (470 Ω) with a 22–33 Ω series damping resistor; remove shunt capacitor `C66`. |
| **M4** | `Ethernet` | **Unnecessary Pull-Up on Push-Pull Clock (`R49` = 2.2 kΩ)**: `ETH_MDC` is a unidirectional push-pull MAC output. | Remove `R49` on `ETH_MDC`; retain `R50` on `ETH_MDIO` only. |
| **M5** | `Ethernet` | **RJ45 Magnetics Pair Inversion**: `T1` Pin 1/2 (RD) is wired to TD, and Pin 3/6 (TD) is wired to RD. | Connect DP83825 TD to `T1` Pin 3/6 and RD to `T1` Pin 1/2 per Würth 7499010211A datasheet. |
| **M6** | `USB_HUB` | **USB Hub Downstream Ports Strapped as Removable**: `NON_REM1` and `NON_REM0` are pulled low (00 = all removable). | Pull `NON_REM1` and `NON_REM0` HIGH to `+3.3V_HUB` with 100 kΩ resistors (strap 11 = all non-removable). |

### Minor Severity (BOM & Reliability Optimization)

| Ref | Sheet | Issue Description | Corrective Action |
|---|---|---|---|
| **N1** | Multi-Sheet | **Corrupted Resistor Syntax (`10]K`)**: 17 resistors across the design have a bracket typo (`10]K`). | Global replace `10]K` with `10K` to prevent automated BOM parsing errors. |
| **N2** | `Controller` | **Missing Low-Pass Filter on MCU Reset**: `NRST` line lacks a debounce capacitor. | Add a 100 nF capacitor from `NRST` to `GND` near `IC3` Pin 14. |
| **N3** | `IMU` | **Pull-Up on SD Card Clock Line (`R58` = 10 kΩ)**: Push-pull `SD_CLK` has an unnecessary pull-up resistor. | Remove `R58`; retain pull-ups on `SD_CMD` and `SD_DAT[0..3]`. |
