# `mux2` Module
![Layout](mux2.png)

## Cell Hierarchy

`mux2` **7** (number MOS pairs)
- `nand2` **2** *x3*
- `inv` **1**

## Netlist

```
.SUBCKT mux2 in0 in1 out sel vdd vss
    Xi2 in0 net7 net9 vdd vss nand2
    Xi1 in1 sel net10 vdd vss nand2
    Xi0 net10 net9 out vdd vss nand2
    Xi3 sel net7 vdd vss inv
.ENDS
```
