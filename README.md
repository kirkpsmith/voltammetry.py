# voltammetry.py
A Python package for working with voltammetry data

Derived from `impedance.py` and `voltcycle`

# TO DO
- [ ] Detect multiple peaks (modify 'peak_detection_fxn' in voltcycle/app/core.py)
- [ ] Deal with multiple experiment cycles
- [ ] Machine learning

# Features
- Visualization of voltammetry data with Altair (V vs. t, I vs. T, and V vs. I, for multiple cycles), intuitive knowledge of scan directions
- ability to specify IUPAC/US convention (default IUPAC)
- Peak finding, baseline fitting
- Peak separation, peak height ratios
- Absolute reference conversion (SCE, MSE etc.)
- Specifying reaction mechanisms: soluble/insoluble species, intercalation, EC/ECE coupling, *etc.*
- Specify experimental setup: standard, RDE/RRDE, microelectrode, *etc.*
- user input mode for complex coupled rxns vs. automatic mode for high-throughput analysis
- Digitizer?
- Application-specific functions:
  - Catalysis: automated hydrogen absorption calculations for determining electrochemically active surface area

# Scope for hack week
- focus on Altair plotting and notebooks only, no GUI/app
- repackage core of `voltcycle` into `impedance.py` structure
- establish which voltammetry methods are fundamental across applications, add to those already implemented with `voltcycle` and tidy up
- establish which voltammetry methods are ripe for automation (like hydrogen absorption calcs)
- high-touch user input mode for complex coupled rxns vs. automatic mode for high-throughput analysis of well-understood systems
