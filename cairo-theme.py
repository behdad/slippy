# Written by Behdad Esfahbod, 2007
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

side_margin = .07
logo_margin = .09
footer_margin = .05
padding = .005
bubble_rad = .25

def bubble (cr, x0, y0, x, y, w, h):

	r = min (w, h) * bubble_rad

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
	
	s = side_margin * width
	l = logo_margin * height
	f = footer_margin * height
	p = padding * min (width, height)
	p2 = 2 * p

	# Blue sky
	sky = cairo.LinearGradient (0, 0, 0, height)
	sky.add_color_stop_rgba (0, .60, .65, 1, 1.0)
	sky.add_color_stop_rgba (1, .92, .93, 1, 1.0)
	cr.set_source (sky)
	cr.paint ()

	# Brown earth
	cr.set_source_rgb (158/255., 87/255., 0/255.)
	cr.rectangle (0, height, width, -p2)
	cr.fill ()

	# GUADEC logo on the bottom
	cr.move_to (.5 * width, height-p2)
	cr.set_source_rgb (0x03/255., 0x40/255., 0x79/255.)
	fw, fh = renderer.put_text ("GUADEC 2007, Birmingham, UK", height=f-p2, valign=-1)
	cr.move_to (.5 * (width - fw), height-p2)
	renderer.put_image ("guadec.svg", height=f-p2, valign=-1, halign=-1)

	# Red Hat/cairo logos at the top
	cr.move_to (p, p)
	renderer.put_image ("redhat.svg", height = l-p2, valign=+1, halign=+1)

	cr.move_to (width-p, p)
	renderer.put_image ("cairo.svg", height = l-p2, valign=+1, halign=-1)

	# Cartoon icons for speakers
	cr.move_to (p, height-p)
	renderer.put_image ("behdad.svg", width = s-p2, valign=-1, halign=+1)

	cr.move_to (width-p, height-p)
	renderer.put_image ("cworth.svg", width = s-p2, valign=-1, halign=-1)

	# Compute rectangle available for slide content
	w = width - s - s - p * 2
	x = s + p
	h = height - l - f - p * 2
	y = l + p
	# Adjust for bubble padding. the 8 comes from bezier calculations
	d = min (w, h) * bubble_rad / 8.
	x, y, w, h = x + d, y + d, w - d*2, h - d*2

	return x, y, w, h

def draw_bubble (renderer, x, y, w, h, data=None):
	# Fancy speech bubble!
	cr = renderer.cr
	width = renderer.width
	height = renderer.height
	
	s = side_margin * width
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
	cr.set_source_rgb (0, 0, 0)
	cr.set_line_width (p)
	cr.set_miter_limit (20)
	cr.stroke_preserve ()

	cr.restore()
	cr.set_source_rgb (1, 1, 1)
	cr.clip ()
	cr.paint ()

	cr.set_source_rgb (0, 0, 0)
