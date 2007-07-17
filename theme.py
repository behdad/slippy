side_margin = .07
logo_margin = .09
footer_margin = .05
padding = .005

def bubble (cr, x0, y0, x, y, w, h):

	x1, y1, x2, y2 = x, y, x + w, y + h
	r = min (w, h) * .15

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
	cr.curve_to (xc+r, y0, .5 * (xc+r+x0), .5 * (yc+y0), x0, y0)
	cr.curve_to (.5 * (xc-r+x0), .5 * (yc+y0), xc-r, y0, xc-r, yc)

	
def prepare_page (renderer):
	cr = renderer.cr
	width = renderer.width
	height = renderer.height
	
	cr.set_source_rgb (1, 1, 1)
	cr.paint ()

	s = side_margin * width
	l = logo_margin * height
	f = footer_margin * height
	p = padding * min (width, height)
	p2 = 2 * p

	cr.move_to (p, p)
	renderer.put_image ("redhat.svg", height = l-p2, valign=+1, halign=+1)

	cr.move_to (width-p, p)
	renderer.put_image ("cairo.svg", height = l-p2, valign=+1, halign=-1)

	cr.move_to (p, height-p)
	renderer.put_image ("behdad.svg", width = s-p2, valign=-1, halign=+1)

	cr.move_to (width-p, height-p)
	renderer.put_image ("cworth.svg", width = s-p2, valign=-1, halign=-1)

	cr.set_source_rgb (0x03/255., 0x40/255., 0x79/255.)

	cr.move_to (.5 * width, height-p)
	fw, fh = renderer.put_text ("GUADEC 2007, Birmingham, UK", height=f-p2, valign=-1)
	cr.move_to (.5 * (width - fw), height-p)
	renderer.put_image ("guadec.svg", height=f-p2, valign=-1, halign=-1)

	w = width - s - s - p2
	x = s + p
	h = height - l - f - p2
	y = l + p

	bubble (cr, s * .5, height - .5 * s, x, y, w, h)
	cr.set_source_rgb (0, 0, 0)
	cr.set_line_width (4)
	cr.stroke_preserve ()
	cr.clip ()
	cr.set_source_rgb (1, 1, 1)
	cr.paint ()

	cr.set_source_rgb (0, 0, 0)

	return x, y, w, h
