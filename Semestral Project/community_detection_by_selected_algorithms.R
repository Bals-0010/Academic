data <- read.csv(file.choose(),header=F)
net <- graph.data.frame(data, directed = FALSE)

grps<-cluster_edge_betweenness(net)

grps<-cluster_fast_greedy(net)
## Remove duplicate edges
#G <-simplify(net)
#grps<-cluster_fast_greedy(G)

grps<-cluster_infomap(net)

grps<-cluster_label_prop(net)

grps<-cluster_leading_eigen(net, options=list(maxiter=1000000))

grps<-cluster_louvain(net)

grps<-cluster_spinglass(net)

grps <- cluster_walktrap(net, steps=1, modularity = TRUE, membership = TRUE)

## plot Community distribution
comm_sizes <- sizes(grps)
## comm_sizes
df_comm_sizes<- as.data.frame(table(comm_sizes))
## df_comm_sizes
ggplot(df_comm_sizes, aes(x = comm_sizes, y = Freq)) +
  geom_bar(stat="identity", fill="steelblue") +
  ## scale_x_discrete("community size (x)") + #, breaks=seq(0,10000, by=4))
  ## scale_y_discrete("No. of communities of this size (y)", breaks=seq(0,100, by=1)) +
  ggtitle("cluster_walktrap(10)") + theme_bw() +
  labs(y= "No. of communities of this size (y)", x = "Community size (x)")+
  theme(plot.title = element_text(hjust = 0.5), axis.text.x = element_text(size=6))


modularity(grps)
length(grps)
sizes(grps) 
## grps[0:length(grps) ] # Print all lines
members <- membership(grps) #for visualization 

## ================================================================================================
## Exporting R communities into Gephi format
edges_df<- as_long_data_frame(net) # getting igraph edges into data frame
edges_df<-within(edges_df, rm(from, to)) # removing metadata from graph data frame, just to keep from and to
# colnames(edges)

names(edges_df)[1]<-"V1" # renaming colname into V1
names(edges_df)[2]<-"V2" # renaming colname into V2
# edges_df

nodes_df<-data.frame("ID"=names(members),"NAME"=names(members))
nodes_att<-data.frame("Modularity Class"=c(members))


## Writing as a gexf file for Gephi visualization
##path_to_save_gexf_file = "E:/cluster_edge_betweenness.gexf"
##write.gexf(nodes=nodes_df,edges=edges_df,nodesAtt=nodes_att, #defaultedgetype="undirected", output=path_to_save_gexf_file)
## =====================================================


## saves node id and modularity class from dataframe into csv
## for gdf conversion for Gephi visualization
filename=""
test_df <-data.frame("ID"=names(members), "MODULARITY CLASS"=c(members))
write.csv(test_df, paste("C:/Users/Bala/Desktop/",filename,".csv", sep=""),row.names = F)
## =================================================================================================