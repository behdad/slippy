#!/usr/bin/python
# -*- coding:utf8 -*-

# Copyright 2014 Behdad Esfahbod <behdad@google.com>

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
whois = 0
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
	return slide_who (f, 0, data=data)

#
# Slides start here
#

who (behdad)

@slide_noone
def title_slide (r):
	r.move_to (400, 100)
	r.put_text ("<b>GLyphy</b>", width=800, valign=1)

	r.move_to (0, 450)
	r.put_text ("""Behdad Esfahbod\n<span font_desc="monospace 16">behdad@google.com</span>""",
		    desc="20", halign=1, valign=-1)
	r.move_to (800, 450)
	r.put_text ("""<span font_desc="monospace 16">glyphy.org\nbehdad.org</span>""",
		    desc="20", halign=-1, valign=-1)

def list_slide (l, data=None):
	def s (r):
		return '\n'.join (l)
		#yield l[0]
		#for i in l[1:]:
		#	yield '\n'+i
	s.__name__ = l[0]
	slide (s, data)

slide_noone("Getting your CFP\nabstract accepted:\n<i>A case study (or 2)</i>")

list_slide ([
		"<b>Helps if…</b>",
		"• Established",
		"• ~100s millions users",
		"• <i>Has</i> changed the world",
		"• Thriving community",
		"• Many high-profile users",
		"• Booming",
	    ], data={'align': pango.ALIGN_LEFT})
slide_noone("<b>HarfBuzz</b>")

list_slide ([
		"<b>But if…</b>",
		"• Experimental",
		"• Unused so far",
		"• <i>Will</i> change the world",
		"• No community",
		"• No users",
		"• Stale",
	    ], data={'align': pango.ALIGN_LEFT})
slide_noone("<b>GLyphy</b>")

slide_noone("Submit!")

slide_noone("<b>How to\n<i>keynote</i>\nLCA</b>")

who ("mjg59.png")
slide("Just cut\nthe jokes\nout <i>dude</i>!")
who (behdad)

#
# Real thing starts here
#

slide_noone("<b>GLyphy</b>\nAn <i>experiment</i> in\nGPU-accelerated\ntext rendering")
slide_noone("GLSL ES2")

list_slide ([
		"<b>Status quo</b>",
		"• Hint",
		"• Rasterize",
		"• Upload to GPU texture",
		"• Blit",
	    ], data={'align': pango.ALIGN_LEFT})
slide_noone("<b>Transformation\ndependent</b>")

slide_noone("<span font_desc='Comic Sans MS'><b>Lets make\ntext beautiful!\n<span font_desc='24'>lolz</span></b></span>")

slide_noone("What would you do\nif you knew <span strikethrough='true'>you\ncould not fail</span> have a\nhigh-resolution display?")
slide_noone("<span strikethrough='true'>200+ppi (160 even)</span>\n300+ppi (450 even)")

def image_slide (f, width=600, height=600, imgwidth=0, imgheight=0, xoffset=0, yoffset=0, data=None):
	def s (r):
		r.move_to (400+xoffset, 300+yoffset)
		r.put_image (f, width=imgwidth, height=imgheight)
		x = (800 - width) * .5
		y = (600 - height) * .5
		r.set_allocation (x, y, width, height)
	s.__name__ = f
	slide (s, data)
	return s

def draw_image (r, f, width=600, height=600, imgwidth=0, imgheight=0, xoffset=0, yoffset=0, data=None):
	r.move_to (400+xoffset, 300+yoffset)
	r.put_image (f, width=imgwidth, height=imgheight)
	x = (800 - width) * .5
	y = (600 - height) * .5
	r.set_allocation (x, y, width, height)

def g_beziers(r):
	draw_image (r, "GwithBeziers.png", width=400, imgheight=660)

@slide
def GBeziers(r):
	g_beziers (r)

slide ("Coverage-based\nAnti-Aliasing")

@slide
def GBeziersSquare (r):
	g_beziers (r)
	r.rectangle (480, 210, 50, 50)
	r.set_source_rgba (0., 0., 1., .4)
	r.fill_preserve ()
	r.stroke ()

slide ("SDF-based\nAnti-Aliasing")

@slide
def GBeziersGaussian (r):
	g_beziers (r)
	gau = cairo.RadialGradient (505, 235, 0, 505, 235, 25 * 2)
	stops = 16
	for stop in (float(x) / stops for x in range(0, stops + 1)):
		shade = stop * stop * (3. - 2. * stop)
		gau.add_color_stop_rgba (stop, 0., 0., 1., .7 * (1. - shade))
	r.set_source (gau)
	r.paint ()

def glyphy_demo(r, f):
	r.set_source_rgb (1, 1, 1)
	r.paint ()
	args = {
		"width": 600,
		"imgheight": 680,
		"yoffset": -15,
		"xoffset": 0,
	}
	draw_image (r, f, **args)

def clamp(x, a, b):
	return min (max (x, a), b)

def smoothstep0(a, b, t):
	scale = 2.
	t = clamp ((float(t) - a)/(b - a)*scale - (scale-1)/2., 0, 1)
	return t

def smoothstep(a, b, t):
	scale = 1./.75
	t = clamp ((float(t) - a)/(b - a)*scale - (scale-1)/2., 0, 1)
	return t * t * (3. - 2. * t)

def smoothstep2(a, b, t):
	scale = 1. # 30./16. # Humm?
	t = clamp ((float(t) - a)/(b - a)*scale - (scale-1)/2., 0, 1)
	return t*t*t*(t*(t*6. - 15.) + 10.)

