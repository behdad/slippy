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

texts = {}
texts['en'] = """“Free software” is a matter of liberty, not price. To understand the 
concept, you should think of “free” as in “free speech”, not as in “free beer.”

Free software is a matter of the users' freedom to run, copy, 
distribute, study, change and improve the software.

More precisely, it refers to four kinds of freedom, for the users of the 
software:
------------------------------------------------------------------------------
0. The freedom to run the program, for any purpose.
1. The freedom to study how the program works, and adapt it to your needs.
   Access to the source code is a precondition for this.
2. The freedom to redistribute copies so you can help your neighbor.
3. The freedom to improve the program, and release your improvements to 
   the public, so that the whole community benefits.
   Access to the source code is a precondition for this.
------------------------------------------------------------------------------
The concept of these 4 freedoms (0-3) were developed by Richard Stallman.

To set a good example he started to write a completely free operating system.

Today Linux based GNU systems are used by millions of people around the world."""

texts['de'] = """Bei dem Begriff „Freie Software“ geht es um Freiheit, nicht um den Preis.
Um dieses Konzept richtig begreifen zu können, sollte man an „frei“ wie in
„freie Rede“ denken, und nicht an „Freibier“.

Bei „Freier Software“ geht es um die Freiheit des Benutzers die Software nach
Belieben zu benutzen, zu kopieren, weiter zu geben, die Software zu studieren,
sowie Änderungen und Verbesserungen an der Software vornehmen zu können.
------------------------------------------------------------------------------
Genauer gesagt, bezieht sich der Begriff „Freie Software“ auf vier Arten von
Freiheit, die der Benutzer der Software hat:

0. Die Freiheit, das Programm für jeden Zweck zu benutzen.
1. Die Freiheit, zu verstehen, wie das Programm funktioniert und wie man es
   für seine Ansprüche anpassen kann.
   Der Zugang zum Quellcode ist dafür Voraussetzung.
------------------------------------------------------------------------------
2. Die Freiheit, Kopien weiterzuverbreiten, so dass man seinem Nächsten
   weiterhelfen kann.
3. Die Freiheit, das Programm zu verbessern und die Verbesserungen der
   Allgemeinheit zur Verfügung zu stellen, damit die ganze Gemeinschaft davon
   profitieren kann.
   Der Zugang zum Quellcode ist dafür Voraussetzung.
------------------------------------------------------------------------------
Diese 4 Freiheiten (0-3) wurden so von Richard Stallman entworfen.

Um mit gutem Beispiel voran zu gehen, hat er angefangen, ein vollständig
freies Betriebssystem zu entwickeln.

Heute werden Linux basierte GNU Systeme von vielen Millionen Anwendern benutzt."""

texts['he'] = """"תוכנה חופשית" זה ענײן של חירות, לא של מחיר. כדי להבין את העקרון,
צריך לחשוב על "חופש" כמו ב"חופש הביטוי"...\
.effectpause
.back 3
 ולא כמו ב"בירה חופשי".

תוכנה חופשית נוגעת לחופש של משתמשים להריץ, להפיץ הפצת-המשך, ללמוד, 
לשנות ולשפר את התוכנה. ליתר דיוק, זה מתײחס לארבעה סוגים של חירות למשתמשי
התוכנה:
------------------------------------------------------------------------------
0. החופש להריץ את התוכנה, לכל מטרה שהיא.
1. החופש ללמוד איך תוכנה עובדת, ולשנות אותה לצרכיהם.
   גישה לקוד המקור היא תנאי מקדים לכך.
2. החופש להפיץ עותקים בהפצה-חוזרת כדי שיוכלו למשל לעזור לשכנים שלהם.
3. החופש לשפר את התוכנה, ולשחרר את השיפורים שלהם לציבור, כך שכל הקהילה תרויח.
   גישה לקוד-המקור היא תנאי מקדים לכך.
------------------------------------------------------------------------------
The concept of these 4 freedoms (0-3) were developed by Richard Stallman.

To set a good example he started to write a completely free operating system.

Today Linux based GNU systems are used by millions of people around the world."""

import os, re
lang = os.getenv ('LANG')
i = lang.find ('_')
if i > 0:
	lang = lang[:i]
text = texts.get (lang, texts['en'])
def break_on_dashlines (text):
	s = ''
	for line in text.split ('\n'):
		if re.match ('^----*$', line):
			yield s
			s = ''
		else:
			if s:
				s += '\n'
			s += line
	yield s
		
for slide in break_on_dashlines (text):
	text_slide (slide)

if __name__ == "__main__":
	import slippy
	import gnu_theme
	slippy.main (slides, gnu_theme, args = ['--slideshow', '--delay', '0.05', '--repeat'])
