# vim: set fileencoding=utf-8 :
# Written by Behdad Esfahbod, 2014
# Not copyrighted, in public domain.

# A theme file should define two functions:
#
# - prepare_page(renderer): should draw any background and return a tuple of
#   x,y,w,h that is the area to use for slide canvas.
# 
# - draw_bubble(renderer, x, y, w, h, data=None): should setup canvas for the
#   slide to run.  Can draw a speaking-bubble for example.  x,y,w,h is the
#   actual extents that the slide will consume.  Data will be the user-data
#   dictionary from the slide.
#
# Renderer is an object similar to a cairo.Context and pangocairo.CairoContext
# but has its own methods too.  The more useful of them here are put_text and
# put_image.  See their pydocs.

import cairo

avatar_margin = .10
logo_margin = .01
footer_margin = .03
padding = .000
bubble_rad = .25

fg_color = (.2,.2,.2)
palette = [
(0x0f,0x00,0x7e),
(0x74,0x00,0xa5),
(0xae,0x00,0x92),
(0xdf,0x00,0x4e),
(0xff,0x1a,0x0f),
(0xff,0x42,0x04),
(0xf1,0x90,0x00),
(0xff,0xbc,0x00),
]
palette = palette + list(reversed(palette[1:-1]))
palette_cairo = [tuple(c/1. for c in color) for color in palette]
palette = ["#%02x%02x%02x" % color for color in palette]
j = 0

def prepare_page (renderer):
	cr = renderer.cr
	width = renderer.width
	height = renderer.height
	
	a = avatar_margin * width
	s = (logo_margin + footer_margin) * .5 * width
	l = logo_margin * height
	f = footer_margin * height
	p = padding * min (width, height)
	p2 = 2 * p

	cr.set_source_rgb (.9, .9, .9)
	cr.paint ()
	cr.set_source_rgb (*fg_color)

	cr.move_to (.5 * width, height-p2)
	text = unicode("Behdad Esfahbod | FontTools/TTX|TYPO Labs Berlin | 11 may 2016")
	letters = []
	global j
	for i,c in enumerate(text):
		color = palette[(i+j) % len(palette)]
		letters.append('<span foreground="%s">%s</span>' % (color, c))
	j -= 1
	markup = ''.join(letters)
	renderer.put_text (markup, height=f-p2, valign=-1, desc="")

	# Compute rectangle available for slide content
	w = width - s - s - p * 2
	x = s + p
	h = height - l - f - p * 2
	y = l + p

	# Adjust for bubble padding. the 8 comes from bezier calculations
	d = min (w, h) * bubble_rad / 8.
	x, y, w, h = x + d, y + d, w - d*2, h - d*2


	return x, y, w, h

def draw_bubble (cr, x, y, w, h, data={}):
	cr.set_source_rgb (*fg_color)
