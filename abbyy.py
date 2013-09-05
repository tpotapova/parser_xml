# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import sys
import os
import fnmatch
import re


class XMLConvertion():
	def __init__(self):
		self.fList = []
	def make_fileList_from_path(self,path):
		for d, subs, files in os.walk(path):
			if len(files) > 0:
				for f in range(len(files)):
					fpath = os.path.join(d,files[f])
					if  os.path.os.path.getsize(fpath)>0:
						self.fList.append(fpath)
			if len(subs) > 0:
				for s in subs:
					self.make_fileList_from_path(os.path.join(s))
		return self.fList
	def parse_dir(self,path):
		fileList = self.make_fileList_from_path(path)
		for f in fileList:
			self.parse(f)
		return self.list
	def convert(self,path):
		targetList = self.parse_dir(path)
		xml_data_list = ['<?xml version="1.0" encoding="UTF-8"?>','<TestDocument>']
		id = 1
		for item in targetList:
			xml_data_list.append('<Unit>')
			data = ['<id>' + str(id) + '</id>','<Source>'+ item + '</Source>','<Target>' + item + '</Target>']
			xml_data_list.extend(data)
			xml_data_list.append('</Unit>')
			id += 1
		xml_data_list.append('</TestDocument>')
		result = '\n'.join(xml_data_list)
		return result
	def write_to_file(self,path):
		resultFile = open(path + '/' + 'resources.xml', 'w')
		resultFile.write(self.convert(path))
		resultFile.close()
		print 'Your files were successfully converted to resources.xml'

class IOSStrings(XMLConvertion):
	def __init__(self):
		XMLConvertion.__init__(self)
		self.list = []
	def parse(self,filename):
		file = open(filename)
		strings = file.readlines()
		for s in strings:
			if "=" in s:
				s = s.split("=")
				matches = re.match(r'^ "(.*)";$',s[1])
				if matches != None:
					target = matches.group(1)
					self.list.append(target)

class AndroidXML(XMLConvertion):
	def __init__(self):
		XMLConvertion.__init__(self)
		self.list = []
	def parse(self,filename):
		tree = ET.parse(filename)
		root = tree.getroot()
		for child in root.iter():
			if child.text != None and child.text.strip():
				self.list.append(child.text.encode('utf-8'))
		return self.list
class siteXML(XMLConvertion):
	def __init__(self):
		XMLConvertion.__init__(self)
		self.list = []
	def parse(self,filename):
		tree = ET.parse(filename)
		root = tree.getroot()
		for i in tree.iter('{http://locale.one.lv/schema/translations}default'):
			if i.text != None:
				text = i.text.encode('utf-8')
				text = re.sub(r'({\d+})', r'<Non>\1</Non>',text)
				self.list.append(text)
		return self.list
		
if __name__ == '__main__':
	path = sys.argv[1]
	a = eval(sys.argv[2])()
	print a.write_to_file(path)