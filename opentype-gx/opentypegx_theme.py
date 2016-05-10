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
footer_margin = .06
padding = .000
bubble_rad = .25

def bubble (cr, x0, y0, x, y, w, h):

	r = min (w, h) * (bubble_rad / (1 - 2./8*bubble_rad))

	p = r / 7.
	x, y, w, h, r = x - p, y - p, w + 2*p, h + 2*p, r + p

	x1, y1, x2, y2 = x, y, x + w, y + h

	cr.move_to (x1+r, y1)
	cr.line_to (x2-r, y1)
	cr.curve_to (x2, y1, x2, y1, x2, y1+r)
	cr.line_to (x2, y2-r)
	cr.curve_to (x2, y2, x2, y2, x2-r, y2)
	cr.line_to (x1+r, y2)
	cr.curve_to (x1, y2, x1, y2, x1, y2-r)
	cr.line_to (x1, y1+r)
	cr.curve_to (x1, y1, x1, y1, x1+r, y1)
	cr.close_path ()

	xc, yc = .5 * (x1 + x2), .5 * (y1 + y2)
	cr.move_to (xc+r, yc)
	cr.curve_to (xc+r, y0, .5 * (xc+r+x0), (yc+y0*2)/3, x0, y0)
	cr.curve_to (.5 * (xc-r+x0), (yc+y0*2)/3, xc-r, y0, xc-r, yc)


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

	cr.paint ()
	sky = cairo.LinearGradient (0, 0, 0, height)
	sky.add_color_stop_rgba (0, 0x02/255., 0x23/255., 0x80/255., 1.)
	sky.add_color_stop_rgba (1, 0x9b/255., 0x84/255., 0x66/255., 1.)
	cr.set_source (sky)
	cr.paint ()

	# Background image
	#cr.move_to (width / 2., height / 2.)
	#renderer.put_image ("pillars.jpg", height = height, width = width)

	cr.move_to (.5 * width, height-p2)
	b = 150.
	cr.set_source_rgb (0x9b/b, 0x84/b, 0x66/b)
	renderer.put_text ("TYPO Labs, 10 &amp; 11 May, 2016, Berlin", height=f-p2, valign=-1, desc="")

	# Cartoon icons for speakers
	who = renderer.data.get ('who', None)
	if who:
		if who < 0:
			cr.move_to (p, height-p)
			renderer.put_image ("behdad.png", width = a-p2, valign=-1, halign=+1)
		else:
			cr.move_to (width-p, height-p)
			renderer.put_image (who, width = a-p2, valign=-1, halign=-1)

	# Compute rectangle available for slide content
	w = width - s - s - p * 2
	x = s + p
	h = height - l - f - p * 2
	y = l + p

	# Adjust for bubble padding. the 8 comes from bezier calculations
	d = min (w, h) * bubble_rad / 8.
	x, y, w, h = x + d, y + d, w - d*2, h - d*2

	return x, y, w, h

def draw_bubble (renderer, x, y, w, h, data={}):
	# Fancy speech bubble!
	cr = renderer.cr
	width = renderer.width
	height = renderer.height
	
	s = avatar_margin * width
	p = padding * min (width, height)

	cr.save()
	x, y = cr.user_to_device (x, y)
	w, h = cr.user_to_device_distance (w, h)
	cr.identity_matrix ()

	who = data.get ('who', None)
	if not who:
		xc, yc = x + w*.5, y + h*.5
	elif who < 0:
		xc, yc = s * .9, height - .7 * s
	else:
		xc, yc = width - s * .9, height - .7 * s

	bubble (cr, xc, yc, x, y, w, h)
	cr.rectangle (width, 0, -width, height)
	cr.clip ()

	bubble (cr, xc, yc, x, y, w, h)
	#cr.set_source_rgb (0, 0, 0)
	#cr.set_line_width (p)
	#cr.set_miter_limit (20)
	#cr.stroke_preserve ()

	cr.restore ()

	cr.clip ()
	cr.set_source_rgba (1, 1, 1, .94)
	cr.paint ()

	b = 700.
	cr.set_source_rgb (0xbe/b, 0xa3/b, 0x89/b)
