# voltammetry.py
A Python package for working with voltammetry data

Derived from `impedance.py` and `voltcycle`

# TO DO
- [ ] Detect multiple peaks (modify 'peak_detection_fxn' in voltcycle/app/core.py)
- [ ] Deal with multiple experiment cycles
- [ ] Machine learning

# Features
- Visualization of voltammetry data with Altair (V vs. t, I vs. T, and V vs. I, for multiple cycles)
- Peak finding, baseline fitting
- Peak separation, peak height ratios
- Absolute reference conversion (SCE, MSE etc.)
- ability to specify IUPAC/US convention (default IUPAC)
- Specifying reaction mechanisms: soluble, insoluble, intercalation, EC/ECE, *etc.*
- Specify experimental setup: standard, RDE/RRDE, *etc.*   
- Digitizer?
- Application-specific functions:
  - Catalysis: automated hydrogen absorption calculations for determining electrochemically active surface area
