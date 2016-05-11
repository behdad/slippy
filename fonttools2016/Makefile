name = fonttools2016
ARGS = --geometry 1920x1200

all: $(name)_slides.pdf

view:
	python slippy.py $(name)_slides.py -t $(name)_theme.py $(ARGS)

%_slides.pdf: slippy.py %_slides.py %_theme.py
	python slippy.py $*_slides.py -t $*_theme.py -o $@ $(ARGS)

clean:
	$(RM) $(name)_slides.pdf *.pyc
