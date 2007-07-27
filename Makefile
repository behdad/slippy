cairo:
	./slippy.py -t cairo_theme.py cairo_slides.py

pdf: cairo_slides.pdf

cairo_slides.pdf cairo_slides.svg cairo_slides.ps: slippy.py cairo_slides.py cairo_theme.py
	./slippy.py -o $@ -t cairo_theme.py cairo_slides.py

clean:
	$(RM) cairo_slides.ps cairo_slides.pdf cairo_slides.svg
