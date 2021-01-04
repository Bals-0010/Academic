import csv, sys, os

def converter(generated_csv, edgelist_csv,delim):

	def error():
		sys.exit('Undefined delimiter\nAllowed delimiters are ";" and ",":\n";" - for pure csv format\n"," - for two column edges list')

	# Creating and saving gdf file in the same directory
	f = open(os.getcwd()+"\\"+"output.gdf","w+")

	# Writing node attributes
	f.write("nodedef>name VARCHAR,Modularity Class INTEGER")
	with open(generated_csv) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=",")
		next(csv_reader)
		try:
			for row in csv_reader:
				f.write("\n")
				f.write(row[0]+','+row[1])
		except IndexError:
			error()
	
	# Writing edge attributes
	f.write("\nedgedef>node1 VARCHAR,node2 VARCHAR")
	with open(edgelist_csv) as csvfile:
		if delim==";":
			csvreader = csv.reader(csvfile, delimiter=";")
		elif delim==",":
			csvreader = csv.reader(csvfile, delimiter=",")
		else:
			error()
		for r in csvreader:
			f.write("\n")
			f.write(r[0]+','+r[1])

	f.close()
	print("File saved in: ",f.name)

converter(sys.argv[1],sys.argv[2],sys.argv[3])
