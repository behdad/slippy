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
	if data and 'who' in data:
		return slide_who (f, data['who'], data=data)
	else:
		return slide_who (f, 0, data=data)

#
# Slides start here
#

who (behdad)

@slide_noone
def title_slide (r):
	r.move_to (400, 100)
	r.put_text ("<b>GLyphy</b>", width=800, valign=1)

	r.move_to (0, 450)
	r.put_text ("""Behdad Esfahbod\n<span font_desc="monospace 16">behdad@google.com</span>""",
		    desc="20", halign=1, valign=-1)
	r.move_to (800, 450)
	r.put_text ("""<span font_desc="monospace 16">glyphy.org\nbehdad.org</span>""",
		    desc="20", halign=-1, valign=-1)

def list_slide (l, data=None):
	def s (r):
		return '\n'.join (l)
		#yield l[0]
		#for i in l[1:]:
		#	yield '\n'+i
	s.__name__ = l[0]
	slide (s, data)

slide_noone("Getting your CFP\nabstract accepted:\n<i>A case study (or 2)</i>")

list_slide ([
		"<b>Helps if…</b>",
		"• Established",
		"• ~100s millions users",
		"• <i>Has</i> changed the world",
		"• Thriving community",
		"• Many high-profile users",
		"• Booming",
	    ], data={'align': pango.ALIGN_LEFT})
slide_noone("<b>HarfBuzz</b>")

list_slide ([
		"<b>But if…</b>",
		"• Experimental",
		"• Unused so far",
		"• <i>Will</i> change the world",
		"• No community",
		"• No users",
		"• Stale",
	    ], data={'align': pango.ALIGN_LEFT})
slide_noone("<b>GLyphy</b>")

slide_noone("Submit!")

slide_noone("<b>How to\n<i>keynote</i>\nLCA</b>")

who ("mjg59.png")
slide("Just cut\nthe jokes\nout <i>dude</i>!")
who (behdad)

#
# Real thing starts here
#

slide_noone("<b>GLyphy</b>\nAn <i>experiment</i> in\nGPU-accelerated\ntext rendering")
slide_noone("GLSL ES2")

list_slide ([
		"<b>Status quo</b>",
		"• Hint",
		"• Rasterize",
		"• Upload to GPU texture",
		"• Blit",
	    ], data={'align': pango.ALIGN_LEFT})
slide_noone("<b>Transformation\ndependent</b>")

slide_noone("<span font_desc='Comic Sans MS'><b>Lets make\ntext beautiful!\n<span font_desc='24'>lolz</span></b></span>")

slide_noone("What would you do\nif you knew <span strikethrough='true'>you\ncould not fail</span> have a\nhigh-resolution display?")
slide_noone("<span strikethrough='true'>200+ppi (160 even)</span>\n300+ppi (450 even)")

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

def g_beziers(r):
	draw_image (r, "GwithBeziers.png", width=400, imgheight=660)

@slide
def GBeziers(r):
	g_beziers (r)

slide ("Coverage-based\nAnti-Aliasing")

@slide
def GBeziersSquare (r):
	g_beziers (r)
	r.rectangle (480, 210, 50, 50)
	r.set_source_rgba (0., 0., 1., .4)
	r.fill_preserve ()
	r.stroke ()

slide ("SDF-based\nAnti-Aliasing")

@slide
def GBeziersGaussian (r):
	g_beziers (r)
	gau = cairo.RadialGradient (505, 235, 0, 505, 235, 25 * 2)
	stops = 16
	for stop in (float(x) / stops for x in range(0, stops + 1)):
		shade = stop * stop * (3. - 2. * stop)
		gau.add_color_stop_rgba (stop, 0., 0., 1., .7 * (1. - shade))
	r.set_source (gau)
	r.paint ()

def glyphy_demo(r, f):
	r.set_source_rgb (1, 1, 1)
	r.paint ()
	args = {
		"width": 600,
		"imgheight": 680,
		"yoffset": -15,
		"xoffset": 0,
	}
	draw_image (r, f, **args)

def clamp(x, a, b):
	return min (max (x, a), b)

def smoothstep0(a, b, t):
	scale = 2.
	t = clamp ((float(t) - a)/(b - a)*scale - (scale-1)/2., 0, 1)
	return t

