data <- read.csv(file.choose(),header=F)
net <- graph.data.frame(data, directed = FALSE)

# Summary
summary(net)

# Density 
edge_density(net,loops = FALSE)

# Average degree
mean(degree(net))

# Average distance
mean_distance(net)

# Average clustering coefficient
transitivity(net,type="average", weights=NULL)

# No.of connected components
components(net)

# Assortativity
assortativity_degree(net)

# Degree distribution
# degree_distribution(net, cumulative = FALSE)
# degree(net, v = V(net), loops = FALSE, normalized = FALSE)

# Plot for degree distribution
degrees <- degree(net)
df_tb_degrees <- as.data.frame(table(degrees))

ggplot(df_tb_degrees, aes(x = degrees, y = Freq, group=1)) +
  geom_line() +
  geom_point() +
  scale_x_discrete("Nodes degree (x)",breaks=seq(0,1000, by=6))+
  scale_y_continuous("No. of nodes with degree (y)",breaks=seq(0,10000, by=400)) +
  ggtitle(filename)+ theme_bw() +
  theme(plot.title = element_text(hjust = 0.5), axis.text.x = element_text())