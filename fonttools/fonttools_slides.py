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

title_font="Cinzel"
head_font="Julius Sans One Bold"
body_font="Merriweather Sans Light"

slides = []
def slide_add(f, data=None, width=800, height=600):
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
	s = "<span font_desc='monospace'>" + s + "</span>"
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
	s = "<span font_desc='monospace'>" + s + "</span>"
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
	s = "<span font_desc='monospace'>" + s + "</span>"
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
	r.move_to (400, 250)
	r.put_text ("<span font_desc='"+title_font+" bold'>FontTools</span>\n"+
		    "<span font_desc='"+head_font+" 30'>"+
		    "reviving an Open Source project,\n"+
		    "<span strikethrough='true'>re</span>building a thriving community"+
		    "</span>", valign=0, halign=0, desc=title_font+" 100")

	r.move_to (400, 550)
	r.put_text ("""Behdad Esfahbod""", desc=body_font+" 20", halign=0, valign=-1)

bullet_list_slide("History", [
	"Started in 1999ish",
	"by Just van Rossum",
	"of LettError fame",
	"Slowed down by 2004",
	"I picked it up last year"])
bullet_list_slide("What is it?", [
	"Two things: TTX and fontTools",
	"TTX converts fonts to XML and back",
	"fontTools is a Python library",
	"Font engineer's calculator",
	"Closely reflecting OpenType tables",
	"Minimum abstractions"])

slide_heading("TTX")
xml_slide("""
<?xml version="1.0" encoding="utf-8"?>
<ttFont sfntVersion="\\x00\\x01\\x00\\x00" ttLibVersion="2.5">

  <GlyphOrder>
    <!-- The 'id' attribute is only for humans; it is ignored when parsed. -->
    <GlyphID id="0" name=".notdef"/>
    <GlyphID id="1" name="T"/>
    <GlyphID id="2" name="X"/>
  </GlyphOrder>

  <head>
    <!-- Most of this table will be recalculated by the compiler -->
    <tableVersion value="1.0"/>
    <fontRevision value="1.001"/>
    <checkSumAdjustment value="0x22ff1f02"/>
    <magicNumber value="0x5f0f3cf5"/>
    <flags value="00000000 00001011"/>
    <unitsPerEm value="1000"/>
    ...
  </head>

  <hhea>
    <tableVersion value="1.0"/>
    <ascent value="863"/>
    <descent value="-228"/>
    <lineGap value="0"/>
    ...
  </hhea>
""")
xml_slide("""
  <maxp>
    <!-- Most of this table will be recalculated by the compiler -->
    <tableVersion value="0x10000"/>
    <numGlyphs value="3"/>
    <maxPoints value="68"/>
    <maxContours value="7"/>
    ...
  </maxp>

  <OS_2>
    <version value="3"/>
    <xAvgCharWidth value="560"/>
    <usWeightClass value="400"/>
    <usWidthClass value="5"/>
    <fsType value="00000000 00000000"/>
    ...
  </OS_2>
""")
xml_slide("""
  <hmtx>
    <mtx name=".notdef" width="260" lsb="0"/>
    <mtx name="T" width="576" lsb="22"/>
    <mtx name="X" width="584" lsb="26"/>
  </hmtx>

  <cmap>
    <tableVersion version="0"/>
    <cmap_format_4 platformID="3" platEncID="1" language="0">
      <map code="0x54" name="T"/><!-- LATIN CAPITAL LETTER T -->
      <map code="0x58" name="X"/><!-- LATIN CAPITAL LETTER X -->
    </cmap_format_4>
  </cmap>

  <loca>
    <!-- The 'loca' table will be calculated by the compiler -->
  </loca>
""")
xml_slide("""
  <glyf>

    <!-- The xMin, yMin, xMax and yMax values
         will be recalculated by the compiler. -->

    <TTGlyph name=".notdef"/><!-- contains no outline data -->

    <TTGlyph name="T" xMin="22" yMin="0" xMax="554" yMax="715">
      <contour>
        <pt x="264" y="673" on="1"/>
        <pt x="22" y="673" on="1"/>
        <pt x="22" y="715" on="1"/>
        <pt x="554" y="715" on="1"/>
        <pt x="554" y="673" on="1"/>
        <pt x="312" y="673" on="1"/>
        <pt x="312" y="0" on="1"/>
        <pt x="264" y="0" on="1"/>
      </contour>
      <instructions><assembly>
        </assembly></instructions>
    </TTGlyph>

    <TTGlyph name="X" xMin="26" yMin="0" xMax="558" yMax="715">
      ...
    </TTGlyph>

  </glyf>
""")
xml_slide("""
  <name>
    <namerecord nameID="1" platformID="3" platEncID="1" langID="0x409">
      Julius Sans One
    </namerecord>
    <namerecord nameID="2" platformID="3" platEncID="1" langID="0x409">
      Regular
    </namerecord>
  </name>

  <post>
    <formatType value="3.0"/>
    <italicAngle value="0.0"/>
    <underlinePosition value="-75"/>
    <underlineThickness value="50"/>
    <isFixedPitch value="0"/>
    <minMemType42 value="0"/>
    <maxMemType42 value="0"/>
    <minMemType1 value="0"/>
    <maxMemType1 value="0"/>
  </post>

</ttFont>
""")

