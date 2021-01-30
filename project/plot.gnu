reset
set terminal pdfcairo size 14, 6 font 'Libertinus Serif,20' lw 1
set output "graph.pdf"
set grid
set key box left top Left reverse height 2
set ylabel "CPU time (s)"
set xlabel "Number of links"
plot \
  'plot_data.dat' u 2:1 w p ls 1 pt 1 pointsize 1 notitle,\
  'linreg' u 1:2 w l title 'Linear regression of the data'
