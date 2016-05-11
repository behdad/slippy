#!/usr/bin/python
# -*- coding:utf8 -*-

# Copyright 2016 Behdad Esfahbod <behdad@google.com>

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

title_font="Impact"
subtitle_font="Oswald Bold"
head_font="sans Bold" # "Oswald Bold"
body_font="sans" # "PT Sans"
mono_font="Consolas, monospace"

slides = []
def slide_add(f, data=None, width=1920, height=1200):
	if data is None:
		data = {}
	if "desc" not in data:
		data['desc'] = body_font
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
def slide_who(f, who, data=None, scale=None):
	if data:
		data = dict (data)
	else:
		data = {}
	data['who'] = who
	if not scale: scale = 1.4
	def slider(r):
		r.move_to (100, 80)
		r.scale(scale, scale)
		r.put_text (f, valign=1, halign=1, desc=body_font)
		#r.set_allocation (x, y, width, height)
	if isinstance(f, basestring):
		return slide_add (slider, data)
	return slide_add (f, data)

def slide(f, data=None, scale=None):
	return slide_who (f, whois, data=data, scale=scale)

def slide_heading(f, data=None):
	if data is None:
		data = {}
	if 'desc' not in data:
		data['desc'] = head_font
	if data and 'who' in data:
		return slide_who (f, data['who'], data=data)
	else:
		return slide_who (f, 0, data=data)

def slide_title (title, text, scale=None):
	ts = '' if not title else "<span font_desc='"+head_font+"'>"+title+"</span>\n\n"
	ts = ts + text.strip()
	#s.__name__ = title
	data={'desc': body_font, 'align': pango.ALIGN_LEFT}
	slide (ts, data, scale=scale)
def bullet_list_slide (title, items):
	ts = "<span font_desc='"+head_font+"'>"+title+"</span>\n\n"
	ts = ts + '\n'.join ("- " + item for item in items)
	#s.__name__ = title
	data={'desc': body_font, 'align': pango.ALIGN_LEFT}
	slide (ts, data)

def image_slide (f, width=1920, height=1200, imgwidth=0, imgheight=0, xoffset=0, yoffset=0, data=None):
	def s (r):
		r.move_to (960+xoffset, 600+yoffset)
		r.put_image (f, width=imgwidth, height=imgheight)
		x = (1920 - width) * .5
		y = (1200 - height) * .5
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

def source_slide(s, lang):
	s = highlight(s, lang)
	s = "<span font_desc='"+mono_font+"'>" + s + "</span>"
	slide_heading (s, data={'align': pango.ALIGN_LEFT})

def python_slide(s):
	source_slide(s, lang="py")

def xml_slide(s):
	source_slide(s, lang="xml")

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
	s = "<span font_desc='"+mono_font+"'>" + s + "</span>"
	slide_heading (s, data={'align': pango.ALIGN_LEFT})

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
	s = "<span font_desc='"+mono_font+"'>" + s + "</span>"
	if who:
		slide_heading (s, data={'align': pango.ALIGN_LEFT, 'who': who})
	else:
		slide_heading (s, data={'align': pango.ALIGN_LEFT})


#
# Slides start here
#

who (behdad)

@slide
def title_slide (r):
	r.move_to (50, 100)
	r.put_text ("<span font_desc='"+title_font+"' font_size='large'>FontTools/TTX\n"+
		    "The Power of Open Source for OpenType</span>",
		    valign=1, halign=1, desc=title_font+" 72")

	r.move_to (300, 600)
	r.scale(1.4, 1.4)
	r.put_text ("Part 1: Just van Rossum\nPart 2: Behdad Esfahbod\nPart 3: Q&amp;A\n\n<span font_desc='"+mono_font+"'>github.com/behdad/fonttools</span>", halign=1, valign=+1)

