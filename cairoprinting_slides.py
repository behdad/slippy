#!/usr/bin/python
# -*- coding:utf8 -*-

# Copyright 2007 Carl Worth <cworth@redhat.com>
# Copyright 2007 Behdad Esfahbod <besfahbo@redhat.com>

# A slides file should populate the variable slides with
# a list of tuples.  Each tuple should have:
#
#	- Slide content
#	- User data
#	- Canvas width
#	- Canvas height
#
# Slide content can be a string, a list of strings,
# a function returning one of those, or a generator
# yielding strings.  The user data should be a dictionary or
# None, and is both used to communicate options to the
# renderer and to pass extra options to the theme functions.
#
# A function-based slide content will be passed a renderer object.
# Renderer is an object similar to a cairo.Context and
# pangocairo.CairoContext but has its own methods too.
# The more useful of them here are put_text, put_image, and
# set_allocation.  See their pydocs.

slides = []
def slide_add(f, data=None, width=800, height=600):
	#slides[:0] = [(f, data, width, height)]
	slides.append ((f, data, width, height))
	return f

import pango, pangocairo, cairo, os, signal

# We use slide data to tell the theme who's speaking.
# That is, which side the bubble should point to.
behdad = -1
whois = None
def who(name):
	global whois
	whois = name
# And convenience functions to add a slide.  Can be
# used as a function decorator, or called directly.
def slide_who(f, who, data=None):
	if data:
		data = dict (data)
	else:
		data = {}
	data['who'] = who
	return slide_add (f, data)
def slide(f, data=None):
	return slide_who (f, whois, data=data)
def slide_noone(f, data=None):
	return slide_who (f, None, data=data)
def slide_behdad(f, data=None):
	return slide_who (f, behdad, data=data)

#
# Slides start here
#

@slide_noone
def title_slide (r):
	r.move_to (400, 150)
	r.put_text (
"""<span size="larger">cairo graphics</span>
<span foreground="gray" size="smaller">http://cairographics.org</span>""", width=800, valign=1)

	r.move_to (0, 450)
	r.put_text ("""Behdad Esfahbod\n<span font_desc="16">besfahbo@<span foreground="#c00">redhat</span>.com</span>""",
		    desc="20", halign=1, valign=-1)

who (behdad)

slide_noone("Intro")

def list_slide (l, data=None):
	def s (r):
		return '\n'.join (l)
		#yield l[0]
		#for i in l[1:]:
		#	yield '\n'+i
	s.__name__ = l[0]
	slide (s, data)

list_slide ([
		"• PostScript-like 2D model",
		"• Porter-Duff compositing model",
		'• <b>Easy to use</b>',
		"• Multiple backends",
		"• Backend-independent drawing",
		"• Portable",
	    ], data={'align': pango.ALIGN_LEFT})
		
list_slide ([
		"<b>Backends</b>",
		"2002-06	Xlib",
		"2003-02	image",
		"2003-10	PostScript",
		'2004-04	<span foreground="#888">XCB</span>',
		'2004-09	<span foreground="#888">glitz</span>',
		"2005-01	Win32",
		"2005-01	PDF",
		'2005-01	<span foreground="#888">Quartz</span>',
		"2005-12	SVG",
		'2005-12	<span foreground="#888">BeOS</span>',
		'2005-12	<span foreground="#888">directfb</span>',
		'2006-09	<span foreground="#888">OS/2</span>',
		'2007-02	<span foreground="#888">Quartz (<i>New!</i>)</span>',
	    ], data={'align': pango.ALIGN_LEFT})

list_slide ([
		"<b>Font backends</b>",
		"FreeType+FontConfig",
		"Win32",
		"ATSUI",
	    ])

list_slide ([
		"<b>Bindings</b>",
		"C++",
		"Common Lisp",
		"D",
		"Haskell",
		"Java",
		".NET",
		"Nickle",
		"O'Caml",
		"Perl",
		"PHP",
		"Python",
		"Ruby",
		"Scheme",
		"Squeak",
	    ])

list_slide ([
		"<b>Users</b>",
		"GTK+",
		"Firefox 3",
		"Mono",
		'<span foreground="#888">Inkscape</span>',
		'<span foreground="#888">OpenOffice.org</span>',
		'<span foreground="#888">...</span>',
	    ])

list_slide ([
		"cairo_surface_t",
		"cairo_t",
		"cairo_pattern_t",
		"cairo_font_face_t",
		"cairo_scaled_font_t",
	    ], data={'align': pango.ALIGN_LEFT})
		
