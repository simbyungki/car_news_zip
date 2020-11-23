
def replaceStr(value, t01, t02) :
	keywords = list(value)
	for idx, keyword in enumerate(keywords) :
		if keyword == t01 :
			keywords[idx] = t02
	
	result = ''.join(keywords)
	return result


if __name__ == '__main__' : 
	replaceStr('te@xt', '@', '')