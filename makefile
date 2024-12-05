HW_DIR := hardware/
FIG_DIR := figures/

FIG_PY_DIR := $(FIG_DIR)python/
FIG_SVG_DIR := $(FIG_DIR)svg/
FIG_PDF_DIR := $(FIG_DIR)pdf/
FIG_DAT_DIR := $(FIG_DIR)data/

HW_MODULES := $(shell basename $(shell find $(HW_DIR) -mindepth 1 -maxdepth 1 -type d))
HW_SVGS := $(join $(addprefix $(HW_DIR), $(addsuffix /, $(HW_MODULES))), $(addsuffix .svg, $(HW_MODULES)))
HW_PNGS := $(join $(addprefix $(HW_DIR), $(addsuffix /, $(HW_MODULES))), $(addsuffix .png, $(HW_MODULES)))
HW_CIRS := $(join $(addprefix $(HW_DIR), $(addsuffix /, $(HW_MODULES))), $(addsuffix .cir, $(HW_MODULES)))
HW_MDS := $(addsuffix readme.md, $(addprefix $(HW_DIR), $(addsuffix /, $(HW_MODULES))))

FIG_PY_FILES := $(shell find $(FIG_PY_DIR) -type f -name "*.py")
FIG_SVG_FILES := $(shell find $(FIG_SVG_DIR) -type f -name "*.svg")
FIG_PY_SVGS := $(addprefix $(FIG_SVG_DIR), $(addsuffix .svg, $(basename $(notdir $(FIG_PY_FILES)))))
FIG_PY_PDFS := $(addprefix $(FIG_PDF_DIR), $(addsuffix .pdf, $(basename $(notdir $(FIG_PY_FILES)))))
FIG_SVG_PDFS := $(addprefix $(FIG_PDF_DIR), $(addsuffix .pdf, $(basename $(notdir $(FIG_SVG_FILES)))))

.SECONDEXPANSION:

all: hw fig

hw: hw_md hw_cir

hw_svg: $(HW_SVGS)

hw_png: $(HW_PNGS)

hw_cir: $(HW_CIRS)

hw_md: $(HW_MDS)

$(HW_DIR)%.svg: $(HW_DIR)%.gds
	python3 lib/gds_to_svg.py -m $(shell basename $*)

$(HW_DIR)%.png: $(HW_DIR)%.svg
	rsvg-convert -h 8192 -w 8192 --keep-aspect-ratio $< > $@

$(HW_DIR)%.cir: $(HW_DIR)%.rcir
	python3 lib/circ_parser.py -m $(shell basename $*)

$(HW_DIR)%/readme.md: $(HW_DIR)$$*/$$*.png
	echo '# `$*` Module' > $@
	echo '![Layout]($*.png)' >> $@

fig: $(FIG_PDF_DIR) $(FIG_PY_PDFS) $(FIG_SVG_PDFS)

fig_svg: $(FIG_SVG_DIR) $(FIG_PY_SVGS)

$(FIG_PDF_DIR)%.pdf: $(FIG_SVG_DIR) $(FIG_SVG_DIR)%.svg
	rsvg-convert -f pdf -o $@ $(FIG_SVG_DIR)$*.svg

$(FIG_SVG_DIR)%.svg: $(FIG_PY_DIR)%.py $(FIG_DAT_DIR) $(FIG_DAT_DIR)%.csv
	python3 $<

$(FIG_DAT_DIR)%.csv: $(FIG_PY_DIR)%.py
	python3 $< -dq

.PRECIOUS: $(FIG_DAT_DIR) $(FIG_DAT_DIR)%.csv

%/:
	mkdir $@

clean: clean_hw clean_fig

realclean: realclean_hw realclean_fig

mrproper: mrproper_hw mrproper_fig

clean_hw: clean_hw_png clean_hw_md

realclean_hw: clean_hw clean_hw_cir

mrproper_hw: realclean_hw clean_hw_svg

clean_hw_svg:
	rm -f $(HW_SVGS)

clean_hw_png:
	rm -f $(HW_PNGS)

clean_hw_cir:
	rm -f $(HW_CIRS)

clean_hw_md:
	rm -f $(HW_MDS)

clean_fig: clean_fig_pdf

realclean_fig: clean_fig clean_fig_data clean_fig_svg

mrproper_fig: realclean_fig

clean_fig_pdf:
	rm -f $(FIG_PY_PDFS) $(FIG_SVG_PDFS)
	rm -df $(FIG_PDF_DIR)

clean_fig_svg:
	rm -f $(addprefix $(FIG_SVG_DIR), $(addsuffix .svg, $(basename $(notdir $(FIG_PY_FILES)))))
	rm -df $(FIG_SVG_DIR)

clean_fig_data:
	rm -f $(addprefix $(FIG_DAT_DIR), $(addsuffix .csv, $(basename $(notdir $(FIG_PY_FILES)))))
	rm -df $(FIG_DAT_DIR)