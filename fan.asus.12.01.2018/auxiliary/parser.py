# -*- coding: utf-8 -*-
import os

def getvalfromconfigbykeyword(keyword, keywords, configfile, defaultlst):
	if os.path.exists(configfile) == False:
		return defaultlst
	f = open(configfile, "r")
	lst = []
	lst = f.readlines()
	f.close()
	kw = False
	lstval = []
	keywords_tmp = keywords.copy();
	keywords_tmp.remove(keyword)
	for word in lst:
		if word.endswith("\n"):
			word = word[:len(word)-1]
		if word == keyword:
			kw = True
			continue
		for kword in keywords_tmp:
			if word == kword:
				kw = False
		if kw == True:
			lstval.append(word)
	if len(lstval) != 0:
		return lstval
	else:
		return defaultlst
		
def getparametersandvals(dirvals, paramlist, splitter, voidsym, separator):
	clean = []
	correctpair = []
	for val in dirvals:
		for sym in voidsym:
			val = val.replace(sym, "")
		clean.append(val)
		
	for val in clean:
		splitted = val.split(splitter)
		if len(splitted) == 2:
			if splitted[1].find(separator) == -1:
				correctpair.append(splitted)
			else:
				separated = splitted[1].split(separator)
				for s in separated:
					if s == "":
						continue
					newsplitted = []
					newsplitted.append(splitted[0])
					newsplitted.append(s)
					correctpair.append(newsplitted)
	return correctpair

def extractvaluebyparam(param, pairslist):
	val = []
	for pairs in pairslist:
		if pairs[0] == param:
			val.append(pairs[1])
	if len(val) != 0:
		return val
	else:
		return [""]
		
def commandparcer(str, singlecommands, multiplecommands, separator):
	ret = []
	lst = str.split(separator)
	if len(lst) == 0:
		return ret
	if lst[0] in singlecommands:
		if len(lst) == 1:
			ret.append(lst[0])
			return ret
	if lst[0] in multiplecommands:
		if len(lst) == 1:
			ret.append(lst[0])
			ret.append("")
		else:
			ret.append(lst[0])
			param = ""
			for word in lst:
					param = param + word + " "
			param = param[len(lst[0]):]
			param = param.rstrip()
			param = param.lstrip()
			ret.append(param)
		return ret
	return ret