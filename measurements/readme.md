# Measurement Data Folder

This folder contains all measurement data. Different measurements are available:
- **m0**: Read all RO frequencies.
- **m5**: Measure jitter strength experiment.
- **m6**: Find an optimized configuration for the ASIC.
- **m7**: Readout a small amount of random samples.

## Folder structure

This measurement folder contains the following sub-folders:
- *m0/*: m0 measurement data.
- *m5/*: m5 measurement data.
- *m6/*: m6 measurement data.
- *m7/*: m7 measurement data.
- *readout/*: The Python scripts used to perform the measurements.

Additionally, the following Python modules are available:
- **meas_helper.py**: Measurement helper functionality.
- **read_asic.py**: Main ASIC readout module.