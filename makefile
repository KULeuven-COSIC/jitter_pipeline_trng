HW_DIR := hardware/
MD_FILE := /readme.md

HW_MODULES := $(shell basename $(shell find $(HW_DIR) -mindepth 1 -maxdepth 1 -type d))
HW_SVGS := $(join $(addprefix $(HW_DIR), $(addsuffix /, $(HW_MODULES))), $(addsuffix .svg, $(HW_MODULES)))
HW_PNGS := $(join $(addprefix $(HW_DIR), $(addsuffix /, $(HW_MODULES))), $(addsuffix .png, $(HW_MODULES)))
HW_MDS := $(addsuffix readme.md, $(addprefix $(HW_DIR), $(addsuffix /, $(HW_MODULES))))

.SECONDEXPANSION:

all: hw_md

hw_svg: $(HW_SVGS)

hw_png: $(HW_PNGS)

hw_md: $(HW_MDS)

$(HW_DIR)%.svg: $(HW_DIR)%.gds
	python3 lib/gds_to_svg.py -m $(shell basename $*)

$(HW_DIR)%.png: $(HW_DIR)%.svg
	rsvg-convert -h 8192 -w 8192 --keep-aspect-ratio $< > $@

$(HW_DIR)%/readme.md: $(HW_DIR)$$*/$$*.png
	echo '# `$*` Module' > $@
	echo '![Layout]($*.png)' >> $@

clean: clean_hw_svg

clean_hw_svg:
	rm -f $(HW_SVGS)

clean_hw_png:
	rm -f $(HW_PNGS)

clean_hw_md:
	rm -f $(HW_MDS)

%/:
	mkdir $@