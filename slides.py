# -*- coding:utf8 -*-

import pango, pangocairo, cairo, os, signal
slides = []
behdad = -1
cworth = +1
whois = None
def who(name):
	global whois
	whois = name
def slide(f):
	slides.append ((f, whois))
	return f
def slide_noone(f):
	slides.append ((f, None))
	return f
def slide_cworth(f):
	slides.append ((f, cworth))
	return f
def slide_behdad(f):
	slides.append ((f, behdad))
	return f

@slide_noone
def title_slide (r):
	r.move_to (400, 100)
	r.put_text (
"""Co-maintaining cairo:
cool community
cool code""", desc="50", valign=1)

	r.move_to (0, 450)
	r.put_text ("""Behdad Esfahbod\n<span font_desc="16">behdad@<span foreground="#c00">redhat</span>.com</span>""",
		    desc="20", halign=1, valign=-1)

	r.move_to (800, 450)
	r.put_text ("""Carl Worth\n<span font_desc="16">cworth@<span foreground="#c00">redhat</span>.com</span>""",
		    desc="20", halign=-1, valign=-1)

who (cworth)

slide_noone("Intro")

slide("Rendering model")

def paint_checkers (cr):
	image = cairo.ImageSurface (cairo.FORMAT_RGB24, 30, 30)
	cr2 = cairo.Context (image)
	cr2.rectangle ( 0,  0, 15, 15)
	cr2.rectangle (15, 15, 15, 15)
	cr2.set_source_rgb (.75, .75, .75)
	cr2.fill ()
	cr2.rectangle (15,  0, 15, 15)
	cr2.rectangle ( 0, 15, 15, 15)
	cr2.set_source_rgb (.94, .94, .94)
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
		r.cr.set_source_rgba (.87, .64, .13, 0.6)
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

who (cworth)

slide_noone("History")

@slide
def trapezoid (r):
	r.set_line_width (1)
	r.set_source_rgb (0, 0, 0)
	pixel_size = 800 / 10
	for x in range(0 - 50, 800 + 50, pixel_size):
		r.move_to (x, -50)
		r.line_to (x, 600 + 50)
		r.stroke ()
	for y in range(0 - 50, 600 + 50, pixel_size):
		r.move_to (-50, y)
		r.line_to (800 + 50, y)
		r.stroke ()
	r.scale (pixel_size / 10, pixel_size / 10)

	# Interior
	r.save ()
	r.move_to (0, 25)
	r.line_to (100, 25)
	r.line_to (100, 50)	
	r.line_to (0, 50)
	r.close_path ()
	r.clip ()

	r.move_to (30, 20)
	r.line_to (10, 60)
	r.line_to (75, 55)
	r.line_to (65, 15)
	r.close_path ()
	r.clip ()

	r.set_source_rgba (.2, .2, .7, 0.5)
	r.paint ()
	r.restore ()

	# top
	r.set_source_rgb (0, 0, 0)
	r.move_to (0, 25)
	r.put_text ("top", desc="5", halign=1, valign=-1)
	r.move_to (0, 25)
	r.line_to (100, 25)
	r.stroke ()

	# bottom
	r.move_to (100, 50)
	r.put_text ("bottom", desc="5", halign=-1, valign=-1)
	r.move_to (0, 50)
	r.line_to (100, 50)
	r.stroke ()

	# left
	r.set_source_rgb (.2, .6, .2)	
	r.move_to (30, 20)
	r.put_text ("left", desc="5", halign=1, valign=-1)
	r.move_to (30, 20)
	r.line_to (10, 60)
	r.stroke ()

	# right
	r.set_source_rgb (.8, .2, .2)
	r.move_to (65, 15)
	r.put_text ("right", desc="5", halign=-1, valign=-1)
	r.move_to (65, 15)
	r.line_to (75, 55)
	r.stroke ()

	r.allocate (0, 0, 100, 60)

pid = None

@slide
def geotv (r):
	r.move_to (400, 300)
	r.put_image ("geotv.jpg", width=900)
	r.move_to (100, 400)
	r.set_source_rgb (1, 1, 1)
	r.put_text ("April 2002", desc="40", halign=1)
	yield ""
	if not compact:
		global pid
		if r.viewer and not pid:
				pid = os.spawnlp (os.P_NOWAIT, 'mplayer', 'mplayer', '-fs', 'geotv.mpg')
				print "mplayer spawned with pid %d" % pid
		yield ""
		pid = None

