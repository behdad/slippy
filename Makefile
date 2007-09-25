cairoprinting:
	./textextraction_slides.py

cairo:
	./cairo_slides.py

gnu:
	./gnu_slides.py

%_slides.pdf %_slides.svg %_slides.ps: slippy.py %_slides.py %_theme.py
	./$*_slides.py -o $@

clean:
	$(RM) cairo_slides.ps cairo_slides.pdf cairo_slides.svg
