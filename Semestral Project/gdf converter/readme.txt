To run:
=======
> python gdf_converter.py "generated_file.csv" "edges.csv" "delimiter"
# File will be saved in the current/running directory

#Examples
> python gdf_converter.py "C:/Desktop/output.csv" "F:/Datasets/edges football.csv" ","
File saved in: C:/output.gdf

> python gdf_converter.py "C:/Desktop/output.csv" "E:/edges football.csv" ";"
File saved in: C:/output.gdf

> python gdf_converter.py "C:/Desktop/output.csv" "F:/Datasets/edges football.csv" "."
Undefined delimiter
Allowed delimiters are ';' and ',':
';' - for pure csv format
',' - for two column edges list