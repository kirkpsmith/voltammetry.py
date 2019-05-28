# voltammetry.py
A Python package for working with voltammetry data

Derived from `impedance.py` and `voltcycle`

# TO DO
- [ ] Detect multiple peaks (modify 'peak_detection_fxn' in voltcycle/app/core.py)
- [ ] Deal with multiple experiment cycles
- [ ] Machine learning

# Features
- Visualization of voltammetry data with Altair
- *everything voltcycle does*
- Automated hydrogen absorption calculations for determining electrochemically active surface area of catalyst
- Peak separation, peak height ratios
- Specifying EC/ECE reaction mechanisms
- RRDE/RDE    
- Show Altair plot with V vs. t, I vs. T, and V vs. I => add multiple cycles
- User interface
- Subfunctions: catalysis, solution phase reactions, intercalation reactions,
- Digitizer?
- Absolute reference conversion (SCE, MSE etc.)
- ability to specify IUPAC/US convention (default IUPAC)