slide_heading("fontTools")
bullet_list_slide("<span font_desc='monospace' foreground='#080'>from <span foreground='#00f'><b>fontTools</b></span> import</span>", [
	"afmLib",
	"cffLib",
	"<span strikethrough='true'>fondLib</span>",
	"<span strikethrough='true'>nfntLib</span>",
	"t1Lib",
	"<b>ttLib</b>",
	])
python_slide(open("snippets/unencoded.py").read())
python_slide("""
set(['A.salt',
     'B.salt',
     'E.salt',
     'E_x',
     'F_i',
     'N.salt',
     'NULL',
     'T_h',
     'T_i',
     'a.end',
     ...
     'y_z'])
""")

bullet_list_slide("Framework", [
	"Compiler / decompiler",
	"XML serialization",
	"Optimizer",
	"Library",
	"A tool to build products with",
	"Not an end product",
])
bullet_list_slide("Philosophy", [
	"Minimal abstraction",
	"Hide byte layout, redundancy, etc",
	"Platform to build on",
])
bullet_list_slide("Why?", [
	"Free Software",
	"Python (2.7+ &amp; 3.x)",
	"Portable",
	"No dependencies",
	"Non-destructive",
	"Batch-friendly",
])
bullet_list_slide("What for?", [
	"Figuring out what's inside a font",
	"Diff'ing font versions",
	"Final steps of producing fonts",
	"Hotfixing existing fonts",
	"Reporting and analysis over <i>many</i> fonts",
	"Server-side reporting and manipulation",
	"Readable VCS-friendly font source code",
	"Subsetting and merging fonts",
])
bullet_list_slide("Hotfixing", [
	"XML and back",
	"Python recipes",
	"Interactive Python",
])
python_slide(open("snippets/drop_glyphnames.py").read())
python_slide(open("snippets/rename_glyphs.py").read())

bullet_list_slide("New work", [
	"Bitmap tables, color tables, misc tables",
	"WOFF1 read and write",
	"More stable XML format",
	"More optimized font files",
	"Bug fixes; many of them",
	"Major speed-up",
	"New tools",
])

bullet_list_slide("Tools", [
	"pyftsubset",
	"pyftmerge",
	"pyftinspect",
])
bullet_list_slide("pyftsubset", [
	"OpenType font subsetter &amp; optimizer",
	"TrueType and CFF flavored",
	"SFNT and WOFF1",
	"Full OpenType Layout support",
	"File-size optimizations",
	"Designed for webfont productions",
	"Used for sub-family instantiation",
])
source_slide(open("snippets/subsetting.txt").read(), "text")
bullet_list_slide("pyftmerge", [
	"Font merging tool",
	"Very early prototype",
	"Fonts having same format, upem",
	"TrueType-flavored only",
	"Retains hinting from one font",
	"Handles conflicting characters",
	"Designed for Noto",
	"Used for merging Latin and non-Latin",
])
source_slide(open("snippets/merging.txt").read(), "text")

# 1. Feel free to mention in your talk Yannis Haralambous' book "Fonts & Encodings" [1], simply because it can be seen as a "user manual for TTX". It talks extensively about the various SFNT tables, and illustrates them using TTX XML structures. So, while fontTools itself has very lacking documentation*, the book is actually a great companion. When I read the book and I look at the .ttx XML representation of a font, I have good chances to actually understand how it all works. 

slide_heading("FontTools")
bullet_list_slide("Strengths", [
	"Supports wide array of tables",
	"Low-level, non-destructive",
	"Python",
	"Self-documenting",
	"Optimized output",
	"Extensible",
	"Supports all color tables",
])
bullet_list_slide("Weaknesses", [
	"Supports wide array of tables",
	"Low-level, non-destructive",
	"Python",
	"Undocumented",
	"Always optimizes output",
	"Not well-extensible",
	"Supports many legacy tables",
])
bullet_list_slide("Users", [
	"Google Fonts; misc foundries",
	"Font Bakery, AFDKO, etc",
	"Adam Twardoch; others",
	"...",
])
bullet_list_slide("Community", [
	"https://github.com/behdad/fonttools/",
	"https://groups.google.com/forum/#!forum/fonttools",
	"http://sourceforge.net/projects/fonttools/",
])

bullet_list_slide("Future work", [
	"More font optimization",
	"Better input: .fea / UFO",
	"Lint tool",
	"TrueType / CFF conversion",
	"Subsetting more tables",
	"Better merging",
])
bullet_list_slide("Future work: optimization", [
	"Optimal packing: glyf flags / PUSH / etc",
	"CFF outline operation specializer",
	"CFF subroutinizer",
	"TrueType outline optimizer? (fontcrunch)",
	"TrueType bytecode analysis",
	"UPEM reduction",
])

slide("<b>Q?</b>", data={"desc":title_font})
python_slide('')

python_slide(open("snippets/drop_glyphnames_cff.py").read())
xml_slide(open("snippets/tofu.ttx").read())

if __name__ == "__main__":
	import slippy
	import fonttools_theme
	slippy.main (slides, fonttools_theme)
