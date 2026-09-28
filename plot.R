library(ggplot2)
library(cowplot)

raw_data = read.csv('evo_results.csv')

ggplot(raw_data, aes(x = gen)) + 
  geom_hline(aes(yintercept = 100), linetype = 'dashed', alpha = 0.5) + 
  geom_line(aes(y = max_fitness, color = 'Max fitness')) + 
  geom_line(aes(y = avg_fitness, color = 'Average fitness')) + 
  theme_cowplot() + 
  theme(legend.position = 'bottom') + 
  labs(color = '') + 
  xlab('Generation') + 
  ylab('Fitness') + 
  scale_color_manual(values = c('Max fitness' = '#000000', 'Average fitness' = '#ff0000'))
ggsave('./evo_results.png')
