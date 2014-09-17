import fontTools.ttLib

font = fontTools.ttLib.TTFont(inpath)
post = font['post']

post.fomratType = 3.0

font.save(outpath)
