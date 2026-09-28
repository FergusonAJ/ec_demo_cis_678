library(ggplot2)

data = read.csv('example_dataset.csv')

ggplot(data, aes(x = x, y = f_x)) + 
  geom_point()
