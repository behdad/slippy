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
def slide_who(f, who, data=None):
	if data:
		data = dict (data)
	else:
		data = {}
	data['who'] = who
	return slide_add (f, data)

def slide(f, data=None):
	return slide_who (f, whois, data=data)

def slide_heading(f, data=None):
	if data is None:
		data = {}
	if 'desc' not in data:
		data['desc'] = head_font
	if data and 'who' in data:
		return slide_who (f, data['who'], data=data)
	else:
		return slide_who (f, 0, data=data)

def slide_title (title, text):
	def s (r):
		ts = "<span font_desc='"+head_font+"'>"+title+"</span>\n"
		return ts + text
	s.__name__ = title
	data={'desc': body_font, 'align': pango.ALIGN_LEFT}
	slide (s, data)
def bullet_list_slide (title, items):
	def s (r):
		ts = "<span font_desc='"+head_font+"'>"+title+"</span>\n"
		return ts + '\n'.join ("• " + item for item in items)
	s.__name__ = title
	data={'desc': body_font, 'align': pango.ALIGN_LEFT}
	slide (s, data)

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
	r.move_to (960, 400)
	r.put_text ("<span font_desc='"+title_font+"' font_size='large'>OpenType GX</span>\n"+
		    "<span font_desc='"+subtitle_font+"' font_size='xx-small'>an exploratory proposal</span>",
		    valign=0, halign=0, desc=title_font+" 200")

	r.move_to (960, 800)
	r.put_text ("<span font_size='large' font_desc='"+mono_font+"' foreground='blue'>https://goo.gl/0N3zLy</span>\n\n"+
		    "Behdad Esfahbod\n<span font_size='x-small' font_desc='"+mono_font+"'>behdad@google.com</span>", desc=body_font+" 50", halign=0, valign=+1)

def agenda(i=None):
	items = [
	"Background",
	"Architecture",
	"Practicalities",
	"Proposal",
	"Implementation",
	"Possibilities",
	"Demos",
	"Discussion",
	]
	if i is not None:
		i = items.index(i)
		items[i] = "<span foreground='#444488'>%s</span>" % items[i]
	bullet_list_slide("Agenda", items)

agenda()

agenda('Background')
bullet_list_slide("Background", [
	"ATypI 2014 Barcelona",
	"Noto Phase III",
	"FontTools + Sascha = gvar",
	"FreeType + Adam = IUP",
	"Skia graphics + Skia font",
	"ATypI 2015: OpenType 2.0",
	"OpenType GX, the proposal",
	])

agenda('Architecture')
bullet_list_slide("Architecture", [
	"MM vs TrueType GX",
	"Copy some tables over",
	"Possibly extend (later)",
	"Extend OpenType tables",
	])
bullet_list_slide("Architecture", [
	"Non-invasive",
	"Existing workflows...\n"
	"  → Glyphs\n"
	"  → UFO+.designspace\n"
	"  → FontLab?"
	])

agenda('Practicalities')
bullet_list_slide("Practicalities", [
	"Overlap removal",
	"Cubic-to-quadratic",
	"CFF point numbers",
	"Extrapolation",
	])

agenda('Proposal')
bullet_list_slide("Proposal", [
	"Font variation metadata",
	"Glyph shape variation",
	"Font metrics variation",
	"Positioning variation",
	"Conditional subst &amp; pos",
	"Glyph metrics variation",
	"Hinting data variation",
	])

bullet_list_slide("Font var metadata", [
	"Apple 'fvar' table\n"
	"  → Arbitrary axes\n"
	"  → Named instances",
	"Apple 'avar' table\n"
	"  → MutatorMath Bender\n"
	"  → Luc(as) curve\n"
	"  → Pablo curve",
	"Clarify standard axes",
	])

bullet_list_slide("Glyph shape var", [
	"Apple 'gvar' table\n"
	"  → Arbitrary masters\n"
	"  → per glyph",
	"Apply to 'glyf' / CFF",
	])

bullet_list_slide("Font metrics var", [
	"Apple 'fmtx' table",
	"'fmtx' 2.0 for OS/2, etc",
	"No UPEM var allowed",
	])

bullet_list_slide("Positioning var", [
	"GPOS / GDEF",
	"Value / Anchor / Caret",
	"Device table\n"
	"  → VariationDevice",
	"Merger script",
	])

bullet_list_slide("Condi'nal subst &amp; pos", [
	"GSUB / GPOS",
	"Alternate lookups\n"
	"  → MutatorMath subst\n"
	"  → Glyphs 'bracket' trick",
	])

bullet_list_slide("Glyph metrics var", [
	"Needed for layout",
	"Performance",
	"New table for\n"
	"  → 'hmtx' vars\n"
	"  → 'vmtx' vars\n"
	"  → 'VORG' vars",
	])

bullet_list_slide("Hinting: TrueType", [
	"Apple 'cvar' table",
	"Extend ttfautohint",
	"FreeType autohinter",
	])
bullet_list_slide("Hinting: CFF", [
	"Hint op vars",
	"Extend AFDKO autohinter",
	"Run-time AFDKO hinter",
	])

agenda('Implementation')
slide_title("Implementation", (
	"fvar / avar / gvar / cvar\n"
	"  → Apple: OS X, iOS?\n"
	"  → FreeType (bug fixes)"
	))
slide_title("Implementation", (
	"fvar / avar / gvar / cvar\n"
	"  → FontTools\n"
	"    → varLib.__init__\n"
	"    → varLib.mutator"
	))
slide_title("Implementation", (
	"Combined with other tools\n"
	"  → UFO + .designspace\n"
	"  → Glyphs"
	))
slide_title("Implementation", (
	"GSUB / GPOS / GDEF\n"
	"  → Design\n"
	"  → Prototype"
	))

agenda('Possibilities')
source_slide("""
@font-face {
	font-family: MyFont;
	font-weight: 700;
	font-stretch: condensed;
	src: url("fonts/myvar.ttc#2,wght=1.4,wdth=0.7")
		format(collection,variation),
	     url("fonts/fallback-bold-cond.ttf"),
		format(truetype);
}
""", "css")
source_slide("""
@font-family {
	font-family: MyFont;
	src: url("myvar.ttf") format(truetype);
	font-weight-min: 100;
	font-weight-max: 500;
	font-stretch-min: 70;
	font-stretch-max: 130;
}
""", "css")
bullet_list_slide("Possibilities", [
	"Justification",
	"Animation",
	"Grading",
	"Tickling",
	"...",
	])

agenda('Demos')

agenda('Discussion')

bullet_list_slide("Links", [
	"https://github.com/behdad/fonttools",
	"https://github.com/googlei18n/fontmake",
	"https://groups.google.com/forum/#!forum/fonttools",
])

slide("<b>Q?</b>", data={"desc":title_font})

if __name__ == "__main__":
	import slippy
	import opentypegx_theme
	slippy.main (slides, opentypegx_theme, args=['--geometry', '1920x1200'])
