reset
set terminal pdfcairo size 12, 6 font 'Libertinus Serif,20' lw 1
set output "graph.pdf"
plot \
  'plot_data.dat' using 1:2 with lines lc rgb "black" lw 2 notitle,\
  'plot_data.dat' using 1:2:(0.1) with circles fill solid lc rgb "black" notitle,\
  'plot_data.dat' using 1:2:3 with labels tc rgb "white" offset (0,0) font 'Arial Bold' notitle
