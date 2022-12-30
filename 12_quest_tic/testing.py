from pyheat import PyHeat
ph = PyHeat("mrfutils_heat.py")
ph.create_heatmap()
# To view the heatmap.
# To output the heatmap as a file.
ph.show_heatmap(output_file='image_file.svg')
ph.show_heatmap(output_file='image_file.png')
ph.show_heatmap(output_file='image_file.eps')