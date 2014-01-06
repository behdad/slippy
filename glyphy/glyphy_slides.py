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
keithp = +1
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

@slide_noone
def title_slide (r):
	r.move_to (400, 100)
	r.put_text (
"""Generating perfectly\ntext-extractable\nPDFs""", width=800, valign=1)

	r.move_to (0, 450)
	r.put_text ("""Behdad Esfahbod\n<span font_desc="16">besfahbo@<span foreground="#c00">redhat</span>.com</span>""",
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

slide_noone("Terminology 101")

list_slide ([
		"• Character",
		"• Glyph",
		"• <i>Codepoint</i>",
	    ], data={'align': pango.ALIGN_LEFT})
list_slide ([
		"• Input text",
		"• Output glyph",
		"• <i>Encoded codepoints</i>",
	    ], data={'align': pango.ALIGN_LEFT})
list_slide ([
		'• "Hello"',
		"• 〈1,2,3,3,4〉",
		"• 〈0102030304〉",
	    ], data={'align': pango.ALIGN_LEFT})
		
slide_noone('<span size="larger">Overview of\nPDF Fonts</span>\n<span size="smaller">(subsetted,\ncustom encoding)</span>')

who (keithp)

list_slide ([
		'• Simple',
		'• Composite',
	    ], data={'align': pango.ALIGN_LEFT})

who (behdad)

slide ('<b>Simple Fonts</b>\neach byte of\nencoded codepoints\nrepresents one codepoint')
list_slide ([
		'<b>Simple Fonts</b>',
		'• Type1',
		'• TrueType',
		'• Type3',
	    ], data={'align': pango.ALIGN_LEFT})

slide ('<b>Composite Fonts</b>\ncomplex mapping of\nencoded codepoints\nto codepoints')
list_slide ([
		'<b>Composite Fonts</b>',
		'<b>(CID-keyed Fonts)</b>',
		'• Type0 (CFF)',
		'• Type2 (TrueType)',
	    ], data={'align': pango.ALIGN_LEFT})

slide ('A CID is exactly\nwhat we called\na codepoint')

slide ('<b>Observation</b>\nAll PDF fonts can\nhave arbitrary\ncodepoint-to-glyph\nmapping')
slide ('<b>ToUnicode</b>\nAll PDF fonts can\nhave a codepoint-to-\nsequence-of-characters\nmapping')
slide ('ToUnicode mapping\nis the only\nstandard way for\ntext extraction')

slide ("<b>Broken Practice</b>\nUse original font's\ncharacter-to-glyph\nmapping to generate\nToUnicode mapping")
slide ('Assumes\nreversible\nchar-to-glyph\nmapping')

slide_noone('What\nTo Do?')
slide('Admit that\nchar-to-glyph\nmapping is\n not 1-to-1')
slide('<b>Corollary</b>\noutput glyphs\nare not enough\nto produce\ngood PDF text')


slide_noone("Terminology 201")

list_slide ([
		"• Cluster",
	    ], data={'align': pango.ALIGN_LEFT})
@slide_noone
def cluster_image (r):
	r.move_to (400, 300)
	r.set_allocation (200, 0, 400, 600)
	yield ""
list_slide ([
		"<b>Cluster</b>",
		"• Grapheme cluster: ö",
		"• Ligature cluster:",
		'  - Typographical: 〈<span font_desc="Doulos SIL">f</span>,<span font_desc="Doulos SIL">i</span>〉 → 〈<span font_desc="Doulos SIL">fi</span>〉',
		'  - Orthographical: 〈‎<span font_desc="Nazli">ﻟ</span>,<span font_desc="Nazli">ﺎ</span>‎〉 → 〈<span font_desc="Nazli">ﻻ</span>〉',
	    ], data={'align': pango.ALIGN_LEFT})
list_slide ([
		"<b>Cluster</b>",
		"• M input character",
		"• N output glyphs",
		"• M→N cluster"
	    ], data={'align': pango.ALIGN_LEFT})
list_slide ([
		"• Cluster mapping",
	    ], data={'align': pango.ALIGN_LEFT})
slide ('Any good\nPDF generator\nshould take\ninput text,\noutput glyphs,\n<i>and</i>\ncluster mapping')

slide_noone("What To Do\nWith Them?")
slide ("M→1")
slide ("M→0")
slide ("M→N")

slide_noone("Issues")
slide ("0→1")
slide ("How to\nbreak?")
slide ("<i>Cursor</i>\npositions")
slide ("Run\norder")
slide ("Bidi")

slide_noone ('<span font_desc="Doulos SIL">~fin~</span>')

if __name__ == "__main__":
	import slippy
	import glyphy_theme
	slippy.main (slides, glyphy_theme)
