.PHONY: pdf clean clean-all figures

ROOT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PAPER_DIR := $(ROOT_DIR)/paper
ROOT_PDF := $(ROOT_DIR)/main.pdf
MAIN_TEX := main.tex
PAPER_ROOT_AUX := main.aux main.blg main.log main.out main.fdb_latexmk main.fls

pdf:
	@rm -f $(ROOT_PDF)
	@cd $(PAPER_DIR) && rm -f $(PAPER_ROOT_AUX) && latexmk -pdf $(MAIN_TEX)

figures:
	@bash figures/scripts/sync-polarization-figures.sh

clean:
	@cd $(PAPER_DIR) && latexmk -C $(MAIN_TEX)
	@cd $(PAPER_DIR) && rm -f $(PAPER_ROOT_AUX)
	@rm -f $(ROOT_PDF)

clean-all: clean
