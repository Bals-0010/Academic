import main
import csv, sys, itertools, pprint
import networkx as nx
import numpy as np
from numpy.linalg import inv, norm, matrix_power

class Walktrap:
	
	# dataset: full path of dataset, example: dataset="E:/folder/karate.csv"
	# output_path: path where files desc stats or community csv will be stored. example: "E:/output_folder"
	# delim: by default "," accepts only 2 column csv edge list
	def __init__(self, dataset=None, output_path=None, delim=","):
		
		self.dataset = dataset
		if self.dataset in [None,""]:
			sys.exit("Invalid dataset !")
		self.delim = delim
		
		self.output_path = output_path
		if self.output_path not in [None,""] and self.output_path[-1] != "/" and len(self.output_path)!=0:
			self.output_path = self.output_path+"/"
		else:
			sys.exit("Invalid output_path !")

		Walktrap.G = nx.Graph()
		Walktrap.G = nx.read_edgelist(self.dataset, delimiter=self.delim, create_using=nx.Graph(), nodetype=int)
		Walktrap.G.name = self.dataset.split("/")[-1]
		

	## Displays the short descriptive statistics
	def desc_stats(self):
		print(nx.info(Walktrap.G)) 


	## Saves the detailed descriptive statistics in the output path given in the main (init)
	## and the name of the file will be "stats.txt" 
	def save_stats_txt(self,save_results=False):
		if save_results:
			print("Name: "+Walktrap.G.name)
			print("No. of Nodes: "+str(Walktrap.G.number_of_nodes()))
			print("No. of Edges: "+str(Walktrap.G.number_of_edges()))
			print("No. of self-Loops: "+str(nx.number_of_selfloops(Walktrap.G)))
			print("\nDegrees:\n"+str(Walktrap.G.degree()))
		else:
			f = open(self.output_path+"stats.txt","w+")
			f.write("Name: "+Walktrap.G.name)
			f.write("\nNo. of Nodes: "+str(Walktrap.G.number_of_nodes()))
			f.write("\nNo. of Edges: "+str(Walktrap.G.number_of_edges()))
			f.write("\nNo. of self-Loops: "+str(nx.number_of_selfloops(Walktrap.G)))
			f.write("\n\nDegrees:\n"+str(Walktrap.G.degree()))
			f.close()
			print(f"Statistics file saved in: {f.name}")

	# Pre process like renaming uniform node lables, normalizing components and reverting back the original node lables
	def pre_process(self):
		a,b = [], []
		with open(self.dataset) as f:
			reader = csv.reader(f)
			for row in reader:
				a.append(int(row[0]))
				b.append(int(row[1]))
		
		G = nx.Graph()
		G = nx.read_edgelist(self.dataset, delimiter=',', create_using=nx.Graph(), nodetype=int)
		G.name = self.dataset.split("/")[-1] 
	
		components = [list(comp) for comp in nx.connected_components(G)]
		# # Below function takes total list of connected components only if the graph is disconnected
		# # and filters the largest component to work with communities
		# # Later the disconnected components will be added to the different communities
		# # This will make error free distance matrixes
		# """
		# For example: if graph is {2: 	[8, 7, 5], 
		# 							8: 	[2], 
		# 							7: 	[2, 5, 10], 
		# 							5: 	[2, 7, 4], 
		# 							4: 	[5, 10], 
		# 							10: [4, 7], 
		# 							19: [20],
		#                           20: [19]	}
		# largest connected component is [2,8,7,5,4,10] and disconnected component [19,20] 
		# hence community detection works with largest component first
		# and disconnected component will be added later to the overall communities
		# """
		def normalize_components(components):
			longest_connected_component = 0
			disconnected_components = components
			length = 0
			index = 0
			for i in components:
				if length<len(i):
					length=len(i)
					index = components.index(i)
					longest_connected_component = components[index]
					disconnected_components.remove(components[index])
			del components # Deleting duplicates to reduce memory space
			disconnected_components_count = len(disconnected_components)
			return longest_connected_component,disconnected_components, disconnected_components_count
		
		lcc, dc, self.dcc = normalize_components(components)
		dc_full_list = list(itertools.chain.from_iterable(dc)) # list disconnected component
		
		edges = [] # Updated edge list 
		for i in range(len(a)):
			if a[i] and b[i] not in dc_full_list:
				edges.append((a[i],b[i]))
		
		a = [edges[i][0] for i in range(len(edges))]
		b = [edges[i][1] for i in range(len(edges))]

		# Reads the new corrected edge list
		adj_list={}
		nodes_list=sorted(set(a+b))
		N = len(nodes_list)
		
		## Network structure may have missing nodes, example nodes may be:  2,4,5,7,8,9,10
		## In the above nodes list 6 and 1 is missing
		## Missing nodes will create 0 division error in calculations and also makes large matrix dimensions 
		## To overcome this issue: below method will assign distinct labels to nodes
		## For example: if we have edge list: [(2,8),(2,7),(2,5),(5,7),(4,5),(4,10),(7,10),(9,9)]
		## There are 7 nodes and 8 edges, and 1 self-looped + isolated node: i.e. node 9
		## node 2 will be 0 and node 4 will be 1, etc
		## map_dict will label like:  {2: 0, 4: 1, 5: 2, 7: 3, 8: 4, 9: 5, 10: 6} #Full node label list 
		self.map_dict = {nodes_list[i]:i for i in range(len(nodes_list))}

		## rev_dict is to reverse the node labels back to original labels for final results
		self.rev_dict = dict([(value, key) for key, value in self.map_dict.items()])

		## Adjacency list creation with updated node labels
		i = 0
		while i < len(a):
			adj_list.setdefault(int(self.map_dict[a[i]]), [])
			adj_list[int(self.map_dict[a[i]])].append(int(self.map_dict[b[i]]))
			if self.map_dict[a[i]] != self.map_dict[b[i]]:
				adj_list.setdefault(int(self.map_dict[b[i]]), [])
				adj_list[int(self.map_dict[b[i]])].append(int(self.map_dict[a[i]]))
			i = i + 1

		nodes = list(adj_list.keys())
		edges = [(k, val) for k, vals in adj_list.items() for val in vals]

		# AMatrix = [[0 for x in range(N)] for y in range(N)]
		AMatrix = np.zeros((N,N))
		for i in range(0, N):
			for j in range(len(adj_list[i])):
				AMatrix[i-1][adj_list[i][j]-1] = 1

		# DMatrix = [[0 for x in range(N)] for y in range(N)]
		DMatrix = np.zeros((N,N))
		for i in range(N):
			DMatrix[i][i] = len(adj_list[i])

		Graph = nx.Graph()
		Graph.add_nodes_from(nodes)
		Graph.add_edges_from(edges)
		no_of_nodes = Graph.number_of_nodes()
		no_of_edges = Graph.number_of_edges()
		N = no_of_nodes
		return AMatrix, DMatrix, Graph, N

	# Default steps(t)=1
	# Returns the communites and modularity detected
	def run_walktrap(self,steps=1):
		AMatrix, DMatrix, Graph, New_nodes = self.pre_process()
		self.communities, self.Q = main.waltrap(Graph=Graph, t=steps, N=New_nodes, AMatrix=AMatrix, DMatrix=DMatrix)
		for i in range(len(self.communities)):
			self.communities[i] = list(map(lambda x: self.rev_dict[x],self.communities[i]))
		self.results()

	def results(self):
		print("\nNo. of Communities:")
		print(len(self.communities)+self.dcc)
		print("\nModularity:")
		print(self.Q)

	def communities_list(self):
		print("\nCommunity List:")
		pprint.pprint(self.communities)

	def community_sizes(self):
		print("\nCommunity Sizes:")
		comm_sizes = list(map(len,self.communities))
		print(comm_sizes)

	# Saves the standard sys output into a result.txt file
	def save_results_txt(self):
		sys.stdout = open(self.output_path+"/results.txt","w+")
		self.save_stats_txt(save_results=True)
		self.results()
		self.communities_list()
		self.community_sizes()


	## Saves a 2 column community csv in the output path given in the main (init)
	## with 1st column: node id and 2nd column: CommunityID/ModularityClassID
	## if output path given in this method, then main output path is rewritten
	## else by default main community csv will be saved in main output path
	def save_community_csv(self):
		L = self.communities
		output_path = self.output_path
		with open(output_path+"/community.csv","w+", newline='') as file:
			csv_writer = csv.writer(file)
			csv_writer.writerow(("NodeID","ModularityClass"))
			for i in range(len(L)):
				for j in range(len(L[i])):
					csv_writer.writerow((L[i][j],i))

