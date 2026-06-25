.PHONY: pdf clean clean-all figures

ROOT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PAPER_DIR := $(ROOT_DIR)/paper
ROOT_PDF := $(ROOT_DIR)/main.pdf
MAIN_TEX := main.tex

pdf:
	@rm -f $(ROOT_PDF)
	@cd $(PAPER_DIR) && rm -f main.fdb_latexmk && latexmk -pdf $(MAIN_TEX)

figures:
	@bash figures/scripts/sync-polarization-figures.sh

clean:
	@cd $(PAPER_DIR) && latexmk -C $(MAIN_TEX)
	@cd $(PAPER_DIR) && rm -f main.fdb_latexmk
	@rm -f $(ROOT_PDF)

clean-all: clean
