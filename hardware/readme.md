# ASIC Hardware

This folder contains all the cells used to build the ASIC.
Each cell contains an SVG showing the layout and a netlist.

## File Structure

Each folder corresponds to a hardware module (cell).
Each folder contains the following files:
- *[module name].cir*: A netlist for this module.
- *[module name].svg*: The layout for this module.
- *[module name].png*: A compressed version of the layout for this module.
- *readme.md*: A `readme` file for this module.

## ASIC Hierarchy

The following hierarchy is used in the ASIC, the number in bold gives the number of MOS pairs in that cell (each cell can be expanded to show its components):

<details>
<summary><code>core_top</code> <b>3832</b> <i></i></summary>
<blockquote>
<details>
<summary><code>control_dc_vdl_send_combo</code> <b>2523</b> <i></i></summary>
<blockquote>
<details>
<summary><code>core_control</code> <b>239</b> <i></i></summary>
<blockquote>
<details>
<summary><code>mux4</code> <b>21</b> <i></i></summary>
<blockquote>
<details>
<summary><code>mux2</code> <b>7</b> <i>x3</i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>freq_scaler</code> <b>165</b> <i></i></summary>
<blockquote>
<details>
<summary><code>tff_st_ar</code> <b>15</b> <i>x11</i></summary>
<blockquote>
<details>
<summary><code>dff_st_ar</code> <b>15</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>mux8</code> <b>49</b> <i></i></summary>
<blockquote>
<details>
<summary><code>mux4</code> <b>21</b> <i>x2</i></summary>
<blockquote>
<details>
<summary><code>mux2</code> <b>7</b> <i>x3</i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>mux2</code> <b>7</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>nand2</code> <b>2</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i>x2</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>dc_vdl_combo</code> <b>981</b> <i></i></summary>
<blockquote>
<details>
<summary><code>dc_top</code> <b>676</b> <i></i></summary>
<blockquote>
<details>
<summary><code>rst_start</code> <b>132</b> <i></i></summary>
<blockquote>
<details>
<summary><code>mux2</code> <b>7</b> <i>x2</i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>nand2</code> <b>2</b> <i>x6</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nor5</code> <b>5</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x5</i></li>
<li><code>p_mos</code> <b>0</b> <i>x5</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nor2</code> <b>2</b> <i>x5</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand2_wide</code> <b>2</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nor2_wide</code> <b>2</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>dff_st_ar_dh</code> <b>14</b> <i>x6</i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv_dh</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>dc_branch</code> <b>272</b> <i>x2</i></summary>
<blockquote>
<details>
<summary><code>first_edge</code> <b>14</b> <i></i></summary>
<blockquote>
<details>
<summary><code>dff_st_ar_dh</code> <b>14</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv_dh</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>mux4</code> <b>21</b> <i></i></summary>
<blockquote>
<details>
<summary><code>mux2</code> <b>7</b> <i>x3</i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>enable_n</code> <b>38</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nor2</code> <b>2</b> <i>x2</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>dff_st_ar_dh</code> <b>14</b> <i>x2</i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv_dh</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>nand2</code> <b>2</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>freq_scaler_248</code> <b>45</b> <i></i></summary>
<blockquote>
<details>
<summary><code>tff_st_ar</code> <b>15</b> <i>x3</i></summary>
<blockquote>
<details>
<summary><code>dff_st_ar</code> <b>15</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>dc_ch_4</code> <b>140</b> <i></i></summary>
<blockquote>
<details>
<summary><code>inv_ch_2</code> <b>3</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv_ch_8</code> <b>9</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>p_mos</code> <b>0</b> <i>x9</i></li>
<li><code>n_mos</code> <b>0</b> <i>x9</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv_ch_4</code> <b>5</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>p_mos</code> <b>0</b> <i>x5</i></li>
<li><code>n_mos</code> <b>0</b> <i>x5</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv_ch_1</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv_ch_8l_mod</code> <b>16</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>p_mos</code> <b>0</b> <i>x16</i></li>
<li><code>n_mos</code> <b>0</b> <i>x16</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand2_dnw</code> <b>2</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>buf_wide</code> <b>2</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>dc_rst_check</code> <b>7</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand5</code> <b>5</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x5</i></li>
<li><code>p_mos</code> <b>0</b> <i>x5</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i>x2</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>vdl_top</code> <b>305</b> <i></i></summary>
<blockquote>
<details>
<summary><code>vdl_branch</code> <b>60</b> <i>x2</i></summary>
<blockquote>
<details>
<summary><code>edge_to_level</code> <b>21</b> <i></i></summary>
<blockquote>
<details>
<summary><code>dff_st_ar</code> <b>15</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>nor2</code> <b>2</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand2</code> <b>2</b> <i>x2</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>vdl_oo_3</code> <b>36</b> <i></i></summary>
<blockquote>
<details>
<summary><code>vdl_oo_2</code> <b>34</b> <i></i></summary>
<blockquote>
<details>
<summary><code>inv_oo_dc_0</code> <b>1</b> <i>x2</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv_oo_dc_1</code> <b>2</b> <i>x16</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>nand2_dnw</code> <b>2</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>buf_en</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>vdl_enable</code> <b>18</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nor2</code> <b>2</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>dff_st_ar_dh</code> <b>14</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv_dh</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>end_detector</code> <b>163</b> <i></i></summary>
<blockquote>
<details>
<summary><code>dff_st_ar</code> <b>15</b> <i>x6</i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i>x8</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>xor2</code> <b>6</b> <i></i></summary>
<blockquote>
<details>
<summary><code>inv</code> <b>1</b> <i>x2</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
<ul>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>tff_st_ar</code> <b>15</b> <i></i></summary>
<blockquote>
<details>
<summary><code>dff_st_ar</code> <b>15</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>mux2</code> <b>7</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>buf_wide</code> <b>2</b> <i>x2</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand2</code> <b>2</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>dff_st_ar_dh</code> <b>14</b> <i>x2</i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv_dh</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>buf_wide</code> <b>2</b> <i>x2</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>send_top</code> <b>1303</b> <i></i></summary>
<blockquote>
<details>
<summary><code>bit_control</code> <b>119</b> <i></i></summary>
<blockquote>
<details>
<summary><code>dff_st_ar</code> <b>15</b> <i>x4</i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nor2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nor4</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>bit_rst_fb</code> <b>23</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nor4</code> <b>4</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nor5</code> <b>5</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x5</i></li>
<li><code>p_mos</code> <b>0</b> <i>x5</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand5</code> <b>5</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x5</i></li>
<li><code>p_mos</code> <b>0</b> <i>x5</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>dff_st_ar_dh</code> <b>14</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv_dh</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>ext_clk_data_chain</code> <b>478</b> <i></i></summary>
<blockquote>
<details>
<summary><code>ext_clk_data_chain_el</code> <b>29</b> <i>x16</i></summary>
<blockquote>
<details>
<summary><code>mux2</code> <b>7</b> <i>x2</i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>dff_st_ar</code> <b>15</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>dff_st_ar_dh</code> <b>14</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv_dh</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>bit_cnt_chain</code> <b>60</b> <i></i></summary>
<blockquote>
<details>
<summary><code>tff_st_ar</code> <b>15</b> <i>x4</i></summary>
<blockquote>
<details>
<summary><code>dff_st_ar</code> <b>15</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>bit_data_chain</code> <b>136</b> <i></i></summary>
<blockquote>
<details>
<summary><code>dff_inv</code> <b>17</b> <i>x8</i></summary>
<blockquote>
<details>
<summary><code>inv</code> <b>1</b> <i>x2</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>dff_st_ar</code> <b>15</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>ext_clk_cnt_chain</code> <b>75</b> <i></i></summary>
<blockquote>
<details>
<summary><code>tff_st_ar</code> <b>15</b> <i>x5</i></summary>
<blockquote>
<details>
<summary><code>dff_st_ar</code> <b>15</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>clk_delay_6</code> <b>6</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x6</i></li>
<li><code>p_mos</code> <b>0</b> <i>x6</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>cnt_data_chain</code> <b>225</b> <i></i></summary>
<blockquote>
<details>
<summary><code>tff_st_ar</code> <b>15</b> <i>x15</i></summary>
<blockquote>
<details>
<summary><code>dff_st_ar</code> <b>15</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>mux2</code> <b>7</b> <i>x5</i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>nand2</code> <b>2</b> <i>x2</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nor2</code> <b>2</b> <i>x2</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>cnt_control</code> <b>146</b> <i></i></summary>
<blockquote>
<details>
<summary><code>dff_st_ar</code> <b>15</b> <i>x4</i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>nor5</code> <b>5</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x5</i></li>
<li><code>p_mos</code> <b>0</b> <i>x5</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i>x2</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand2</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nor2</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>cnt_rst_fb</code> <b>28</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nor5</code> <b>5</b> <i>x2</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x5</i></li>
<li><code>p_mos</code> <b>0</b> <i>x5</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nor4</code> <b>4</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand5</code> <b>5</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x5</i></li>
<li><code>p_mos</code> <b>0</b> <i>x5</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>cnt_vdl_rst_fb</code> <b>21</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nor4</code> <b>4</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand4</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>dff_st_ar_dh</code> <b>14</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x3</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>inv_dh</code> <b>1</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>dff_st_ar</code> <b>15</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>conf_top</code> <b>1309</b> <i></i></summary>
<blockquote>
<details>
<summary><code>dff_inv_c</code> <b>17</b> <i>x77</i></summary>
<blockquote>
<details>
<summary><code>dff_st_ar</code> <b>15</b> <i></i></summary>
<blockquote>
<details>
<summary><code>nand2</code> <b>2</b> <i>x4</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x2</i></li>
<li><code>p_mos</code> <b>0</b> <i>x2</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3_r</code> <b>4</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x4</i></li>
<li><code>p_mos</code> <b>0</b> <i>x4</i></li>
</ul>
</blockquote>
</details>
<details>
<summary><code>nand3</code> <b>3</b> <i></i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i>x3</i></li>
<li><code>p_mos</code> <b>0</b> <i>x3</i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><code>inv</code> <b>1</b> <i>x2</i></summary>
<blockquote>
<ul>
<li><code>n_mos</code> <b>0</b> <i></i></li>
<li><code>p_mos</code> <b>0</b> <i></i></li>
</ul>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>

## Make Usage

Use the provided *makefile* to generate the layout figures and netlists.
The following make targets are available:

- `hw_svg`: Generate all SVGs, the corresponding GDS files are required (not provided in the public archive).
- `hw_png`: Generate all PNGs from the SVG files.
- `hw_cir`: Generate all netlists, the corresponding raw netlists are required (not provided in the public archive).
- `hw_md`: Generate all readmes, the corresponding PNG files are required.
- `hw_top_md`: Generate this readme.
- `clean_hw`: Remove all PNGs and readmes.
- `realclean_hw`: `clean_hw` and remove netlists.
- `mrproper_hw`: `realclean_hw`, remove this readme and remove SVGs, note that regenerating the SVGs might take a long time!