slide("""cairo_surface_t *surface;
cairo_t *cr;

surface = cairo_pdf_surface_create ("out.pdf", 100, 100);

cr = cairo_create (surface);
cairo_move_to (cr, 10, 10);
cairo_line_to (cr, 90, 90);
cairo_stroke (cr);
cairo_destroy (cr);

cairo_surface_destroy (surface);""", data={'align': pango.ALIGN_LEFT})

def paint_checkers (cr):
	image = cairo.ImageSurface (cairo.FORMAT_ARGB32, 30, 30)
	cr2 = cairo.Context (image)
	cr2.rectangle ( 0,  0, 15, 15)
	cr2.rectangle (15, 15, 15, 15)
	cr2.set_source_rgba (.75, .75, .75, .75)
	cr2.fill ()
	cr2.rectangle (15,  0, 15, 15)
	cr2.rectangle ( 0, 15, 15, 15)
	cr2.set_source_rgba (1, 1, 1, 0)
	cr2.set_operator (cairo.OPERATOR_SOURCE)
	cr2.fill ()
	checker = cairo.SurfacePattern (image)
	checker.set_filter (cairo.FILTER_NEAREST)
	checker.set_extend (cairo.EXTEND_REPEAT)
	cr.set_source (checker)
	cr.paint ()

def gnome_foot_path (cr):
	# Originally 96 x 118, scaling to fit in 80x80
	cr.save ()
	cr.translate ((96 - 80) / 2., 0)
	cr.scale (80. / 118., 80. / 118.)
	cr.move_to (86.068, 1.)
	cr.curve_to (61.466, 0., 56.851, 35.041, 70.691, 35.041)
	cr.curve_to (84.529, 35.041, 110.671, 0., 86.068, 0.)
	cr.move_to (45.217, 30.699)
	cr.curve_to (52.586, 31.149, 60.671, 2.577, 46.821, 4.374)
	cr.curve_to (32.976, 6.171, 37.845, 30.249, 45.217, 30.699)
	cr.move_to (11.445, 48.453)
	cr.curve_to (16.686, 46.146, 12.12, 23.581, 3.208, 29.735)
	cr.curve_to (-5.7, 35.89, 6.204, 50.759, 11.445, 48.453)
	cr.move_to (26.212, 36.642)
	cr.curve_to (32.451, 35.37, 32.793, 9.778, 21.667, 14.369)
	cr.curve_to (10.539, 18.961, 19.978, 37.916, 26.212, 36.642)
	cr.line_to (26.212, 36.642)
	cr.move_to (58.791, 93.913)
	cr.curve_to (59.898, 102.367, 52.589, 106.542, 45.431, 101.092)
	cr.curve_to (22.644, 83.743, 83.16, 75.088, 79.171, 51.386)
	cr.curve_to (75.86, 31.712, 15.495, 37.769, 8.621, 68.553)
	cr.curve_to (3.968, 89.374, 27.774, 118.26, 52.614, 118.26)
	cr.curve_to (64.834, 118.26, 78.929, 107.226, 81.566, 93.248)
	cr.curve_to (83.58, 82.589, 57.867, 86.86, 58.791, 93.913)
	cr.line_to (58.791, 93.913)
	cr.restore ()

