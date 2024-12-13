# `dc_top` Module
![Layout](dc_top.png)

## Cell Hierarchy

`dc_top` **676** (number MOS pairs)
- `rst_start` **132**
- `dc_branch` **272** *x2*

## Netlist

```
.SUBCKT dc_top conf_dc0'<0> conf_dc0'<1> conf_dc0'<2> conf_dc0'<3> conf_dc0'<4> conf_dc0'<5>
               + conf_dc0'<6> conf_dc0'<7> conf_dc0'<8> conf_dc0'<9> conf_dc0'<10> conf_dc0'<11>
               + conf_dc0'<12> conf_dc0'<13> conf_dc0'<14> conf_dc0'<15> conf_dc0<0> conf_dc0<1>
               + conf_dc0<2> conf_dc0<3> conf_dc0<4> conf_dc0<5> conf_dc0<6> conf_dc0<7> conf_dc0<8>
               + conf_dc0<9> conf_dc0<10> conf_dc0<11> conf_dc0<12> conf_dc0<13> conf_dc0<14>
               + conf_dc0<15> conf_dc1'<0> conf_dc1'<1> conf_dc1'<2> conf_dc1'<3> conf_dc1'<4>
               + conf_dc1'<5> conf_dc1'<6> conf_dc1'<7> conf_dc1'<8> conf_dc1'<9> conf_dc1'<10>
               + conf_dc1'<11> conf_dc1'<12> conf_dc1'<13> conf_dc1'<14> conf_dc1'<15> conf_dc1<0>
               + conf_dc1<1> conf_dc1<2> conf_dc1<3> conf_dc1<4> conf_dc1<5> conf_dc1<6> conf_dc1<7>
               + conf_dc1<8> conf_dc1<9> conf_dc1<10> conf_dc1<11> conf_dc1<12> conf_dc1<13>
               + conf_dc1<14> conf_dc1<15> conf_enhigh conf_fb conf_freqsel<0> conf_freqsel<1> out0
               + out1 out_raw_0 out_raw_1 rst_glob rst_glob' start_glob vdd vdd_0 vdd_1 vss vss_0
               + vss_1
    Xi11 conf_fb dc_rst_0 dc_rst_1 out0 out1 rst rst' rst_glob rst_glob' start_glob start vdd vss
         + rst_start
    Xi13 conf_dc1'<0> conf_dc1'<1> conf_dc1'<2> conf_dc1'<3> conf_dc1'<4> conf_dc1'<5> conf_dc1'<6>
         + conf_dc1'<7> conf_dc1'<8> conf_dc1'<9> conf_dc1'<10> conf_dc1'<11> conf_dc1'<12>
         + conf_dc1'<13> conf_dc1'<14> conf_dc1'<15> conf_dc1<0> conf_dc1<1> conf_dc1<2> conf_dc1<3>
         + conf_dc1<4> conf_dc1<5> conf_dc1<6> conf_dc1<7> conf_dc1<8> conf_dc1<9> conf_dc1<10>
         + conf_dc1<11> conf_dc1<12> conf_dc1<13> conf_dc1<14> conf_dc1<15> conf_enhigh
         + conf_freqsel<0> conf_freqsel<1> dc_rst_1 out1 out_raw_1 rst rst' rst_glob rst_glob' start
         + vdd vdd_1 vss vss_1 dc_branch
    Xi12 conf_dc0'<0> conf_dc0'<1> conf_dc0'<2> conf_dc0'<3> conf_dc0'<4> conf_dc0'<5> conf_dc0'<6>
         + conf_dc0'<7> conf_dc0'<8> conf_dc0'<9> conf_dc0'<10> conf_dc0'<11> conf_dc0'<12>
         + conf_dc0'<13> conf_dc0'<14> conf_dc0'<15> conf_dc0<0> conf_dc0<1> conf_dc0<2> conf_dc0<3>
         + conf_dc0<4> conf_dc0<5> conf_dc0<6> conf_dc0<7> conf_dc0<8> conf_dc0<9> conf_dc0<10>
         + conf_dc0<11> conf_dc0<12> conf_dc0<13> conf_dc0<14> conf_dc0<15> conf_enhigh
         + conf_freqsel<0> conf_freqsel<1> dc_rst_0 out0 out_raw_0 rst rst' rst_glob rst_glob' start
         + vdd vdd_0 vss vss_0 dc_branch
.ENDS
```
