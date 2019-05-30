# voltammetry.py
A Python package for working with voltammetry data

Inspired by [`impedance.py`](https://github.com/ECSHackWeek/impedance.py) and [`voltcycle`](https://github.com/sabiharustam/voltcycle)

# TO DO
- establish which voltammetry methods are ripe for automation (like hydrogen absorption calculation)


# Features
- Visualization of voltammetry data with Altair (V vs. t, I vs. T, and V vs. I, for multiple cycles), intuitive knowledge of scan directions
- ability to specify IUPAC/US convention (default IUPAC)
- Peak finding, baseline fitting
- Peak separation, peak height ratios
- Absolute reference conversion (SCE, MSE etc.)
- Specifying reaction mechanisms: soluble/insoluble species, intercalation, EC/ECE coupling, *etc.*
- Specify experimental setup: standard, RDE/RRDE, microelectrode, *etc.*
- user input mode for complex coupled rxns vs. automatic mode for high-throughput analysis
- high-touch user input mode for complex coupled rxns vs. automatic mode for high-throughput analysis of well-understood systems
- Application-specific functions:
  - Catalysis: automated hydrogen absorption calculations for determining electrochemically active surface area
