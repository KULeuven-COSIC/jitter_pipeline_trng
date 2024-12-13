# `dc_rst_check` Module
![Layout](dc_rst_check.png)

## Cell Hierarchy

`dc_rst_check` **7** (number MOS pairs)
- `nand5` **5**
- `inv` **1** *x2*

## Netlist

```
.SUBCKT dc_rst_check dc_in int0 int1 int2 muxin0 out vdd vss
    Xi0 dc_in int0' int1 int2' muxin0 out vdd vss nand5
    Xi2 int2 int2' vdd vss inv
    Xi1 int0 int0' vdd vss inv
.ENDS
```
