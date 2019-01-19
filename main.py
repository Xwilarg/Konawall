#!/usr/bin/env python3
import urllib.request
import urllib.parse
import xml.etree.ElementTree
import random
import os
import ctypes
import time
import json
import ssl
from pathlib import Path

def GetImageUrl(maxPage, counter, allowNsfw, tags):
	xmlContent = xml.etree.ElementTree.fromstring(urllib.request.urlopen("https://konachan.com/post.xml?limit=1&page=" + str(random.randint(0, maxPage + 1)) + "&tags=" + urllib.parse.quote(tags)).read())[0]
	if not allowNsfw and xmlContent.get("rating") != "s":
		if counter == 0:
			print("No image found after 10 iterations. That may mean there is no safe image available with the tags you choosed")
			return (None)
		return (GetImageUrl(maxPage, counter - 1, allowNsfw, tags))
	url = xmlContent.get("file_url")
	fileName = "wallpaper." + url.split('.')[-1]
	urllib.request.urlretrieve(url, fileName)
	return (fileName)

def GetImage():
	jsonContent = json.loads(open("config.json").read())
	allowNsfw = jsonContent["allowNsfw"] == 1
	tags = jsonContent["tags"].replace(' ', '+')
	print("Current configuration:")
	print("Allow NSFW: " + str(allowNsfw))
	print("Tags: " + ("None" if (tags == "") else tags))
	print("\nDownloading image...")
	maxPage = int(xml.etree.ElementTree.fromstring(urllib.request.urlopen("https://konachan.com/post.xml?limit=1&tags=" + urllib.parse.quote(tags)).read()).get("count"))
	if maxPage == 0:
		print("There is no image with the tags you specified, please correct them on the configuration file")
		return (None)
	return (GetImageUrl(maxPage, 10, allowNsfw, tags))

if __name__ == "__main__":
	ssl._create_default_https_context = ssl._create_unverified_context
	for path in Path(".").glob("wallpaper*"):
		os.remove(path)
	fileName = GetImage()
	if fileName is not None:
		if os.name == 'nt':
			ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.dirname(os.path.realpath(__file__)) + "\\" + fileName, 0)
		else:
			os.system("gsettings set org.gnome.desktop.background picture-uri " + os.path.dirname(os.path.realpath(__file__)) + "/" + fileName)
		print("The wallpaper was saved as " + fileName)
