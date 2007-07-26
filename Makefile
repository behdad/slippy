show:
	./slippy.py -t theme.py slides.py

pdf: slides.pdf

slides.pdf slides.svg slides.ps: slippy.py slides.py theme.py
	./slippy.py -o $@ -t theme.py slides.py

clean:
	$(RM) slides.ps slides.ps slides.pdf
