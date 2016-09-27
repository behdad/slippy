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
head_font="noto sans bold" # "Oswald Bold"
body_font="noto sans condensed 50" # "PT Sans"
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
	r.put_text ("<span font_desc='"+title_font+"' font_size='large'>Ten\nYears\nof\n"+
		    "HarfBuzz</span>",
		    valign=-1, halign=1, desc=title_font+" 128")

	r.restore()
	r.move_to (1890, 1000)
	r.scale(1.4, 1.4)
	r.put_text ("Behdad Esfahbod\nGoogle", halign=-1, valign=-1)

#slide_big("FontTools")

slide_title("Pre History", '\n'.join([
	"FreeType Layout",
	'',
	"Pango",
	'',
	"Qt",
	]))
slide_title("Early Days", '\n'.join([
	"<b>2006Q1</b> Import FTL code from Pango into HarfBuzz(old)",
	'',
	"<b>2006Q4</b> Start experimental rewrite, called harfbuzz-ng",
	'',
	"<b>2007Q1</b> Qt donated their shapers to HarfBuzz(old)",
	]))

slide_title("harfbuzz-ng goals", '\n'.join([
	"user-friendly",
	'',
	"robust",
	'',
	"efficient",
	'',
	"threadsafe",
	'',
	"portable",
	'',
	"featureful",
	]))

slide_title("Slow Days", '\n'.join([
	"<b>2007</b> 3 commits",
	'',
	"<b>2008</b> 25 commits",
	]))

slide_title("Faster Days", '\n'.join([
	"<b>2009</b> over 400 commits",
	"",
	"<b>2009Q4</b> HarfBuzz Hackfest at Mozilla Toronto",
	'',
	"<b>2009Q4</b> WebkitGTK+ Hackfest",
	'',
	'<b>2010Q2</b> HarfBuzz Hackfest in Reading, UK',
	'',
	'<b>2010</b> Firefox ships for Latin',
	]))

slide_title("Slower then Even Faster Days", '\n'.join([
	"<b>2012Q2</b> HarfBuzz Hackfest at Google Zurich",
	"",
	"<b>2012Q3</b> HarfBuzz Hackfest at Mozilla Toronto",
	'',
	"<b>2012Q3</b> Pango switches over",
	'',
	"<b>2012Q4</b> HarfBuzz Hackfest at Mozilla Vancouver",
	'',
	"<b>2012Q4</b> ChromeOS / Chrome Linux",
	'',
	"<b>2012Q4</b> ICU Layout port",
	]))

slide_title("Taking off", '\n'.join([
	"<b>2013Q1</b> HarfBuzz Hackfest at Google London / Mozilla London",
	'',
	"<b>2013Q2</b> Android switches",
	"",
	"<b>2013Q4</b> HarfBuzz Hackfest at Mozilla Paris / Google Paris",
	'',
	"<b>~2014</b> Firefox switches for all scripts",
	'',
	"<b>2014Q1</b> Chrome Windows switches",
	]))

slide_title("Maturity", '\n'.join([
	"<b>~2015</b> Chrome Mac switch",
	'',
	"<b>2015Q3</b> HarfBuzz Hackfest at Mozilla London: USE",
	'',
	"<b>2015Q3</b> HarfBuzz 1.0.0",
	'',
	"<b>2015Q4</b> HarfBuzz Hackfest at Mozilla London: Unicode 8.0",
	'',
	"<b>2016Q2</b> HarfBuzz Hackfest at Mozilla London: Unicode 9.0",
	]))

slide_title("Future", '\n'.join([
	"hb-ot-font",
	'',
	"OpenType MATH",
	'',
	"OpenType COLR/CPAL, SVG",
	'',
	"OpenType Variation Fonts (mutator?)",
	]))

#image_slide("pipeline.png", imgwidth=1900, imgheight=1000)

slide_big("Q&amp;A")

if __name__ == "__main__":
	import slippy
	import harfbuzz10years_theme
	slippy.main (slides, harfbuzz10years_theme, args=['--geometry', '1920x1024'])