def agenda(i=None):
	items = [
	]
	if i is not None:
		i = items.index(i)
		items[i] = "<span foreground='#0f007e'>%s</span>" % items[i]
	bullet_list_slide("Agenda", items)


bullet_list_slide("Background: 2003", [
	"FarsiWeb days",
	])
bullet_list_slide("Background: 2013", [
	"July: Subsetter is born",
	])
bullet_list_slide("Background: 2013", [
	"July: 'COLR'/'CPAL' table",
	"August: Google color fonts",
	"August: 'SVG ' table from Read Roberts",
	"August: Cosimo shows up",
	"August: Remove numpy dependency",
	"September: 'sbix' table form Jens Kutilek",
	"October: ATypI 2013 Amsterdam",
	"November: Port to Python 2/3",
	"...",
	])

bullet_list_slide("2014", [
	"Optimized the subsetter",
	"Implemented merger",
	"Hooked up the test suite",
	"Released 2.5",
	"ATypI 2014 Barcelona",
	])

bullet_list_slide("2015", [
	"Sascha joiners",
	"gvar/fvar/avar",
	"Noto pipeline starts",
	"Released 3.0",
	"ATypI 2015 Saõ Paulo",
	"Coninuous integration",
	])

bullet_list_slide("Noto pipeline", [
	"glyphs2ufo",
	"robofab vs extractor",
	])

slide_title("2015-01", """
https://github.com/robofab-developers/robofab/pull/29

@letterror:
Does this pull make robofab dependent on a
specific fork of FontTools?
""")

slide_title("2015-04", """
https://github.com/typesupply/compositor/issues/7

Subject: test Coverage object if it has a Format attr

@typemytype:
a small patch to make compositor work with the github
fontTools version

@typesupply:
Is there a change list somewhere of all the things that
you've done since forking from the original FontTools?
We're running into lots of things so it would be good to
have something to review.
""", scale=1.3)

image_slide("lucky-cat.jpg")

slide_title("\n\n", """
"These Dutch people..."

"Google forked us..."
""")

bullet_list_slide("Noto pipeline", [
	"glyphs2ufo",
	"robofab",
	"ufo2fdk",
	])

bullet_list_slide("Noto pipeline: feaLib", [
	"glyphs2ufo",
	"robofab",
	"ufo2fdk → ufo2ft",
	"fontTools.feaLib",
	"booleanOperations",
	])

bullet_list_slide("Noto pipeline: mtiLib", [
	"glyphs2ufo",
	"robofab",
	"ufo2fdk → ufo2ft",
	"fontTools.feaLib / fontTools.mtiLib",
	"booleanOperations",
	])

bullet_list_slide("Noto pipeline: MutatorMath", [
	"glyphs2ufo",
	"robofab",
	"MutatorMath",
	"ufo2fdk → ufo2ft",
	"fontTools.feaLib",
	"booleanOperations",
	])

bullet_list_slide("Noto pipeline: cu2qu", [
	"glyphs2ufo",
	"robofab",
	"MutatorMath",
	"ufo2fdk → ufo2ft",
	"fontTools.feaLib",
	"booleanOperations",
	"cu2qu",
	])

bullet_list_slide("Noto pipeline: defcon", [
	"glyphs2ufo",
	"ufoLib",
	"<span strikethrough='true'>robofab</span> → defcon",
	"MutatorMath",
	"ufo2fdk → ufo2ft",
	"fontTools.feaLib",
	"booleanOperations",
	"cu2qu",
	])

bullet_list_slide("OpenType 2.0 / GX / Saõ Paulo", '')

slide_title("2015-11-26","""
From: Behdad Esfahbod
To: Erik van Blokland

Hi Erik,

I'm planning to visit The Hague in January, mostly to
meet Bahman, and hopefully to work with you.  We
can discuss / hack on interpolation, OpenType GX,
or really anything fonts &amp; Python.  Would you be
interested in that?  I'm thinking some time the week
of January 18th.
""")
slide_title("2015-11-27","""
From: Erik van Blokland
To: Behdad Esfahbod

Hi Behdad,

That's unexpected :) I have time that week and we
can meet earlier in the week.  I do have some
academic obligations on Thursday and Friday and
the Type and Media open day that Saturday.

Would that work for you?
""")

