cairo:
	./slippy.py -t cairo-theme.py cairo-slides.py

pdf: cairo-slides.pdf

cairo-slides.pdf cairo-slides.svg cairo-slides.ps: slippy.py cairo-slides.py cairo-theme.py
	./slippy.py -o $@ -t cairo-theme.py cairo-slides.py

clean:
	$(RM) cairo-slides.ps cairo-slides.pdf cairo-slides.svg
