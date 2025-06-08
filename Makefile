all: fig2 fig3 fig5 fig6 fig7 fig8 fig9 fig10
.PHONY: all fig2 fig3 fig5 fig6 fig7 fig8 fig9 fig10

fig2:
	cd Fig-2 && python3 plot.py

fig3:
	cd Fig-3 && python3 plot.py

fig5:
	cd Fig-5 && python3 plot.py

fig6:
	cd Fig-6 && python3 plot.py

fig7:
	cd Fig-7 && python3 plot.py

fig8:
	cd Fig-8 && python3 plot.py

fig9:
	cd Fig-9 && python3 plot.py

fig10:
	cd Fig-10 && python3 plot.py && python3 plot-heatmap.py