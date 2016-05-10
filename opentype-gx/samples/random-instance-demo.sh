#!/bin/bash

if test $# -lt 2; then
	echo "usage: $0 font.ttf text" >&2
	exit 2
fi
font=$1
outfont=${font%.ttf}-instance.ttf
outpng=${outfont%.ttf}.png
text=$2

python list-axes.py $font |
while read tag min default max; do
	rnd=`python -c "print $((RANDOM%(100*(max-min))+min))/100."`
	echo "$tag=$rnd"
done | tee | (
	xargs python varLib/mutator.py "$font" &&
	hb-view "$outfont" "$text" > "$outpng" &&
	(display "$outpng" &)
)
