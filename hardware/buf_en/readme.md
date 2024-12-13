# `buf_en` Module
![Layout](buf_en.png)

## Cell Hierarchy

`buf_en` **3** (number MOS pairs)
- `n_mos` **0** *x3*
- `p_mos` **0** *x3*

## Netlist

```
.SUBCKT buf_en enable in out vdd vss
    Mm2 net7 enable vss vss n_mos l=30n w=400n m=4 nf=1
    Mm1 out int net7 vss n_mos l=30n w=400n m=4 nf=1
    Mm0 int in vss vss n_mos l=30n w=200n m=2 nf=1
    Mm5 out int vdd vdd p_mos l=30n w=200n m=4 nf=1
    Mm4 out enable vdd vdd p_mos l=30n w=100n m=4 nf=1
    Mm3 int in vdd vdd p_mos l=30n w=200n m=2 nf=1
.ENDS
```