@slide
def first_post (r):
	r.move_to (400, 300)
	r.put_text("""Subject: Xr API strawman
To: Keith Packard <keithp@keithp.com>
Date: Tue, 4 Jun 2002 19:55:06 +0000

Hi Keith,

I read up a bit on PostScript. It's the obvious source of the
proposals you were making.

I like it much better than GL as a model for Xr. It's cleaner in
general, (IMHO). And PS has larger overlap with the primitives we want
in Xr, (eg. bezier curves as opposed to just triangle meshes).

So, here's what I'm thinking of so far. This sticks fairly close to
PostScript, (but with an explicit rather than an implicit state
object).

Feedback welcome,

-Carl""", desc="Monospace", markup=False, width=800, height=600, align=pango.ALIGN_LEFT)

@slide
def api_strawman (r):
	r.move_to (400, 300)
	r.put_text("""/* Opaque state structure */
typedef struct _XrState XrState;

/* Functions for manipulating state objects */

/* XXX: Do we want to add `State' to any of these functions?
        eg. XrStateCreate, XrStateClone? */
XrState *XrCreate(void);
void XrDestroy(XrState *xrs);

void XrSave(XrState *xrs);
void XrRestore(XrState *xrs);

XrState *XrClone(XrState *xrs);

/* Modify state */
void XrSetPicture(XrState *xrs, XrPicture)
void XrSetColor(XrState *xrs, XrColor);

/* XXX: XrSetLineWidth, XrSetLineCap, XrSetLineJoin, XrSetDash, ... */

/* Path creation */

/* XXX: I'm thinking that it might make sense to do away with the
        notion of a "current path" in the state object and instead
        provide functions to manipulate an opaque XrPath object. This
        would add one more argument to XrStroke/XrFill, but it would
        unify support for PS "user paths" */

void XrNewPath(XrState *xrs);
void XrMoveTo(XrState *xrs, double x, double y);
void XrLineTo(XrState *xrs, double x, double y);
void XrClosePath(XrState *xrs);

/* XXX: XrRLineTo, XrArc, XrCurveTo, XrRCurveTo, ... */

/* Render current path */
void XrStroke(XrState *xrs);
void XrFill(XrState *xrs);
""", desc="Monospace", markup=False, width=800, height=600, align=pango.ALIGN_LEFT)

def list_slide (l):
	def s (r):
		if compact:
			yield '\n'.join (l)
		else:
			yield l[0]
			for i in l[1:]:
				yield '\n'+i
	s.__name__ = l[0]
	slide (s)

list_slide ([
		'<b>Committers</b>',
		'2002	2',
		'2003	11',
		'2004	12',
		'2005	26',
		'2006	54',
		'2007	<span foreground="#888">44</span>',
	    ])

who (behdad)

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

slide_noone ("News")

slide_behdad ("Mutex rework")

slide_cworth ("Error-handling")

slide_behdad ("Great malloc hunt")

slide_cworth ("PDF hotness")

slide_behdad ("Xlib work queue")

slide_noone ("Lessons")

who (behdad)

@slide
def git (r):
	yield "If you don't <i>git</i> it,\nyou don't get it"

	yield "\n\nIt's the\nRight Thing To Do"
	r.move_to (400, 300)
	r.put_image ("street.jpg", height=650)
	r.set_allocation (50, 0, 800, 550)
	yield ""

@slide
def git2 (r):
	yield "Tiny commits"

	yield "\n\n<i>Earn points faster</i>"
	r.move_to (400, 300)
	r.put_image ("apply-now.png", height=50)
	yield ""

who (cworth)

slide ("Commit-access\nfor everyone!")

who (behdad)

slide ("Tricking others\ninto doing <i>their</i> work")

who (cworth)

slide ("Don't go AWOL")

slide_noone ("Why do we\nlove cairo?")

slide_noone ('Why do <span foreground="#c00"><i>you</i></span>\nlove cairo?')
