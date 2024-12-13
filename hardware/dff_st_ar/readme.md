# `dff_st_ar` Module
![Layout](dff_st_ar.png)

## Cell Hierarchy

`dff_st_ar` **15** (number MOS pairs)
- `nand2` **2** *x4*
- `nand3_r` **4**
- `nand3` **3**

## Netlist

```
.SUBCKT dff_st_ar clk d q q' rst rst' vdd vss
    Xi5 q n1 q' vdd vss nand2
    Xi4 n0 q' q vdd vss nand2
    Xi3 n1 d n3 vdd vss nand2
    Xi2 n3 n0 n2 vdd vss nand2
    Xi6 clk n0 n3 n1 rst vdd vss nand3_r
    Xi7 clk n2 rst' n0 vdd vss nand3
.ENDS
```