def aa_diagonal(a, b, t):
	scale = 1. # 2**.5 # Humm?
	t = clamp ((float(t) - a)/(b - a)*scale - (scale-1)/2., 0, 1)
	if t <= .5:
		return t*t * 2
	else:
		t = 1. - t
		return 1 - (t*t * 2)

def plot(r, f, a, b, line=0, scale=1.):
	r.save ()
	r.translate (400, 60)
	r.scale (scale, scale)
	r.scale (50, -50.5)
	r.translate (0, -line * 1.5)
	r.move_to (-4, 0)
	r.line_to (4, 0)
	r.move_to (0, -.1)
	r.line_to (0, 1.1)
	r.set_source_rgba (0, 0, 0, .1)
	r.save ()
	r.identity_matrix ()
	r.set_line_width (1.)
	r.stroke ()
	r.restore ()
	steps = 200
	for step in (x* 8./ steps for x in range(-steps/2,steps/2+1)):
		r.line_to (step, f (a, b, step))
	r.set_source_rgba (0, 0, 0, .9)
	r.save ()
	r.identity_matrix ()
	r.set_line_width (1.)
	r.stroke ()
	r.restore ()
	r.restore ()

@slide
def GSdf(r):
	glyphy_demo (r, "sdf.png")

@slide
def GRaster(r):
	glyphy_demo (r, "g.png")
	plot (r, smoothstep, -1., +1.)

@slide
def GRasterBlurry(r):
	glyphy_demo (r, "g-blurry.png")
	plot (r, smoothstep, -1.*4, +1.*4)

@slide
def GRasterAliased(r):
	glyphy_demo (r, "g-aliased.png")
	plot (r, smoothstep, -1./10, +1./10)

@slide
def GRaster(r):
	glyphy_demo (r, "g.png")
	plot (r, smoothstep, -1., +1.)

@slide
def GRasterEmboldened(r):
	glyphy_demo (r, "g-emboldened.png")
	plot (r, smoothstep, -1.+2., +1.+2.)

@slide
def GRasterLightened(r):
	glyphy_demo (r, "g-lightened.png")
	plot (r, smoothstep, -1.-1., +1.-1.)

@slide
def AntiAliasFuncs(r):
	r.set_source_rgb (1, 1, 1)
	r.paint ()
	plot (r, smoothstep0, -1., +1., line=1, scale=1.4)
	plot (r, smoothstep, -1., +1., line=2, scale=1.4)
	plot (r, smoothstep2, -1., +1., line=3, scale=1.4)
	plot (r, aa_diagonal, -1., +1., line=4, scale=1.4)
	r.set_allocation (100, 50, 600, 480)

slide("SDF is <i>linear</i> over\nuniform-scaling\n and translation")

slide_noone("<b>Represent\nSDF on GPU</b>")

image_slide("g-texture-raster.png")
image_slide("g-texture-sdf.png")
# TODO bilinear effects on texture raster
# TODO bilinear effects on texture sdf

slide_noone("<i>Vector\nall the\nglyphs!</i>")

slide("Distance\nto Bézier")

slide("<b>Ouch!</b>")

slide("Convert\nto line\nsegments")
@slide
def GLines(r):
	glyphy_demo (r, "g-lines.png")

slide("Convert to\ncircular arc\nsplines")
@slide
def GLines(r):
	glyphy_demo (r, "g-arcs.png")

slide_noone("<b>Arc-spline\napproximation</b>")
slide("Error\nfunction")
@slide
def CurveArc(r):
	r.set_source_rgb (1, 1, 1)
	r.paint ()
	draw_image (r, "curve-arc.png", width=600, imgheight=750)
slide("Physics\nsimulation")
@slide
def Spiral(r):
	r.set_source_rgb (1, 1, 1)
	r.paint ()
	draw_image (r, "spiral.png", width=600, imgheight=650)

@slide
def GArcsCloseup(r):
	glyphy_demo (r, "g-arcs-closeup.png")
@slide
def GArcsAll(r):
	glyphy_demo (r, "g-arcs-all.png")
list_slide ([
		"<b>GPU time!</b>",
		"• Stuff it all in a texture",
		"• Ship it!",
	    ], data={'align': pango.ALIGN_LEFT})
@slide
def GReal(r):
	glyphy_demo (r, "g-real.png")
slide_noone("<b><i>You're</i> insane!</b>")

list_slide ([
		"<b>Random access</b>",
		"• Coarse grid",
		"• Various optimizations",
	    ], data={'align': pango.ALIGN_LEFT})
@slide
def GArcsAll(r):
	glyphy_demo (r, "g-grid.png")
who ("keithp.png")
slide("<b><i>It's</i> insane!</b>")
who (behdad)

slide_noone("<b>Demo\ntime!</b>")

# Demo!

slide_noone("<b>Limitations</b>")
slide("Speed+memory\nfont-dependent")
@slide
def A(r):
	glyphy_demo (r, "A.png")
@slide
def A(r):
	glyphy_demo (r, "A-debug.png")
@slide
def Arcano(r):
	glyphy_demo (r, "arcano.png")

slide_noone("<b>Practicality</b>")

slide_noone("<b>Challenges</b>")

"""
Sample shaders

Mobile GPU perf unheard of.  Old Tegra had one fetch one add...
http://venturebeat.com/2014/01/05/nvidia-announces-tegra-k1-a-super-mobile-chip-with-192-cores/

Bugs w drivers

Image gallery.  Spooky etc.
"""

if __name__ == "__main__":
	import slippy
	import glyphy_theme
	slippy.main (slides, glyphy_theme)
