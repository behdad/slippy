#!/usr/bin/python
# -*- coding:utf8 -*-

slides = []
def slide_add(f, data=None, width=800, height=400):
	slides.append ((f, data, width, height))
	return f
import pango
def text_slide (l):
	def s (r):
		for i in l:
			yield i
		for i in range (30):
			yield ''
	slide_add (s, data={'align': pango.ALIGN_LEFT})

text = ["""“Free software” is a matter of liberty, not price. To understand the 
concept, you should think of “free” as in “free speech”, not as in “free beer.”

Free software is a matter of the users' freedom to run, copy, 
distribute, study, change and improve the software.""",
"""More precisely, it refers to four kinds of freedom, for the users of the 
software:
------------------------------------------------------------------------------
0. The freedom to run the program, for any purpose.
1. The freedom to study how the program works, and adapt it to your needs.
   Access to the source code is a precondition for this.
2. The freedom to redistribute copies so you can help your neighbor.
3. The freedom to improve the program, and release your improvements to 
   the public, so that the whole community benefits.
   Access to the source code is a precondition for this.
------------------------------------------------------------------------------""",
"""The concept of these 4 freedoms (0-3) were developed by Richard 
Stallman.

To set a good example he started to write a completely free operating system.

Today Linux based GNU systems are used by millions of people around 
the world."""]

for slide in text:
	text_slide (slide)

if __name__ == "__main__":
	import slippy
	import gnu_theme
	slippy.main (slides, gnu_theme, args = ['--slideshow', '--delay', '0.05', '--repeat'])
