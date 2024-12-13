# `cnt_data_chain` Module
![Layout](cnt_data_chain.png)

## Cell Hierarchy

`cnt_data_chain` **225** (number MOS pairs)
- `tff_st_ar` **15** *x15*

## Netlist

```
.SUBCKT cnt_data_chain out<0> out<1> out<2> out<3> out<4> out<5> out<6> out<7> out<8> out<9> out<10>
                       + out<11> out<12> out<13> out<14> rand_in rst rst' vdd vss
    Xi15 out<13> out<14> net10 rst rst' vdd vss tff_st_ar
    Xi14 out<12> out<13> net17 rst rst' vdd vss tff_st_ar
    Xi13 out<11> out<12> net24 rst rst' vdd vss tff_st_ar
    Xi12 out<7> out<8> net31 rst rst' vdd vss tff_st_ar
    Xi11 out<8> out<9> net38 rst rst' vdd vss tff_st_ar
    Xi10 out<9> out<10> net45 rst rst' vdd vss tff_st_ar
    Xi9 out<10> out<11> net52 rst rst' vdd vss tff_st_ar
    Xi8 out<6> out<7> net59 rst rst' vdd vss tff_st_ar
    Xi7 out<5> out<6> net66 rst rst' vdd vss tff_st_ar
    Xi6 out<4> out<5> net73 rst rst' vdd vss tff_st_ar
    Xi4 out<2> out<3> net87 rst rst' vdd vss tff_st_ar
    Xi3 out<1> out<2> net94 rst rst' vdd vss tff_st_ar
    Xi2 out<0> out<1> net101 rst rst' vdd vss tff_st_ar
    Xi1 rand_in out<0> net108 rst rst' vdd vss tff_st_ar
    Xi5 out<3> out<4> net80 rst rst' vdd vss tff_st_ar
.ENDS
```
