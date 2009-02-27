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
	r.move_to (800, 100)
	r.put_text (
"""<b>GNOME</b>\n<span font_size="smaller">and</span>\nLiving a Happy Life""",
width=800, valign=1, halign=-1)

	r.move_to (0, 450)
	r.put_text ("""Behdad Esfahbod\n<span font_desc="16">behdad@behdad.org</span>""",
		    desc="20", halign=1, valign=-1)

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
		"<b>Organization</b>",
		"• Who am I?",
		"• What is GNOME?",
		"• What can GNOME do for you?",
		"• What can <i>you</i> do for GNOME?",
		"• Why should you join GNOME?",
	    ], data={'align': pango.ALIGN_LEFT})



slide_noone("Who am I?")

slide("Born in 1982\nin Sari, Iran")
list_slide ([
		"• Math?",
		"• Physics?",
		"• Computers?",
	    ], data={'align': pango.ALIGN_LEFT})
list_slide ([
		"IOI'99, Antalya",
		"IOI'2000, Beijing",
	    ], data={'align': pango.ALIGN_LEFT})
slide("Sharif\nUniversity of\nTechnology")
slide("FarsiWeb")
slide("Free\nas in\nFreedom")
slide("KDE\nor\nGNOME")
slide("University\nof\nToronto")
slide("First\nLaptop")
slide("P=NP?")
slide("Performance\nPatches")
slide("System\nSoftware")
slide("Summer\nof Code")
slide("PhD?")
slide("Red Hat")
slide("Board of\nDirectors")
slide("MBA!")



slide_noone("What is\nGNOME?")

slide("GNOME\n<span font_desc=\"smaller\">is</span>\nPeople")
slide_image("gnome-is-people.png")
slide("GNOME\nis the\nFree Desktop")
slide_image("screenshot-gnome-desktop.png", height=500)
slide("GNOME is\nInternationalized\nand Localized")
slide_image("gnome-ar.png")
slide("GNOME\nis a\nPlatform")
slide("GNOME\nMobile")
@slide_noone
def mobile_image_func (r):
	r.set_source_rgb (1, 1, 1)
	r.paint ()
	r.move_to (200, 400)
	r.put_image ("olpc.jpg", height=300)
	r.move_to (600, 400)
	r.put_image ("n810.jpg", height=300)
	r.move_to (380, 150)
	r.put_image ("openmoko.jpg", height=300)
	#r.set_allocation (000, 0, 800, 600)
	yield ""



slide_noone("What can GNOME\ndo for you?")

slide("Learning\nopportunities")
list_slide ([
		"• Reading Code",
		"• Code Review",
		"• Mentorship",
		"• ...",
	    ], data={'align': pango.ALIGN_LEFT})

slide("Internship\nopportunities")
list_slide ([
		"• Google Summer of Code",
		"• GNOME Outreach Program",
		"• Individual Companies",
		"• ...",
	    ], data={'align': pango.ALIGN_LEFT})

slide("Employment\nopportunities")
list_slide ([
		"• Red Hat",
		"• Novell",
		"• Canonical",
		"• Sun",
		"• Nokia",
		"• Google",
		"• ...",
	    ], data={'align': pango.ALIGN_LEFT})

slide("Entrepreneurship\nopportunities")
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



slide_noone("What can <i>you</i>\ndo for GNOME?")
slide("Testing")
slide("Translation")
slide("Usability")
slide("Bug Fixing")
slide("Development")
slide("Web\nDevelopment")
slide("Artistic\nContent")
slide("Marketing")
slide("Journalism")



slide_noone("Why should you\njoin GNOME?")
slide("Cool\nPeople")
slide_image("berlin.jpg")
slide("Helping\nPeople")
slide("Recognition")
slide("Satisfaction")
slide("Living\nHappily")
slide_noone("http://live.gnome.org/JoinGnome")

if __name__ == "__main__":
	import slippy
	import turkey_theme
	import sys
	slippy.main (slides, turkey_theme)
	#slippy.main ("turkey_slides.py", "turkey_theme.py")
	sys.exit (0)

