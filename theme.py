side_margin = .03
logo_margin = .15
padding = .01

def prepare_page (renderer):
	cr = renderer.cr
	width = renderer.width
	height = renderer.height
	
	cr.set_source_rgb (0, 0, 0)
	cr.paint ()

	cr.rectangle (0, 0, side_margin * width, height)
	cr.rectangle (width, 0, -side_margin * width, height)
	cr.set_source_rgb (1, 1, 1)
	cr.fill ()

	cr.rectangle (0, 0, side_margin * width, logo_margin * height)
	cr.rectangle (width, 0, -side_margin * width, logo_margin * height)
	cr.set_source_rgb (.8, 0, 0)
	cr.fill ()

	cr.set_source_rgb (1, 1, 1)

	layout = renderer.create_layout ("<i>GUADEC 2007, Birmingham, UK</i>")
	w, h = renderer.fit_layout (layout, .5 * width, 0)
	cr.move_to (.5 * (width - w), height - h)
	cr.show_layout (layout)

	p = min (padding * width, padding * height)
	w = width * (1 - 2 * side_margin) - 2 * p
	x = width * side_margin + p
	h = height * (1 - logo_margin) - h - 2 * p
	y = height * logo_margin + p

	return x, y, w, h