def smoothstep(a, b, t):
	scale = 1./.75
	t = clamp ((float(t) - a)/(b - a)*scale - (scale-1)/2., 0, 1)
	return t * t * (3. - 2. * t)

def smoothstep2(a, b, t):
	scale = 1. # 30./16. # Humm?
	t = clamp ((float(t) - a)/(b - a)*scale - (scale-1)/2., 0, 1)
	return t*t*t*(t*(t*6. - 15.) + 10.)

def aa_diagonal(a, b, t):
	scale = 1. # 2**.5 # Humm?
	t = clamp ((float(t) - a)/(b - a)*scale - (scale-1)/2., 0, 1)
	if t <= .5:
		return t*t * 2
	else:
		t = 1. - t
		return 1 - (t*t * 2)

def plot(r, f, a, b, line=0, scale=1.):
	r.save ()
	r.translate (400, 60)
	r.scale (scale, scale)
	r.scale (50, -50.5)
	r.translate (0, -line * 1.5)
	r.move_to (-4, 0)
	r.line_to (4, 0)
	r.move_to (0, -.1)
	r.line_to (0, 1.1)
	r.set_source_rgba (0, 0, 0, .1)
	r.save ()
	r.identity_matrix ()
	r.set_line_width (1.)
	r.stroke ()
	r.restore ()
	steps = 200
	for step in (x* 8./ steps for x in range(-steps/2,steps/2+1)):
		r.line_to (step, f (a, b, step))
	r.set_source_rgba (0, 0, 0, .9)
	r.save ()
	r.identity_matrix ()
	r.set_line_width (1.)
	r.stroke ()
	r.restore ()
	r.restore ()

@slide
def GSdf(r):
	glyphy_demo (r, "sdf.png")

@slide
def GRaster(r):
	glyphy_demo (r, "g.png")
	plot (r, smoothstep, -1., +1.)

@slide
def GRasterBlurry(r):
	glyphy_demo (r, "g-blurry.png")
	plot (r, smoothstep, -1.*4, +1.*4)

@slide
def GRasterAliased(r):
	glyphy_demo (r, "g-aliased.png")
	plot (r, smoothstep, -1./10, +1./10)

@slide
def GRaster(r):
	glyphy_demo (r, "g.png")
	plot (r, smoothstep, -1., +1.)

@slide
def GRasterEmboldened(r):
	glyphy_demo (r, "g-emboldened.png")
	plot (r, smoothstep, -1.+2., +1.+2.)

@slide
def GRasterLightened(r):
	glyphy_demo (r, "g-lightened.png")
	plot (r, smoothstep, -1.-1., +1.-1.)

@slide
def AntiAliasFuncs(r):
	r.set_source_rgb (1, 1, 1)
	r.paint ()
	plot (r, smoothstep0, -1., +1., line=1, scale=1.4)
	plot (r, smoothstep, -1., +1., line=2, scale=1.4)
	plot (r, smoothstep2, -1., +1., line=3, scale=1.4)
	plot (r, aa_diagonal, -1., +1., line=4, scale=1.4)
	r.set_allocation (100, 50, 600, 480)

slide("SDF is <i>linear</i> over\nuniform-scaling\n and translation")

slide_noone("<b>Represent\nSDF on GPU</b>")

image_slide("g-texture-raster.png")
image_slide("g-texture-sdf.png")
# TODO bilinear effects on texture raster
# TODO bilinear effects on texture sdf

slide_noone("<i>Vector\nall the\nglyphs!</i>")

slide("Distance\nto Bézier")

slide("<b>Ouch!</b>")

slide("Convert\nto line\nsegments")
@slide
def GLines(r):
	glyphy_demo (r, "g-lines.png")

slide("Convert to\ncircular arc\nsplines")
@slide
def GLines(r):
	glyphy_demo (r, "g-arcs.png")

slide_noone("<b>Arc-spline\napproximation</b>")
slide("Error\nfunction")
@slide
def CurveArc(r):
	r.set_source_rgb (1, 1, 1)
	r.paint ()
	draw_image (r, "curve-arc.png", width=600, imgheight=750)
