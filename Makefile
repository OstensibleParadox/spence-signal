.PHONY: pdf paper clean clean-all clean-root-latex figures

ROOT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PAPER_DIR := $(ROOT_DIR)/paper
PAPER_TEX := main.tex
SUPPLEMENT_TEX := supplement.tex
LATEXMK ?= latexmk
LATEXMK_FLAGS := -interaction=nonstopmode -halt-on-error -pdf

ROOT_LATEX_ARTIFACTS := \
	main.aux \
	main.bbl \
	main.blg \
	main.fdb_latexmk \
	main.fls \
	main.log \
	main.out \
	main.pdf \
	main.spl \
	main.synctex.gz \
	supplement.aux \
	supplement.bbl \
	supplement.blg \
	supplement.fdb_latexmk \
	supplement.fls \
	supplement.log \
	supplement.out \
	supplement.pdf \
	supplement.spl \
	supplement.synctex.gz

paper pdf:
	@cd $(PAPER_DIR) && rm -f $(ROOT_LATEX_ARTIFACTS)
	@cd $(PAPER_DIR) && $(LATEXMK) $(LATEXMK_FLAGS) $(PAPER_TEX)

figures:
	@bash figures/scripts/sync-polarization-figures.sh

clean-root-latex: clean

clean:
	@cd $(PAPER_DIR) && rm -f $(ROOT_LATEX_ARTIFACTS)
	@cd $(PAPER_DIR) && $(LATEXMK) -C $(PAPER_TEX) || true
	@if [ -f "$(PAPER_DIR)/$(SUPPLEMENT_TEX)" ]; then \
		cd $(PAPER_DIR) && $(LATEXMK) -C $(SUPPLEMENT_TEX) || true; \
	fi
	@rm -rf $(PAPER_DIR)/build

clean-all: clean
