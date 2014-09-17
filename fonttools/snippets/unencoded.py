import fontTools.ttLib

font = fontTools.ttLib.TTFont("Lobster.ttf")
cmap = font['cmap']

encoded = set()
for subtable in cmap.tables:
	encoded.update(subtable.cmap.values())
unencoded = set(font.getGlyphOrder()).difference(encoded)

import pprint
pprint.pprint(unencoded)
