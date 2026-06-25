$aux_dir = 'build';
$out_dir = '.';
$fdb_file = 'build/main.fdb_latexmk';
$pdflatex = 'pdflatex %O %S; cp build/%R.bbl %R.bbl 2>/dev/null || true';
$bibtex = 'bibtex %O %B; cp build/%R.bbl %R.bbl 2>/dev/null || true';
