# `dc_vdl_combo` Module
![Layout](dc_vdl_combo.png)

## Cell Hierarchy

`dc_vdl_combo` **981** (number MOS pairs)
- `dc_top` **676**
- `vdl_top` **305**

## Netlist

```
.SUBCKT dc_vdl_combo conf_dc0'<0> conf_dc0'<1> conf_dc0'<2> conf_dc0'<3> conf_dc0'<4> conf_dc0'<5>
                     + conf_dc0'<6> conf_dc0'<7> conf_dc0'<8> conf_dc0'<9> conf_dc0'<10>
                     + conf_dc0'<11> conf_dc0'<12> conf_dc0'<13> conf_dc0'<14> conf_dc0'<15>
                     + conf_dc0<0> conf_dc0<1> conf_dc0<2> conf_dc0<3> conf_dc0<4> conf_dc0<5>
                     + conf_dc0<6> conf_dc0<7> conf_dc0<8> conf_dc0<9> conf_dc0<10> conf_dc0<11>
                     + conf_dc0<12> conf_dc0<13> conf_dc0<14> conf_dc0<15> conf_dc1'<0> conf_dc1'<1>
                     + conf_dc1'<2> conf_dc1'<3> conf_dc1'<4> conf_dc1'<5> conf_dc1'<6> conf_dc1'<7>
                     + conf_dc1'<8> conf_dc1'<9> conf_dc1'<10> conf_dc1'<11> conf_dc1'<12>
                     + conf_dc1'<13> conf_dc1'<14> conf_dc1'<15> conf_dc1<0> conf_dc1<1> conf_dc1<2>
                     + conf_dc1<3> conf_dc1<4> conf_dc1<5> conf_dc1<6> conf_dc1<7> conf_dc1<8>
                     + conf_dc1<9> conf_dc1<10> conf_dc1<11> conf_dc1<12> conf_dc1<13> conf_dc1<14>
                     + conf_dc1<15> conf_enhigh_dc conf_enhigh_vdl conf_enhigh_vdl' conf_fb
                     + conf_freqsel<0> conf_freqsel<1> conf_vdl0'<0> conf_vdl0'<1> conf_vdl0'<2>
                     + conf_vdl0'<3> conf_vdl0'<4> conf_vdl0'<5> conf_vdl0'<6> conf_vdl0'<7>
                     + conf_vdl0'<8> conf_vdl0'<9> conf_vdl0'<10> conf_vdl0'<11> conf_vdl0'<12>
                     + conf_vdl0'<13> conf_vdl0'<14> conf_vdl0'<15> conf_vdl0<0> conf_vdl0<1>
                     + conf_vdl0<2> conf_vdl0<3> conf_vdl0<4> conf_vdl0<5> conf_vdl0<6> conf_vdl0<7>
                     + conf_vdl0<8> conf_vdl0<9> conf_vdl0<10> conf_vdl0<11> conf_vdl0<12>
                     + conf_vdl0<13> conf_vdl0<14> conf_vdl0<15> conf_vdl1'<0> conf_vdl1'<1>
                     + conf_vdl1'<2> conf_vdl1'<3> conf_vdl1'<4> conf_vdl1'<5> conf_vdl1'<6>
                     + conf_vdl1'<7> conf_vdl1'<8> conf_vdl1'<9> conf_vdl1'<10> conf_vdl1'<11>
                     + conf_vdl1'<12> conf_vdl1'<13> conf_vdl1'<14> conf_vdl1'<15> conf_vdl1<0>
                     + conf_vdl1<1> conf_vdl1<2> conf_vdl1<3> conf_vdl1<4> conf_vdl1<5> conf_vdl1<6>
                     + conf_vdl1<7> conf_vdl1<8> conf_vdl1<9> conf_vdl1<10> conf_vdl1<11>
                     + conf_vdl1<12> conf_vdl1<13> conf_vdl1<14> conf_vdl1<15> dc_raw_0 dc_raw_1
                     + ext_start rand ready rst rst' vdd vdd_0 vdd_1 vdl_raw_0 vdl_raw_1 vdl_rst
                     + vdl_rst' vss vss_0 vss_1
    Xi0 conf_dc0'<0> conf_dc0'<1> conf_dc0'<2> conf_dc0'<3> conf_dc0'<4> conf_dc0'<5> conf_dc0'<6>
        + conf_dc0'<7> conf_dc0'<8> conf_dc0'<9> conf_dc0'<10> conf_dc0'<11> conf_dc0'<12>
        + conf_dc0'<13> conf_dc0'<14> conf_dc0'<15> conf_dc0<0> conf_dc0<1> conf_dc0<2> conf_dc0<3>
        + conf_dc0<4> conf_dc0<5> conf_dc0<6> conf_dc0<7> conf_dc0<8> conf_dc0<9> conf_dc0<10>
        + conf_dc0<11> conf_dc0<12> conf_dc0<13> conf_dc0<14> conf_dc0<15> conf_dc1'<0> conf_dc1'<1>
        + conf_dc1'<2> conf_dc1'<3> conf_dc1'<4> conf_dc1'<5> conf_dc1'<6> conf_dc1'<7> conf_dc1'<8>
        + conf_dc1'<9> conf_dc1'<10> conf_dc1'<11> conf_dc1'<12> conf_dc1'<13> conf_dc1'<14>
        + conf_dc1'<15> conf_dc1<0> conf_dc1<1> conf_dc1<2> conf_dc1<3> conf_dc1<4> conf_dc1<5>
        + conf_dc1<6> conf_dc1<7> conf_dc1<8> conf_dc1<9> conf_dc1<10> conf_dc1<11> conf_dc1<12>
        + conf_dc1<13> conf_dc1<14> conf_dc1<15> conf_enhigh_dc conf_fb conf_freqsel<0>
        + conf_freqsel<1> dc_out_0 dc_out_1 dc_raw_0 dc_raw_1 rst rst' ext_start vdd vdd_0 vdd_1 vss
        + vss_0 vss_1 dc_top
    Xi1 conf_enhigh_vdl conf_enhigh_vdl' conf_vdl0'<0> conf_vdl0'<1> conf_vdl0'<2> conf_vdl0'<3>
        + conf_vdl0'<4> conf_vdl0'<5> conf_vdl0'<6> conf_vdl0'<7> conf_vdl0'<8> conf_vdl0'<9>
        + conf_vdl0'<10> conf_vdl0'<11> conf_vdl0'<12> conf_vdl0'<13> conf_vdl0'<14> conf_vdl0'<15>
        + conf_vdl0<0> conf_vdl0<1> conf_vdl0<2> conf_vdl0<3> conf_vdl0<4> conf_vdl0<5> conf_vdl0<6>
        + conf_vdl0<7> conf_vdl0<8> conf_vdl0<9> conf_vdl0<10> conf_vdl0<11> conf_vdl0<12>
        + conf_vdl0<13> conf_vdl0<14> conf_vdl0<15> conf_vdl1'<0> conf_vdl1'<1> conf_vdl1'<2>
        + conf_vdl1'<3> conf_vdl1'<4> conf_vdl1'<5> conf_vdl1'<6> conf_vdl1'<7> conf_vdl1'<8>
        + conf_vdl1'<9> conf_vdl1'<10> conf_vdl1'<11> conf_vdl1'<12> conf_vdl1'<13> conf_vdl1'<14>
        + conf_vdl1'<15> conf_vdl1<0> conf_vdl1<1> conf_vdl1<2> conf_vdl1<3> conf_vdl1<4>
        + conf_vdl1<5> conf_vdl1<6> conf_vdl1<7> conf_vdl1<8> conf_vdl1<9> conf_vdl1<10>
        + conf_vdl1<11> conf_vdl1<12> conf_vdl1<13> conf_vdl1<14> conf_vdl1<15> dc_out_0 dc_out_1
        + vdl_raw_0 vdl_raw_1 rand ready vdl_rst vdl_rst' vdd vdd_0 vdd_1 vss vss_0 vss_1 vdl_top
.ENDS
```
