How to run:
===========
# In the current file directory; for example: if files are in E:/Test
# input edge list file should be 2 columns

E:/Test> python
>>> from Walktrap import Walktrap
>>> wt = Walktrap(dataset="E:/Test/filename.csv", output_path="E:/Test") 
>>> wt.desc_stats() #shows the short description of the dataset
>>> wt.save_stats_txt() #saves only the statistics in to a txt file
>>> wt.run_walktrap(1) # parameter: t steps 
>>> wt.results() #shows only modularity and no. of communities
>>> wt.save_community_csv() #saves the communities into 2 column csv with: nodeID, ModularityClass
>>> wt.community_sizes() #displays the community sizes
>>> wt.communities_list() #displays the communities list

# large datasets takes more time to run

==========
Examples: 
==========
E:/Test> python
>>> from Walktrap import Walktrap
>>> wt = Walktrap("E:/Test/edges football.csv", output_path="E:")
>>> wt.run_walktrap(1)
Steps(t):
1        
>>> wt.results()
No. of Communities:
10
Modularity:        
0.47045924490844104

>>> wt.communities_list()
Community List:
[[25, 37, 45, 89, 103, 105, 109],
 [46, 49, 53, 67, 73, 83, 88, 110, 114],
 [7, 8, 21, 22, 51, 68, 77, 78, 108, 111],
 [3, 5, 10, 40, 52, 72, 74, 81, 84, 98, 102, 107],
 [19, 29, 30, 35, 55, 79, 80, 82, 94, 101],
 [44, 48, 57, 66, 75, 86, 91, 92, 112],
 [14, 18, 31, 34, 38, 43, 54, 61, 71, 85, 99],
 [1, 17, 20, 27, 33, 56, 62, 65, 70, 76, 87, 95, 96, 113],
 [0, 4, 9, 11, 16, 23, 24, 28, 41, 50, 69, 90, 93, 104],
 [2, 6, 12, 13, 15, 26, 32, 36, 39, 42, 47, 58, 59, 60, 63, 64, 97, 100, 106]]

>>> wt.community_sizes()
Community Sizes:
[7, 9, 10, 12, 10, 9, 11, 14, 14, 19]
