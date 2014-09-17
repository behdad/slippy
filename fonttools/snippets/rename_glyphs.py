import fontTools.ttLib

font = fontTools.ttLib.TTFont(inpath)
glyphnames = font.getGlyphOrder()

# ...do the actual renaming in glyphnames...

font = fontTools.ttLib.TTFont(inpath) # load again
font.setGlyphOrder(glyphnames)
post = font['post'] # make sure post table is loaded

font.save(outpath)
