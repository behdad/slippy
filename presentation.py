#!/usr/bin/python
# -*- coding:utf8 -*-

import sys
import types
import cairo
import pygtk
pygtk.require('2.0')
import gtk
import gtk.gdk
import pango
import pangocairo
import gobject

class ViewerGTK(gtk.Widget):

	def do_realize(self):
		self.set_flags(self.flags() | gtk.REALIZED)

		self.window = gtk.gdk.Window(
			self.get_parent_window(),
			width=self.allocation.width,
			height=self.allocation.height,
			window_type=gtk.gdk.WINDOW_CHILD,
			wclass=gtk.gdk.INPUT_OUTPUT,
			event_mask=self.get_events() | gtk.gdk.EXPOSURE_MASK)

		self.window.set_user_data(self)

		self.style.attach(self.window)

		self.style.set_background(self.window, gtk.STATE_NORMAL)
		self.window.move_resize(*self.allocation)

	def do_unrealize(self):
		self.window.destroy()

	def do_expose_event(self, event):
		cr = pangocairo.CairoContext (self.window.cairo_create())

		cr.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
		cr.clip()

		renderer = self.Renderer (cr, self.allocation.width, self.allocation.height)

		self.slide.show_page (renderer, self.step)

		return False

	def go_forward_full(self):
		if self.slide_no + 1 < len (self.slides):
			self.slide_no += 1
			self.slide = Slide (self.slides[self.slide_no])
			self.step = 0
			self.queue_draw()

	def go_forward(self):
		if self.step + 1 < len (self.slide):
			self.step += 1
			self.queue_draw()
		else:
			self.go_forward_full ()

	def go_backward_full(self):
		if self.slide_no > 0:
			self.slide_no -= 1
			self.slide = Slide (self.slides[self.slide_no])
			self.step = 0
			self.queue_draw()

	def go_backward(self):
		if self.step > 0:
			self.step -= 1
			self.queue_draw()
		else:
			self.go_backward_full ()
			self.step = len (self.slide) - 1
			self.queue_draw()

	def key_press_event(self, widget, event):
		if event.string in [' ', '\r'] or event.keyval in [gtk.keysyms.Right, gtk.keysyms.Down]:
			self.go_forward()
		elif event.keyval in [gtk.keysyms.Page_Down]:
			self.go_forward_full()
		elif event.keyval == gtk.keysyms.BackSpace or event.keyval in [gtk.keysyms.Left, gtk.keysyms.Up]:
			self.go_backward()
		elif event.keyval in [gtk.keysyms.Page_Up]:
			self.go_backward_full()
		elif event.string == 'q':# or event.keyval == gtk.keysyms.Escape:
			gtk.main_quit()

	def run (self, Renderer, slides):
		self.Renderer = Renderer
		self.slides = slides

		window = gtk.Window()
		window.add(self)
		window.connect("destroy", gtk.main_quit)
		window.connect("key-press-event", self.key_press_event)
		window.set_default_size (800, 600)
		window.show_all()

		self.slide_no = 0
		self.step = 0
		self.slide = Slide (self.slides[self.slide_no])

		gtk.main()


class ViewerPDF:

	def __init__ (self, filename):
		self.width, self.height = 8.5 * 4/3 * 72, 8.5 * 72
		self.surface = cairo.PDFSurface (filename, self.width, self.height)

	def run (self, Renderer, slides):
		cr = pangocairo.CairoContext (cairo.Context (self.surface))
		renderer = Renderer (cr, self.width, self.height)
		for slide in slides:
			slide = Slide (slide)
			for step in range (len (slide)):
				slide.show_page (renderer, step)


class Slide:

	nullcr = cairo.Context (cairo.ImageSurface (0, 0, 0))

	def get_items (self, cr):
		items = self.slide
		if isinstance (items, types.FunctionType):
			items = items(cr)
		if items == None or items == "":
			items = (" ",)
		if isinstance (items, str):
			items = (items,)
		return items

	def __init__ (self, slide):
		self.slide = slide
		self.texts = [x for x in self.get_items (self.nullcr)]
		self.text = ''.join (self.texts)
	
	def __len__ (self):
		return len (self.texts)
	
	def show_page (self, renderer, pageno):
		cr = renderer.cr
		cr.save ()
		w, h = renderer.prepare_page ()
		layout = renderer.create_layout ()
		lw, lh = renderer.prepare_layout (layout, self.text, w, h)
		text = ""
		i = 0;
		for page in self.get_items (cr):
			text += page
			if i == pageno:
				break;
			i += 1
		layout.set_markup (text)
		cr.move_to ((w - lw) * .5, (h - lh) * .5)
		cr.show_layout (layout)
		cr.restore ()

		cr.show_page()
		

class Renderer():
	
	side_margin = .03
	logo_margin = .15
	padding = .01

	def __init__ (self, cr, width, height):
		self.cr = cr
		self.width, self.height = width, height
		

	def prepare_page (self):

		cr = self.cr
		
		cr.set_source_rgb (0, 0, 0)
		cr.paint ()

		cr.rectangle (0, 0, self.side_margin * self.width, self.height)
		cr.rectangle (self.width, 0, -self.side_margin * self.width, self.height)
		cr.set_source_rgb (1, 1, 1)
		cr.fill ()

		cr.rectangle (0, 0, self.side_margin * self.width, self.logo_margin * self.height)
		cr.rectangle (self.width, 0, -self.side_margin * self.width, self.logo_margin * self.height)
		cr.set_source_rgb (.8, 0, 0)
		cr.fill ()

		cr.set_source_rgba (1, 1, 1, .95)

		layout = self.create_layout ()
		layout.set_markup ("<i>GUADEC 2007, Birmingham, UK</i>")

		w, h = self.fit_layout (layout, .5 * self.width, 0)
		cr.move_to (.5 * (self.width - w), self.height - h)
		cr.show_layout (layout)

		p = min (self.padding * self.width, self.padding * self.height)
		w = self.width * (1 - 2 * self.side_margin) - 2 * p
		x = self.width * self.side_margin + p
		h = self.height * (1 - self.logo_margin) - h - 2 * p
		y = self.height * self.logo_margin + p

		cr.translate (x, y)
		return w, h

	def create_layout (self):

		cr = self.cr
		
		layout = cr.create_layout ()
		font_options = cairo.FontOptions ()
		font_options.set_hint_metrics (cairo.HINT_METRICS_OFF)
		pangocairo.context_set_font_options (layout.get_context (), font_options)
		return layout

	def fit_layout (self, layout, width, height):

		width *= pango.SCALE
		height *= pango.SCALE

		cr = self.cr

		cr.update_layout (layout)
		desc = pango.FontDescription("Sans")
		s = int (max (height * 5., width / 50.))
		desc.set_size (s)
		layout.set_font_description (desc)
		w,h = layout.get_size ()
		if width > 0:
			size = float (width) / w
			if height > 0:
				size = min (size, float (height) / h)
		else:
			size = float (height) / h

		desc.set_size (int (s * size)) 
		layout.set_font_description (desc)

		return layout.get_pixel_size ()

	def prepare_layout (self, layout, text, w, h):
		layout.set_markup (text)
		return self.fit_layout (layout, w, h)
	

gobject.type_register(ViewerGTK)


def main():
	import slides
	all_slides = slides.slides

	if len(sys.argv) == 2:
		viewer = ViewerPDF (sys.argv[1])
	else:
		viewer = ViewerGTK ()

	viewer.run (Renderer, all_slides)

if __name__ == "__main__":
	main()