slide("Physics\nsimulation")
@slide
def Spiral(r):
	r.set_source_rgb (1, 1, 1)
	r.paint ()
	draw_image (r, "spiral.png", width=600, imgheight=650)

@slide
def GArcsCloseup(r):
	glyphy_demo (r, "g-arcs-closeup.png")
@slide
def GArcsAll(r):
	glyphy_demo (r, "g-arcs-all.png")
list_slide ([
		"<b>GPU time!</b>",
		"• Stuff it all in a texture",
		"• Ship it!",
	    ], data={'align': pango.ALIGN_LEFT})
@slide
def GReal(r):
	glyphy_demo (r, "g-real.png")
slide_noone("<b><i>You're</i> insane!</b>")

list_slide ([
		"<b>Corner cases</b>",
		"• Overlappingcontours",
		"• Tangent arcs",
		"• Float preceision",
	    ], data={'align': pango.ALIGN_LEFT})

list_slide ([
		"<b>Random access</b>",
		"• Coarse grid",
		"• Various optimizations",
	    ], data={'align': pango.ALIGN_LEFT})
@slide
def NumClosestArcWithArcs(r):
	r.set_source_rgb (0x15/255., 0x15/255., 0x15/255.)
	r.paint ()
	draw_image (r, "NumClosestArcsWithArcs.png", width=700*.9, height=400*.9, imgwidth=700)
@slide
def ThinkGridC(r):
	r.set_source_rgb (1, 1, 1)
	r.paint ()
	draw_image (r, "thickGridC2.png", width=495, height=600, imgheight=658, xoffset=3)
@slide
def ThinGridC(r):
	r.set_source_rgb (1, 1, 1)
	r.paint ()
	draw_image (r, "thinGridC2.png", width=495, height=600, imgheight=658, xoffset=3)
@slide
def GArcsAll(r):
	glyphy_demo (r, "g-grid.png")
@slide
def GReal1(r):
	glyphy_demo (r, "g-real.png")
who ("keithp.png")
slide("<b><i>It's</i> insane!</b>")
who (behdad)

slide_noone("<b>Demo\ntime!</b>")

# Demo!

slide_noone("<b>Limitations</b>")
slide("Memory\nfootprint")
slide("Speed+memory\nfont-dependent")
@slide
def A(r):
	glyphy_demo (r, "A.png")
@slide
def A(r):
	glyphy_demo (r, "A-debug.png")
@slide
def Arcano(r):
	glyphy_demo (r, "arcano.png")

slide_noone("<b>Advantages</b>")
slide("Memory\nfootprint")
slide("Subpixel\npositioning")
slide("Pinch-to-zoom")

list_slide ([
		"<b>Challenges</b>",
		"• Shader size / complexity",
		"• Pixel cost",
		"• Dependent texture lookups",
		"• Variable loop iterations",
		"• Interpolation accuracy",
	    ], data={'align': pango.ALIGN_LEFT})

def source_slide(s):
	s = s.replace("&", "&amp;").replace("<", "&lt;")
        s = "<span font_desc='monospace'>" + s + "</span>"
	slide_noone (s, data={'align': pango.ALIGN_LEFT})

source_slide("""
varying vec3 lightDir,normal;
uniform sampler2D tex,l3d;
 
void main()
{
    vec3 ct,cf,c;
    vec4 texel;
    float intensity,at,af,a;
 
    intensity = max(dot(lightDir,normalize(normal)),0.0);
 
    cf = intensity * (gl_FrontMaterial.diffuse).rgb +
                      gl_FrontMaterial.ambient.rgb;
    af = gl_FrontMaterial.diffuse.a;
 
    texel = texture2D(tex,gl_TexCoord[0].st);
 
    ct = texel.rgb;
    at = texel.a;
 
    c = cf * ct;
    a = af * at;
 
    float coef = smoothstep(1.0,0.2,intensity);
    c += coef *  vec3(texture2D(l3d,gl_TexCoord[0].st));
 
    gl_FragColor = vec4(c, a);
}
""")
@slide_noone
def TexGlow(r):
	r.set_source_rgb (1, 1, 1)
	r.paint ()
	draw_image (r, "texGlow.jpg", width=600, imgheight=150)

