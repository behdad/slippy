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
head_font="noto sans" # "Oswald Bold"
body_font="noto sans light 50" # "PT Sans"
xbody_font="noto sans thin 200" # "PT Sans"
mono_font="Consolas, monospace"

slides = []
def slide_add(f, data=None, width=1920, height=1024):
	if data is None:
		data = {}
	if "desc" not in data:
		data['desc'] = body_font
	slides.append ((f, data, width, height))
	return f

import pango, pangocairo, cairo

# And convenience functions to add a slide.  Can be
# used as a function decorator, or called directly.
def slide(f, data=None, scale=None):
	if data:
		data = dict (data)
	else:
		data = {}
	if not scale: scale = 1.
	def slider(r):
		r.move_to (50, 30)
		r.scale(scale, scale)
		r.put_text (f, valign=1, halign=1, desc=body_font)
		#r.set_allocation (x, y, width, height)
	if isinstance(f, basestring):
		return slide_add (slider, data)
	return slide_add (f, data)

def slide_big(f, data=None, scale=None):
	if data:
		data = dict (data)
	else:
		data = {}
	if not scale: scale = 1
	def slider(r):
		r.move_to (960, 512)
		r.scale(scale, scale)
		r.put_text (f, valign=0, halign=0, desc=xbody_font)
		#r.set_allocation (x, y, width, height)
	if isinstance(f, basestring):
		return slide_add (slider, data)
	return slide_add (f, data)

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

def image_slide (f, width=1920, height=1024, imgwidth=0, imgheight=0, xoffset=0, yoffset=0, data=None):
	def s (r):
		r.move_to (960+xoffset, 512+yoffset)
		r.put_image (f, width=imgwidth, height=imgheight)
		x = (1920 - width) * .5
		y = (1024 - height) * .5
		r.set_allocation (x, y, width, height)
	s.__name__ = f
	slide (s, data)
	return s

#
# Slides start here
#

@slide
def title_slide (r):
	r.move_to (30, 1000)
	r.save()
	r.set_source_rgb(0xf6/255., 0x48/255., 0x48/255.)
	r.put_text ("<span font_desc='"+title_font+"' font_size='large'>The\nOpen\nSource\n"+
		    "Python\nFont\nProduction\nPipeline</span>",
		    valign=-1, halign=1, desc=title_font+" 72")

	r.restore()
	r.move_to (1890, 1000)
	r.scale(1.4, 1.4)
	r.put_text ("Marek Jeziorek\nBehdad Esfahbod\nGoogle", halign=-1, valign=-1)

slide_big("FontTools")
slide_big("UFO")
slide_big("ATypI 2014")
slide_big("FontTools")
slide_big("AFDKO")
slide_big("Noto")

bullet_list_slide("Noto pipeline", [
	"glyphs2ufo",
	"robofab vs extractor",
	])

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

bullet_list_slide("Noto pipeline: ttfautohint", [
	"glyphs2ufo",
	"ufoLib",
	"defcon",
	"MutatorMath",
	"ufo2fdk → ufo2ft",
	"fontTools.feaLib",
	"booleanOperations",
	"cu2qu",
	"compreffor",
	"ttfautohint",
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
	"ttfautohint",
	"fontmake",
	])

image_slide("pipeline.png", imgwidth=1900, imgheight=1000)
image_slide("jenga2.jpg")

bullet_list_slide("Noto pipeline: challenges", [
	"Dependency hell",
	"Stability",
	"Speed",
	"Flexibility",
])

bullet_list_slide("Noto pipeline: TODO", [
	"fontTools.varLib",
	"CFF operator specializer",
	"FDK hinter",
])

slide_title("", """
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
github.com/googlei18n/noto-source
www.freetype.org/ttfautohint/
""")

slide_big("Q&amp;A")

if __name__ == "__main__":
	import slippy
	import fontpipeline_theme
	slippy.main (slides, fontpipeline_theme, args=['--geometry', '1920x1024'])
