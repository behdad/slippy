name = fonttools

all: $(name)_slides.pdf

view:
	python slippy.py $(name)_slides.py -t $(name)_theme.py

%_slides.pdf: slippy.py %_slides.py %_theme.py
	python slippy.py $*_slides.py -t $*_theme.py -o $@

clean:
	$(RM) $(name)_slides.pdf *.pyc
