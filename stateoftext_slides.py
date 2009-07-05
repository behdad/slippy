#!/usr/bin/python
# -*- coding:utf8 -*-

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

#
# Slides start here
#

@slide_noone
def title_slide (r):
	r.move_to (800, 50)
	r.put_text (
"""State\nof\nText\nRendering""",
width=800, height=500, valign=1, halign=-1)

	r.move_to (0, 530)
	r.put_text ("""Behdad Esfahbod\n<span font_desc="monospace">behdad@gnome.org\nhttp://behdad.org/text</span>""",
		    desc="12", halign=1, valign=-1)

who (behdad)

def list_slide (l, data=None):
	def s (r):
		return '\n'.join (l)
		#yield l[0]
		#for i in l[1:]:
		#	yield '\n'+i
	s.__name__ = l[0]
	slide (s, data)

list_slide ([
		"• CodeThink",
		"• Collabora",
		"• Fluendo",
		"• Igalia",
		"• Imendio",
		"• Opened Hand *",
		"• Openismus",
		"• ...",
	    ], data={'align': pango.ALIGN_LEFT})

@slide
def where_is_my_vote (r):
	r.set_source_rgb (0, .9, 0)
	r.paint ()
	r.set_source_rgb (1, 1, 1)
	return "Where\nis\nMy Vote?"

slide_noone("Q?")

if __name__ == "__main__":
	import slippy
	import stateoftext_theme
	import sys
	slippy.main (slides, stateoftext_theme)
	#slippy.main ("stateoftext_slides.py", "stateoftext_theme.py")
	sys.exit (0)

