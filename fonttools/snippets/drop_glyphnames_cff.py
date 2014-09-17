cff = font['CFF '].cff.topDictIndex[0]
cff.ROS = ('Adobe','Identity',0)
mapping = {name:("cid"+str(n) if n else ".notdef") for n,name in enumerate(cff.charset)}
charstrings = cff.CharStrings
charstrings.charStrings = {mapping[name]:v for name,v in charstrings.charStrings.items()}
cff.charset = ["cid"+str(n) if n else ".notdef" for n in range(len(cff.charset))]
