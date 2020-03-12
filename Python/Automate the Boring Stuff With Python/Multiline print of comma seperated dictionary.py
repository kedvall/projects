print(', '.join( \
	  [': '.join( \
	  [key, str(get_column_letter(val))]) \
	  for key, val in selectedCols.items()]))