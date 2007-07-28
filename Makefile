cairo:
	./cairo_slides.py

gnu:
	./gnu_slides.py

pdf: cairo_slides.pdf

cairo_slides.pdf cairo_slides.svg cairo_slides.ps: slippy.py cairo_slides.py cairo_theme.py
	./cairo_slides.py -o $@

clean:
	$(RM) cairo_slides.ps cairo_slides.pdf cairo_slides.svg
