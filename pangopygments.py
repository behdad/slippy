#!/usr/bin/python
# -*- coding:utf8 -*-
'''
A pygments formatter for Pango text markup.

Written by Soheil Hasss Yeganeh, 2014.
Not copyrighted, in public domain.
'''

import pygments
from pygments import lexers
from pygments.formatter import Formatter

class PangoFormatter(Formatter):
  ''' Based on the HTML 3.2 formatter in pygments:
      http://pygments.org/docs/formatterdevelopment/ '''
  def __init__(self, **options):
    Formatter.__init__(self, **options)

    self.styles = {}

    for token, style in self.style:
      start_tag = close_tag = ''

      if style['color']:
        start_tag += '<span fgcolor="#%s">' % style['color']
        close_tag = '</span>' + close_tag

      if style['bold']:
        start_tag += '<b>'
        close_tag = '</b>' + close_tag

      if style['italic']:
        start_tag += '<i>'
        close_tag = '</i>' + close_tag

      if style['underline']:
        start_tag += '<u>'
        close_tag = '</u>' + close_tag

      self.styles[token] = (start_tag, close_tag)

  def format(self, tokensource, outfile):
    lastval = ''
    lasttype = None

    for ttype, value in tokensource:
      while ttype not in self.styles:
        ttype = ttype.parent

      if ttype == lasttype:
        lastval += value
      else:
        if lastval:
          stylebegin, styleend = self.styles[lasttype]
          outfile.write(stylebegin + lastval + styleend)

        lastval = value
        lasttype = ttype

    if lastval:
      stylebegin, styleend = self.styles[lasttype]
      outfile.write(stylebegin + lastval + styleend)

__LEXERS = {
    'c': lexers.CLexer,
    'cpp': lexers.CppLexer,
    'java': lexers.JavaLexer,
    'go': lexers.GoLexer,
    'py': lexers.PythonLexer,
    'scala': lexers.ScalaLexer,
    }

def highlight(snippet, lang):
  ''' snippet is the string of code snippets, and lang, the language name. '''
  # The highlighter highlights (i.e., adds tags around) operators
  # (& and ;, here), so let's use a non-highlighted keyword, and escape them
  # after highlighting.
  snippet = snippet.replace("&", "__AMP__").replace("<", "__LT__")

  # Pygments messes up initial and final newlines; fix up
  begin = ''
  if snippet[0] == '\n':
	  begin = '\n'
	  snippet = snippet[1:]
  end = ''
  if snippet[-1] == '\n':
	  end = '\n'
	  snippet = snippet[:-1]

  if __LEXERS.get(lang):
    snippet = pygments.highlight(snippet, __LEXERS[lang](), PangoFormatter())
  else:
    print("Language %s is not supported." % lang)

  if snippet[0] == '\n' and start == '\n':
	  start = ''
  if snippet[-1] == '\n' and end == '\n':
	  end = ''

  snippet = snippet.replace("__AMP__", "&amp;").replace("__LT__", "&lt;")

  return begin + snippet + end

if __name__ == '__main__':
  code = 'print "Hello World"'
  print highlight(code, 'py')

