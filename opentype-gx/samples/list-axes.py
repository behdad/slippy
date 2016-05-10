#!/usr/bin/python

from fontTools.ttLib import TTFont
import sys

font = TTFont(sys.argv[1])
axes = font['fvar'].axes
for axis in axes:
	print "%s	%g	%g	%g" % (axis.axisTag,
					       axis.minValue,
					       axis.defaultValue,
					       axis.maxValue)
