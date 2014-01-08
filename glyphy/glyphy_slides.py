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

who ("keithp.png")
slide("<b>It's insane!</b>")
who (behdad)


"""
Make ten times faster, thought Im insane.
Now Keith thinks the code is insane.
Have to make it another 5 times faster, now I think I'm becoming insane.

Mobile GPU perf unheard of.  Old Tegra had one fetch one add...
http://venturebeat.com/2014/01/05/nvidia-announces-tegra-k1-a-super-mobile-chip-with-192-cores/

bugs w drivers

Image gallery.  Spooky etc.

bilinear comparison
freetype-gl comparison
"""

@slide_noone
def cluster_image (r):
	r.move_to (400, 300)
	r.set_allocation (200, 0, 400, 600)
	yield ""

if __name__ == "__main__":
	import slippy
	import glyphy_theme
	slippy.main (slides, glyphy_theme)
