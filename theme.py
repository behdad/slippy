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

	cr.set_source_rgb (.8, .85, 1)
	cr.paint ()

	cr.set_source_rgb (158/255., 87/255., 0/255.)
	cr.rectangle (0, height, width, -p2)
	cr.fill ()
	cr.move_to (.5 * width, height-p2)
	cr.set_source_rgb (0x03/255., 0x40/255., 0x79/255.)
	fw, fh = renderer.put_text ("GUADEC 2007, Birmingham, UK", height=f-p2, valign=-1)
	cr.move_to (.5 * (width - fw), height-p2)
	renderer.put_image ("guadec.svg", height=f-p2, valign=-1, halign=-1)

	cr.move_to (p, p)
	renderer.put_image ("redhat.svg", height = l-p2, valign=+1, halign=+1)

	cr.move_to (width-p, p)
	renderer.put_image ("cairo.svg", height = l-p2, valign=+1, halign=-1)

	cr.move_to (p, height-p)
	renderer.put_image ("behdad.svg", width = s-p2, valign=-1, halign=+1)

	cr.move_to (width-p, height-p)
	renderer.put_image ("cworth.svg", width = s-p2, valign=-1, halign=-1)

	w = width - s - s - p2
	x = s + p
	h = height - l - f - p2
	y = l + p

	bubble (cr, s * .9, height - .7 * s, x, y, w, h)
	cr.set_source_rgb (0, 0, 0)
	cr.save()
	cr.set_line_width (p)
	cr.set_miter_limit (20)
	cr.stroke_preserve ()
	cr.restore()
	cr.clip ()
	cr.set_source_rgb (1, 1, 1)
	cr.paint ()

	cr.set_source_rgb (0, 0, 0)

	p *= 3
	
	return x + p, y + p, w - 2 * p, h - 2 * p