source_slide("""
/*
 * Copyright 2012 Google, Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Google Author(s): Behdad Esfahbod, Maysum Panju
 */
""")
source_slide("""
#ifndef GLYPHY_TEXTURE1D_FUNC
#define GLYPHY_TEXTURE1D_FUNC glyphy_texture1D_func
#endif
#ifndef GLYPHY_TEXTURE1D_EXTRA_DECLS
#define GLYPHY_TEXTURE1D_EXTRA_DECLS
#endif
#ifndef GLYPHY_TEXTURE1D_EXTRA_ARGS
#define GLYPHY_TEXTURE1D_EXTRA_ARGS
#endif

#ifndef GLYPHY_SDF_TEXTURE1D_FUNC
#define GLYPHY_SDF_TEXTURE1D_FUNC GLYPHY_TEXTURE1D_FUNC
#endif
#ifndef GLYPHY_SDF_TEXTURE1D_EXTRA_DECLS
#define GLYPHY_SDF_TEXTURE1D_EXTRA_DECLS GLYPHY_TEXTURE1D_EXTRA_DECLS
#endif
#ifndef GLYPHY_SDF_TEXTURE1D_EXTRA_ARGS
#define GLYPHY_SDF_TEXTURE1D_EXTRA_ARGS GLYPHY_TEXTURE1D_EXTRA_ARGS
#endif
#ifndef GLYPHY_SDF_TEXTURE1D
#define GLYPHY_SDF_TEXTURE1D(offset) GLYPHY_RGBA(GLYPHY_SDF_TEXTURE1D_FUNC (offset GLYPHY_TEXTURE1D_EXTRA_ARGS))
#endif

#ifndef GLYPHY_MAX_NUM_ENDPOINTS
#define GLYPHY_MAX_NUM_ENDPOINTS 32
#endif
""")
source_slide("""
glyphy_arc_list_t
glyphy_arc_list (const vec2 p, const ivec2 nominal_size GLYPHY_SDF_TEXTURE1D_EXTRA_DECLS)
{
  int cell_offset = glyphy_arc_list_offset (p, nominal_size);
  vec4 arc_list_data = GLYPHY_SDF_TEXTURE1D (cell_offset);
  return glyphy_arc_list_decode (arc_list_data, nominal_size);
}
""")
source_slide("""
float
glyphy_sdf (const vec2 p, const ivec2 nominal_size GLYPHY_SDF_TEXTURE1D_EXTRA_DECLS)
{
  glyphy_arc_list_t arc_list = glyphy_arc_list (p, nominal_size  GLYPHY_SDF_TEXTURE1D_EXTRA_ARGS);

  /* Short-circuits */
  if (arc_list.num_endpoints == 0) {
    /* far-away cell */
    return GLYPHY_INFINITY * float(arc_list.side);
  } if (arc_list.num_endpoints == -1) {
    /* single-line */
    float angle = arc_list.line_angle;
    vec2 n = vec2 (cos (angle), sin (angle));
    return dot (p - (vec2(nominal_size) * .5), n) - arc_list.line_distance;
  }
""")
source_slide("""
  float side = float(arc_list.side);
  float min_dist = GLYPHY_INFINITY;
  glyphy_arc_t closest_arc;

  glyphy_arc_endpoint_t endpoint_prev, endpoint;
  endpoint_prev = glyphy_arc_endpoint_decode (GLYPHY_SDF_TEXTURE1D (arc_list.offset), nominal_size);
""")
source_slide("""
  for (int i = 1; i < GLYPHY_MAX_NUM_ENDPOINTS; i++)
  {
    if (i >= arc_list.num_endpoints) {
      break;
    }
    endpoint = glyphy_arc_endpoint_decode (GLYPHY_SDF_TEXTURE1D (arc_list.offset + i), nominal_size);
    glyphy_arc_t a = glyphy_arc_t (endpoint_prev.p, endpoint.p, endpoint.d);
    endpoint_prev = endpoint;
    if (glyphy_isinf (a.d)) continue;
""")
source_slide("""
    if (glyphy_arc_wedge_contains (a, p))
    {
      float sdist = glyphy_arc_wedge_signed_dist (a, p);
      float udist = abs (sdist) * (1. - GLYPHY_EPSILON);
      if (udist <= min_dist) {
	min_dist = udist;
	side = sdist <= 0. ? -1. : +1.;
      }
    }
""")
source_slide("""
    else
    {
      float udist = min (distance (p, a.p0), distance (p, a.p1));
      if (udist < min_dist) {
	min_dist = udist;
	side = 0.; /* unsure */
	closest_arc = a;
      } else if (side == 0. && udist == min_dist) {
	/* If this new distance is the same as the current minimum,
	 * compare extended distances.  Take the sign from the arc
	 * with larger extended distance. */
	float old_ext_dist = glyphy_arc_extended_dist (closest_arc, p);
	float new_ext_dist = glyphy_arc_extended_dist (a, p);

	float ext_dist = abs (new_ext_dist) <= abs (old_ext_dist) ?
			 old_ext_dist : new_ext_dist;

	side = sign (ext_dist);
      }
    }
  }
""")
source_slide("""
  if (side == 0.) {
    // Technically speaking this should not happen, but it does.  So try to fix it.
    float ext_dist = glyphy_arc_extended_dist (closest_arc, p);
    side = sign (ext_dist);
  }

  return min_dist * side;
}
""")
@slide
def GReal2(r):
	glyphy_demo (r, "g-real.png")

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
	slide_noone (s, data={'align': pango.ALIGN_LEFT})

