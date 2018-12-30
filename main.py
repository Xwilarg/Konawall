#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree
import random
import os
import ctypes
import time
import json

def GetImageUrl(maxPage, counter, allowNsfw, tags):
	xmlContent = xml.etree.ElementTree.fromstring(urllib.request.urlopen("https://konachan.com/post.xml?limit=1&page=" + str(random.randint(0, maxPage + 1)) + "&tags=" + tags).read())[0]
	if not allowNsfw and xmlContent.get("rating") != "s":
		if counter == 0:
			print("No image found after 10 iterations. That may mean there is no safe image available with the tags you choosed")
			return (None)
		else:
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
	maxPage = int(xml.etree.ElementTree.fromstring(urllib.request.urlopen("https://konachan.com/post.xml?limit=1&tags=" + tags).read()).get("count"))
	if maxPage == 0:
		print("There is no image with the tags you specified, please correct them on the configuration file")
		return (None)
	image = GetImageUrl(maxPage, 10, allowNsfw, tags)
	if image is not None:
		print("Done, cleaning...")
	return (image)

if __name__ == "__main__":
	if os.name == 'nt':
		fileName = GetImage()
		if fileName is not None:
			ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.dirname(os.path.realpath(__file__)) + "\\" + fileName, 0)
			time.sleep(2)
			os.remove(fileName)
	else:
		print("Your OS is not supported")
