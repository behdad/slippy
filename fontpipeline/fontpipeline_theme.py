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

fg_color = (.3,.3,.3)
bg_color = (0xf6/255., 0x48/255., 0x48/255.)

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

	cr.set_source_rgb (1, 1, 1)
	cr.paint ()
	cr.set_source_rgb (*fg_color)

	cr.move_to (.5 * width, height-p2)
	text = unicode("Behdad Esfahbod | Pipeline | ATypI 2016 Warsaw | September 14, 2016")
	renderer.save()
	renderer.set_source_rgb (*bg_color)
	renderer.put_text (text, height=f-p2, valign=-1, desc="")
	renderer.restore()


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