def commit_slide(s, who=None):
	lines = s.split ("\n")
	new_lines = []
	for s in lines:
		s = s.replace("&", "&amp;").replace("<", "&lt;")
		if not s: s = ' '
		elif s[0] != ' ':
			s = "<b>%s</b>" % s

		new_lines.append (s)

	s = '\n'.join (new_lines)
        s = "<span font_desc='monospace'>" + s + "</span>"
	if who:
		slide_noone (s, data={'align': pango.ALIGN_LEFT, 'who': who})
	else:
		slide_noone (s, data={'align': pango.ALIGN_LEFT})

slide_noone("<b>Drivers</b>")

slide("<b>Case study</b>\nMesa\nsoftware\nrenderer")
source_slide("""
  "Infinite loop detected in fragment program"  
""")

slide("<b>Case study</b>\nNvidia+Mac")
patch_slide("""
diff --git a/src/glyphy-common.glsl b/src/glyphy-common.glsl
index 2021d74..95f857b 100644
--- a/src/glyphy-common.glsl
+++ b/src/glyphy-common.glsl
@@ -16,17 +16,6 @@
 
-#define GLYPHY_PASTE_ARGS(prefix, name) prefix ## name
-#define GLYPHY_PASTE(prefix, name) GLYPHY_PASTE_ARGS (prefix, name)
-
-#ifndef GLYPHY_PREFIX
-#define GLYPHY_PREFIX glyphy_
-#endif
-
-#ifndef glyphy
-#define glyphy(name) name
-#endif
-
 
@@ -36,13 +25,13 @@
 
-struct glyphy(arc_t) {
+struct glyphy_arc_t {
   vec2  p0;
""")
slide("150+fps\nMacbook Air 2011")
slide("~30fps\nretina")

slide("<b>Case study</b>\nAMD+Mac")
patch_slide("""
diff --git a/src/glyphy-common.glsl b/src/glyphy-common.glsl
index 5e969c2..c9349b7 100644
--- a/src/glyphy-common.glsl
+++ b/src/glyphy-common.glsl
@@ -151,25 +151,30 @@ glyphy_arc_wedge_contains (const glyphy_arc_t a, const vec2 p)
 }
 
 float
+glyphy_arc_wedge_signed_dist_shallow (const glyphy_arc_t a, const vec2 p)
+{
+  vec2 v = normalize (a.p1 - a.p0);
+  float line_d = dot (p - a.p0, glyphy_perpendicular (v));
+  ...
+  return line_d + r;
+}
+
+float
 glyphy_arc_wedge_signed_dist (const glyphy_arc_t a, const vec2 p)
 {
-  if (abs (a.d) <= .01)
-  {
-    vec2 v = normalize (a.p1 - a.p0);
-    float line_d = dot (p - a.p0, glyphy_perpendicular (v));
-    ...
-    return line_d + r;
-  }
+  if (abs (a.d) <= .01)
+    return glyphy_arc_wedge_signed_dist_shallow (a, p);
   vec2 c = glyphy_arc_center (a);
   return sign (a.d) * (distance (a.p0, c) - distance (p, c));
 }
""")

