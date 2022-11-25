run:
	poetry run python classifier.pyw

precise ?= 0.97
model ?= classified_figure.txt
search:
	poetry run python search_entry_points.py -p $(precise) -m $(model)


currency ?= eurusd
calc:
	poetry run python generate_entry_points.py --currency=$(currency)
