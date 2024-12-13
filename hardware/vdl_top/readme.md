# `vdl_top` Module
![Layout](vdl_top.png)

## Cell Hierarchy

`vdl_top` **305** (number MOS pairs)
- `vdl_branch` **60** *x2*
- `vdl_enable` **18**
- `end_detector` **163**
- `buf_wide` **2** *x2*

## Netlist

```
.SUBCKT vdl_top conf_enhigh conf_enhigh' conf_vdl0'<0> conf_vdl0'<1> conf_vdl0'<2> conf_vdl0'<3>
                + conf_vdl0'<4> conf_vdl0'<5> conf_vdl0'<6> conf_vdl0'<7> conf_vdl0'<8>
                + conf_vdl0'<9> conf_vdl0'<10> conf_vdl0'<11> conf_vdl0'<12> conf_vdl0'<13>
                + conf_vdl0'<14> conf_vdl0'<15> conf_vdl0<0> conf_vdl0<1> conf_vdl0<2> conf_vdl0<3>
                + conf_vdl0<4> conf_vdl0<5> conf_vdl0<6> conf_vdl0<7> conf_vdl0<8> conf_vdl0<9>
                + conf_vdl0<10> conf_vdl0<11> conf_vdl0<12> conf_vdl0<13> conf_vdl0<14>
                + conf_vdl0<15> conf_vdl1'<0> conf_vdl1'<1> conf_vdl1'<2> conf_vdl1'<3>
                + conf_vdl1'<4> conf_vdl1'<5> conf_vdl1'<6> conf_vdl1'<7> conf_vdl1'<8>
                + conf_vdl1'<9> conf_vdl1'<10> conf_vdl1'<11> conf_vdl1'<12> conf_vdl1'<13>
                + conf_vdl1'<14> conf_vdl1'<15> conf_vdl1<0> conf_vdl1<1> conf_vdl1<2> conf_vdl1<3>
                + conf_vdl1<4> conf_vdl1<5> conf_vdl1<6> conf_vdl1<7> conf_vdl1<8> conf_vdl1<9>
                + conf_vdl1<10> conf_vdl1<11> conf_vdl1<12> conf_vdl1<13> conf_vdl1<14>
                + conf_vdl1<15> in0 in1 out_raw_0 out_raw_1 rand ready rst rst' vdd vdd_0 vdd_1 vss
                + vss_0 vss_1
    Xi1 conf_vdl1'<0> conf_vdl1'<1> conf_vdl1'<2> conf_vdl1'<3> conf_vdl1'<4> conf_vdl1'<5>
        + conf_vdl1'<6> conf_vdl1'<7> conf_vdl1'<8> conf_vdl1'<9> conf_vdl1'<10> conf_vdl1'<11>
        + conf_vdl1'<12> conf_vdl1'<13> conf_vdl1'<14> conf_vdl1'<15> conf_vdl1<0> conf_vdl1<1>
        + conf_vdl1<2> conf_vdl1<3> conf_vdl1<4> conf_vdl1<5> conf_vdl1<6> conf_vdl1<7> conf_vdl1<8>
        + conf_vdl1<9> conf_vdl1<10> conf_vdl1<11> conf_vdl1<12> conf_vdl1<13> conf_vdl1<14>
        + conf_vdl1<15> conf_enhigh' in1 enable enable' clk rst rst' vdd vdd_1 vss vss_1 vdl_branch
    Xi0 conf_vdl0'<0> conf_vdl0'<1> conf_vdl0'<2> conf_vdl0'<3> conf_vdl0'<4> conf_vdl0'<5>
        + conf_vdl0'<6> conf_vdl0'<7> conf_vdl0'<8> conf_vdl0'<9> conf_vdl0'<10> conf_vdl0'<11>
        + conf_vdl0'<12> conf_vdl0'<13> conf_vdl0'<14> conf_vdl0'<15> conf_vdl0<0> conf_vdl0<1>
        + conf_vdl0<2> conf_vdl0<3> conf_vdl0<4> conf_vdl0<5> conf_vdl0<6> conf_vdl0<7> conf_vdl0<8>
        + conf_vdl0<9> conf_vdl0<10> conf_vdl0<11> conf_vdl0<12> conf_vdl0<13> conf_vdl0<14>
        + conf_vdl0<15> conf_enhigh' in0 enable enable' d rst rst' vdd vdd_0 vss vss_0 vdl_branch
    Xi2 conf_enhigh conf_enhigh' enable enable' ready rst rst' vdd vss vdl_enable
    Xi3 d clk rand ready rst rst' vdd vss end_detector
    Xi7 clk out_raw_1 vdd vss buf_wide
    Xi6 d out_raw_0 vdd vss buf_wide
.ENDS
```
