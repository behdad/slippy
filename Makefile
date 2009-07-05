all: stateoftext
	@:

%:
	./$@_slides.py

%_slides.pdf %_slides.svg %_slides.ps: slippy.py %_slides.py %_theme.py
	./$*_slides.py -o $@

clean:
	$(RM) *_slides.ps *_slides.pdf *_slides.svg
