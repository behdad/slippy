show:
	./slippy.py slides.py theme.py

pdf: slides.pdf

slides.pdf slides.svg slides.ps: slippy.py slides.py theme.py
	python $^ $@

clean:
	$(RM) slides.ps slides.ps slides.pdf
