side_margin = .07
logo_margin = .09
footer_margin = .05

def prepare_page (renderer):
	cr = renderer.cr
	width = renderer.width
	height = renderer.height
	
	cr.set_source_rgb (0, 0, 0)
	cr.paint ()

	s = side_margin * width
	l = logo_margin * height

	cr.rectangle (0, 0, s, height)
	cr.rectangle (width, 0, -s, height)
	cr.set_source_rgb (1, 1, 1)
	cr.fill ()

	cr.move_to (0, 0)
	renderer.put_image ("redhat.svg", height = l, valign=+1, halign=+1)

	cr.move_to (width, 0)
	renderer.put_image ("cairo.svg", height = l, valign=+1, halign=-1)


	cr.set_source_rgb (1, 1, 1)

	layout = renderer.create_layout ("<i>GUADEC 2007, Birmingham, UK</i>")
	w, h = renderer.fit_layout (layout, 0, height * footer_margin)
	cr.move_to (.5 * (width - w), height - h)
	cr.show_layout (layout)

	w = width * (1 - 2 * side_margin)
	x = width * side_margin
	h = height * (1 - logo_margin) - h
	y = height * logo_margin

	return x, y, w, h
