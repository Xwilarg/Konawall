#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree
import random
import os
import ctypes
import time
import json

def GetImageUrl(allowNsfw):
	maxPage = int(xml.etree.ElementTree.fromstring(urllib.request.urlopen("https://konachan.com/post.xml?limit=1").read()).get("count"))
	xmlContent = xml.etree.ElementTree.fromstring(urllib.request.urlopen("https://konachan.com/post.xml?limit=1&page=" + str(random.randint(0, maxPage + 1))).read())[0]
	if allowNsfw == False and xmlContent.get("rating") != "s":
		return (GetImageUrl(allowNsfw))
	url = xmlContent.get("file_url")
	fileName = "wallpaper." + url.split('.')[-1]
	urllib.request.urlretrieve(url, fileName)
	return (fileName)

def GetImage():
	jsonContent = json.loads(open("config.json").read())
	allowNsfw = jsonContent["allowNsfw"] == 1
	print("Current configuration:")
	print("Allow NSFW: " + str(allowNsfw))
	print("\nDownloading image...")
	image = GetImageUrl(allowNsfw);
	print("Done, cleaning...")
	return (image)

if __name__ == "__main__":
	if os.name == 'nt':
		fileName = GetImage()
		ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.dirname(os.path.realpath(__file__)) + "\\" + fileName, 0)
		time.sleep(2)
		os.remove(fileName)
	else:
		print("Your OS is not supported")