#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree
import random
import os
import ctypes
import time

def GetImage():
	maxPage = int(xml.etree.ElementTree.fromstring(urllib.request.urlopen("https://konachan.com/post.xml?limit=1").read()).get("count"))
	return (xml.etree.ElementTree.fromstring(urllib.request.urlopen("https://konachan.com/post.xml?limit=1&page=" + str(random.randint(0, maxPage + 1))).read())[0].get("file_url"))

if __name__ == "__main__":
	if os.name == 'nt':
		url = GetImage()
		fileName = "wallpaper." + url.split('.')[-1]
		urllib.request.urlretrieve(url, fileName)
		ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.dirname(os.path.realpath(__file__)) + "\\" + fileName, 0)
		time.sleep(2)
		os.remove(fileName)
	else:
		print("Your OS is not supported")