#!/usr/bin/python
# -*- coding:utf8 -*-

if __name__ == "__main__":
	import slippy
	import sys
	import freetextstack_theme as theme
	slippy.main (__file__, theme, sys.argv[1:])
	sys.exit (0)

# Copyright 2007,2009 Behdad Esfahbod <besfahbo@redhat.com>

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
def slide_image (f, height=650, data=None):
	@slide_noone
	def image_func (r):
		r.move_to (400, 300)
		r.put_image (f, height=height)
		#r.set_allocation (000, 0, 800, 600)
		yield ""

"""
Free Software stack for Unicode Text Rendering

The Free Software world has a lot to offer when it comes to building a stack
up from the grounds.  Be it building an ARM-based Linux mobile platform or
cross-platform text rendering to rendering downloadable CFF fonts on Windows,
the Free Software stack provides all the bits and pieces one needs to assemble
a high quality OpenType-based Unicode text rendering pipeline with great
flexibility.  In this tutorial we will go over the building blocks involved
and how to put them together.

The session can be divided in three parts logically.  The first section
introduces different libraries involved: FreeType, fontconfig, HarfBuzz,
FriBidi, cairo, glib, Pango, GTK+, Qt, and possibly others.  In the second
part, we'll focus on hands on development of text rendering code based on the
highlevel Pango+Cairo interface.  In the final part, we dig down in the stack
and put together a barebone quick and dirty text rendering system using
FreeType, glib, FriBidi, HarfBuzz, and cairo only, to see first hand how the
different pieces fit together.

We will also cover licensing and support options and community models of the
libraries involved.  What will NOT be covered in this session is how to
cross-compile or otherwise build components.
"""

#
# Slides start here
#

@slide_noone
def title_slide (r):
	r.move_to (800, 30)
	r.put_text (
"""Free Software\nstack for\nUnicode\nText\nRendering""",
width=800, height=500, valign=1, halign=-1)

	r.move_to (0, 570)
	r.put_text ("""Behdad Esfahbod\n<span font_desc="monospace">behdad@redhat.com\nhttp://behdad.org/</span>""", height=130, width=300, halign=1, valign=-1)


who (behdad)

def list_slide (l, data=None):
	def s (r):
		return '\n'.join (l)
		#yield l[0]
		#for i in l[1:]:
		#	yield '\n'+i
	s.__name__ = l[0]
	slide (s, data)
def step_slide (l, data=None):
	def s (r):
		yield l[0]
		for i in l[1:]:
			yield '\n'+i
	s.__name__ = l[0]
	slide (s, data)


list_slide ([
		"<b>Agenda</b>",
		"• Introduction",
		"• Overview",
		"• Community &amp; Culture",
		"• Bits and Pieces",
		"• Hello World",
		"• Digging Deeper",
	    ], data={'align': pango.ALIGN_LEFT})

list_slide([	"<b>Intro</b>",
		"• FarsiWeb",
		"• Unicode",
		"• GNOME",
		"• Red Hat",
	   ], data={'align': pango.ALIGN_LEFT})

slide_noone("<b>Overview</b>")
slide("Flexibility")
list_slide([	"<b>Licensing</b>",
		"• BSD-Style",
		"• LGPL",
	   ], data={'align': pango.ALIGN_LEFT})

list_slide([	"<b>Community</b>",
		"• Mailing list",
		"• The team",
		"• Bugzilla",
		"• IRC",
		"• Releases",
	   ], data={'align': pango.ALIGN_LEFT})

slide_noone("<b>Bits &amp;\nPieces</b>")
slide("FreeType")
slide("Fontconfig")
slide("Glib")
slide("FriBidi")
slide("HarfBuzz")
slide("Cairo")
slide("Pango")
slide("GTK+")
#slide("Qt")

slide_noone("<b>Hello\nWorld</b>")
slide("Demo\nTime!")

slide_noone("<b>Digging\nDeeper</b>")
list_slide ([	"<b>Consumers</b>",
		"• GUI Toolkits",
		"• Web Browsers",
		"• Word Processors",
		"• Designer Tools",
		"• Font Design Tools",
		"• Terminal Emulators",
		"• Batch Doc Processors",
		"• TeX Engines",
	    ], data={'align': pango.ALIGN_LEFT})

list_slide ([	"<b>Demystifying Fontconfig</b>",
		"• Patterns",
		"• Cache",
		"• Config",
	    ], data={'align': pango.ALIGN_LEFT})

list_slide ([	"<b>Pillars of Pango</b>",
		"• pango_itemize()",
		"• pango_shape()",
		"• pango_break()",
	    ], data={'align': pango.ALIGN_LEFT})

list_slide ([	"<b>Further Down</b>",
		"• Glib",
		"• FreeType",
		"• Fontconfig",
		"• FriBidi",
		"• Cairo",
		"• HarfBuzz",
	    ], data={'align': pango.ALIGN_LEFT})

list_slide ([	"<b>More Demos</b>",
		"• Vertical text",
		"• Online font add/remove",
		"• Automatic font installation",
	    ], data={'align': pango.ALIGN_LEFT})


"""
list_slide ([	"<b></b>",
		"• ",
		"• ",
		"• ",
		"• ",
		"• ",
		"• ",
	    ], data={'align': pango.ALIGN_LEFT})
"""

slide_noone("Q?")
