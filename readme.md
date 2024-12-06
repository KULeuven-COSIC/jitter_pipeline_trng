# Oscillator Jitter Based Pipelined TRNG

This archive contains a hardware implementation of an oscillator jitter based pipelined True Random Number Generator (TRNG) design.

## Archive Structure

This archive contains the following folders:
- *measurements/*: Contains measurement data from a 28 nm ASIC implementation.
- *math_model/*: Contains a Python implementation of the stochastic model for the pipelined TRNG.
- *hardware/*: Contains netlist and layout views of the ASIC implementation.
- *figures/*: Contains Python scripts to generate the figures in the publication below and visualizes the data in the *measurement* folder.
- *lib/*: Contains helper Python scripts and figure generation options.

## Publication

The data contained in this archive supports the following publications
- Adriaan Peetermans, and Ingrid Verbauwhede. **[An Energy and Area Efficient, All Digital Entropy Source Compatible with Modern Standards Based on Jitter Pipelining](https://tches.iacr.org/index.php/TCHES/article/view/9814)**. In: *IACR Transactions on Cryptographic Hardware and Embedded Systems (TCHES)*, vol. 2022, no. 4, pp. 88-109, 2022.
