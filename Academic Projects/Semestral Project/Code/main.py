import sys, ast
import numpy as np
import networkx as nx
import math, time, xlrd
from numpy.linalg import inv, norm, matrix_power


Q, hierarchy, distances, community, communities = {},{},{},{},{}


# Choosing two closest communities and merge them
def update_communities(C1, C2, C3):
	new_P_t_C=((len(C1) * community[str(sorted(C1))])+(len(C2) * community[str(sorted(C2))]))/(len(C1) + len(C2))
	del community[str(sorted(C1))]
	del community[str(sorted(C2))]
	community[str(sorted(C3))] = new_P_t_C


# delete old distances and insert new distances
def update_distance(C1, C2, C3, C, var):
	distances.pop(sort_communities_str(C1, C2), None)
	distances.pop(sort_communities_str(C1, C), None)
	distances.pop(sort_communities_str(C2, C), None)
	distances[sort_communities_str(C3, C)] = var


# calculate distance between merged and all other communities
def calculate_distance_c(C1, C2, C3):
	return ( \
		((len(C1) + len(C3)) * distances[sort_communities_str(C1, C3)]) + \
		((len(C2) + len(C3)) * distances[sort_communities_str(C2, C3)]) + \
		(len(C3) * distances[sort_communities_str(C1, C2)]) ) / \
		(len(C1) + len(C2) + len(C3))


# choose communities based on best distance
def choose_communities():
	return string_list_to_lists(min(distances, key=distances.get)) 


# calculate modularity
def calculate_mod(i, Graph):
	q, edges = 0, Graph.number_of_edges()
	for C in hierarchy[i]:
		CG = nx.subgraph(Graph, C)
		links_in_C = CG.number_of_edges()
		links_to_C = len(Graph.edges(C))
		q += (links_in_C / edges) - ((links_to_C / edges)**2)
	Q[i] = q


# calculate distance newly merged community with other community
def calculate_distance(C1, C2, C3):
	return (distances.get(sort_communities_str(C1, C2)) is not None and 
		distances.get(sort_communities_str(C1, C3)) is not None and
		distances.get(sort_communities_str(C2, C3)) is not None)


# calculate distance based on links
def calculate_distance_links(N, Dd, C1, C2):
	return (((len(C1) * len(C2)) / (len(C1) + len(C2))) * 
		norm((Dd @ community[str(sorted(C1))]) - 
			(Dd @ community[str(sorted(C2))]))) / N


# calculate distance from a community to all its adjacent vertices
def community_to_adj(R_t, C):
	if C != []:
		N = len(R_t)
		R_t_C =	np.zeros(N)

		for j in range(N):
			total = 0 
			for i in C:
				total = total + R_t.item((i-1, j))
			R_t_C[j] = total / len(C) 
		return R_t_C 

# convert a string list into integer list
def string_list_to_lists(s):
	return (ast.literal_eval(s[:s.index("]",2)+1]),
		ast.literal_eval(s[s.index("]")+1:]))

# sort commumities 
def sort_communities(C1, C2):
	return sorted(min(C1, C2) + max(C1, C2))


def sort_communities_str(C1, C2):
	return (str(min(C1, C2)) + str(max(C1, C2)))


def waltrap(Graph,t,N, AMatrix, DMatrix):
	print("\nSteps(t):")
	print(t)
	N = Graph.number_of_nodes()
	Dtemp = np.diagonal(DMatrix)
	Dd = np.diag(np.power(Dtemp, (-0.5)))
	P = inv(DMatrix) @ AMatrix # Probability Matrix P
	R_t = matrix_power(P, t) # Distance Matrix P^t
	# Initialize hierarchy 1, its modularity, and community
	hier_cuts = []
	for n in Graph.nodes:
		communities[n] = [n]
		hier_cuts.append([n])
	hierarchy[1] = hier_cuts
	calculate_mod(1, Graph)

	# Populate initial community dictionary
	for C in hier_cuts:
		community[str(C)] = community_to_adj(R_t, C)

	# Populate initial distances
	for (s, d) in Graph.edges:
		if s != d:
			distances[sort_communities_str([s], [d])] = \
				calculate_distance_links(N, Dd, [s], [d])

	for step in range(1,N):
		# Choose first two communities based on distance
		(C1,C2) = choose_communities()
		C3 = sort_communities(C1, C2)
		# Insert new hierarchy and its modularity 
		hier_cuts = list(hierarchy.get(step))
		hier_cuts.remove(C1)
		hier_cuts.remove(C2)
		hier_cuts.append(C3)
		hierarchy[step+1] = hier_cuts
		calculate_mod(step+1, Graph)
		update_communities(C1, C2, C3)
		adj_vertices = set()
		for v in C3:
			communities[v] = sorted(C3)
			adj_vertices |= set(Graph.adj[v])
		adj_vertices = list(adj_vertices - set(C3)) # delete duplicates nodes present in C3

		# Find communities present for each node
		adj_communities = []
		for C in adj_vertices:
			adj_communities.append(communities[C])

		adj_communities = \
			list(dict((x[0], x) for x in adj_communities).values())

		for C in adj_communities:
			var = 0
			if calculate_distance(C1, C2, C):
				var = calculate_distance_c(C1, C2, C)
			else:
				var = calculate_distance_links(N, Dd, C3, C)
			update_distance(C1, C2, C3, C, var)
	return hierarchy[max(Q, key=Q.get)], max(Q.values())

