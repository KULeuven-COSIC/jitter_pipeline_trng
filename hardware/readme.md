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

The following hierarchy is used in the ASIC (each cell can be expanded to show its components):

<details>
    <summary>top_level</summary>
    <blockquote>
        <details>
            <summary>pad_frame</summary>
            <blockquote>
                <ul>
                    <li>in_pad</li>
                    <li>in_pad</li>
                    <li>in_pad</li>
                    <li>in_pad</li>
                    <li>in_pad</li>
                    <li>in_pad</li>
                    <li>out_pad</li>
                    <li>out_pad</li>
                    <li>out_pad</li>
                    <li>vdd_0_pad</li>
                    <li>vdd_1_pad</li>
                    <li>vdd_io_pad</li>
                    <li>vdd_pad</li>
                    <li>vss_0_pad</li>
                    <li>vss_1_pad</li>
                    <li>vss_pad</li>
                </ul>
            </blockquote>
        </details>
        <details>
            <summary>core_top</summary>
            <blockquote>
                <details>
                    <summary>control_dc_vdl_send_combo</summary>
                    <blockquote>
                        <details>
                            <summary>dc_vdl_combo</summary>
                            <blockquote>
                                <details>
                                    <summary>dc_top</summary>
                                    <blockquote>
                                        <details>
                                            <summary>dc_branch</summary>
                                            <blockquote>
                                                <ul>
                                                    <li>buf_wide</li>
                                                    <li>dc_ch_4</li>
                                                    <li>dc_rst_check</li>
                                                    <li>enable_n</li>
                                                    <li>first_edge</li>
                                                    <li>freq_scaler_248</li>
                                                    <li>inv</li>
                                                    <li>mux4</li>
                                                    <li>nand2</li>
                                                    <li>nand2_dnw</li>
                                                </ul>
                                            </blockquote>
                                        </details>
                                        <details>
                                            <summary>dc_branch</summary>
                                            <blockquote>
                                                <ul>
                                                    <li>buf_wide</li>
                                                    <li>dc_ch_4</li>
                                                    <li>dc_rst_check</li>
                                                    <li>enable_n</li>
                                                    <li>first_edge</li>
                                                    <li>freq_scaler_248</li>
                                                    <li>inv</li>
                                                    <li>mux4</li>
                                                    <li>nand2</li>
                                                    <li>nand2_dnw</li>
                                                </ul>
                                            </blockquote>
                                        </details>
                                        <ul>
                                            <li>rst_start</li>
                                        </ul>
                                    </blockquote>
                                </details>
                                <details>
                                    <summary>vdl_top</summary>
                                    <blockquote>
                                        <details>
                                            <summary>vdl_branch</summary>
                                            <blockquote>
                                                <ul>
                                                    <li>buf_en</li>
                                                    <li>edge_to_level</li>
                                                    <li>vdl_oo_3</li>
                                                </ul>
                                            </blockquote>
                                        </details>
                                        <details>
                                            <summary>vdl_branch</summary>
                                            <blockquote>
                                                <ul>
                                                    <li>buf_en</li>
                                                    <li>edge_to_level</li>
                                                    <li>vdl_oo_3</li>
                                                </ul>
                                            </blockquote>
                                        </details>
                                        <ul>
                                            <li>buf_wide</li>
                                            <li>buf_wide</li>
                                            <li>end_detector</li>
                                            <li>vdl_enable</li>
                                        </ul>
                                    </blockquote>
                                </details>
                            </blockquote>
                        </details>
                        <details>
                            <summary>send_top</summary>
                            <blockquote>
                                <ul>
                                    <li>bit_cnt_chain</li>
                                    <li>bit_control</li>
                                    <li>bit_data_chain</li>
                                    <li>clk_delay_6</li>
                                    <li>cnt_control</li>
                                    <li>cnt_data_chain</li>
                                    <li>dff_st_ar</li>
                                    <li>ext_clk_cnt_chain</li>
                                    <li>ext_clk_data_chain</li>
                                    <li>mux2</li>
                                    <li>mux2</li>
                                    <li>mux2</li>
                                    <li>mux2</li>
                                    <li>mux2</li>
                                    <li>nand2</li>
                                    <li>nand2</li>
                                    <li>nor2</li>
                                    <li>nor2</li>
                                </ul>
                            </blockquote>
                        </details>
                        <ul>
                            <li>core_control</li>
                        </ul>
                    </blockquote>
                </details>
                <ul>
                    <li>conf_top</li>
                </ul>
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
- `clean_hw`: Remove all PNGs and readmes.
- `realclean_hw`: `clean_hw`and remove netlists.
- `mrproper_hw`: `realclean_hw` and remove SVGs, note that regenerating the SVGs might take a long time!