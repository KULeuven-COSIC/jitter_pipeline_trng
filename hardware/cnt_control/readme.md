# `cnt_control` Module
![Layout](cnt_control.png)

## Cell Hierarchy

`cnt_control` **146** (number MOS pairs)
- `dff_st_ar` **15** *x4*
- `nor5` **5**
- `inv` **1** *x2*
- `nand2` **2** *x4*
- `nor2` **2** *x4*
- `cnt_rst_fb` **28**
- `cnt_vdl_rst_fb` **21**
- `dff_st_ar_dh` **14**

## Netlist

```
.SUBCKT cnt_control cnt_data<0> cnt_data<1> cnt_data<2> cnt_data<3> cnt_data<4> cnt_data<5>
                    + cnt_data<6> cnt_data<7> cnt_data<8> cnt_data<9> cnt_data<10> cnt_data<11>
                    + cnt_data<12> cnt_data<13> cnt_data<14> cnt_ready cnt_rst cnt_rst'
                    + extclk_cnt<0> extclk_cnt<1> extclk_cnt<2> extclk_cnt<3> extclk_cnt<4> ext_clk
                    + ready_clk rst_glob rst_glob' vdd vdl_rst_loc vdl_rst_loc' vss
    Xi10 pre_rst vdl_rst_loc vdl_rst_rst_loc vdl_rst_rst_loc' vdl_rst_loc' vdl_rst_loc vdd vss
         + dff_st_ar
    Xi8 ready_clk net019 vdl_rst_0 vdl_rst_0' vdl_rst_rst vdl_rst_rst' vdd vss dff_st_ar
    Xi1 ready_clk ready2 cnt_ready vdl_rst_1' cnt_rst_pre cnt_rst_pre' vdd vss dff_st_ar
    Xi0 ext_clk net19 cnt_rst_loc cnt_rst_loc' cnt_rst_rst cnt_rst_rst' vdd vss dff_st_ar
    Xi2 extclk_cnt<0> extclk_cnt<1> extclk_cnt<2> extclk_cnt<3> net27 net19 vdd vss nor5
    Xi9 ready2 net019 vdd vss inv
    Xi3 extclk_cnt<4> net27 vdd vss inv
    Xi14 vdl_rst_0' vdl_rst_1' vdl_rst_loc vdd vss nand2
    Xi17 vdl_rst_0' cnt_rst_pre' cnt_rst vdd vss nand2
    Xi11 cnt_rst_pre' vdl_rst_rst_loc' vdl_rst_rst vdd vss nand2
    Xi5 cnt_rst_loc' rst_glob' cnt_rst_pre vdd vss nand2
    Xi18 vdl_rst_0 cnt_rst_pre cnt_rst' vdd vss nor2
    Xi15 vdl_rst_0 cnt_ready vdl_rst_loc' vdd vss nor2
    Xi12 cnt_rst_pre vdl_rst_rst_loc vdl_rst_rst' vdd vss nor2
    Xi6 cnt_rst_loc rst_glob cnt_rst_pre' vdd vss nor2
    Xi7 cnt_data<0> cnt_data<1> cnt_data<2> cnt_data<3> cnt_data<4> cnt_data<5> cnt_data<6>
        + cnt_data<7> cnt_data<8> cnt_data<9> cnt_data<10> cnt_data<11> cnt_data<12> cnt_data<13>
        + cnt_data<14> extclk_cnt<0> extclk_cnt<1> extclk_cnt<2> extclk_cnt<3> extclk_cnt<4>
        + cnt_rst_rst cnt_rst_rst' ready2 vdd vdl_rst_loc vss cnt_rst_fb
    Xi16 cnt_data<0> cnt_data<1> cnt_data<2> cnt_data<3> cnt_data<4> cnt_data<5> cnt_data<6>
         + cnt_data<7> cnt_data<8> cnt_data<9> cnt_data<10> cnt_data<11> cnt_data<12> cnt_data<13>
         + cnt_data<14> pre_rst ready_clk vdd vss cnt_vdl_rst_fb
    Xi4 ready_clk ready2 net03 cnt_rst_pre cnt_rst_pre' vdd vss dff_st_ar_dh
.ENDS
```
