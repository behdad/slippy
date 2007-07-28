import cairo

logo_height = .3
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
	
	cr.save ()
	cr.set_operator (cairo.OPERATOR_CLEAR)
	cr.paint ()
	cr.restore ()

	cr.move_to (0, height)
	global logo_w, logo_h
	logo_w, logo_h = renderer.put_image ("gnu-bold.svg", height=logo_height*height, valign=-1, halign=+1)

	# Compute rectangle available for slide content
	w = width
	x = 0
	h = height * (1 - logo_height)
	y = 0
	# Adjust for bubble padding. the 8 comes from bezier calculations
	d = min (w, h) * bubble_rad / 8.
	x, y, w, h = x + d, y + d, w - d*2, h - d*2

	return x, y, w, h

def draw_bubble (renderer, x, y, w, h, data=None):
	# Fancy speech bubble!
	cr = renderer.cr
	width = renderer.width
	height = renderer.height
	
	cr.save()
	x, y = cr.user_to_device (x, y)
	w, h = cr.user_to_device_distance (w, h)
	cr.identity_matrix ()

	xc, yc = logo_w, height - .5 * logo_h
	bubble (cr, xc, yc, x, y, w, h)
	cr.set_source_rgb (0, 0, 0)
	cr.set_line_width (min (w, h) * .01)
	cr.set_miter_limit (20)
	cr.stroke_preserve ()

	cr.restore()
	cr.set_source_rgb (1, 1, 1)
	cr.clip ()
	cr.paint ()

	cr.set_source_rgb (0, 0, 0)
