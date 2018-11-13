PYTHON=/usr/bin/python3
DESTINATION=/home/jairo/Cloud/CIC/PhD/test


clean:
	find . -name "*.pgf" -exec rm {} \;

clean-all:
	find $(DESTINATION) -name "*.pgf" -exec rm {} \;

build:
	$(PYTHON) ./MANET/plot_for_paper.py -c ./MANET/results_full.csv
	$(PYTHON) ./VANET/plot_for_paper.py -c ./VANET/results_all.csv
	$(PYTHON) ./infocomm/plot_for_paper.py -c ./infocomm/results_all.csv

install:
	find . -name "*.pgf" -exec mv {} $(DESTINATION) \;

.PHONY: clean clean-all build install
