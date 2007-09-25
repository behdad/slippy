#!/usr/bin/python

def slide_add(f, data=None, width=800, height=600):
	if not data:
		data = {'who': -1}
        slides.append ((f, data, width, height))
	return f

slides = []
slide_add ("GTK+ Printing")
slide_add ("History")
slide_add ("Native dialogs\n on Win32 / OS X")
slide_add ("App can add\n widgets / pages\n to dialog")
slide_add ("App can ask\n for notification\n even after spooling")
slide_add ("Cairo\n for rendering")
slide_add ("On Unix,\n passthrough\n Postscript too")
slide_add ('Backends:\nFile\nCUPS\nlpr\n<span foreground="gray">PAPI</span>')
slide_add ("External\n application for\n preview by default\n (evince)")
slide_add ("Async operation\n (not on Win32)\n Redo CUPS convenience API")
slide_add ("That's\n mostly\n it!")

if __name__ == "__main__":
	import slippy
	import gtkprinting_theme
	slippy.main (slides, gtkprinting_theme)
