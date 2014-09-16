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
from pangopygments import highlight

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
	if data and 'who' in data:
		return slide_who (f, data['who'], data=data)
	else:
		return slide_who (f, 0, data=data)

#
# Slides start here
#

who (behdad)

@slide
def title_slide (r):
	r.move_to (400, 250)
	r.put_text ("<b>FontTools</b>\n"+
		    "<span font_desc='30'>"+
		    "reviving an Open Source project &amp;\n"+
		    "<span strikethrough='true'>re</span>building a thriving community"+
		    "</span>", valign=0, halign=0, desc="100")

	r.move_to (400, 550)
	r.put_text ("""Behdad Esfahbod\n<span font_desc="monospace 16">behdad@google.com\nhttp://behdad.org</span>""",
		    desc="20", halign=0, valign=-1)

def list_slide (l, data=None):
	def s (r):
		return '\n'.join (l)
		#yield l[0]
		#for i in l[1:]:
		#	yield '\n'+i
	s.__name__ = l[0]
	slide (s, data)

slide_noone("History")
slide_noone("Where")

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

slide_noone("<b>Demo\ntime!</b>")

# Demo!

slide_noone("<b>Limitations</b>")
slide("Memory\nfootprint")
slide("Speed+memory\nfont-dependent")

slide_noone("<b>Advantages</b>")
slide("Memory\nfootprint")
slide("Subpixel\npositioning")
slide("Pinch-to-zoom")

list_slide ([
		"<b>Challenges</b>",
		"• Shader size / complexity",
		"• Pixel cost",
		"• Conditionals",
		"• Dependent texture lookups",
		"• Variable loop iterations",
		"• Interpolation accuracy",
	    ], data={'align': pango.ALIGN_LEFT})

def source_slide(s, lang="python"):
	s = highlight(s, lang)
	s = "<span font_desc='monospace'>" + s + "</span>"
	slide_noone (s, data={'align': pango.ALIGN_LEFT})

def patch_slide(s):
	lines = s.split ("\n")
	new_lines = []
	for s in lines:
		s = s.replace("&", "&amp;").replace("<", "&lt;")
		if not s: s = ' '
		if s[0] == '-':
			s = "<span fgcolor='#d00'>%s</span>" % s
		elif s[0] == '+':
			s = "<span fgcolor='#0a0'>%s</span>" % s
		elif s[0] != ' ':
			s = "<b>%s</b>" % s

		new_lines.append (s)

	s = '\n'.join (new_lines)
	s = "<span font_desc='monospace'>" + s + "</span>"
	slide_noone (s, data={'align': pango.ALIGN_LEFT})

def commit_slide(s, who=None):
	lines = s.split ("\n")
	new_lines = []
	for s in lines:
		s = s.replace("&", "&amp;").replace("<", "&lt;")
		if not s: s = ' '
		if s[0] != ' ':
			s = "<b>%s</b>" % s

		new_lines.append (s)

	s = '\n'.join (new_lines)
	s = "<span font_desc='monospace'>" + s + "</span>"
	if who:
		slide_noone (s, data={'align': pango.ALIGN_LEFT, 'who': who})
	else:
		slide_noone (s, data={'align': pango.ALIGN_LEFT})

list_slide ([
		"<b>Code: libglyphy</b>",
		"• ~400 lines *.h",
		"• ~2500 lines *.cc *.hh",
		"• ~370 lines *.glsl",
		"• No dependencies",
	    ], data={'align': pango.ALIGN_LEFT})
list_slide ([
		"<b>Code: glyphy-demo</b>",
		"• ~2800 lines *.cc *.h",
		"• ~150 lines *.glsl",
		"• FreeType, GLUT",
	    ], data={'align': pango.ALIGN_LEFT})
list_slide ([
		"<b>More work</b>",
		"• Subpixel-rendering",
		"• Anisotropic-antialiasing",
	    ], data={'align': pango.ALIGN_LEFT})

slide("<b>Gallery!</b>")
slide("<b>Q?</b>")

if __name__ == "__main__":
	import slippy
	import fonttools_theme
	slippy.main (slides, fonttools_theme)
