# `buf_wide` Module
![Layout](buf_wide.png)

## Cell Hierarchy

`buf_wide` **2** (number MOS pairs)
- `n_mos` **0** *x2*
- `p_mos` **0** *x2*

## Netlist

```
.SUBCKT buf_wide in out vdd vss
    Mm1 out int vss vss n_mos l=30n w=200n m=4 nf=1
    Mm0 int in vss vss n_mos l=30n w=100n m=1 nf=1
    Mm3 out int vdd vdd p_mos l=30n w=200n m=4 nf=1
    Mm2 int in vdd vdd p_mos l=30n w=100n m=1 nf=1
.ENDS
```
