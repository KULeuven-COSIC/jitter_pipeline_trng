# Figure Generation Python Scripts

This folder contains the figure generation Python scripts.

## Scripts

The scripts are divided in the following categories.

### Ring Oscillator Model

- **mod_phase_example.py**: Generate example instances of a random phase process figure.
- **mod_square_wave.py**: Generate RO waveform and corresponding phase versus time figure.

### Stochastic Model

- **mod_vdl_sampling.py**: Generate relation between TDC phases and sampling time instances figure.
- **mod_vdl_zone.py**: Generate relation between the TDC phases and sampling time instances figure.
- **mod_tpi_bounds.py**: Generate lower and upper bounds from figure.
- **mod_vdl_phase_error.py**: Generate histogram of repeated simulations illustrating the absolute phase error figure.

### Jitter Strength Measurement

- **jit_meas.py**: Generate jitter measurement results figure.

###  Design Parameter Selection Criteria

- **opt_h_vs_res.py**: Generate minimal alpha required figure.

### Experimental Results

- **expe_count.py**: Measured sample correlation obtained from chip 0.
- **expe_results.py**: Measurement results.

## Script Options

The following script arguments are available:
- `-v`: Enable verbose output.
- `-d`: Generate processed data and store in the *data/* folder.
- `-q`: Quit the script as soon as the processed data is generated, without generating the figure. Should only be used in combination with the `-d` argument.
- `-l`: For lengthy execution times, the log option might be available, indicating the time required to execute the script.