slide_title("2016-01-16","""
From: Erik van Blokland
To: Behdad Esfahbod

Hi Behdad,

I hope to see you next week! It’s above freezing
but a lot of rain.

Just is at the academy on Wednesday and would like
to meet you.  Frederik Berlaen lives in Gent, Belgium
and can come up on Friday or Thursday.
""")

slide_title("2016-01-20","""
Tabs or spaces?
""", scale=2)

bullet_list_slide("Noto pipeline", [
	"glyphs2ufo",
	"ufoLib",
	"defcon",
	"MutatorMath",
	"ufo2fdk → ufo2ft",
	"fontTools.feaLib",
	"booleanOperations",
	"cu2qu",
	])

bullet_list_slide("Noto pipeline: compreffor", [
	"glyphs2ufo",
	"ufoLib",
	"defcon",
	"MutatorMath",
	"ufo2fdk → ufo2ft",
	"fontTools.feaLib",
	"booleanOperations",
	"cu2qu",
	"compreffor",
	])

bullet_list_slide("Noto pipeline: fontmake", [
	"glyphs2ufo",
	"ufoLib",
	"defcon",
	"MutatorMath",
	"ufo2fdk → ufo2ft",
	"fontTools.feaLib",
	"booleanOperations",
	"cu2qu",
	"compreffor",
	"fontmake",
	])

bullet_list_slide("Noto pipeline: noto-source", [
	"glyphs2ufo",
	"ufoLib",
	"defcon",
	"MutatorMath",
	"ufo2fdk → ufo2ft",
	"fontTools.feaLib",
	"booleanOperations",
	"cu2qu",
	"compreffor",
	"fontmake",
	"noto-source",
	])

bullet_list_slide("Noto pipeline: TODO", [
	"fontTools.varLib",
	"CFF operator specializer",
	"ttfautohint",
	"FDK hinter",
])

image_slide("jenga1.jpg")
image_slide("jenga2.jpg")

bullet_list_slide("Noto pipeline: challenges", [
	"Dependency hell (see pen hell?!)",
	"Stability",
	"Speed",
	"Flexibility",
])

slide_title("Eng time!", "")
slide_title("from fontTools.misc.py23 import *", "")
slide_title("Snippets/symfont.py roboto.ttf", """
glyph: slash
Area: 0.0631374
Correlation: 0.964027
Covariance: 0.0190825
MeanX: 0.196996
MeanY: 0.324567
Moment1X: 0.0124378
Moment1Y: 0.0204923
Moment2XX: 0.00294835
Moment2XY: 0.00524173
Moment2YY: 0.00978664
Perimeter: 1.81758
Slant: 0.38425
StdDevX: 0.0888251
StdDevY: 0.222849
VarianceX: 0.0078899
VarianceY: 0.0496617
""", scale=1.0)
slide_title("compreffor", "")
slide_title("cu2qu", "")

slide_title("Links", """
github.com/googlei18n/noto-source
github.com/googlei18n/fontmake
github.com/googlei18n/glyphsLib
github.com/unified-font-object/ufoLib
github.com/typesupply/defcon
github.com/LettError/MutatorMath
github.com/typesupply/fontMath
github.com/googlei18n/ufo2ft
github.com/typemytype/booleanOperations
github.com/googlei18n/cu2qu
github.com/googlei18n/compreffor
github.com/behdad/fonttools
""")

slide_title("Q&amp;A", '')

if __name__ == "__main__":
	import slippy
	import fonttools2016_theme
	slippy.main (slides, fonttools2016_theme, args=['--geometry', '1920x1200'])
