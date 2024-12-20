# `conf_top` Module
![Layout](conf_top.png)

## Cell Hierarchy

`conf_top` **1309** (number MOS pairs)
- `dff_inv_c` **17** *x77*

## Netlist

```
.SUBCKT conf_top conf_bit'cnt conf_clk conf_dc0'<0> conf_dc0'<1> conf_dc0'<2> conf_dc0'<3>
                 + conf_dc0'<4> conf_dc0'<5> conf_dc0'<6> conf_dc0'<7> conf_dc0'<8> conf_dc0'<9>
                 + conf_dc0'<10> conf_dc0'<11> conf_dc0'<12> conf_dc0'<13> conf_dc0'<14>
                 + conf_dc0'<15> conf_dc0<0> conf_dc0<1> conf_dc0<2> conf_dc0<3> conf_dc0<4>
                 + conf_dc0<5> conf_dc0<6> conf_dc0<7> conf_dc0<8> conf_dc0<9> conf_dc0<10>
                 + conf_dc0<11> conf_dc0<12> conf_dc0<13> conf_dc0<14> conf_dc0<15> conf_dc1'<0>
                 + conf_dc1'<1> conf_dc1'<2> conf_dc1'<3> conf_dc1'<4> conf_dc1'<5> conf_dc1'<6>
                 + conf_dc1'<7> conf_dc1'<8> conf_dc1'<9> conf_dc1'<10> conf_dc1'<11> conf_dc1'<12>
                 + conf_dc1'<13> conf_dc1'<14> conf_dc1'<15> conf_dc1<0> conf_dc1<1> conf_dc1<2>
                 + conf_dc1<3> conf_dc1<4> conf_dc1<5> conf_dc1<6> conf_dc1<7> conf_dc1<8>
                 + conf_dc1<9> conf_dc1<10> conf_dc1<11> conf_dc1<12> conf_dc1<13> conf_dc1<14>
                 + conf_dc1<15> conf_enhigh_dc conf_enhigh_vdl conf_enhigh_vdl' conf_fb
                 + conf_freqsel<0> conf_freqsel<1> conf_in conf_rochoose<0> conf_rochoose<1>
                 + conf_roen conf_rofreq<0> conf_rofreq<1> conf_rofreq<2> conf_rst conf_rst'
                 + conf_sendenable conf_sendenable' conf_vdl0'<0> conf_vdl0'<1> conf_vdl0'<2>
                 + conf_vdl0'<3> conf_vdl0'<4> conf_vdl0'<5> conf_vdl0'<6> conf_vdl0'<7>
                 + conf_vdl0'<8> conf_vdl0'<9> conf_vdl0'<10> conf_vdl0'<11> conf_vdl0'<12>
                 + conf_vdl0'<13> conf_vdl0'<14> conf_vdl0'<15> conf_vdl0<0> conf_vdl0<1>
                 + conf_vdl0<2> conf_vdl0<3> conf_vdl0<4> conf_vdl0<5> conf_vdl0<6> conf_vdl0<7>
                 + conf_vdl0<8> conf_vdl0<9> conf_vdl0<10> conf_vdl0<11> conf_vdl0<12> conf_vdl0<13>
                 + conf_vdl0<14> conf_vdl0<15> conf_vdl1'<0> conf_vdl1'<1> conf_vdl1'<2>
                 + conf_vdl1'<3> conf_vdl1'<4> conf_vdl1'<5> conf_vdl1'<6> conf_vdl1'<7>
                 + conf_vdl1'<8> conf_vdl1'<9> conf_vdl1'<10> conf_vdl1'<11> conf_vdl1'<12>
                 + conf_vdl1'<13> conf_vdl1'<14> conf_vdl1'<15> conf_vdl1<0> conf_vdl1<1>
                 + conf_vdl1<2> conf_vdl1<3> conf_vdl1<4> conf_vdl1<5> conf_vdl1<6> conf_vdl1<7>
                 + conf_vdl1<8> conf_vdl1<9> conf_vdl1<10> conf_vdl1<11> conf_vdl1<12> conf_vdl1<13>
                 + conf_vdl1<14> conf_vdl1<15> vdd vss
    Xi77 conf_clk conf_rofreq<1> conf_rofreq<2> net0200 conf_rst conf_rst' vdd vss dff_inv_c
    Xi75 conf_clk conf_rofreq<0> conf_rofreq<1> net12 conf_rst conf_rst' vdd vss dff_inv_c
    Xi74 conf_clk conf_roen conf_rofreq<0> net20 conf_rst conf_rst' vdd vss dff_inv_c
    Xi73 conf_clk conf_enhigh_vdl conf_roen net28 conf_rst conf_rst' vdd vss dff_inv_c
    Xi72 conf_clk conf_rochoose<1> conf_enhigh_vdl conf_enhigh_vdl' conf_rst conf_rst' vdd vss
         + dff_inv_c
    Xi71 conf_clk conf_rochoose<0> conf_rochoose<1> net44 conf_rst conf_rst' vdd vss dff_inv_c
    Xi70 conf_clk conf_vdl1<15> conf_rochoose<0> net52 conf_rst conf_rst' vdd vss dff_inv_c
    Xi69 conf_clk conf_vdl1<14> conf_vdl1<15> conf_vdl1'<15> conf_rst conf_rst' vdd vss dff_inv_c
    Xi68 conf_clk conf_vdl1<13> conf_vdl1<14> conf_vdl1'<14> conf_rst conf_rst' vdd vss dff_inv_c
    Xi67 conf_clk conf_vdl1<12> conf_vdl1<13> conf_vdl1'<13> conf_rst conf_rst' vdd vss dff_inv_c
    Xi66 conf_clk conf_vdl1<11> conf_vdl1<12> conf_vdl1'<12> conf_rst conf_rst' vdd vss dff_inv_c
    Xi65 conf_clk conf_vdl1<10> conf_vdl1<11> conf_vdl1'<11> conf_rst conf_rst' vdd vss dff_inv_c
    Xi64 conf_clk conf_vdl1<9> conf_vdl1<10> conf_vdl1'<10> conf_rst conf_rst' vdd vss dff_inv_c
    Xi63 conf_clk conf_vdl1<8> conf_vdl1<9> conf_vdl1'<9> conf_rst conf_rst' vdd vss dff_inv_c
    Xi62 conf_clk conf_vdl1<7> conf_vdl1<8> conf_vdl1'<8> conf_rst conf_rst' vdd vss dff_inv_c
    Xi61 conf_clk conf_vdl1<6> conf_vdl1<7> conf_vdl1'<7> conf_rst conf_rst' vdd vss dff_inv_c
    Xi60 conf_clk conf_vdl1<5> conf_vdl1<6> conf_vdl1'<6> conf_rst conf_rst' vdd vss dff_inv_c
    Xi59 conf_clk conf_vdl1<4> conf_vdl1<5> conf_vdl1'<5> conf_rst conf_rst' vdd vss dff_inv_c
    Xi58 conf_clk conf_vdl1<3> conf_vdl1<4> conf_vdl1'<4> conf_rst conf_rst' vdd vss dff_inv_c
    Xi57 conf_clk conf_vdl1<2> conf_vdl1<3> conf_vdl1'<3> conf_rst conf_rst' vdd vss dff_inv_c
    Xi56 conf_clk conf_vdl1<1> conf_vdl1<2> conf_vdl1'<2> conf_rst conf_rst' vdd vss dff_inv_c
    Xi55 conf_clk conf_vdl1<0> conf_vdl1<1> conf_vdl1'<1> conf_rst conf_rst' vdd vss dff_inv_c
    Xi54 conf_clk conf_vdl0<15> conf_vdl1<0> conf_vdl1'<0> conf_rst conf_rst' vdd vss dff_inv_c
    Xi53 conf_clk conf_vdl0<14> conf_vdl0<15> conf_vdl0'<15> conf_rst conf_rst' vdd vss dff_inv_c
    Xi52 conf_clk conf_vdl0<13> conf_vdl0<14> conf_vdl0'<14> conf_rst conf_rst' vdd vss dff_inv_c
    Xi51 conf_clk conf_vdl0<12> conf_vdl0<13> conf_vdl0'<13> conf_rst conf_rst' vdd vss dff_inv_c
    Xi50 conf_clk conf_vdl0<11> conf_vdl0<12> conf_vdl0'<12> conf_rst conf_rst' vdd vss dff_inv_c
    Xi49 conf_clk conf_vdl0<10> conf_vdl0<11> conf_vdl0'<11> conf_rst conf_rst' vdd vss dff_inv_c
    Xi48 conf_clk conf_vdl0<9> conf_vdl0<10> conf_vdl0'<10> conf_rst conf_rst' vdd vss dff_inv_c
    Xi47 conf_clk conf_vdl0<8> conf_vdl0<9> conf_vdl0'<9> conf_rst conf_rst' vdd vss dff_inv_c
    Xi46 conf_clk conf_vdl0<7> conf_vdl0<8> conf_vdl0'<8> conf_rst conf_rst' vdd vss dff_inv_c
    Xi45 conf_clk conf_vdl0<6> conf_vdl0<7> conf_vdl0'<7> conf_rst conf_rst' vdd vss dff_inv_c
    Xi44 conf_clk conf_vdl0<5> conf_vdl0<6> conf_vdl0'<6> conf_rst conf_rst' vdd vss dff_inv_c
    Xi43 conf_clk conf_vdl0<4> conf_vdl0<5> conf_vdl0'<5> conf_rst conf_rst' vdd vss dff_inv_c
    Xi42 conf_clk conf_vdl0<3> conf_vdl0<4> conf_vdl0'<4> conf_rst conf_rst' vdd vss dff_inv_c
    Xi41 conf_clk conf_vdl0<2> conf_vdl0<3> conf_vdl0'<3> conf_rst conf_rst' vdd vss dff_inv_c
    Xi40 conf_clk conf_vdl0<1> conf_vdl0<2> conf_vdl0'<2> conf_rst conf_rst' vdd vss dff_inv_c
    Xi39 conf_clk conf_vdl0<0> conf_vdl0<1> conf_vdl0'<1> conf_rst conf_rst' vdd vss dff_inv_c
    Xi38 conf_clk conf_freqsel<1> conf_vdl0<0> conf_vdl0'<0> conf_rst conf_rst' vdd vss dff_inv_c
    Xi37 conf_clk conf_freqsel<0> conf_freqsel<1> net316 conf_rst conf_rst' vdd vss dff_inv_c
    Xi36 conf_clk conf_enhigh_dc conf_freqsel<0> net324 conf_rst conf_rst' vdd vss dff_inv_c
    Xi35 conf_clk conf_fb conf_enhigh_dc net332 conf_rst conf_rst' vdd vss dff_inv_c
    Xi34 conf_clk conf_dc1<15> conf_fb net340 conf_rst conf_rst' vdd vss dff_inv_c
    Xi33 conf_clk conf_dc1<14> conf_dc1<15> conf_dc1'<15> conf_rst conf_rst' vdd vss dff_inv_c
    Xi32 conf_clk conf_dc1<13> conf_dc1<14> conf_dc1'<14> conf_rst conf_rst' vdd vss dff_inv_c
    Xi31 conf_clk conf_dc1<12> conf_dc1<13> conf_dc1'<13> conf_rst conf_rst' vdd vss dff_inv_c
    Xi30 conf_clk conf_dc1<11> conf_dc1<12> conf_dc1'<12> conf_rst conf_rst' vdd vss dff_inv_c
    Xi29 conf_clk conf_dc1<10> conf_dc1<11> conf_dc1'<11> conf_rst conf_rst' vdd vss dff_inv_c
    Xi28 conf_clk conf_dc1<9> conf_dc1<10> conf_dc1'<10> conf_rst conf_rst' vdd vss dff_inv_c
    Xi27 conf_clk conf_dc1<8> conf_dc1<9> conf_dc1'<9> conf_rst conf_rst' vdd vss dff_inv_c
    Xi26 conf_clk conf_dc1<7> conf_dc1<8> conf_dc1'<8> conf_rst conf_rst' vdd vss dff_inv_c
    Xi25 conf_clk conf_dc1<6> conf_dc1<7> conf_dc1'<7> conf_rst conf_rst' vdd vss dff_inv_c
    Xi24 conf_clk conf_dc1<5> conf_dc1<6> conf_dc1'<6> conf_rst conf_rst' vdd vss dff_inv_c
    Xi23 conf_clk conf_dc1<4> conf_dc1<5> conf_dc1'<5> conf_rst conf_rst' vdd vss dff_inv_c
    Xi22 conf_clk conf_dc1<3> conf_dc1<4> conf_dc1'<4> conf_rst conf_rst' vdd vss dff_inv_c
    Xi21 conf_clk conf_dc1<2> conf_dc1<3> conf_dc1'<3> conf_rst conf_rst' vdd vss dff_inv_c
    Xi20 conf_clk conf_dc1<1> conf_dc1<2> conf_dc1'<2> conf_rst conf_rst' vdd vss dff_inv_c
    Xi19 conf_clk conf_dc1<0> conf_dc1<1> conf_dc1'<1> conf_rst conf_rst' vdd vss dff_inv_c
    Xi18 conf_clk conf_dc0<15> conf_dc1<0> conf_dc1'<0> conf_rst conf_rst' vdd vss dff_inv_c
    Xi17 conf_clk conf_dc0<14> conf_dc0<15> conf_dc0'<15> conf_rst conf_rst' vdd vss dff_inv_c
    Xi16 conf_clk conf_dc0<13> conf_dc0<14> conf_dc0'<14> conf_rst conf_rst' vdd vss dff_inv_c
    Xi15 conf_clk conf_dc0<12> conf_dc0<13> conf_dc0'<13> conf_rst conf_rst' vdd vss dff_inv_c
    Xi14 conf_clk conf_dc0<11> conf_dc0<12> conf_dc0'<12> conf_rst conf_rst' vdd vss dff_inv_c
    Xi13 conf_clk conf_dc0<10> conf_dc0<11> conf_dc0'<11> conf_rst conf_rst' vdd vss dff_inv_c
    Xi12 conf_clk conf_dc0<9> conf_dc0<10> conf_dc0'<10> conf_rst conf_rst' vdd vss dff_inv_c
    Xi11 conf_clk conf_dc0<8> conf_dc0<9> conf_dc0'<9> conf_rst conf_rst' vdd vss dff_inv_c
    Xi10 conf_clk conf_dc0<7> conf_dc0<8> conf_dc0'<8> conf_rst conf_rst' vdd vss dff_inv_c
    Xi9 conf_clk conf_dc0<6> conf_dc0<7> conf_dc0'<7> conf_rst conf_rst' vdd vss dff_inv_c
    Xi8 conf_clk conf_dc0<5> conf_dc0<6> conf_dc0'<6> conf_rst conf_rst' vdd vss dff_inv_c
    Xi7 conf_clk conf_dc0<4> conf_dc0<5> conf_dc0'<5> conf_rst conf_rst' vdd vss dff_inv_c
    Xi6 conf_clk conf_dc0<3> conf_dc0<4> conf_dc0'<4> conf_rst conf_rst' vdd vss dff_inv_c
    Xi5 conf_clk conf_dc0<2> conf_dc0<3> conf_dc0'<3> conf_rst conf_rst' vdd vss dff_inv_c
    Xi4 conf_clk conf_dc0<1> conf_dc0<2> conf_dc0'<2> conf_rst conf_rst' vdd vss dff_inv_c
    Xi3 conf_clk conf_dc0<0> conf_dc0<1> conf_dc0'<1> conf_rst conf_rst' vdd vss dff_inv_c
    Xi2 conf_clk conf_sendenable conf_dc0<0> conf_dc0'<0> conf_rst conf_rst' vdd vss dff_inv_c
    Xi1 conf_clk conf_bit'cnt conf_sendenable conf_sendenable' conf_rst conf_rst' vdd vss dff_inv_c
    Xi0 conf_clk conf_in conf_bit'cnt net612 conf_rst conf_rst' vdd vss dff_inv_c
.ENDS
```