slide("<b>Case study</b>\nIntel+Linux")
commit_slide("""
commit 137c5ece7d22bcbb017e52f00273b42a191f496d
Author: Eric Anholt <eric@anholt.net>
Date:   Wed Apr 11 13:24:22 2012 -0700

    i965: Convert live interval computation to using live variable analysis.
    
    Our previous live interval analysis just said that anything in a loop
    was live for the whole loop.  If you had to spill a reg in a loop,
    then we would consider the unspilled value live across the loop too,
    so you never made progress by spilling.  Eventually it would consider
    everything in the loop unspillable and fail out.
    
    With the new analysis, things completely deffed and used inside the
    loop won't be marked live across the loop, so even if you
    spill/unspill something that used to be live across the loop, you
    reduce register pressure.  But you usually don't even have to spill
    any more, since our intervals are smaller than before.
    
    This fixes assertion failure trying to compile the shader for the
    "glyphy" text rasterier and piglit glsl-fs-unroll-explosion.
    
    Improves Unigine Tropics performance 1.3% +/- 0.2% (n=5), by allowing
    more shaders to be compiled in 16-wide mode.
""", who="anholt.png")
slide("60+fps\ni965 Thinkpad")

slide("<b>Case study</b>\niPod 3G")
source_slide("""
  "Demo runs SLOW on my iPod 3G. ~3 FPS"  
""")

slide("<b>Case study</b>\nAndroid 4.3+LGE")
patch_slide("""
 int
 test()
 {
-   float f = 1.0;
-   return int(f);
+   float f = 1.0;
+   int cx = int(f);
+   return cx;
 }
""")

slide("<b>Case study</b>\nAndroid 4.4+LGE")
patch_slide("""
diff --git a/src/glyphy-sdf.glsl b/src/glyphy-sdf.glsl
index a46c0d4..6cc827c 100644
--- a/src/glyphy-sdf.glsl
+++ b/src/glyphy-sdf.glsl
@@ -36,7 +36,7 @@
 #define GLYPHY_SDF_TEXTURE1D_EXTRA_ARGS GLYPHY_TEXTURE1D_EXTRA_ARGS
 #endif
 #ifndef GLYPHY_SDF_TEXTURE1D
-#define GLYPHY_SDF_TEXTURE1D(offset) GLYPHY_RGBA (GLYPHY_SDF_TEXTURE1D_FUNC (...))
+#define GLYPHY_SDF_TEXTURE1D(offset) GLYPHY_RGBA(GLYPHY_SDF_TEXTURE1D_FUNC (...))
 #endif
 
 #ifndef GLYPHY_MAX_NUM_ENDPOINTS
""")
slide("25fps\nNexus 4/5")

list_slide ([
		"<b>Code: libglyphy</b>",
		"• ~400 lines *.h",
		"• ~2500 lines *.cc *.hh",
		"• ~370 lines *.glsl",
		"• No dependencies",
	    ], data={'align': pango.ALIGN_LEFT})
list_slide ([
		"<b>Code: glyphy-demo</b>",
		"• ~2800 lines *.cc *.h",
		"• ~150 lines *.glsl",
		"• FreeType, GLUT",
	    ], data={'align': pango.ALIGN_LEFT})
list_slide ([
		"<b>More work</b>",
		"• Subpixel-rendering",
		"• Anisotropic-antialiasing",
	    ], data={'align': pango.ALIGN_LEFT})

slide("<b>Gallery!</b>")

for filename in file("gallery.txt").read().split('\n'):
	if not filename: continue
	def closure(filename):
		def slideFunc(r):
			glyphy_demo (r, filename)
		return slideFunc
	slide(closure(filename))

@slide
def GReal1(r):
	glyphy_demo (r, "q.png")

if __name__ == "__main__":
	import slippy
	import glyphy_theme
	slippy.main (slides, glyphy_theme)