@slide
def imaging_model (r):

	paint_checkers (r.cr)

	r.allocate (100, 130, 550, 450)
	r.cr.translate (200, 130)

	### Column 1
	r.cr.save ()

	r.cr.move_to (0, 0)
	r.cr.set_source_rgb (0, 0, 0)
	r.put_text ("source", height=40, valign=-1)

	def done_with_header ():
		r.cr.translate (-40, 20)
	done_with_header ()

	# Solid source
	def set_solid_source ():
		r.cr.set_source_rgba (.87, .64, .13, 0.7)
	set_solid_source ()
	r.cr.rectangle (0, 0, 80, 80)
	r.cr.fill ()

	def next_row ():
		r.cr.translate (0, 110)

	next_row ()

	# Linear source
	def set_linear_source ():
		linear = cairo.LinearGradient (0, 0, 0, 80)
		linear.add_color_stop_rgba (0.0,  .96, .43, .11, 1.0)
		linear.add_color_stop_rgba (0.2,  .96, .43, .11, 1.0)
		linear.add_color_stop_rgba (0.5,  .96, .43, .11, 0.2)
		linear.add_color_stop_rgba (0.8,  .11, .22, .96, 1.0)
		linear.add_color_stop_rgba (1.0,  .11, .22, .96, 1.0)
		r.cr.set_source (linear)
	set_linear_source ()
	r.cr.rectangle (0, 0, 80, 80)
	r.cr.fill ()

	next_row ()

	# Radial source
	def set_radial_source ():
		radial = cairo.RadialGradient (40, 40, 0, 40, 40, 40)
		radial.add_color_stop_rgba (0.0, .55, .15, .63, 1.0)
		radial.add_color_stop_rgba (0.3, .55, .15, .63, 1.0)
		radial.add_color_stop_rgba (1.0, .91, .89, .39, 0.5)
		r.cr.set_source (radial)
	set_radial_source ()
	r.cr.rectangle (0, 0, 80, 80)
	r.cr.fill ()

	next_row ()

	# Image pattern source
	def set_image_source ():
		image = cairo.ImageSurface.create_from_png ("pumpkin-small.png")
		r.cr.set_source_surface (image, 0, 0)
	set_image_source ()
	r.cr.paint ()

	r.cr.restore ()

	def next_column ():
		r.cr.translate (200, 0)

	next_column ()

	### Column 2
	r.cr.save ()

	r.cr.move_to (0, 0)
	r.cr.set_source_rgb (0, 0, 0)
	r.put_text ("mask", height=40, valign=-1)

	done_with_header ()

	# Gnome foot
	gnome_foot_path (r.cr)
	r.cr.set_line_width (1.0)
	r.cr.stroke ()

	next_row ()

	# Gnome foot
	gnome_foot_path (r.cr)
	r.cr.set_line_width (1.0)
	r.cr.stroke ()

	next_row ()

	# 'G'
	def draw_G ():
		r.cr.move_to (40, 0)
		r.put_text ("<b>G</b>", height=80, valign=1)
	draw_G ()

	next_row ()

	# Radial mask
	def get_radial_mask_pattern ():
		radial = cairo.RadialGradient (40, 40, 0, 40, 40, 40)
		radial.add_color_stop_rgba (0.0, 0, 0, 0, 1.0)
		radial.add_color_stop_rgba (0.3, 0, 0, 0, 1.0)
		radial.add_color_stop_rgba (1.0, 0, 0, 0, 0.0)
		return radial
	r.cr.set_source (get_radial_mask_pattern ())
	r.cr.rectangle (0, 0, 80, 80)
	r.cr.fill ()

	r.cr.restore ()
	next_column ()

	### Column 3
	r.cr.save ()

	r.cr.move_to (0, 0)
	r.cr.set_source_rgb (0, 0, 0)
	r.put_text ("source\nIN mask\nOVER dest", height=120, valign=-1)

	done_with_header ()

	# Stroked GNOME foot
	set_solid_source ()
	gnome_foot_path (r.cr)
	r.cr.set_line_width (6)
	r.cr.stroke ()

	next_row ()

	# Filled GNOME foot
	set_linear_source ()
	gnome_foot_path (r.cr)
	r.cr.fill ()

	next_row ()

	# Filled 'G'
	set_radial_source ()
	draw_G ()

	next_row ()

	# Masked image
	set_image_source ()
	r.cr.mask (get_radial_mask_pattern ())

	r.cr.restore ()

	return ""

slide_noone("Vector Backends")

list_slide (["PS", "PDF", "SVG"])
list_slide (['<b>Roundtrip</b>',
	     'cairo→PS→<span foreground="red">╳</span>',
	     "cairo→PDF→poppler→cairo",
	     "cairo→SVG→librsvg→cairo",
	    ], data={'align': pango.ALIGN_LEFT})
list_slide (['<b>Conversion</b>',
	     'PS→<span foreground="red">╳</span>',
	     "PDF→poppler→cairo→SVG",
	     "SVG→librsvg→cairo→PDF",
	    ], data={'align': pango.ALIGN_LEFT})
list_slide (["<b>Anatomy</b>",
	     "cairo_paginated_surface",
	     "cairo_meta_surface", 
	     "cairo_analysis_surface",
	    ], data={'align': pango.ALIGN_LEFT})
list_slide (["PS", "<b>PDF</b>", "SVG"])
list_slide (["<b>Font subsetters</b>",
	     "TrueType",
	     "OpenType CFF",
	     "Type1",
	     "Type1 fallback",
	     '<span foreground="#888">Type3</span>',
	    ])
list_slide (["<b>New in 1.6</b>",
	     'Native gradients',
	     'Fine-grained fallback images',
	    ])
list_slide (["<b>Planned for 1.8</b>",
	     'Improved text extraction',
	     'User-fonts',
	     'Metadata API',
	     'Reduced file size',
	     'JPEG support',
	    ])
list_slide (["<b>Not Planned Yet</b>",
	     'Colorspace API',
	     'Higher-level integration',
	    ])

slide ("Q?")

if __name__ == "__main__":
	import slippy
	import cairoprinting_theme
	slippy.main (slides, cairoprinting_theme)
